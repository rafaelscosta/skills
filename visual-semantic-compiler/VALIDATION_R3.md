# Visual Semantic Compiler v1.2.0 — R3 Validation

## Contract checks executed

```bash
python3 -m py_compile scripts/validate_perceptual_review.py
node --check scripts/visual_check.mjs
python3 -m unittest tests/test_perceptual_r3.py -v
```

## Result

- Python compile: PASS
- Node syntax check: PASS
- R3 review/binding tests: **9/9 PASS**
- `passed` review requires browser evidence PASS: covered
- artifact SHA mismatch: rejected
- evidence SHA mismatch: rejected
- failed review without a defect: rejected
- failed review with concrete defect: preserved as `perceptually-failed`
- skipped review without reason: rejected
- skipped review with reason: preserved as `perceptual-review-skipped`

## Live Chromium evidence smoke

Browser available in the implementation environment:

```text
Chromium 144.0.7559.96 built on Debian GNU/Linux 13 (trixie)
```

Positive fixture:

```bash
node scripts/visual_check.mjs \
  tests/fixtures/perceptual-good.html \
  /tmp/vsc-perceptual-good
```

Observed:

- exit code: 0
- browser evidence: PASS
- required viewports measured: **4/4**
- 1440×900: PASS
- 1600×1000: PASS
- 1920×1080: PASS
- 2048×1320: PASS
- retained screenshots: 2/2
- automated errors: 0
- automated warnings: 0
- `perceptual_review`: `pending` after capture, as required

Fixture SHA-256:

```text
078c24b2046a540d67ca6b052a73369e2a9e56d85b730a264fd31e87f464d91e
```

Screenshot SHA-256 values from the smoke run:

```text
1440x900  27915a913591590bbac98b5758060de9f5e5b6d5870dac83e9cc4b74d04fc347
2048x1320 84647b6af2c31f6f6acdcb3c11d9a8e2fbb1bf9eb04a920acf1f75b23b61c8c3
```

The 1440×900 screenshot was then inspected with a vision-capable GPT-5.6 Sol session. The reviewer found the main path, labels, hierarchy, and whitespace readable and authored a zero-defect `visual-perceptual-review/v1` receipt. The binding validator returned:

```text
delivery_status: perceptually-passed
```

This is a smoke proof for the R3 protocol and fixture, not a certification of every renderer output.

## Negative live browser case

```bash
node scripts/visual_check.mjs \
  tests/fixtures/perceptual-overflow.html \
  /tmp/vsc-perceptual-overflow
```

Observed:

- exit code: 1
- evidence status: `failed`
- detected error: `document-horizontal-overflow`

## Exact-artifact handling

The environment blocked Chromium navigation to local `file://` and loopback URLs. R3 therefore uses Chrome DevTools `Page.setDocumentContent` with the exact UTF-8 artifact bytes already bound by `artifact_sha256`. The checker does not patch the HTML, inject review CSS, or invoke a second renderer.

The receipt records:

```text
render_source: exact-artifact-bytes-via-Page.setDocumentContent
```

## Stale-evidence safety

Before every browser run, the checker removes its previous receipt, contact sheet, and known screenshot sidecars. A skipped or failed recapture cannot leave old screenshots positioned as current evidence.

## Claim boundary

R3 v1 certifies only the declared desktop perceptual-delivery protocol:

- 1440×900
- 1600×1000
- 1920×1080
- 2048×1320

It does **not** certify mobile/narrow usability.

Automated browser evidence does not itself prove perceptual quality. A final perceptual pass still requires inspection by an identified human or vision-capable model and a hash-bound review receipt.
