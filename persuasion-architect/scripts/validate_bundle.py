#!/usr/bin/env python3
"""Validate the persuasion-architect skill bundle structure and structured-file integrity."""

from __future__ import annotations

import argparse
import json
import re
import sys

try:
    import yaml
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
except ImportError as exc:
    raise SystemExit("Install scripts/requirements.txt before validation: " + str(exc))
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

class UniqueSafeLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node, deep=False):
    result={}
    for key_node,value_node in node.value:
        key=loader.construct_object(key_node,deep=deep)
        if key in result:
            raise yaml.constructor.ConstructorError(None,None,'duplicate mapping key: '+str(key),key_node.start_mark)
        result[key]=loader.construct_object(value_node,deep=deep)
    return result
UniqueSafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique_mapping)
def load_yaml(source):
    return yaml.load(source,Loader=UniqueSafeLoader)

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REFERENCE_RE = re.compile(r"`((?:references|scripts|evals)/[^`]+)`")

REQUIRED = [
    "SKILL.md",
    "config.yaml",
    "agents/openai.yaml",
    "references/belief-and-evidence.md",
    "references/failure-catalog.md",
    "references/mechanism-contract.md",
    "references/persuasion-architecture.schema.json",
    "evals/rubric.yaml",
    "evals/fixtures.yaml",
    "evals/oracle.yaml",
    "scripts/validate_bundle.py",
]


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    message: str


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter delimiter '---'.")
    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("SKILL.md frontmatter is not closed.") from exc

    values: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"Unsupported frontmatter syntax at line {number}: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key or not value:
            raise ValueError(f"Empty frontmatter key/value at line {number}.")
        if key in values:
            raise ValueError(f"Duplicate frontmatter key: {key}")
        values[key] = value
    return values


