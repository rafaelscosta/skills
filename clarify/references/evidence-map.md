# Evidence Map and Research Boundaries

Use this reference to distinguish established mechanisms, official notations, institutional guidance, practitioner frameworks, and local heuristics.

## Evidence discipline

Never infer that a technique is empirically proven because it is popular, intuitive, standardized, or widely used.

Distinguish five questions:

1. **Is the underlying mechanism supported?**
2. **Is this named technique itself directly tested?**
3. **For which audience, domain, medium, and outcome?**
4. **Against which comparison condition?**
5. **What boundary conditions or implementation details change the result?**

A formal standard establishes shared definitions and rules. It does not automatically prove that every standards-compliant artifact is easier to understand.

## Source hierarchy

| Level | Source type | Best use | Main limitation |
|---|---|---|---|
| 1 | Official standard, regulation, or specification | Canonical definitions and notation | Does not alone establish learning effect |
| 2 | Systematic review or meta-analysis | Aggregate effect and moderators | Quality depends on included studies and comparability |
| 3 | Primary controlled or field study | Causal evidence in defined conditions | May generalize poorly |
| 4 | Institutional guideline | Operational recommendations and implementation | Evidence may be indirect or selectively synthesized |
| 5 | Established professional framework | Reproducible practice and shared vocabulary | Often lacks controlled comparison |
| 6 | Expert opinion or local heuristic | Hypothesis generation and fast practice | High risk of overgeneralization |

## Confidence labels

- **Strong:** converging high-quality evidence for the relevant outcome and conditions.
- **Moderate:** credible evidence with important moderators or limited domains.
- **Mixed:** studies or implementations differ materially.
- **Practice-supported:** operationally established, but direct causal evidence is sparse.
- **Spec-defined:** semantics are authoritative, comprehension effects are not implied.
- **Insufficient:** no dependable conclusion for the proposed use.

## Core authoritative and research sources

### Plain language and clear communication

- **ISO 24495-1:2023 — Plain language, Part 1: Governing principles and guidelines.** Defines plain-language principles around audience use, relevance, findability, understandability, and usability. Official page: https://www.iso.org/standard/78907.html
- **U.S. Federal Plain Language Guidelines.** Institutional authoring guidance: https://www.plainlanguage.gov/guidelines/
- **CDC Clear Communication Index.** Research-informed scoring tool for public communication: https://www.cdc.gov/ccindex/
- **AHRQ Health Literacy Universal Precautions Toolkit.** Includes teach-back and “show-me” implementation: https://www.ahrq.gov/health-literacy/improve/precautions/index.html

Interpretation: strong authority for principles and institutional use; effect size depends on the specific intervention, audience, content, and measurement. Do not treat readability alone as evidence of comprehension.

### Controlled technical language

- **ASD-STE100 Simplified Technical English.** Official controlled-language specification and resources: https://www.asd-ste100.org/

Interpretation: spec-defined vocabulary and grammar with extensive aerospace/technical use. Strong for canonical rules; comparative outcome evidence is more limited and context-specific.

### Cognitive load, multimedia learning, and worked examples

- Sweller, J., van Merriënboer, J. J. G., & Paas, F. (2019). *Cognitive Architecture and Instructional Design: 20 Years Later*. Educational Psychology Review. https://doi.org/10.1007/s10648-019-09465-5
- Mayer, R. E. (2021). *Multimedia Learning* (3rd ed.). Cambridge University Press.
- Atkinson, R. K., Derry, S. J., Renkl, A., & Wortham, D. (2000). *Learning from Examples: Instructional Principles from the Worked Examples Research*. Review of Educational Research. https://doi.org/10.3102/00346543070002181

Interpretation: strong support for cognitive limits and several design effects, including segmenting, signaling, spatial integration, and worked examples under suitable conditions. Effects are moderated by prior knowledge, domain, pacing, redundancy, and implementation. Avoid “seven items” or a universal chunk size as a rule.

### Retrieval, spacing, and interleaving

- Dunlosky, J. et al. (2013). *Improving Students’ Learning With Effective Learning Techniques*. Psychological Science in the Public Interest. https://doi.org/10.1177/1529100612453266
- Cepeda, N. J. et al. (2006). *Distributed Practice in Verbal Recall Tasks: A Review and Quantitative Synthesis*. Psychological Bulletin. https://doi.org/10.1037/0033-2909.132.3.354
- Brunmair, M., & Richter, T. (2019). *Similarity Matters: A Meta-Analysis of Interleaved Learning and Its Moderators*. Psychological Bulletin. https://doi.org/10.1037/bul0000209

Interpretation: retrieval and spacing have strong broad support for retention. Interleaving is more moderator-dependent and should not be introduced before minimal category grounding.

### Concept maps and analogical learning

