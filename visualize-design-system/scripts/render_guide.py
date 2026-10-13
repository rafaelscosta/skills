#!/usr/bin/env python3
"""Render a standalone HTML design-system visual guide from guide-spec.json."""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import sys
from pathlib import Path
from typing import Any


PROVENANCE_LABELS = {
    "implemented": "IMPLEMENTADO",
    "documented": "DOCUMENTADO",
    "inferred": "INFERIDO",
    "proposed": "PROPOSTO",
    "missing": "AUSENTE",
    "deprecated": "DEPRECADO",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="guide-spec.json")
    parser.add_argument("--output", type=Path, required=True, help="Standalone HTML output")
    return parser.parse_args()


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"file not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value


def data_uri(src: str, base_dir: Path) -> str:
    if src.startswith(("data:", "http://", "https://")):
        return src
    path = (base_dir / src).resolve()
    if not path.exists() or not path.is_file():
        return src
    mime, _ = mimetypes.guess_type(path.name)
    mime = mime or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def provenance_badge(status: Any) -> str:
    if not isinstance(status, str) or status not in PROVENANCE_LABELS:
        return ""
    return f'<span class="provenance provenance-{esc(status)}">{esc(PROVENANCE_LABELS[status])}</span>'


def render_sample(sample: Any, base_dir: Path) -> str:
    if not isinstance(sample, dict):
        return '<div class="sample empty-sample">—</div>'
    kind = sample.get("kind", "empty")
    provenance = provenance_badge(sample.get("provenance"))

    if kind == "button":
        label = esc(sample.get("label", "Button"))
        variant = esc(sample.get("variant", "primary"))
        state = esc(sample.get("state", "default"))
        size = esc(sample.get("size", "md"))
        icon = sample.get("icon")
        icon_html = '<span class="button-icon" aria-hidden="true">→</span>' if icon else ""
        spinner = '<span class="spinner" aria-hidden="true"></span>' if state == "loading" else ""
        disabled = " disabled" if state == "disabled" else ""
        return (
            f'<div class="sample sample-button">'
            f'<button class="ds-button {variant} state-{state} size-{size}"{disabled}>'
            f'{spinner}{icon_html}<span>{label}</span></button>{provenance}</div>'
        )

    if kind == "input":
        label = esc(sample.get("label", "Label"))
        value = esc(sample.get("value", ""))
        description = esc(sample.get("description", ""))
        state = esc(sample.get("state", "default"))
        disabled = " disabled" if state == "disabled" else ""
        readonly = " readonly" if state in {"read-only", "readonly"} else ""
        supporting = f'<span class="input-description">{description}</span>' if description else ""
        return (
            f'<div class="sample input-sample state-{state}">'
            f'<label>{label}<input value="{value}"{disabled}{readonly}></label>{supporting}{provenance}</div>'
        )

    if kind == "badge":
        label = esc(sample.get("label", "Badge"))
        variant = esc(sample.get("variant", "neutral"))
        return f'<div class="sample"><span class="ds-badge {variant}">{label}</span>{provenance}</div>'

    if kind == "swatch":
        value = esc(sample.get("value", "#000000"))
        token = esc(sample.get("token", ""))
        label = esc(sample.get("label", ""))
        return (
            f'<div class="sample swatch-sample"><span class="swatch" style="--swatch:{value}"></span>'
            f'<span class="swatch-copy"><strong>{label or value}</strong><code>{token or value}</code></span>'
            f'{provenance}</div>'
        )

    if kind == "typography":
        label = esc(sample.get("label", "Aa"))
        value = esc(sample.get("value", "16 / 24"))
        token = esc(sample.get("token", ""))
        size = esc(sample.get("size", "md"))
        return (
            f'<div class="sample type-sample type-{size}"><span class="type-preview">{label}</span>'
            f'<span class="type-meta"><code>{token}</code><small>{value}</small></span>{provenance}</div>'
        )

    if kind == "spacing":
        label = esc(sample.get("label", "Spacing"))
        value = sample.get("value", 16)
        try:
            numeric = max(2, min(240, float(value)))
        except (TypeError, ValueError):
            numeric = 16
        token = esc(sample.get("token", ""))
        return (
            f'<div class="sample spacing-sample"><span class="spacing-bar" style="width:{numeric * 2}px"></span>'
            f'<span><strong>{label}</strong><code>{token or esc(value)}</code></span>{provenance}</div>'
        )

    if kind == "code":
        value = esc(sample.get("value", sample.get("label", "")))
        return f'<div class="sample code-sample"><code>{value}</code>{provenance}</div>'

    if kind == "image":
        src = sample.get("src", "")
        alt = esc(sample.get("alt", sample.get("label", "")))
        resolved = esc(data_uri(str(src), base_dir))
        return f'<figure class="sample image-sample"><img src="{resolved}" alt="{alt}">{provenance}</figure>'

    if kind == "html":
        raw = str(sample.get("html", ""))
        content = raw if sample.get("trusted_html") is True else esc(raw)
        return f'<div class="sample html-sample">{content}{provenance}</div>'

    return f'<div class="sample empty-sample">{esc(sample.get("label", "—"))}{provenance}</div>'


