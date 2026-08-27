#!/usr/bin/env node
import { spawn, execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const VIEWPORTS = [
  { width: 1440, height: 900, capture: true },
  { width: 1600, height: 1000, capture: false },
  { width: 1920, height: 1080, capture: false },
  { width: 2048, height: 1320, capture: true },
];
const EXIT = { pass: 0, fail: 1, skipped: 2 };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const sha256 = (b) => createHash('sha256').update(b).digest('hex');
function sidecarNames(artifact, outDir) {
  const stem = path.basename(artifact).replace(/\.html?$/i,'');
  return {
    stem,
    receipt: path.join(outDir, `${stem}.visual-evidence.json`),
    contact: path.join(outDir, `${stem}.visual-evidence.html`),
    screenshots: VIEWPORTS.filter((v)=>v.capture).map((v)=>path.join(outDir, `${stem}.${v.width}x${v.height}.png`)),
  };
}
function cleanupSidecars(names) {
  for (const f of [names.receipt,names.contact,...names.screenshots]) { try { fs.rmSync(f,{force:true}); } catch {} }
}

function executable(file) {
  if (!file) return null;
  try { fs.accessSync(file, fs.constants.X_OK); return path.resolve(file); } catch { return null; }
}
function findOnPath(cmd) {
  for (const dir of String(process.env.PATH || '').split(path.delimiter).filter(Boolean)) {
    const p = executable(path.join(dir, cmd)); if (p) return p;
  }
  return null;
}
export function findChrome() {
  if (process.env.VSC_CHROME) return executable(process.env.VSC_CHROME);
  if (process.platform === 'darwin') {
    return executable('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
      || executable('/Applications/Chromium.app/Contents/MacOS/Chromium');
  }
  if (process.platform === 'win32') {
    for (const root of [process.env.PROGRAMFILES, process.env['PROGRAMFILES(X86)'], process.env.LOCALAPPDATA].filter(Boolean)) {
      const p = executable(path.join(root, 'Google', 'Chrome', 'Application', 'chrome.exe'))
        || executable(path.join(root, 'Chromium', 'Application', 'chrome.exe'));
      if (p) return p;
    }
    return null;
  }
  return findOnPath('google-chrome') || findOnPath('google-chrome-stable') || findOnPath('chromium') || findOnPath('chromium-browser');
}

class CDP {
  constructor(ws) {
    this.ws = ws; this.id = 1; this.pending = new Map(); this.waiters = [];
    ws.onmessage = (ev) => {
      const msg = JSON.parse(String(ev.data));
      if (msg.id) {
        const p = this.pending.get(msg.id); if (!p) return;
        this.pending.delete(msg.id); clearTimeout(p.timer);
        msg.error ? p.reject(new Error(`${p.method}: ${msg.error.message}`)) : p.resolve(msg.result || {}); return;
      }
      for (const w of [...this.waiters]) {
        if (w.method !== msg.method || (w.sessionId && w.sessionId !== msg.sessionId)) continue;
        this.waiters.splice(this.waiters.indexOf(w), 1); clearTimeout(w.timer); w.resolve(msg.params || {});
      }
    };
  }
  send(method, params = {}, sessionId, timeout = 15000) {
    const id = this.id++; const msg = { id, method, params }; if (sessionId) msg.sessionId = sessionId;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => { this.pending.delete(id); reject(new Error(`${method}: timeout`)); }, timeout);
      this.pending.set(id, { method, resolve, reject, timer }); this.ws.send(JSON.stringify(msg));
    });
  }
  waitFor(method, sessionId, timeout = 15000) {
    return new Promise((resolve, reject) => {
      const w = { method, sessionId, resolve, reject, timer: null };
      w.timer = setTimeout(() => { this.waiters.splice(this.waiters.indexOf(w), 1); reject(new Error(`${method}: event timeout`)); }, timeout);
      this.waiters.push(w);
    });
  }
}

