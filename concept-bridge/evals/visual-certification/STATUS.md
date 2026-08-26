# Visual Behavioral Certification Status

**Skill:** Concept Bridge v3.1.0  
**Harness:** READY  
**Behavioral certification:** PENDING

The blind Generator → sealed Judge harness is implemented and structurally validated.

Do not claim `CONCEPT-BRIDGE v3.1 VISUAL BEHAVIOR: CERTIFIED` until a fresh generator run completes both strict gates defined in `judge.md`:

- Route Gate: 15/15
- Render Gate: 6/6

The implementation session that authored this harness is **not eligible** to act as the blind generator because it has seen the sealed oracle during construction.

A passing certification report must be stored under `runs/<run-id>/` with immutable predictions, render receipts, artifact hashes, run metadata, rendered artifacts, and the sealed judge report.