- Nesbit, J. C., & Adesope, O. O. (2006). *Learning With Concept and Knowledge Maps: A Meta-Analysis*. Review of Educational Research. https://doi.org/10.3102/00346543076003413
- Gentner, D. (1983). *Structure-Mapping: A Theoretical Framework for Analogy*. Cognitive Science. https://doi.org/10.1207/s15516709cog0702_3

Interpretation: concept maps can aid learning when relations are meaningful and the learner can interpret the notation. Analogies help when structural mapping is explicit and prior knowledge is suitable; they can also produce systematic misconceptions.

### Risk and numerical communication

- Gigerenzer, G., & Edwards, A. (2003). *Simple tools for understanding risks: from innumeracy to insight*. BMJ. https://doi.org/10.1136/bmj.327.7417.741
- CDC Clear Communication Index, Part B on numbers: https://www.cdc.gov/ccindex/tool/index.html

Interpretation: natural frequencies, explicit denominators, baselines, and transparent uncertainty often improve risk interpretation. No single numerical format is universally best; test against the actual decision and audience.

### Universal Design for Learning and accessibility

- CAST Universal Design for Learning Guidelines: https://udlguidelines.cast.org/
- Web Content Accessibility Guidelines (WCAG): https://www.w3.org/WAI/standards-guidelines/wcag/

Interpretation: WCAG is a normative accessibility standard/guideline set for digital content. UDL is a broad educational design framework; individual principles have varying evidence, and claims about the complete framework should be bounded.

### Process and software notations

- **BPMN 2.0.2**, Object Management Group: https://www.omg.org/spec/BPMN/2.0.2/
- **UML 2.5.1**, Object Management Group: https://www.omg.org/spec/UML/2.5.1/
- **C4 Model**, official documentation: https://c4model.com/

Interpretation: BPMN and UML are spec-defined; correct syntax and semantics do not guarantee novice comprehension. C4 is a practice-supported architecture communication model rather than an empirical learning theory.

### Documentation and collaborative modeling frameworks

- **Diátaxis:** https://diataxis.fr/
- **EventStorming:** https://www.eventstorming.com/

Interpretation: mature practitioner frameworks with strong operational rationale and case experience; direct controlled comparative evidence is limited.

## Technique evidence matrix

| Technique family | Evidence status | Supported claim | Do not overclaim |
|---|---|---|---|
| Plain language | Authority + moderate/mixed empirical | Audience-centered wording and organization can improve find/understand/use outcomes | Any “simple” rewrite is clearer; reading grade proves comprehension |
| Controlled language | Spec-defined + practice-supported | Terminology and grammar constraints improve consistency and may reduce ambiguity/translation burden | Every controlled sentence is natural or sufficient for learning |
| Audience diagnosis | Moderate/practice-supported | Prior knowledge and task context materially affect effective explanation | Demographic persona predicts comprehension by itself |
| Chunking | Strong mechanism, implementation-dependent | Meaningful grouping and reduced simultaneous burden can help processing | A fixed universal number of items exists |
| Signaling | Strong/moderate | Relevant cues can guide attention to structure and essential relations | More highlighting always helps |
| Segmenting | Strong/moderate | Learner-manageable coherent segments can reduce overload | Shorter fragments are always better |
| Spatial contiguity | Strong/moderate | Keeping related words and visuals together can reduce split attention | Any image next to text improves learning |
| Worked examples | Strong/moderate | Novices often benefit from complete solutions, especially with guidance and fading | Experts always benefit equally; passive copying is sufficient |
| Retrieval practice | Strong | Active recall with feedback improves durable retention | Re-reading or recognition quiz is equivalent |
| Spacing | Strong | Distributed practice improves long-term retention | One interval schedule fits every retention goal |
| Interleaving | Moderate/mixed | Mixing can improve discrimination and transfer under suitable similarity and prior grounding | Random mixture always improves learning |
| Teach-back | Moderate/strong in health contexts | Reconstruction can expose misunderstanding and support correction | Asking once guarantees comprehension in every domain |
| Show-me | Practice-supported/direct assessment | Observed execution is better evidence of procedural ability than verbal assent | One successful demonstration proves durable transfer |
| Analogy | Mixed/moderate | Explicit structural mapping can bootstrap a model | Familiarity guarantees accuracy; analogy can replace exact rule |
| Examples/non-examples | Moderate | Contrasting instances can clarify category boundaries | Any vivid example is representative |
| Concept maps | Moderate/mixed | Meaningful relational mapping can support organization and learning | Unlabeled associative maps prove understanding |
| BLUF/inverted pyramid | Practice-supported | Conclusion-first organization supports scanning and action in many contexts | It is always best for pedagogy or sensitive narratives |
| Pyramid Principle/SCQA/MECE | Practice-supported | Provides disciplined professional organization and decomposition | Direct broad causal superiority has been established |
| Progressive disclosure | Practice-supported/HCI | Can reduce initial complexity while retaining advanced access | Hidden information is harmless or always discoverable |
| Diátaxis | Practice-supported | Separating documentation purposes improves authoring/navigation coherence | Four categories solve all documentation problems automatically |
| Flowchart/swimlane/SIPOC | Practice-supported | Externalizes sequence, ownership, and scope when notation matches the question | A diagram is clearer regardless of density or literacy |
| BPMN/UML | Spec-defined | Provides formal shared semantics | Formal correctness means easy comprehension |
| C4 Model | Practice-supported | Progressive architectural zoom can support audience-specific views | It is a complete runtime, deployment, security, and data model |
| Event Storming | Practice-supported | Collaborative event discovery can reveal domain assumptions and hotspots | Workshop artifacts are validated specifications |
| Feynman technique | Heuristic with indirect support | Explaining simply can expose gaps and invoke retrieval/self-explanation | The branded sequence has a unique proven effect |
| First principles | Reasoning heuristic | Makes assumptions and derivations inspectable | Re-derivation is superior to domain evidence |
| Abstraction ladder | Moderate/practice-supported | Moving between concrete and abstract can support transfer | More examples automatically produce abstraction |
| Causal diagrams | Spec/practice + domain evidence needed | Externalizes proposed causal structure and feedback | Drawing an arrow establishes causality |
| Readability formulas | Measurement heuristic | Flags sentence/word complexity | Predicts comprehension, accuracy, usability, or accessibility alone |