async function waitForDevTools(profile, child) {
  const file = path.join(profile, 'DevToolsActivePort');
  for (let i = 0; i < 120; i++) {
    if (child.exitCode != null) throw new Error(`Chromium exited with ${child.exitCode}`);
    if (fs.existsSync(file)) {
      const [port, browserPath] = fs.readFileSync(file, 'utf8').trim().split(/\r?\n/);
      if (port && browserPath) return `ws://127.0.0.1:${port}${browserPath}`;
    }
    await sleep(50);
  }
  throw new Error('Timed out waiting for Chromium DevTools endpoint');
}
async function connect(wsUrl) {
  if (typeof WebSocket === 'undefined') throw new Error('Node runtime lacks the built-in WebSocket required by visual_check.mjs');
  const ws = new WebSocket(wsUrl);
  await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = () => reject(new Error('WebSocket connection failed')); });
  return new CDP(ws);
}
async function evaluate(cdp, sessionId, expression, awaitPromise = false) {
  const r = await cdp.send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise }, sessionId);
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text || 'Runtime.evaluate failed');
  return r.result?.value;
}

const metricExpression = `(() => {
  const px = (v) => Number.parseFloat(v || '0') || 0;
  const rect = (el) => { const r = el?.getBoundingClientRect(); return r ? {x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom} : null; };
  const doc = document.documentElement;
  const panel = document.querySelector('.panel');
  const svg = document.querySelector('svg[role="img"]');
  const vb = svg?.viewBox?.baseVal;
  const svgRect = rect(svg);
  const scale = svgRect && vb && vb.width ? svgRect.width / vb.width : 0;
  const text = (sel) => Array.from(document.querySelectorAll(sel));
  const projected = (sel) => {
    const vals = text(sel).map((el) => px(getComputedStyle(el).fontSize) * (el.closest('svg') ? scale : 1)).filter((n) => n > 0);
    return vals.length ? Math.min(...vals) : null;
  };
  const clipped = text('h1,.lede,.notes p,.notes li,.node-label,.node-desc,.edge-label').filter((el) => el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1).length;
  const nodeTextOverflow = Array.from(document.querySelectorAll('[data-node-id]')).filter((g) => {
    const gr = rect(g.querySelector('rect')); const labels = Array.from(g.querySelectorAll('text')).map(rect).filter(Boolean);
    return gr && labels.some((r) => r.x < gr.x - 1 || r.right > gr.right + 1 || r.y < gr.y - 1 || r.bottom > gr.bottom + 1);
  }).map((g) => g.getAttribute('data-node-id'));
  return {
    innerWidth: window.innerWidth, innerHeight: window.innerHeight,
    scrollWidth: doc.scrollWidth, scrollHeight: doc.scrollHeight,
    documentOverflowX: doc.scrollWidth > window.innerWidth + 1,
    panel: panel ? {clientWidth:panel.clientWidth,scrollWidth:panel.scrollWidth,clientHeight:panel.clientHeight,scrollHeight:panel.scrollHeight,overflowX:panel.scrollWidth > panel.clientWidth + 1} : null,
    svg: svgRect ? {width:svgRect.width,height:svgRect.height,viewBoxWidth:vb?.width || 0,viewBoxHeight:vb?.height || 0,scale} : null,
    fonts: {
      h1: projected('h1'), body: projected('.lede,.notes p,.notes li'),
      node: projected('.node-label'), nodeDescription: projected('.node-desc'), edge: projected('.edge-label')
    },
    clippedTextCount: clipped,
    nodeTextOverflow,
    nodeCount: document.querySelectorAll('[data-node-id]').length,
    edgeLabelCount: document.querySelectorAll('.edge-label').length,
    svgVisible: !!(svgRect && svgRect.width > 1 && svgRect.height > 1)
  };
})()`;

