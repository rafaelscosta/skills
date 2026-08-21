# Failure-Mode Catalog

Use this catalog during audit, self-review, evaluation design, or recovery after a failed comprehension test.

## Failure record

```text
Failure
→ symptom
→ likely cause
→ consequence
→ detection
→ correction
→ prevention
```

## 1. Vocabulary substitution without model repair

- **Symptom:** words look simpler, but the audience still cannot explain or predict.
- **Cause:** conceptual or causal difficulty was misdiagnosed as lexical.
- **Consequence:** illusion of clarity.
- **Detection:** transfer test fails despite good paraphrase.
- **Correction:** build prerequisites and mechanism.
- **Prevention:** diagnose the audience-content gap before rewriting.

## 2. Jargon laundering

- **Symptom:** one unfamiliar term is replaced by another polished but undefined expression.
- **Cause:** author optimizes tone rather than meaning.
- **Consequence:** hidden terminology barrier.
- **Detection:** ask for a concrete example and distinguishing rule.
- **Correction:** use plain meaning → canonical term → example → consequence.
- **Prevention:** maintain a term inventory.

## 3. Canonical-term erasure

- **Symptom:** the reader understands locally but cannot recognize the term in real tools or documentation.
- **Cause:** simplification permanently removed professional vocabulary.
- **Consequence:** poor transfer and dependence on the simplified source.
- **Detection:** recognition test using canonical terminology.
- **Correction:** reintroduce the canonical term after plain meaning.
- **Prevention:** preserve term bridges.

## 4. Synonym drift

- **Symptom:** one entity appears under multiple labels.
- **Cause:** stylistic variety or merged sources.
- **Consequence:** false distinctions and broken reference chains.
- **Detection:** entity/term concordance audit.
- **Correction:** choose canonical terms and map aliases.
- **Prevention:** one concept–one term governance.

## 5. Polysemy collision

- **Symptom:** the same word means different things in different sections.
- **Cause:** local terminology was not normalized.
- **Consequence:** contradictory decisions and ownership.
- **Detection:** classify every occurrence by concept.
- **Correction:** split labels or qualify scope.
- **Prevention:** one term–one meaning rule.

## 6. Hidden actor

- **Symptom:** readers cannot identify responsibility.
- **Cause:** passive voice, nominalization, or source omission.
- **Consequence:** failed execution and accountability.
- **Detection:** ask “quem faz isso?” for every action.
- **Correction:** actor–action–object or explicit unknown.
- **Prevention:** responsibility audit.

## 7. Condition burial

- **Symptom:** users act before discovering a restriction.
- **Cause:** condition follows action or appears in a note.
- **Consequence:** incorrect or unsafe execution.
- **Detection:** branch scenario test.
- **Correction:** place condition before action; elevate warning.
- **Prevention:** conditional-instruction lint.

## 8. Compound step

- **Symptom:** users complete only part of an instruction.
- **Cause:** several independent actions share one numbered step.
- **Consequence:** skipped validation or incomplete state.
- **Detection:** show-me observation.
- **Correction:** split at decisions and verification points.
- **Prevention:** one independently verifiable action per step.

## 9. Premature compression

- **Symptom:** summary is short but deletes evidence, caveat, mechanism, or next action.
- **Cause:** word count is treated as the goal.
- **Consequence:** distortion and unsafe confidence.
- **Detection:** invariant diff.
- **Correction:** remove repetition/background before material content.
- **Prevention:** lock invariants before shortening.

## 10. Detail-first disorientation

- **Symptom:** individual facts are clear but feel unrelated.
- **Cause:** parts precede whole and purpose.
- **Consequence:** poor integration and memory.
- **Detection:** ask for the system’s purpose and major parts.
- **Correction:** whole–part–whole or main-message layer.
- **Prevention:** dependency-aware ordering.

## 11. Conclusion burial

- **Symptom:** reader cannot find the answer or decision.
- **Cause:** chronology or background dominates.
- **Consequence:** slow action and inconsistent interpretation.
- **Detection:** five-second main-message test.
- **Correction:** BLUF or informative heading.
- **Prevention:** one-sentence essence before drafting details.

## 12. False causal bridge

- **Symptom:** explanation supplies a plausible mechanism not supported by the source.
- **Cause:** pressure for coherence or LLM completion behavior.
- **Consequence:** persuasive misinformation.
- **Detection:** trace each causal link to evidence.
- **Correction:** mark unknown link; present alternatives.
- **Prevention:** known/inferred/uncertain split.

## 13. Correlation-as-causation

- **Symptom:** temporal or statistical association becomes a causal recommendation.
- **Cause:** missing causal discipline.
- **Consequence:** ineffective or harmful intervention.
- **Detection:** counterfactual and confounder questions.
- **Correction:** downgrade claim or provide causal evidence.
- **Prevention:** cause→mechanism→effect audit.

## 14. Analogy overreach