## Evidence use protocol for each technique

Record:

```yaml
technique: ""
claim_being_made: ""
source_type: "standard | systematic_review | meta_analysis | controlled_study | field_study | institutional_guidance | practitioner_framework | heuristic"
population: ""
domain: ""
medium: ""
comparison: ""
outcome: ""
effect_direction: ""
effect_size: "unknown or reported value"
moderators: []
limitations: []
generalization: ""
confidence: "strong | moderate | mixed | practice-supported | spec-defined | insufficient"
```

Do not copy an effect label from one outcome to another. Retention evidence does not automatically establish transfer or actionability.

## Evidence-sensitive selection rules

1. Prefer strong mechanisms when several techniques fit equally well.
2. Prefer formal standards when interoperability or canonical semantics is the objective.
3. Prefer practitioner frameworks when the task is organizational and evidence is inherently field-based, but label the basis accurately.
4. Use heuristics as hypotheses and validate against user performance.
5. In high-risk contexts, do not rely on popularity, anecdotes, or perceived clarity.
6. Treat LLM-generated analogies, causal links, and diagrams as proposals requiring source and semantic review.

## Research gaps

### Cross-domain generalization

Many effects are demonstrated in education, health, or controlled learning tasks. Their magnitude in business operations, AI-agent documentation, executive decision support, and software onboarding remains under-tested.

### Portuguese Brazilian controlled language

There is no universally accepted PT-BR equivalent with the same governance maturity as ASD-STE100. Research is needed on:

- approved vocabulary and verb senses;
- sentence patterns;
- pronoun ambiguity;
- conditional instruction order;
- terminology governance;
- readability and task performance across Brazilian audiences.

### LLM clarification fidelity

Open questions include:

- how often simplification changes causal or modal meaning;
- which invariant extraction methods reduce silent omission;
- whether self-critique catches fabricated bridges;
- when examples improve understanding but increase false confidence;
- how to evaluate model-generated diagrams semantically.

### Adaptive explanation

Research is needed on when personalization by inferred prior knowledge helps versus stereotyping or destabilizing terminology.

### Optimal layering

The best number, depth, and navigation of explanation layers likely depend on task, medium, expertise, and urgency. Fixed “10-second/1-minute/5-minute” structures are design heuristics, not universal findings.

### Diagram complexity thresholds

Node counts alone are inadequate. Better predictors may include relation types, crossings, symbol entropy, label distance, branch depth, and notation literacy.

### Clarity versus epistemic humility

More fluent explanations can appear more certain. Evaluation should measure whether users retain uncertainty and evidence limits, not only main-message recall.

### Multimodal accessibility

A visual plus a text equivalent may still impose unequal cognitive burden. More work is needed on equivalent task performance across assistive modalities.

### Durable operational transfer

Most documentation analytics measure reading or task completion once. Stronger evaluation should include later recovery from faults and performance after system changes.

## Update protocol

When maintaining this evidence map:

1. search for newer systematic reviews and official standard revisions;
2. compare event date, publication date, and applicability date;
3. record retractions or major critiques;
4. update confidence only when evidence addresses the same population, task, medium, and outcome;
5. preserve conflicting credible findings;
6. add the “last reviewed” date in a local governance layer if the skill is deployed operationally.
