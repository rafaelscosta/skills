import hashlib, importlib.util, json, subprocess, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
vr=load('validate_perceptual_review',ROOT/'scripts'/'validate_perceptual_review.py')
class PerceptualR3Tests(unittest.TestCase):
    def evidence(self,status='passed'):
        return {'schema_version':'visual-evidence-receipt/v1','status':status,'artifact_sha256':'a'*64,'perceptual_review':'pending','errors':[],
          'viewports':[{'width':1440,'height':900},{'width':1600,'height':1000},{'width':1920,'height':1080},{'width':2048,'height':1320}],
          'screenshots':[]}
    def write_pair(self,td,evidence,review,with_shots=True):
        if with_shots and evidence.get('status')=='passed':
            shots=[]
            for w,h in [(1440,900),(2048,1320)]:
                name=f'shot-{w}x{h}.png';raw=f'{w}x{h}'.encode();(Path(td)/name).write_bytes(raw);shots.append({'width':w,'height':h,'path':name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
            evidence=dict(evidence);evidence['screenshots']=shots
        ep=Path(td)/'evidence.json'; ep.write_text(json.dumps(evidence,separators=(',',':')))
        raw=ep.read_bytes(); review=dict(review); review.setdefault('evidence_sha256',hashlib.sha256(raw).hexdigest()); review.setdefault('artifact_sha256',evidence['artifact_sha256'])
        rp=Path(td)/'review.json';rp.write_text(json.dumps(review));return ep,rp
    def base_review(self,status='passed'):
        return {'schema_version':'visual-perceptual-review/v1','reviewer':{'id':'reviewer-1','type':'model'},'status':status,'defects':[]}
    def test_pass_requires_binding_and_zero_defects(self):
        with tempfile.TemporaryDirectory() as td:
            ep,rp=self.write_pair(td,self.evidence(),self.base_review());r=vr.validate(ep,rp);self.assertEqual(r['delivery_status'],'perceptually-passed');self.assertEqual(r['status'],'valid')
    def test_artifact_binding_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as td:
            ep,rp=self.write_pair(td,self.evidence(),self.base_review());d=json.loads(rp.read_text());d['artifact_sha256']='b'*64;rp.write_text(json.dumps(d));self.assertIn('artifact-binding',{e['code'] for e in vr.validate(ep,rp)['errors']})
    def test_evidence_binding_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as td:
            ep,rp=self.write_pair(td,self.evidence(),self.base_review());d=json.loads(rp.read_text());d['evidence_sha256']='c'*64;rp.write_text(json.dumps(d));self.assertIn('evidence-binding',{e['code'] for e in vr.validate(ep,rp)['errors']})
    def test_pass_rejected_when_browser_evidence_failed(self):
        with tempfile.TemporaryDirectory() as td:
            ep,rp=self.write_pair(td,self.evidence('failed'),self.base_review(),with_shots=False);self.assertIn('evidence-not-passed',{e['code'] for e in vr.validate(ep,rp)['errors']})
    def test_pass_rejects_missing_screenshot(self):
        with tempfile.TemporaryDirectory() as td:
            ep,rp=self.write_pair(td,self.evidence(),self.base_review());(Path(td)/'shot-1440x900.png').unlink();self.assertIn('screenshot-missing',{e['code'] for e in vr.validate(ep,rp)['errors']})
    def test_pass_rejects_tampered_screenshot(self):
        with tempfile.TemporaryDirectory() as td:
            ep,rp=self.write_pair(td,self.evidence(),self.base_review());(Path(td)/'shot-2048x1320.png').write_bytes(b'tampered');self.assertIn('screenshot-sha',{e['code'] for e in vr.validate(ep,rp)['errors']})
    def test_pass_rejects_incomplete_viewports(self):
        with tempfile.TemporaryDirectory() as td:
            e=self.evidence();e['viewports']=e['viewports'][:-1];ep,rp=self.write_pair(td,e,self.base_review());self.assertIn('viewport-coverage',{x['code'] for x in vr.validate(ep,rp)['errors']})
    def test_failed_review_requires_concrete_defect(self):
        with tempfile.TemporaryDirectory() as td:
            ep,rp=self.write_pair(td,self.evidence(),self.base_review('failed'));self.assertIn('failure-without-defect',{e['code'] for e in vr.validate(ep,rp)['errors']})
    def test_failed_review_with_defect_is_valid(self):
        with tempfile.TemporaryDirectory() as td:
            q=self.base_review('failed');q['defects']=[{'code':'label-overlap','severity':'major','evidence':'1440x900 screenshot'}];ep,rp=self.write_pair(td,self.evidence(),q);r=vr.validate(ep,rp);self.assertEqual(r['status'],'valid');self.assertEqual(r['delivery_status'],'perceptually-failed')
    def test_skipped_requires_reason(self):
        with tempfile.TemporaryDirectory() as td:
            ep,rp=self.write_pair(td,self.evidence(),self.base_review('skipped'));self.assertIn('skip-without-reason',{e['code'] for e in vr.validate(ep,rp)['errors']})
    def test_skipped_with_reason_is_valid(self):
        with tempfile.TemporaryDirectory() as td:
            q=self.base_review('skipped');q['reason']='no capable image reviewer';ep,rp=self.write_pair(td,self.evidence(),q);r=vr.validate(ep,rp);self.assertEqual(r['delivery_status'],'perceptual-review-skipped')
    def test_visual_checker_javascript_syntax(self):
        p=subprocess.run(['node','--check',str(ROOT/'scripts'/'visual_check.mjs')],capture_output=True,text=True);self.assertEqual(p.returncode,0,p.stderr)
if __name__=='__main__': unittest.main()