def validate(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    if not root.is_dir():
        return [Finding("error", "P001", str(root), "Skill root does not exist or is not a directory.")]

    for relative in REQUIRED:
        path = root / relative
        if not path.is_file():
            findings.append(Finding("error", "P002", str(path), f"Required file missing: {relative}"))

    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        return findings

    text = skill_path.read_text(encoding="utf-8")
    try:
        frontmatter = parse_frontmatter(text)
    except ValueError as exc:
        findings.append(Finding("error", "P003", str(skill_path), str(exc)))
        frontmatter = {}

    allowed = {"name", "description"}
    missing = allowed - set(frontmatter)
    extras = set(frontmatter) - allowed
    if missing:
        findings.append(Finding("error", "P004", str(skill_path), f"Missing frontmatter keys: {sorted(missing)}"))
    if extras:
        findings.append(Finding("error", "P005", str(skill_path), f"Unsupported frontmatter keys: {sorted(extras)}"))

    name = frontmatter.get("name", "")
    if name and not NAME_RE.fullmatch(name):
        findings.append(Finding("error", "P006", str(skill_path), f"Invalid skill name: {name}"))
    if name and root.name != name:
        findings.append(Finding("error", "P007", str(root), f"Folder '{root.name}' must match skill name '{name}'."))

    description = frontmatter.get("description", "")
    if description:
        if len(description) > 1024:
            findings.append(Finding("error", "P008", str(skill_path), "Description exceeds 1024 characters."))
        if "Use when" not in description or "Do not use" not in description:
            findings.append(Finding("error", "P009", str(skill_path), "Description must include positive and negative routing boundaries."))

    line_count = len(text.splitlines())
    if line_count > 500:
        findings.append(Finding("warning", "P010", str(skill_path), f"SKILL.md has {line_count} lines; prefer reference loading under 500."))

    for match in REFERENCE_RE.finditer(text):
        relative = match.group(1)
        if not (root / relative).is_file():
            findings.append(Finding("error", "P011", str(skill_path), f"Referenced file missing: {relative}"))

    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            findings.append(Finding("error", "P012", str(path), "Symlinks are not allowed in the portable bundle."))
            continue
        if not path.is_file():
            continue
        try:
            source = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            findings.append(Finding("error", "P013", str(path), f"File is not valid readable UTF-8 text: {exc}"))
            continue

        if path.suffix == ".json":
            try:
                json.loads(source)
            except json.JSONDecodeError as exc:
                findings.append(Finding("error", "P014", str(path), f"Invalid JSON: {exc}"))
        elif path.suffix in {".yaml", ".yml"} and yaml is not None:
            try:
                load_yaml(source)
            except yaml.YAMLError as exc:
                findings.append(Finding("error", "P019", str(path), f"Invalid YAML: {exc}"))
        elif path.suffix == ".py":
            try:
                compile(source, str(path), "exec")
            except SyntaxError as exc:
                findings.append(Finding("error", "P015", str(path), f"Python compile failure: {exc}"))

    metadata_path = root / "agents/openai.yaml"
    if metadata_path.is_file():
        metadata = metadata_path.read_text(encoding="utf-8")
        for required_text in ("interface:", "display_name:", "short_description:", "default_prompt:"):
            if required_text not in metadata:
                findings.append(Finding("error", "P016", str(metadata_path), f"Missing metadata field: {required_text}"))
        if name and f"${name}" not in metadata:
            findings.append(Finding("warning", "P017", str(metadata_path), f"Default prompt should mention explicit invocation '${name}'."))

    try:
        config = load_yaml((root / 'config.yaml').read_text())
        metadata = load_yaml((root / 'agents/openai.yaml').read_text())
        if not isinstance(config, dict) or not isinstance(metadata, dict):
            raise ValueError('config and agent metadata must be mappings')
        contract = config.get('contract')
        if not isinstance(contract, dict):
            raise ValueError('contract must be a mapping')
        expected = {'repository_scope':'read_only','mutation_scope':'none','network_default':'deny','provider_default':'deny','publication_default':'deny','original_input_overwrite':'deny','invented_evidence_policy':'fail_closed','invented_scarcity_policy':'fail_closed','critical_gate_floor':3,'evidence_ledger_required_for_material_claims':True,'mechanism_contract_required_for_material_outcome_claims':True}
        for key, value in expected.items():
            if type(contract.get(key)) is not type(value) or contract.get(key) != value:
                raise ValueError('invalid contract field: ' + key)
        if config.get('output_language') != 'pt-BR':
            raise ValueError('output_language must be pt-BR')
        interface = metadata.get('interface')
        if not isinstance(interface, dict) or any(not isinstance(interface.get(k), str) or not interface[k].strip() for k in ['display_name','short_description','default_prompt']):
            raise ValueError('agent interface requires nonempty string fields')
        rubric = load_yaml((root / 'evals/rubric.yaml').read_text())
        if not isinstance(rubric, dict) or rubric.get('certification_rule',{}).get('average_cannot_override_critical_floor') is not True:
            raise ValueError('rubric must preserve critical floor')
        schema = json.loads((root / 'references/persuasion-architecture.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        for name in ['decision_contract','mechanism_model','beliefs','blocks','qa']:
            if name not in schema.get('required',[]):
                raise ValueError('schema missing required root: ' + name)
        qa = schema['properties']['qa']
        if not {'scores','critical_floor_passed','unresolved_risks'} <= set(qa.get('required',[])):
            raise ValueError('schema must require complete QA')
        score_names = set(rubric['criteria'])
        if set(qa['properties']['scores'].get('required',[])) != score_names:
            raise ValueError('schema must require every score dimension')
    except (ValueError, TypeError, KeyError, OSError, yaml.YAMLError, SchemaError) as exc:
        findings.append(Finding('error','P018',str(root),'Invalid structured contract: ' + str(exc)))

    return findings


def validate_architecture(root: Path, value: dict) -> list[Finding]:
    schema=json.loads((root/'references/persuasion-architecture.schema.json').read_text())
    failures=[Finding('error','P020','architecture',e.message) for e in Draft202012Validator(schema).iter_errors(value)]
    if failures: return failures
    rubric=load_yaml((root/'evals/rubric.yaml').read_text())
    scores=value['qa']['scores']
    floor=all(scores[k]>=rubric['certification_rule']['minimum_each_critical'] for k in rubric['critical_dimensions'])
    if value['qa']['critical_floor_passed'] is not floor:
        failures.append(Finding('error','P021','architecture.qa','Declared critical floor differs from actual scores'))
    beliefs={b['belief_id']:b for b in value['beliefs']}
    if len(beliefs)!=len(value['beliefs']):
        failures.append(Finding('error','P022','architecture.beliefs','Duplicate belief IDs'))
    visiting=set();visited=set()
    def visit(key):
        if key not in beliefs: raise ValueError('unknown belief reference: '+key)
        if key in visiting: raise ValueError('belief dependency cycle')
        if key in visited: return
        visiting.add(key)
        for dep in beliefs[key]['dependencies']: visit(dep)
        visiting.remove(key);visited.add(key)
    try:
        for key in beliefs: visit(key)
    except ValueError as exc:
        failures.append(Finding('error','P023','architecture.beliefs',str(exc)))
    return failures


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate persuasion-architect skill bundle.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--warnings-as-errors", action="store_true")
    parser.add_argument("--architecture", type=Path)
    parser.add_argument("--require-certification", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    findings = validate(root)
    if args.architecture and not findings:
        try:
            findings.extend(validate_architecture(root,json.loads(args.architecture.read_text())))
        except (ValueError,OSError) as exc:
            findings.append(Finding('error','P024',str(args.architecture),str(exc)))
    if args.require_certification:
        config=load_yaml((root/'config.yaml').read_text())
        if config.get('certification',{}).get('behavioral_status') != 'passed':
            findings.append(Finding('error','P025',str(root/'config.yaml'),'Behavioral promotion is not certified'))
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]
    passed = not errors and not (args.warnings_as_errors and warnings)

    if args.json:
        print(json.dumps({"root": str(root), "passed": passed, "findings": [asdict(f) for f in findings]}, ensure_ascii=False, indent=2))
    else:
        print("PERSUASION-ARCHITECT BUNDLE VALIDATION")
        print(f"Root: {root}")
        print(f"Result: {'PASS' if passed else 'FAIL'}")
        print(f"Errors: {len(errors)}")
        print(f"Warnings: {len(warnings)}")
        for finding in findings:
            print(f"\n[{finding.severity.upper()}] {finding.code} {finding.path}\n  {finding.message}")

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