- **Symptom:** the audience transfers unsupported properties from the familiar domain.
- **Cause:** mapping and limits were omitted.
- **Consequence:** systematic misconception.
- **Detection:** ask which properties do not correspond.
- **Correction:** explicit mapping, limit, and exact model.
- **Prevention:** bounded analogy record.

## 15. Example becomes the rule

- **Symptom:** learner applies incidental details from one example.
- **Cause:** only one narrow case was shown.
- **Consequence:** brittle transfer.
- **Detection:** changed-surface transfer case.
- **Correction:** state rule and add varied/non-example cases.
- **Prevention:** representative example plus boundary.

## 16. Non-example too easy

- **Symptom:** learner succeeds without learning the defining distinction.
- **Cause:** negative case is unrelated rather than a near-miss.
- **Consequence:** category boundary remains hidden.
- **Detection:** present a plausible near-miss.
- **Correction:** change only the defining property.
- **Prevention:** design discriminating cases.

## 17. All exceptions at once

- **Symptom:** default model is buried under branches.
- **Cause:** completeness is attempted in the first layer.
- **Consequence:** cognitive overload and no usable baseline.
- **Detection:** reader cannot narrate the happy path.
- **Correction:** progressive views, unless exception is critical.
- **Prevention:** happy-path-first rule with risk override.

## 18. Exception burial

- **Symptom:** a frequent or harmful path appears only in advanced detail.
- **Cause:** progressive disclosure used mechanically.
- **Consequence:** incorrect action.
- **Detection:** task scenario involving the exception.
- **Correction:** promote it to the first actionable layer.
- **Prevention:** frequency × consequence test.

## 19. Giant diagram

- **Symptom:** everything is technically present but no question is answerable quickly.
- **Cause:** multiple views and relation types were merged.
- **Consequence:** visual overload and semantic confusion.
- **Detection:** one-sentence diagram question cannot be stated.
- **Correction:** split by question and zoom level.
- **Prevention:** one-question visual contract.

## 20. Wrong notation

- **Symptom:** a flowchart is used to show responsibility, state, data, architecture, and causality simultaneously.
- **Cause:** visual preference overrides information structure.
- **Consequence:** relationships become ambiguous.
- **Detection:** ask what each arrow means; meanings vary.
- **Correction:** select notation by primary relationship.
- **Prevention:** visual selector.

## 21. Semantic decoration

- **Symptom:** shapes and colors look meaningful but have no consistent definition.
- **Cause:** visual styling precedes semantics.
- **Consequence:** false interpretation.
- **Detection:** remove legend and ask independent readers what symbols mean.
- **Correction:** define shape/line semantics; remove decorative distinctions.
- **Prevention:** grammar before styling.

## 22. Split attention

- **Symptom:** reader repeatedly moves between distant diagram and explanatory text.
- **Cause:** labels and referents are spatially separated.
- **Consequence:** avoidable cognitive load.
- **Detection:** observation of backtracking or reference searching.
- **Correction:** integrate labels or create local callouts.
- **Prevention:** spatial contiguity audit.

## 23. Color-only meaning

- **Symptom:** status or branch disappears in grayscale or for color-vision differences.
- **Cause:** no redundant cue.
- **Consequence:** inaccessible or wrong interpretation.
- **Detection:** grayscale and assistive test.
- **Correction:** add labels, shape, pattern, or position cues.
- **Prevention:** accessibility gate.

## 24. Happy path without recovery

- **Symptom:** procedure works only when nothing fails.
- **Cause:** failure modeling omitted.
- **Consequence:** operational paralysis or duplication.
- **Detection:** inject timeout, duplicate, or dependency failure.
- **Correction:** add detection, state, retry/fallback/compensation/escalation.
- **Prevention:** flow failure taxonomy.

## 25. Retry without idempotency

- **Symptom:** repeated requests create duplicate side effects.
- **Cause:** retries are described without logical operation identity.
- **Consequence:** duplicate payments, records, or messages.
- **Detection:** replay the same request after ambiguous timeout.
- **Correction:** define idempotency key and replay behavior.
- **Prevention:** retry-safety review.

## 26. State/action confusion

- **Symptom:** lifecycle diagram uses verbs as states or omits transition events.
- **Cause:** sequence and persistence are conflated.
- **Consequence:** invalid transition assumptions.
- **Detection:** ask how long the “state” persists and what event exits it.
- **Correction:** rename stable conditions; label triggers/guards.
- **Prevention:** state-model grammar.

## 27. Numerator without denominator

- **Symptom:** a count or percentage cannot be interpreted.
- **Cause:** baseline, total, or population omitted.
- **Consequence:** exaggerated or minimized risk.
- **Detection:** ask “out of how many?”
- **Correction:** add denominator, timeframe, population, and comparison.
- **Prevention:** numerical framing checklist.

## 28. Relative-risk inflation

- **Symptom:** large relative change hides a small absolute difference.
- **Cause:** only relative percentage reported.
- **Consequence:** distorted decisions.
- **Detection:** compute absolute change and natural frequency.
- **Correction:** show both absolute and relative values.
- **Prevention:** baseline requirement.

