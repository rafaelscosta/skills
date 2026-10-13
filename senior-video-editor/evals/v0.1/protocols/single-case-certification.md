# Senior Video Editor v0.1 — single-case certification protocol

## Purpose

Test whether the skill system changes behavior, not whether an agent can restate editing vocabulary.

## Roles

- **Generator:** receives only the frozen fixture plus the skills allowed by the case.
- **Judge:** receives the frozen fixture, the sealed oracle, and the generator output. It must not receive hidden generator reasoning.
- **Recorder:** stores model/runtime identity, skill commit, input hash, output hash, verdict, and blocker evidence.

## Run order

1. Freeze the skill commit and fixture bytes.
2. Run the generator in a fresh context.
3. Seal the output before opening the oracle to the judge.
4. Run every blocking assertion first.
5. If any automatic failure occurs, verdict is `BLOCK` regardless of prose quality.
6. Only after blockers pass, score non-blocking dimensions.
7. Record observable evidence for each judgment.

## Non-blocking dimensions

Score 0–4 each:

- objective clarity;
- source-truth discipline;
- distinction between constraints and tactics;
- routing precision;
- economy of context/instructions;
- quality of acceptance gates.

## Verdict policy

- `PASS`: all blockers pass and every scored dimension >= 3.
- `PASS_WITH_NOTES`: all blockers pass, no dimension < 2, and at most one dimension = 2.
- `REVISE`: blockers pass but quality threshold is not met.
- `BLOCK`: any blocking assertion fails or any automatic failure is present.

## Evidence policy

Judge observable output only. Do not reward length, confidence, terminology density, or software fluency by themselves.

The generator is not required to match oracle wording. Semantic equivalence is sufficient.
