# GPT-5.6 execution profile

This reference tunes long or ambiguous design-system work for GPT-5.6 without overconstraining the model.

## 1. Define the outcome, not every micro-step

Keep these explicit:

- desired artifact;
- target audience;
- repository or source scope;
- output location;
- brand/language constraints;
- approval boundaries;
- success criteria.

Let the model infer routine intermediate steps. Overly prescriptive prompts can waste context and reduce useful judgment.

## 2. Bias toward completion

A plan is not a deliverable. Continue through:

```text
discovery → normalization → specification → rendering → inspection → correction → export → QA
```

Do not stop after discovery, a TODO list, a draft specification, or a successful command. Stop only at completion or a genuine blocker.

## 3. Minimize communication overhead

Do not emit an upfront plan or routine status commentary unless requested. Long-running execution should remain focused on tool use and artifact quality.

Communicate during execution only when:

- user approval is required;
- credentials or permissions are missing;
- a destructive scope decision is unavoidable;
- two target interpretations would produce materially different work;
- the environment cannot provide a required source or runtime.

## 4. Use tools as evidence

Prefer direct inspection and execution over memory or assumption:

- search the repository;
- read exact source files;
- run the component library;
- inspect rendered output;
- execute validation scripts;
- compare actual states and breakpoints;
- verify exports.

When a command fails, diagnose and continue. Do not treat the first tool error as a reason to fall back to speculative prose.

## 5. Protect the main context

Large repositories and visual atlases create context pollution. Keep the main thread focused on:

- user intent;
- source-of-truth decisions;
- conflicts;
- architecture choice;
- final specification;
- final QA.

Move noisy exploration, logs, and independent inventories to subagents or bounded tool calls. Return distilled evidence with paths, not raw dumps.

## 6. Delegate only separable work

Good parallel tasks:

- token inventory;
- component API inventory;
- Storybook/test inventory;
- accessibility review;
- documentation conflict scan;
- independent visual QA of a rendered artifact.

Poor parallel tasks:

- multiple agents editing the same guide specification;
- simultaneous changes to shared CSS;
- several agents deciding the final taxonomy independently;
- write-heavy work with overlapping files.

The coordinating agent owns the source map, taxonomy, visual architecture, final files, and completion decision.

## 7. Use an iterative visual loop

GPT-5.6 has strong layout and visual judgment, but it still needs rendered evidence.

Required loop:

1. render;
2. open or screenshot;
3. inspect hierarchy, spacing, clipping, and comparison clarity;
4. adjust source;
5. render again;
6. verify at full and reduced scale.

Do not judge a visual artifact only from HTML/CSS source or a successful build.

## 8. Keep assumptions explicit

GPT-5.6 can infer intent well, but existing-system facts must remain grounded. Distinguish:

- what the user wants;
- what the repository implements;
- what documentation claims;
- what the model inferred;
- what the model proposes.

Use provenance tags rather than hiding ambiguity in polished copy.

## 9. Reasoning and model selection

When the operator can choose:

- use GPT-5.6 Sol at medium reasoning for a normal single-guide production task;
- increase to high or extra high for whole-repository audits, conflicting sources, or complex atlas planning;
- reserve Max for unusually difficult quality-first work;
- use Ultra/subagents only when the task divides into meaningful independent workstreams;
- use Terra for routine updates with clear acceptance criteria;
- use Luna for high-volume extraction, normalization, or validation after the architecture is stable.

Use the lowest setting that consistently passes representative quality gates.

## 10. Final response discipline

The final response should report:

- what was created;
- where the files are;
- what was verified;
- any remaining limitation;
- the shortest useful invocation/install instruction.

Do not replace deliverable links with a long narrative of the work process.
