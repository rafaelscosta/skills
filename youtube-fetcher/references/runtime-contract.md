# YouTube Fetcher v2 Runtime Contract

Load this reference only for non-default execution, integration, troubleshooting, or
precise CLI/schema semantics. The bare-link archive path should not need it.

## Invocation

```bash
python3 "$SKILL_DIR/scripts/fetch_transcript.py" "URL_OR_VIDEO_ID" [options]
```

Supported inputs include standard watch URLs, `youtu.be`, embed/shorts/live/legacy
`/v/` URLs, YouTube Music watch URLs, privacy-enhanced embeds, and raw 11-character
video IDs. Lookalike hosts are rejected.

## Operation routing

The runtime chooses one internal operation:

| Trigger | Operation | Transcript endpoint | Metadata stack |
|---|---|---:|---:|
| Default Markdown | `archive` | yes | yes |
| `--metadata-only` | `metadata` | no | yes |
| `--chapters-only` | `chapters` | no | yes |
| `--list` | `list` | yes | no |
| JSON/SRT/chunks or selected transcript | `transcript` | yes | only when Markdown or chapter selection needs it |

This dependency routing is intentional. Metadata-only and chapters-only must not
require `youtube-transcript-api`; raw JSON/SRT/chunks without chapter selection must
not require the metadata stack.

## Flags

| Flag | Semantics |
|---|---|
| `--output PATH`, `-o PATH` | Exact output file; highest destination precedence. |
| `--output-dir DIR` | Directory/vault for generated artifacts. |
| `--stdout` | Emit the primary payload instead of saving its artifact. |
| `--machine` | Emit one JSON receipt on stdout. Mutually exclusive with `--stdout`. |
| `--manifest [PATH]` | Write execution manifest; no PATH means automatic sidecar. |
| `--metadata-only` | JSON metadata without touching transcript endpoints. |
| `--chapters-only` | JSON normalized chapters without touching transcript endpoints. |
| `--no-description` | Omit description from Markdown; in metadata-only mode return an empty description field. |
| `--lang CODE`, `-l CODE` | Request caption language; English remains truthful fallback. |
| `--list` | List available caption tracks. |
| `--timestamps`, `-t` | Timestamp Markdown transcript lines. |
| `--start TIME` | Inclusive selection start; seconds, `MM:SS`, or `HH:MM:SS`. |
| `--end TIME` | Exclusive selection end in the same formats. |
| `--chapter VALUE` | 1-based index, exact title, or unique title substring. |
| `--format text|json|srt|chunks`, `-f ...` | Markdown, raw transcript JSON, SRT, or chunk JSON. |
| `--chunk-seconds N` | Fixed absolute window size for `--format chunks`; default 300. |
| `--source NAME`, `-s NAME` | Override source-project provenance in Markdown. |
| `--force` | Explicitly authorize overwrite/re-fetch. |
| `--check-deps` | Check the full dependency set and exit; with `--machine`, return a JSON receipt with dependency data. |

`--chapter` cannot be combined with `--start` or `--end`. `--chunk-seconds` requires
`--format chunks`.

## Destination precedence and default filenames

Destination precedence remains:

1. `--output`
2. `--output-dir`
3. `YOUTUBE_FETCHER_DIR`
4. `~/yt_transcripts/`

Default artifact names:

- Markdown: `YYYY-MM-DD_<slug>_[VIDEO_ID].md`
- transcript JSON: `<VIDEO_ID>.json`
- SRT: `<VIDEO_ID>.srt`
- chunks: `<VIDEO_ID>.chunks.json`
- metadata: `<VIDEO_ID>.metadata.json`
- chapters: `<VIDEO_ID>.chapters.json`

Selected transcript artifacts receive a provenance suffix so they cannot collide
with full-video outputs, for example:

- `<VIDEO_ID>.range-000750-001260.chunks.json`
- `<VIDEO_ID>.chapter-03-agent-runtime.srt`
- `YYYY-MM-DD_<slug>_[VIDEO_ID].chapter-03-agent-runtime.md`