def section_shell(section: dict[str, Any], body: str, extra_class: str = "") -> str:
    span = section.get("span", "full")
    title = esc(section.get("title", ""))
    subtitle = section.get("subtitle")
    subtitle_html = f'<p class="section-subtitle">{esc(subtitle)}</p>' if subtitle else ""
    badge = provenance_badge(section.get("provenance"))
    return (
        f'<section class="guide-section span-{esc(span)} {extra_class}" id="{esc(section.get("id", "section"))}">'
        f'<div class="section-heading"><div><h2>{title}</h2>{subtitle_html}</div>{badge}</div>{body}</section>'
    )


def render_matrix(section: dict[str, Any], base_dir: Path) -> str:
    columns = section.get("columns", [])
    rows = section.get("rows", [])
    header = '<div class="matrix-corner"></div>' + "".join(
        f'<div class="matrix-column"><strong>{esc(col.get("label"))}</strong>'
        f'{f"<small>{esc(col.get('description'))}</small>" if col.get("description") else ""}</div>'
        for col in columns
    )
    row_html: list[str] = []
    for row in rows:
        label = (
            f'<div class="matrix-row-label"><strong>{esc(row.get("label"))}</strong>'
            f'<small>{esc(row.get("description", ""))}</small></div>'
        )
        cells: list[str] = []
        for cell in row.get("cells", []):
            if cell.get("unavailable"):
                content = '<div class="unavailable">N/D</div>'
            else:
                content = render_sample(cell.get("sample"), base_dir)
                if cell.get("caption"):
                    content += f'<small class="cell-caption">{esc(cell.get("caption"))}</small>'
            cells.append(f'<div class="matrix-cell">{content}</div>')
        row_html.append(label + "".join(cells))
    style = f'--matrix-columns:{len(columns)}'
    return section_shell(section, f'<div class="matrix" style="{style}">{header}{"".join(row_html)}</div>', "section-matrix")


def render_cards(section: dict[str, Any], base_dir: Path) -> str:
    columns = int(section.get("columns", 2))
    cards: list[str] = []
    for item in section.get("items", []):
        number = f'<span class="item-number">{esc(item.get("number"))}</span>' if item.get("number") is not None else ""
        body = f'<p>{esc(item.get("body"))}</p>' if item.get("body") else ""
        use_when = f'<p class="rule"><strong>Use:</strong> {esc(item.get("use_when"))}</p>' if item.get("use_when") else ""
        avoid_when = f'<p class="rule"><strong>Evite:</strong> {esc(item.get("avoid_when"))}</p>' if item.get("avoid_when") else ""
        technical = f'<code class="technical">{esc(item.get("technical"))}</code>' if item.get("technical") else ""
        sample = render_sample(item.get("sample"), base_dir) if item.get("sample") else ""
        cards.append(
            f'<article class="mini-card">{number}<div class="mini-card-copy"><h3>{esc(item.get("title"))}</h3>'
            f'{body}{use_when}{avoid_when}{technical}</div>{sample}{provenance_badge(item.get("provenance"))}</article>'
        )
    body = f'<div class="cards-grid" style="--card-columns:{columns}">{"".join(cards)}</div>'
    return section_shell(section, body, "section-cards")