## 29. Average-only story

- **Symptom:** mean looks acceptable while variability or tails cause failures.
- **Cause:** distribution omitted.
- **Consequence:** wrong capacity, quality, or risk decision.
- **Detection:** inspect distribution and quantiles.
- **Correction:** add interval/distribution view.
- **Prevention:** match statistic to decision.

## 30. Readability-as-proof

- **Symptom:** a favorable score is presented as evidence of comprehension.
- **Cause:** easy-to-compute proxy replaces user testing.
- **Consequence:** undetected model and action errors.
- **Detection:** teach-back/show-me fails despite score.
- **Correction:** use score as lint; run outcome test.
- **Prevention:** validation hierarchy.

## 31. Assent-as-understanding

- **Symptom:** “sim, entendi” is accepted as validation.
- **Cause:** social pressure and weak assessment.
- **Consequence:** hidden misunderstanding.
- **Detection:** teach-back or performance differs from assent.
- **Correction:** normalize reconstruction as a test of the explanation.
- **Prevention:** outcome-matched validation.

## 32. Recognition mistaken for recall

- **Symptom:** learner chooses the answer but cannot produce it unaided later.
- **Cause:** multiple-choice familiarity is treated as memory.
- **Consequence:** fragile real-world performance.
- **Detection:** delayed free recall.
- **Correction:** retrieval practice with feedback.
- **Prevention:** separate recognition and retention outcomes.

## 33. Immediate success mistaken for transfer

- **Symptom:** learner copies the example but fails a changed context.
- **Cause:** practice preserves surface cues.
- **Consequence:** dependence on templates.
- **Detection:** structurally similar, surface-different case.
- **Correction:** explain deep rule and vary examples.
- **Prevention:** transfer test in acceptance criteria.

## 34. Confidence inflation

- **Symptom:** explanation feels fluent, so user confidence rises more than accuracy.
- **Cause:** polished prose and coherent narrative hide uncertainty.
- **Consequence:** overconfident decisions.
- **Detection:** confidence-performance calibration gap.
- **Correction:** expose evidence status and test application.
- **Prevention:** epistemic labels and prediction tests.

## 35. Human-review theater

- **Symptom:** “human in the loop” appears without role, authority, evidence, or deadline.
- **Cause:** governance phrase substitutes for control design.
- **Consequence:** unowned risk and stalled flows.
- **Detection:** ask who decides what, using which evidence, by when.
- **Correction:** define human-gate contract.
- **Prevention:** explicit approval boundary.

## 36. Source-fragment reconstruction

- **Symptom:** transformation fills gaps from partial snippets.
- **Cause:** source not fully inspected.
- **Consequence:** confident fabrication or lost exceptions.
- **Detection:** compare against complete relevant source.
- **Correction:** retrieve source or mark limitations.
- **Prevention:** source-completeness gate.

## 37. Version or jurisdiction loss

- **Symptom:** rule is stated without the version, date, or jurisdiction that governs it.
- **Cause:** contextual metadata removed during simplification.
- **Consequence:** outdated or inapplicable action.
- **Detection:** applicability question.
- **Correction:** restore exact scope and current authoritative source.
- **Prevention:** high-risk invariant lock.

## 38. Unsupported personalization

- **Symptom:** explanation assumes knowledge, culture, goals, or constraints based on a vague persona.
- **Cause:** inference substitutes for diagnosis.
- **Consequence:** exclusion or wrong depth.
- **Detection:** ask which evidence supports the adaptation.
- **Correction:** use bounded assumptions or one material question.
- **Prevention:** operational audience contract.

## 39. Endless layering

- **Symptom:** explanation keeps expanding after the outcome is already met.
- **Cause:** completeness is treated as the goal.
- **Consequence:** wasted attention and reduced usability.
- **Detection:** remaining detail does not alter action, decision, or model.
- **Correction:** apply stop criteria and link deeper reference.
- **Prevention:** lightest sufficient mode.

## 40. Same-method repetition after failure

- **Symptom:** the same explanation is repeated with more words.
- **Cause:** failed validation is not re-diagnosed.
- **Consequence:** frustration and no model repair.
- **Detection:** repeated error persists.
- **Correction:** identify failed dependency and switch representation.
- **Prevention:** diagnose→reroute→retest recovery loop.

## Recovery routing

| Failed test | Likely repair |
|---|---|
| Teach-back misses main point | Main message + whole-system view |
| Teach-back uses terms but wrong mechanism | Cause chain + worked example |
| Prediction fails | State/causal model + boundary case |
| Show-me skips step | One-action steps + verification cue |
| Wrong branch | Decision table/tree + condition-before-action |
| Transfer fails | Abstraction ladder + varied examples/non-examples |
| Information cannot be found | BLUF + chunking + informative headings |
| Confidence exceeds accuracy | Epistemic split + counterexample + delayed test |
| Diagram misread | Correct notation + semantic labels + text equivalent |
| High-risk action wrong | Exact rule first + teach-back/show-me + qualified review |
