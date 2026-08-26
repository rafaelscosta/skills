# GPT-5.6 Agent Recipes

Use these patterns only when the request needs more than the default archive path.
They optimize evidence coverage, context cost, and provenance.

Assume:

```bash
PY="python3 $SKILL_DIR/scripts/fetch_transcript.py"
```

## 1. Cheap orientation before analysis

When the video is unknown or long and the user asks a question rather than a full
archive, inspect compact metadata first:

```bash
$PY URL --metadata-only --no-description --stdout
```

If chapters exist and the question clearly maps to one, use targeted chapter
selection rather than fetching broad transcript context.

## 2. Analyze one chapter

```bash
$PY URL --chapter 4 --format chunks --chunk-seconds 300 \
  --output /tmp/video.chapter4.chunks.json --manifest --machine
```

Read only the resulting chunk objects required to answer the question.

A unique title is also valid:

```bash
$PY URL --chapter "evaluation" --format chunks \
  --output /tmp/evaluation.chunks.json --manifest --machine
```

## 3. Analyze a time range

```bash
$PY URL --start 12:30 --end 21:00 --format chunks \
  --output /tmp/range.chunks.json --manifest --machine
```

Use the `[start,end)` semantics recorded in the chunks and manifest.

## 4. Broad long-video analysis without permanent archive

Prefer a temporary chunks artifact:

```bash
$PY URL --format chunks --chunk-seconds 300 \
  --output /tmp/video.chunks.json --manifest --machine
```

Then:

1. inspect the chunks index/metadata;
2. read only one or a few chunks at a time;
3. maintain a compact evidence ledger of claims and chunk IDs;
4. synthesize only after coverage is adequate;
5. remove temporary artifacts after the answer if no archive was requested and the
   environment permits.

Do not pipe the full video through `--stdout` merely to feed model context.

## 5. RAG ingestion

```bash
$PY URL --format chunks --chunk-seconds 180 \
  --output ./rag/source.chunks.json \
  --manifest ./rag/source.manifest.json --machine
```

Use `video_id + chunk_id` as a stable logical key. Keep the manifest beside the
chunks file so downstream indexing can verify source, selection, language and hash.

## 6. Archival Markdown with machine receipt

```bash
$PY URL --output-dir ~/Notes/Vault --manifest --machine
```

The archival note remains the primary artifact; stdout is only the JSON receipt.

## 7. Metadata-only programmatic capture

```bash
$PY URL --metadata-only --output ./source.metadata.json --manifest --machine
```

This path must not require or import `youtube-transcript-api`.

## 8. Chapter inventory only

```bash
$PY URL --chapters-only --stdout
```

If the result is empty and `metadata_source` is not `yt-dlp`, surface the metadata
degradation rather than concluding that the creator definitively published no
chapters.