def render_pairs(section: dict[str, Any], base_dir: Path) -> str:
    pairs: list[str] = []
    for item in section.get("items", []):
        sides: list[str] = []
        for key, label in (("do", "DO"), ("dont", "DON'T")):
            side = item.get(key, {})
            cls = "positive" if key == "do" else "negative"
            sample = render_sample(side.get("sample"), base_dir) if side.get("sample") else ""
            technical = f'<code class="technical">{esc(side.get("technical"))}</code>' if side.get("technical") else ""
            sides.append(
                f'<div class="pair-side {cls}"><div class="pair-label">{label}</div>{sample}'
                f'<h3>{esc(side.get("title"))}</h3><p>{esc(side.get("body"))}</p>{technical}</div>'
            )
        pairs.append(
            f'<article class="pair"><div class="pair-topic">{esc(item.get("topic"))}</div>'
            f'<div class="pair-grid">{"".join(sides)}</div></article>'
        )
    return section_shell(section, f'<div class="pairs-list">{"".join(pairs)}</div>', "section-pairs")


def render_anatomy(section: dict[str, Any], base_dir: Path) -> str:
    callouts = "".join(
        f'<div class="callout"><strong>{esc(item.get("label"))}</strong><span>{esc(item.get("detail"))}</span>'
        f'{f"<code>{esc(item.get('token'))}</code>" if item.get("token") else ""}</div>'
        for item in section.get("callouts", [])
    )
    specs = "".join(
        f'<div class="spec"><span>{esc(item.get("label"))}</span><strong>{esc(item.get("value"))}</strong>'
        f'{f"<code>{esc(item.get('token'))}</code>" if item.get("token") else ""}</div>'
        for item in section.get("specs", [])
    )
    body = (
        f'<div class="anatomy-stage">{render_sample(section.get("sample"), base_dir)}</div>'
        f'<div class="callouts-grid">{callouts}</div>'
        f'{f"<div class=\"specs-grid\">{specs}</div>" if specs else ""}'
    )
    return section_shell(section, body, "section-anatomy")


def render_tokens(section: dict[str, Any], base_dir: Path) -> str:
    groups: list[str] = []
    for group in section.get("groups", []):
        tokens: list[str] = []
        for token in group.get("tokens", []):
            preview = render_sample(token.get("preview"), base_dir) if token.get("preview") else ""
            alias = f'<small>← {esc(token.get("alias_of"))}</small>' if token.get("alias_of") else ""
            role = f'<p>{esc(token.get("role"))}</p>' if token.get("role") else ""
            tokens.append(
                f'<article class="token-row">{preview}<div><code>{esc(token.get("name"))}</code>'
                f'<strong>{esc(token.get("value"))}</strong>{role}{alias}</div>{provenance_badge(token.get("provenance"))}</article>'
            )
        groups.append(f'<div class="token-group"><h3>{esc(group.get("title"))}</h3>{"".join(tokens)}</div>')
    return section_shell(section, f'<div class="token-groups">{"".join(groups)}</div>', "section-tokens")


def render_decision(section: dict[str, Any]) -> str:
    headers = "".join(f'<th>{esc(value)}</th>' for value in section.get("columns", []))
    rows = "".join(
        f'<tr>{"".join(f"<td>{esc(value)}</td>" for value in row.get("cells", []))}</tr>'
        for row in section.get("rows", [])
    )
    return section_shell(section, f'<div class="decision-wrap"><table><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table></div>', "section-decision")


def render_responsive(section: dict[str, Any], base_dir: Path) -> str:
    frames = "".join(
        f'<article class="responsive-frame"><div class="frame-top"><strong>{esc(frame.get("label"))}</strong>'
        f'<code>{esc(frame.get("condition"))}</code></div>{render_sample(frame.get("sample"), base_dir)}'
        f'<p>{esc(frame.get("behavior", ""))}</p>{provenance_badge(frame.get("provenance"))}</article>'
        for frame in section.get("frames", [])
    )
    return section_shell(section, f'<div class="responsive-strip">{frames}</div>', "section-responsive")


