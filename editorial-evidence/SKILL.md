---
name: editorial-evidence
description: Build an auditable, source-bound claim ledger for editorial work. Use when videos, articles, carousels, presentations, reports, or marketing content depend on factual, quantitative, quoted, causal, contested, or time-sensitive claims that must be verified before downstream writing. Do not use for pure fiction, opinion-only work, or generic research reports that do not need claim-level provenance.
---

# Editorial Evidence

Turn sources into **downstream-safe claims**, not a pile of links.

## Mission

Produce a portable evidence ledger in which every material factual statement has a stable claim id, explicit evidence bindings, epistemic status, allowed editorial use, and the qualifiers needed to prevent downstream exaggeration.

Default reader-facing claim wording and notes to Brazilian Portuguese unless the user requests another language. Keep ids, enums, routing metadata, and implementation instructions in English.

## Core rule

```text
material claim -> source binding -> verification state -> editorial-use decision
```

No material claim is `VERIFIED` merely because a source was found. A citation proves only that a source exists; the binding must support the actual wording.

## What this skill owns

- atomic claim extraction from a brief, draft, script, or research pack;
- source registration and claim-to-source bindings;
- contradiction, freshness, quote, number, and causal checks when triggered;
- editorial wording constraints and `ALLOW / ALLOW_WITH_QUALIFICATION / BLOCK` decisions;
- a deterministic validation receipt for the final ledger.

It does **not** own long-form synthesis, final copywriting, charts, motion design, video rendering, or generic asset licensing.

## Workflow

### 1. Bind the editorial question

Identify the subject, intended downstream artifact, audience, time horizon, and claims that would materially change the audience's understanding or decision.

Do not atomize decorative language, obvious transitions, or harmless subjective framing into fake evidence work.

### 2. Atomize material claims

One claim should be independently verifiable. Split sentences that contain multiple factual propositions.

Classify each claim as one of:

`FACT | QUANTITATIVE | CAUSAL | CORRELATIONAL | ESTIMATE | QUOTE | INTERPRETATION | EXPERT_OPINION | UNCERTAIN`

Use `materiality: HIGH | MEDIUM | LOW` based on the consequence of being wrong in this artifact, not on how interesting the claim sounds.

### 3. Choose the evidence lane

Read `references/risk-routing.md` when a claim is causal, contested, high-consequence, time-sensitive, or unusually load-bearing.

Use the lightest sufficient lane:

- **standard** — ordinary factual support, source binding, and targeted verification;
- **heightened** — contradiction search plus stronger source diversity;
- **adversarial** — hypothesis/falsifier-style investigation when the claim is materially contested or causal and wrongness would be costly.

When available, `brennerbot-with-ntm` is an optional adversarial escalation lane, not a default dependency.

### 4. Register sources before verdicts

Prefer the user's supplied primary material first. When research is required and allowed, prefer primary records, official data, original papers, source code, filings, transcripts, or direct statements over commentary about them.

Record exact locators: page, section, table, timestamp, paragraph anchor, dataset row/query, commit/file line, or equivalent. A homepage URL is not a sufficient locator for a load-bearing claim.

Read `references/evidence-contract.md` for source and binding fields.

### 5. Verify the claim, not the source

For each material claim:

1. test whether the cited evidence supports the exact wording;
2. search for material contradiction when the risk lane requires it;
3. verify freshness for time-sensitive claims;
4. preserve denominator, unit, period, uncertainty, and comparison basis for numbers;
5. preserve exact original wording for quotes and label translations;
6. never upgrade correlation to causation;
7. record unresolved ambiguity rather than forcing a clean verdict.

### 6. Assign epistemic status and editorial use

Use these statuses:

- `VERIFIED` — evidence supports the claim as worded;
- `QUALIFIED` — usable only with stated caveats or narrower wording;
- `CONTESTED` — credible evidence materially disagrees;
- `UNSUPPORTED` — evidence is insufficient for the wording;
- `STALE` — freshness is inadequate for the intended use;
- `RETRACTED` — the source or claim has been formally withdrawn or invalidated.

Then assign:

- `ALLOW`
- `ALLOW_WITH_QUALIFICATION`
- `BLOCK`

Status and editorial use must be compatible. `UNSUPPORTED`, `STALE`, and `RETRACTED` claims are blocked.

### 7. Validate before handoff

Write the ledger as `editorial-evidence-ledger/v1`, then run:

```bash
python3 scripts/validate_ledger.py <ledger.json> --json
```

A deterministic pass proves contract integrity and evidence bindings, not that every external source is truthful. Source truth still depends on the actual research performed.

If validation fails, repair only the diagnosed claim/source fields and rerun. Do not rewrite the whole ledger to hide one bad claim.

## Output contract

For non-trivial work, the canonical handoff is:

```text
sources.json or embedded sources[]
claims.json or embedded claims[]
ledger.json
validation-receipt.json
```

A downstream writer should consume only claims whose `editorial_use` permits use and must preserve every `required_qualifier`.

Read `references/downstream-handoff.md` before wiring this skill into another skill or content compiler.

## Hard fails

Never certify a ledger when any of these are true:

- duplicate source or claim ids;
- a binding points to a missing source;
- a `VERIFIED` material claim has no supporting evidence;
- a high-materiality binding lacks a usable locator;
- a quote lacks exact original text;
- a time-sensitive verified claim was not freshness-checked;
- a verified causal claim skipped causal review / contradiction search;
- `editorial_use` permits wording that the epistemic status requires blocking.

## Definition of done

The skill is done when every material claim is either safely usable with explicit constraints or explicitly blocked, and the deterministic ledger validator passes on the exact handoff bytes.