function findingsFor(viewport, m) {
  const errors = []; const warnings = [];
  if (!m.svgVisible) errors.push({ code:'svg-not-visible', message:'Inline SVG is missing or has zero rendered size.' });
  if (m.documentOverflowX) errors.push({ code:'document-horizontal-overflow', message:`Document scrollWidth ${m.scrollWidth} exceeds viewport ${m.innerWidth}.` });
  if (m.panel?.overflowX) errors.push({ code:'desktop-panel-horizontal-scroll', message:`Diagram panel requires horizontal scrolling at ${viewport.width}x${viewport.height}.` });
  if (m.nodeTextOverflow?.length) errors.push({ code:'node-text-overflow', message:`Node text escapes ${m.nodeTextOverflow.length} node(s).`, evidence:m.nodeTextOverflow });
  if ((m.fonts.node ?? 99) < 12) errors.push({ code:'node-text-too-small', message:`Projected node text ${m.fonts.node.toFixed(1)}px is below 12px.` });
  if ((m.fonts.edge ?? 99) < 9) errors.push({ code:'edge-text-too-small', message:`Projected edge text ${m.fonts.edge.toFixed(1)}px is below 9px.` });
  if ((m.fonts.body ?? 99) < 14) errors.push({ code:'body-text-too-small', message:`Body text ${m.fonts.body.toFixed(1)}px is below 14px.` });
  if (m.clippedTextCount) warnings.push({ code:'text-clipping-suspected', message:`${m.clippedTextCount} text element(s) report scroll clipping.` });
  if (m.scrollHeight > viewport.height * 2.2) warnings.push({ code:'long-page', message:`Document height ${m.scrollHeight}px exceeds 2.2 viewport heights.` });
  return { errors, warnings };
}

function contactSheet(artifactName, shots, artifactSha) {
  const cards = shots.map((s) => `<figure><img src="${path.basename(s.path)}" alt="${s.width}x${s.height}"><figcaption>${s.width}×${s.height}</figcaption></figure>`).join('');
  return `<!doctype html><html><head><meta charset="utf-8"><title>Visual evidence — ${artifactName}</title><style>body{font-family:Arial;margin:24px;background:#f5f5f5;color:#111}header{margin-bottom:24px}code{font-size:12px}main{display:grid;grid-template-columns:1fr;gap:28px}figure{margin:0;background:white;padding:12px;border:1px solid #bbb}img{width:100%;height:auto;display:block}figcaption{margin-top:8px}</style></head><body><header><h1>Visual evidence</h1><p>${artifactName}</p><code>${artifactSha}</code></header><main>${cards}</main></body></html>`;
}