def render_notes(section: dict[str, Any]) -> str:
    notes = "".join(
        f'<article class="note-card"><span class="note-icon">{esc(item.get("icon", "•"))}</span>'
        f'<div><h3>{esc(item.get("title"))}</h3><p>{esc(item.get("body"))}</p></div></article>'
        for item in section.get("items", [])
    )
    return section_shell(section, f'<div class="notes-grid">{notes}</div>', "section-notes")


def render_section(section: dict[str, Any], base_dir: Path) -> str:
    stype = section.get("type")
    if stype == "matrix":
        return render_matrix(section, base_dir)
    if stype == "cards":
        return render_cards(section, base_dir)
    if stype == "pairs":
        return render_pairs(section, base_dir)
    if stype == "anatomy":
        return render_anatomy(section, base_dir)
    if stype == "tokens":
        return render_tokens(section, base_dir)
    if stype == "decision":
        return render_decision(section)
    if stype == "responsive":
        return render_responsive(section, base_dir)
    if stype == "notes":
        return render_notes(section)
    return section_shell(section, f'<p>Unsupported section type: <code>{esc(stype)}</code></p>', "section-unsupported")


def build_css(theme: dict[str, Any], width: int, height: int) -> str:
    def value(key: str, default: str) -> str:
        return str(theme.get(key, default))

    texture = theme.get("texture", "none")
    texture_css = ""
    if texture == "subtle-grid":
        texture_css = "background-image:linear-gradient(rgba(23,25,20,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(23,25,20,.035) 1px,transparent 1px);background-size:24px 24px;"
    elif texture == "paper":
        texture_css = "background-image:radial-gradient(rgba(23,25,20,.05) .6px,transparent .6px);background-size:5px 5px;"
    elif texture == "noise":
        texture_css = "background-image:radial-gradient(rgba(23,25,20,.045) .7px,transparent .7px);background-size:3px 3px;"

    return f"""
:root {{
  --bg: {value('background', '#F4F1E8')};
  --surface: {value('surface', '#FFFDF8')};
  --surface-alt: {value('surface_alt', '#ECE9DF')};
  --text: {value('text', '#171914')};
  --muted: {value('muted', '#61655B')};
  --accent: {value('accent', '#5E6B35')};
  --accent-text: {value('accent_text', '#FFFFFF')};
  --border: {value('border', '#C8C7BC')};
  --positive: {value('positive', '#2F6A4F')};
  --negative: {value('negative', '#A24338')};
  --warning: {value('warning', '#B47A24')};
  --radius: {int(theme.get('radius', 16))}px;
  --font-sans: {value('font_sans', 'Inter, Arial, sans-serif')};
  --font-display: {value('font_display', 'Inter, Arial, sans-serif')};
}}
* {{ box-sizing: border-box; }}
html, body {{ margin:0; padding:0; width:{width}px; min-width:{width}px; height:{height}px; min-height:{height}px; background:var(--bg); color:var(--text); font-family:var(--font-sans); }}
body {{ overflow:hidden; }}
.page {{ width:{width}px; height:{height}px; padding:34px 38px 26px; display:flex; flex-direction:column; gap:16px; background-color:var(--bg); {texture_css} overflow:hidden; }}
.header {{ border-bottom:2px solid var(--text); padding-bottom:18px; }}
.header-meta {{ display:flex; justify-content:space-between; gap:20px; align-items:center; margin-bottom:10px; font-size:13px; font-weight:800; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); }}
.header h1 {{ margin:0; max-width:900px; font-family:var(--font-display); font-size:66px; line-height:.93; letter-spacing:-.055em; text-transform:uppercase; font-weight:900; }}
.header-bottom {{ display:flex; justify-content:space-between; align-items:flex-end; gap:28px; margin-top:10px; }}
.header-subtitle {{ margin:0; max-width:760px; font-size:20px; line-height:1.35; font-weight:560; }}
.system-chip {{ flex:0 0 auto; display:inline-flex; gap:8px; align-items:center; background:var(--text); color:var(--bg); border-radius:999px; padding:8px 12px; font-size:12px; font-weight:800; letter-spacing:.05em; }}
.sections {{ flex:1; min-height:0; display:grid; grid-template-columns:repeat(12,minmax(0,1fr)); grid-auto-flow:row dense; gap:14px; align-content:start; }}
.guide-section {{ background:color-mix(in srgb,var(--surface) 94%,transparent); border:1px solid var(--border); border-radius:var(--radius); padding:16px; min-width:0; box-shadow:0 1px 0 rgba(23,25,20,.03); }}
.span-full {{ grid-column:span 12; }} .span-half {{ grid-column:span 6; }} .span-third {{ grid-column:span 4; }} .span-two-thirds {{ grid-column:span 8; }}
.section-heading {{ display:flex; align-items:flex-start; justify-content:space-between; gap:12px; margin-bottom:12px; border-bottom:1px solid var(--border); padding-bottom:9px; }}
.section-heading h2 {{ margin:0; font-size:20px; line-height:1; letter-spacing:-.02em; font-weight:900; text-transform:uppercase; }}
.section-subtitle {{ margin:5px 0 0; color:var(--muted); font-size:12px; line-height:1.35; }}
.provenance {{ display:inline-flex; align-items:center; border:1px solid currentColor; border-radius:999px; padding:4px 7px; font-size:8px; line-height:1; letter-spacing:.08em; font-weight:900; white-space:nowrap; color:var(--muted); }}
.provenance-proposed,.provenance-inferred {{ color:var(--warning); }} .provenance-missing,.provenance-deprecated {{ color:var(--negative); }} .provenance-implemented {{ color:var(--positive); }}
.sample {{ position:relative; display:flex; justify-content:center; align-items:center; min-width:0; }}
.sample > .provenance {{ position:absolute; right:0; bottom:-12px; transform:scale(.82); transform-origin:right bottom; }}
.ds-button {{ appearance:none; border:1px solid transparent; border-radius:10px; min-width:112px; display:inline-flex; align-items:center; justify-content:center; gap:7px; font-family:var(--font-sans); font-size:13px; font-weight:750; line-height:1; white-space:nowrap; cursor:default; transition:none; }}
.ds-button.size-sm {{ height:30px; padding:0 11px; font-size:11px; }} .ds-button.size-md {{ height:36px; padding:0 14px; }} .ds-button.size-lg {{ height:42px; padding:0 17px; font-size:14px; }}
.ds-button.primary {{ background:var(--accent); color:var(--accent-text); }}
.ds-button.primary.state-hover {{ background:color-mix(in srgb,var(--accent) 82%,#000); }}
.ds-button.secondary {{ background:var(--surface); color:var(--accent); border-color:var(--accent); }}
.ds-button.secondary.state-hover {{ background:color-mix(in srgb,var(--accent) 10%,var(--surface)); }}
.ds-button.ghost {{ background:transparent; color:var(--text); }}
.ds-button.ghost.state-hover {{ background:var(--surface-alt); }}
.ds-button.destructive {{ background:var(--negative); color:#fff; }}
.ds-button.destructive.state-hover {{ background:color-mix(in srgb,var(--negative) 82%,#000); }}
.ds-button.state-focus {{ outline:3px solid color-mix(in srgb,var(--accent) 38%,transparent); outline-offset:2px; }}
.ds-button.destructive.state-focus {{ outline-color:color-mix(in srgb,var(--negative) 38%,transparent); }}
.ds-button.state-disabled,.ds-button:disabled {{ opacity:.38; filter:saturate(.45); }}
.button-icon {{ font-size:15px; line-height:1; }}
.spinner {{ width:13px; height:13px; border:2px solid currentColor; border-right-color:transparent; border-radius:50%; }}
.inline-buttons {{ display:flex; gap:7px; align-items:center; justify-content:center; flex-wrap:wrap; }}
.input-sample {{ flex-direction:column; align-items:stretch; gap:4px; }} .input-sample label {{ display:flex; flex-direction:column; gap:5px; font-size:11px; font-weight:750; }} .input-sample input {{ height:36px; min-width:180px; border:1px solid var(--border); background:var(--surface); border-radius:8px; padding:0 10px; color:var(--text); font:inherit; }} .input-sample.state-focus input {{ outline:3px solid color-mix(in srgb,var(--accent) 30%,transparent); border-color:var(--accent); }} .input-sample.state-error input {{ border-color:var(--negative); }} .input-description {{ font-size:10px; color:var(--muted); }}
.ds-badge {{ display:inline-flex; border-radius:999px; border:1px solid var(--border); padding:5px 8px; font-size:10px; font-weight:800; }} .ds-badge.positive {{ color:var(--positive); border-color:var(--positive); }} .ds-badge.negative {{ color:var(--negative); border-color:var(--negative); }}
.swatch-sample {{ justify-content:flex-start; gap:10px; }} .swatch {{ width:42px; height:42px; border-radius:10px; background:var(--swatch); border:1px solid rgba(0,0,0,.12); flex:none; }} .swatch-copy {{ display:flex; flex-direction:column; gap:3px; }}
.type-sample {{ justify-content:space-between; gap:12px; }} .type-preview {{ font-size:30px; font-weight:800; }} .type-lg .type-preview {{ font-size:42px; }} .type-sm .type-preview {{ font-size:20px; }} .type-meta {{ display:flex; flex-direction:column; align-items:flex-end; }}
.spacing-sample {{ justify-content:flex-start; gap:10px; }} .spacing-bar {{ height:12px; min-width:4px; max-width:220px; background:var(--accent); border-radius:999px; }} .spacing-sample > span:last-of-type {{ display:flex; flex-direction:column; }}
.code-sample code,.technical,code {{ font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:10px; }} .code-sample {{ padding:8px 10px; background:var(--surface-alt); border-radius:8px; justify-content:flex-start; }}
.image-sample {{ margin:0; overflow:hidden; border-radius:10px; background:var(--surface-alt); }} .image-sample img {{ width:100%; height:100%; object-fit:cover; display:block; }}
.matrix {{ display:grid; grid-template-columns:150px repeat(var(--matrix-columns),minmax(0,1fr)); border:1px solid var(--border); border-radius:12px; overflow:hidden; }}
.matrix > * {{ min-width:0; border-right:1px solid var(--border); border-bottom:1px solid var(--border); }} .matrix > *:nth-child(calc(var(--matrix-columns) + 1n)) {{ }}
.matrix-corner,.matrix-column {{ background:var(--text); color:var(--bg); min-height:38px; }} .matrix-column {{ display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding:6px; font-size:11px; }} .matrix-column small {{ font-size:9px; opacity:.72; }}
.matrix-row-label {{ background:var(--surface-alt); display:flex; flex-direction:column; justify-content:center; padding:9px 10px; }} .matrix-row-label strong {{ font-size:12px; }} .matrix-row-label small {{ color:var(--muted); font-size:9px; margin-top:2px; }}
.matrix-cell {{ min-height:54px; padding:8px 6px; display:flex; flex-direction:column; align-items:center; justify-content:center; background:var(--surface); }} .matrix-cell .ds-button {{ transform:scale(.9); }} .cell-caption {{ margin-top:5px; color:var(--muted); font-size:8px; }} .unavailable {{ color:var(--muted); font-size:10px; }}
.cards-grid {{ display:grid; grid-template-columns:repeat(var(--card-columns),minmax(0,1fr)); gap:8px; }} .mini-card {{ position:relative; display:grid; grid-template-columns:auto 1fr auto; align-items:center; gap:9px; padding:9px 10px; border:1px solid var(--border); border-radius:11px; background:var(--surface); min-width:0; }} .item-number {{ display:grid; place-items:center; width:24px; height:24px; border-radius:7px; background:var(--accent); color:var(--accent-text); font-size:11px; font-weight:900; }} .mini-card h3 {{ margin:0; font-size:12px; }} .mini-card p {{ margin:2px 0 0; color:var(--muted); font-size:9.5px; line-height:1.3; }} .mini-card .technical {{ display:block; margin-top:3px; color:var(--accent); }} .mini-card > .provenance {{ position:absolute; right:7px; top:6px; transform:scale(.72); transform-origin:right top; }} .rule strong {{ color:var(--text); }}
.anatomy-stage {{ min-height:76px; display:grid; place-items:center; margin-bottom:10px; border-radius:11px; background:var(--surface-alt); }} .callouts-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:6px; }} .callout {{ padding:7px 8px; border-left:3px solid var(--accent); background:var(--surface); border-radius:6px; display:flex; flex-direction:column; }} .callout strong {{ font-size:10px; }} .callout span {{ font-size:9px; color:var(--muted); }} .callout code {{ margin-top:2px; color:var(--accent); font-size:8px; }} .specs-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:6px; margin-top:8px; }} .spec {{ padding:7px; background:var(--text); color:var(--bg); border-radius:8px; display:flex; flex-direction:column; }} .spec span {{ font-size:8px; opacity:.72; }} .spec strong {{ font-size:11px; }} .spec code {{ font-size:7px; opacity:.7; }}
.pairs-list {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; }} .pair {{ border:1px solid var(--border); border-radius:11px; overflow:hidden; background:var(--surface); }} .pair-topic {{ padding:6px 9px; background:var(--text); color:var(--bg); font-size:10px; font-weight:900; text-transform:uppercase; letter-spacing:.05em; }} .pair-grid {{ display:grid; grid-template-columns:1fr 1fr; }} .pair-side {{ min-width:0; padding:8px; position:relative; }} .pair-side + .pair-side {{ border-left:1px solid var(--border); }} .pair-label {{ display:inline-flex; margin-bottom:6px; padding:3px 5px; border-radius:5px; color:#fff; font-size:8px; font-weight:900; }} .pair-side.positive .pair-label {{ background:var(--positive); }} .pair-side.negative .pair-label {{ background:var(--negative); }} .pair-side .sample {{ min-height:42px; margin-bottom:5px; }} .pair-side .ds-button {{ transform:scale(.82); }} .pair-side h3 {{ margin:0; font-size:10px; }} .pair-side p {{ margin:2px 0 0; color:var(--muted); font-size:8.5px; line-height:1.25; }}
.token-groups {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; }} .token-group {{ border:1px solid var(--border); border-radius:10px; overflow:hidden; }} .token-group > h3 {{ margin:0; padding:7px 9px; background:var(--text); color:var(--bg); font-size:11px; }} .token-row {{ display:grid; grid-template-columns:auto 1fr auto; gap:8px; align-items:center; padding:7px 9px; border-top:1px solid var(--border); }} .token-row:first-of-type {{ border-top:0; }} .token-row > div {{ min-width:0; display:flex; flex-direction:column; }} .token-row code {{ overflow:hidden; text-overflow:ellipsis; }} .token-row strong {{ font-size:10px; }} .token-row p,.token-row small {{ margin:2px 0 0; color:var(--muted); font-size:8px; }}
.decision-wrap {{ overflow:hidden; border:1px solid var(--border); border-radius:10px; }} table {{ width:100%; border-collapse:collapse; table-layout:fixed; }} th {{ background:var(--text); color:var(--bg); font-size:9px; text-transform:uppercase; padding:7px; }} td {{ border-top:1px solid var(--border); border-right:1px solid var(--border); padding:7px; font-size:9px; line-height:1.25; vertical-align:top; }} td:last-child,th:last-child {{ border-right:0; }}
.responsive-strip {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:8px; }} .responsive-frame {{ border:1px solid var(--border); border-radius:10px; padding:8px; min-width:0; }} .frame-top {{ display:flex; justify-content:space-between; gap:5px; align-items:center; margin-bottom:7px; }} .frame-top strong {{ font-size:10px; }} .frame-top code {{ color:var(--accent); }} .responsive-frame .sample {{ min-height:70px; background:var(--surface-alt); border-radius:8px; }} .responsive-frame p {{ margin:6px 0 0; font-size:8.5px; color:var(--muted); }}
.notes-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; }} .note-card {{ display:flex; gap:9px; padding:9px; border:1px solid var(--border); border-radius:10px; background:var(--surface); }} .note-icon {{ display:grid; place-items:center; width:25px; height:25px; flex:none; border-radius:7px; background:var(--accent); color:var(--accent-text); font-weight:900; }} .note-card h3 {{ margin:0; font-size:11px; }} .note-card p {{ margin:2px 0 0; color:var(--muted); font-size:9px; line-height:1.3; }}
.footer {{ display:grid; grid-template-columns:auto 1fr auto; gap:13px; align-items:center; border-top:2px solid var(--text); padding-top:12px; }} .footer-kicker {{ background:var(--accent); color:var(--accent-text); border-radius:999px; padding:7px 10px; font-size:10px; font-weight:900; letter-spacing:.08em; }} .footer-text {{ margin:0; font-size:13px; line-height:1.3; font-weight:650; }} .footer-source {{ max-width:270px; color:var(--muted); font-size:8px; line-height:1.25; text-align:right; }}
.legend {{ display:flex; gap:6px; flex-wrap:wrap; align-items:center; }} .legend-label {{ font-size:8px; font-weight:900; letter-spacing:.08em; color:var(--muted); }}
@media print {{ @page {{ size:{width}px {height}px; margin:0; }} html,body,.page {{ print-color-adjust:exact; -webkit-print-color-adjust:exact; }} }}
"""


