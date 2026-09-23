# Validation

## Release

- Skill: `visualize-design-system`
- Version: `1.0.0`
- Validation date: `2026-09-22`

## Checks executed

```bash
python3 -m py_compile scripts/*.py
python3 scripts/smoke_test.py
shasum -a 256 -c MANIFEST.sha256
```

The smoke suite exercises the bundled minimal design-system fixture end to end:

- repository inventory;
- strict guide-spec validation;
- deterministic HTML rendering;
- PNG and PDF export of the canonical example;
- validation and rendering of the all-section fixture;
- PNG export of the all-section fixture.

Observed fixture inventory: **1 component, 1 story, 9 CSS custom properties, 0 JSON token leaves**. Both strict guide-spec validations completed with **0 warnings**, and the smoke suite finished with `SMOKE TEST PASS`.

## Runtime compatibility fix validated

`capture_guide.py` now discovers Chromium-family browsers both on `PATH` and at common macOS application paths, including Google Chrome, Chromium, Microsoft Edge, and Brave. This allows export on a standard macOS workstation even when the Python Playwright package is not installed.

## Known validation boundary

The validation host did not have the Python Playwright package installed, so capture used the Chrome CLI fallback. PNG/PDF generation passed, but the fallback cannot collect DOM overflow diagnostics. Full DOM-bound overflow evidence therefore still requires Playwright. Non-fatal macOS `CVDisplayLink` messages emitted by headless Chrome did not prevent artifact generation.

## Integrity

`MANIFEST.sha256` is regenerated from the repository payload after release edits and verified before publication.