export async function runVisualCheck(artifactPath, outDir, { chromePath = findChrome() } = {}) {
  const artifact = path.resolve(artifactPath); const raw = fs.readFileSync(artifact); const artifactSha = sha256(raw); const artifactHtml = raw.toString('utf8');
  fs.mkdirSync(outDir, { recursive:true }); const names=sidecarNames(artifact,outDir); cleanupSidecars(names);
  if (!chromePath) {
    const receipt={schema_version:'visual-evidence-receipt/v1',status:'skipped',artifact_sha256:artifactSha,artifact_path:artifact,reason:'chromium-unavailable',errors:[],warnings:[],perceptual_review:'pending'};
    fs.writeFileSync(names.receipt,JSON.stringify(receipt,null,2)); return { exit:EXIT.skipped, receipt, receiptPath:names.receipt };
  }
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'vsc-visual-'));
  const args = ['--headless=new','--remote-debugging-port=0','--disable-gpu','--disable-background-networking','--disable-component-update','--disable-sync','--no-first-run','--no-default-browser-check','--force-device-scale-factor=1',`--user-data-dir=${profile}`,'about:blank'];
  if (typeof process.getuid === 'function' && process.getuid() === 0) args.unshift('--no-sandbox');
  const child = spawn(chromePath, args, { stdio:['ignore','ignore','pipe'] });
  const stderr = []; child.stderr?.on('data', (d) => stderr.push(String(d)));
  let cdp;
  try {
    cdp = await connect(await waitForDevTools(profile, child));
    const targets = await cdp.send('Target.getTargets');
    let target = targets.targetInfos?.find((t) => t.type === 'page');
    if (!target) target = { targetId:(await cdp.send('Target.createTarget',{url:'about:blank'})).targetId };
    const { sessionId } = await cdp.send('Target.attachToTarget',{targetId:target.targetId,flatten:true});
    await cdp.send('Page.enable',{},sessionId); await cdp.send('Runtime.enable',{},sessionId);
    const viewportReceipts = []; const shots = []; const allErrors=[]; const allWarnings=[];
    for (const vp of VIEWPORTS) {
      await cdp.send('Emulation.setDeviceMetricsOverride',{width:vp.width,height:vp.height,deviceScaleFactor:1,mobile:false},sessionId);
      const tree = await cdp.send('Page.getFrameTree',{},sessionId);
      await cdp.send('Page.setDocumentContent',{frameId:tree.frameTree.frame.id,html:artifactHtml},sessionId);
      await evaluate(cdp,sessionId,`(async()=>{ if(document.fonts?.ready) await document.fonts.ready; await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))); return true; })()`,true);
      const metrics = await evaluate(cdp,sessionId,metricExpression);
      const f = findingsFor(vp,metrics); allErrors.push(...f.errors.map((x)=>({...x,viewport:`${vp.width}x${vp.height}`}))); allWarnings.push(...f.warnings.map((x)=>({...x,viewport:`${vp.width}x${vp.height}`})));
      viewportReceipts.push({width:vp.width,height:vp.height,metrics,errors:f.errors,warnings:f.warnings});
      if (vp.capture) {
        const png = Buffer.from((await cdp.send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false,fromSurface:true},sessionId)).data,'base64');
        const shotPath = path.join(outDir,`${names.stem}.${vp.width}x${vp.height}.png`); fs.writeFileSync(shotPath,png);
        shots.push({width:vp.width,height:vp.height,path:shotPath,sha256:sha256(png),bytes:png.length});
      }
    }
    const contact = names.contact; const contactBytes=Buffer.from(contactSheet(path.basename(artifact),shots,artifactSha)); fs.writeFileSync(contact,contactBytes);
    let version='unknown'; try { version=execFileSync(chromePath,['--version'],{encoding:'utf8'}).trim(); } catch {}
    const status = allErrors.length ? 'failed' : 'passed';
    const receipt = {schema_version:'visual-evidence-receipt/v1',status,artifact_path:artifact,artifact_sha256:artifactSha,render_source:'exact-artifact-bytes-via-Page.setDocumentContent',browser:{path:chromePath,version},viewports:viewportReceipts,screenshots:shots.map((s)=>({...s,path:path.basename(s.path)})),contact_sheet:{path:path.basename(contact),sha256:sha256(contactBytes),bytes:contactBytes.length},errors:allErrors,warnings:allWarnings,perceptual_review:'pending'};
    const receiptPath=names.receipt; fs.writeFileSync(receiptPath,JSON.stringify(receipt,null,2));
    return {exit:status==='passed'?EXIT.pass:EXIT.fail,receipt,receiptPath,contactSheet:contact,screenshots:shots};
  } catch (error) {
    cleanupSidecars(names);
    const receipt={schema_version:'visual-evidence-receipt/v1',status:'failed',artifact_path:artifact,artifact_sha256:artifactSha,errors:[{code:'browser-capture-failed',message:error.message,stderr:stderr.join('').slice(-4000)}],warnings:[],perceptual_review:'pending'};
    const receiptPath=names.receipt; fs.writeFileSync(receiptPath,JSON.stringify(receipt,null,2));
    return {exit:EXIT.fail,receipt,receiptPath};
  } finally {
    try { cdp?.ws?.close(); } catch {} try { child.kill('SIGTERM'); } catch {} try { fs.rmSync(profile,{recursive:true,force:true}); } catch {}
  }
}

async function main() {
  const [artifact, out = '.'] = process.argv.slice(2); if (!artifact) { console.error('usage: visual_check.mjs <artifact.html> [evidence-dir]'); process.exit(2); }
  const r = await runVisualCheck(artifact,path.resolve(out)); console.log(JSON.stringify(r.receipt)); process.exit(r.exit);
}
if (import.meta.url === pathToFileURL(process.argv[1]).href) main();