def render_document(spec: dict[str, Any], spec_path: Path) -> str:
    meta = spec.get("meta", {})
    theme = spec.get("theme", {})
    canvas = meta.get("canvas", {})
    width = int(canvas.get("width", 1080))
    height = int(canvas.get("height", 1350))
    sections = "".join(render_section(section, spec_path.parent) for section in spec.get("sections", []))

    system_bits = [value for value in (meta.get("system_name"), meta.get("system_version")) if value]
    system_text = " · ".join(map(str, system_bits)) or "DESIGN SYSTEM"
    status = provenance_badge(meta.get("status"))
    chip = f'<span class="system-chip">{esc(system_text)} {status}</span>'

    footer = spec.get("footer", {})
    footer_html = ""
    if footer:
        footer_html = (
            '<footer class="footer">'
            f'<span class="footer-kicker">{esc(footer.get("kicker", "TAKEAWAY"))}</span>'
            f'<p class="footer-text">{esc(footer.get("text", ""))}</p>'
            f'<div class="footer-source">{esc(footer.get("source_note", ""))}</div>'
            '</footer>'
        )

    legend_html = ""
    if spec.get("provenance_legend"):
        badges = "".join(provenance_badge(key) for key in ("implemented", "documented", "inferred", "proposed"))
        legend_html = f'<div class="legend"><span class="legend-label">PROVENIÊNCIA</span>{badges}</div>'

    css = build_css(theme, width, height)
    language = esc(meta.get("language", "pt-BR"))
    title = esc(meta.get("title", "Design-system guide"))
    return f"""<!doctype html>
<html lang="{language}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width={width}, initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<main class="page" id="guide-page">
  <header class="header">
    <div class="header-meta"><span>{esc(meta.get('eyebrow', 'DESIGN SYSTEM GUIDE'))}</span>{legend_html}</div>
    <h1>{title}</h1>
    <div class="header-bottom"><p class="header-subtitle">{esc(meta.get('subtitle', ''))}</p>{chip}</div>
  </header>
  <div class="sections">{sections}</div>
  {footer_html}
</main>
<script>
window.addEventListener('load', () => {{
  const page = document.getElementById('guide-page');
  const overflow = [];
  document.querySelectorAll('.guide-section, .matrix-cell, .mini-card, .pair-side').forEach((el) => {{
    if (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1) {{
      overflow.push({{tag: el.tagName, id: el.id || null, className: el.className, scrollWidth: el.scrollWidth, clientWidth: el.clientWidth, scrollHeight: el.scrollHeight, clientHeight: el.clientHeight}});
    }}
  }});
  window.__guideDiagnostics = {{
    expectedWidth: {width},
    expectedHeight: {height},
    pageWidth: page.scrollWidth,
    pageHeight: page.scrollHeight,
    bodyWidth: document.body.scrollWidth,
    bodyHeight: document.body.scrollHeight,
    overflow
  }};
  if (overflow.length || page.scrollHeight > {height} || page.scrollWidth > {width}) {{
    console.warn('GUIDE_OVERFLOW', window.__guideDiagnostics);
  }}
}});
</script>
</body>
</html>
"""


def main() -> int:
    args = parse_args()
    try:
        spec = load_json(args.spec)
        rendered = render_document(spec, args.spec.resolve())
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