An automatic manifest is `<artifact>.manifest.json`, or `<VIDEO_ID>.manifest.json`
when there is no primary artifact.

## Safe overwrite behavior

Default Markdown keeps v1 video-level duplicate detection. Exact output paths across
v2 modes are also protected. In a non-interactive agent session, an existing output
is preserved and exits with code `3`. `--force` is the explicit overwrite contract.

## Time and chapter selection

Temporal selection uses `[start, end)` semantics. Caption snippets are selected when
they overlap that interval. A zero-duration snippet is selected when its start is
inside the interval.

Chapter normalization produces:

```json
{
  "index": 2,
  "title": "Agent Runtime",
  "start": 300.0,
  "end": 620.0,
  "start_timestamp": "05:00",
  "end_timestamp": "10:20"
}
```

Missing chapter end times are derived from the next chapter; the final chapter uses
video duration when available.

## Deterministic chunks

`--format chunks` emits `youtube-fetcher.chunks/v2`.

For `--chunk-seconds 300`, absolute buckets are `[0,300)`, `[300,600)`, etc. A
caption is assigned to the bucket containing its **start timestamp**. The chunk ID is
therefore stable across full and filtered executions, e.g.:

```text
chunk-000000-000300
chunk-000300-000600
chunk-000600-000900
```

Each chunk includes window bounds, actual content bounds, snippet count, char count,
joined text, and the original snippet-level timing fields.

## Machine stdout contract

With `--machine`, stdout contains exactly one compact JSON object matching
`references/receipt.schema.json`. Human-readable diagnostics and warnings stay on
stderr. `--check-deps --machine` follows the same JSON-only stdout rule.

Successful artifact example:

```json
{
  "schema_version": "youtube-fetcher.receipt/v2",
  "status": "success",
  "exit_code": 0,
  "operation": "transcript",
  "video_id": "dQw4w9WgXcQ",
  "artifact_path": "/tmp/dQw4w9WgXcQ.chunks.json",
  "manifest_path": "/tmp/dQw4w9WgXcQ.chunks.json.manifest.json",
  "language": "en",
  "caption_type": "manual",
  "warnings": [],
  "error": null
}
```

Do not combine `--machine` with `--stdout`.

## Manifest contract

`--manifest` emits `youtube-fetcher.manifest/v2`. It records:

- status and UTC start/completion timestamps;
- original input, canonical video ID and URL;
- selected operation/format/language/chunk parameters;
- chapter/range selection provenance;
- actual caption language/type and transcript counts;
- metadata source and summary fields when metadata was used;
- artifact path, stdout flag, media type, SHA-256 and byte size;
- warnings and error state.

The runtime attempts to seal a requested failure manifest once the video ID and
manifest destination can be resolved. Failure to write that secondary manifest never
masks the original runtime error.

Schemas live under `references/` as `*.schema.json`.

## Exit codes

| Code | Meaning | Agent behavior |
|---|---|---|
| `0` | Success | Consume the requested payload/artifact. |
| `1` | Invalid input, selection, or fetch failure | Report the concrete runtime error; never fabricate content. |
| `2` | Required dependency missing for selected operation | Show the suggested install command; do not install automatically. |
| `3` | Existing output preserved | Report the preserved output; retry with `--force` only if overwrite is authorized. |

## Dependency behavior

`youtube-transcript-api` is required only for transcript/list operations. `requests`
is required when metadata fallback may be needed. `yt-dlp` remains optional and is
the rich metadata source for descriptions, chapters, duration, and upload date.

An optional `yt-dlp` warning is not a transcript failure. If metadata falls back to
oEmbed, do not claim chapters/description/duration are present when they are not.

## Capability boundary

The runtime consumes captions YouTube makes accessible. It does not download video,
run Whisper/audio ASR, identify speakers, translate captions, or bypass private,
restricted, or caption-disabled content.
