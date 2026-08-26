from __future__ import annotations
import argparse
import hashlib
import importlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import parse_qs, urlparse
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_MISSING_DEPS = 2
EXIT_DUPLICATE_SKIPPED = 3
MANIFEST_SCHEMA = 'youtube-fetcher.manifest/v2'
RECEIPT_SCHEMA = 'youtube-fetcher.receipt/v2'
CHUNKS_SCHEMA = 'youtube-fetcher.chunks/v2'
METADATA_SCHEMA = 'youtube-fetcher.metadata/v2'
CHAPTERS_SCHEMA = 'youtube-fetcher.chapters/v2'
DEFAULT_OUTPUT_DIRNAME = 'yt_transcripts'
OUTPUT_DIR_ENV = 'YOUTUBE_FETCHER_DIR'
DEFAULT_CHUNK_SECONDS = 300
VIDEO_ID_PATTERN = re.compile('^[A-Za-z0-9_-]{11}$')
YOUTUBE_HOSTS = {'youtube.com', 'www.youtube.com', 'm.youtube.com', 'music.youtube.com', 'youtube-nocookie.com', 'www.youtube-nocookie.com'}
SHORT_YOUTUBE_HOSTS = {'youtu.be', 'www.youtu.be'}

class RuntimeFailure(Exception):

    def __init__(self, message: str, exit_code: int=EXIT_ERROR):
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')

def eprint(message: str='') -> None:
    print(message, file=sys.stderr)

def dependency_requirements(operation: str, fmt: str='text', chapter: bool=False) -> Dict[str, bool]:
    needs_transcript = operation in {'archive', 'transcript', 'list'}
    needs_metadata = operation in {'archive', 'metadata', 'chapters'} or chapter or (operation == 'transcript' and fmt == 'text')
    if operation == 'transcript' and fmt in {'json', 'srt', 'chunks'} and (not chapter):
        needs_metadata = False
    return {'transcript': needs_transcript, 'metadata': needs_metadata}

def check_dependencies(require_transcript: bool=True, require_metadata: bool=True) -> List[Dict[str, Any]]:
    missing: List[Dict[str, Any]] = []
    python_deps = []
    if require_transcript:
        python_deps.append({'module': 'youtube_transcript_api', 'name': 'youtube-transcript-api', 'install': 'python3 -m pip install youtube-transcript-api'})
    if require_metadata:
        python_deps.append({'module': 'requests', 'name': 'requests', 'install': 'python3 -m pip install requests'})
    for dep in python_deps:
        try:
            importlib.import_module(dep['module'])
        except ImportError:
            missing.append({'name': dep['name'], 'type': 'python', 'install': dep['install']})
    if require_metadata and (not shutil.which('yt-dlp')):
        missing.append({'name': 'yt-dlp', 'type': 'system', 'install': 'brew install yt-dlp  # or: python3 -m pip install yt-dlp', 'optional': True})
    return missing

def print_dependency_report(missing: Sequence[Dict[str, Any]]) -> None:
    required = [d for d in missing if not d.get('optional')]
    optional = [d for d in missing if d.get('optional')]
    if required:
        eprint('\nMissing required dependencies:')
        for dep in required:
            eprint(f"  - {dep['name']}")
            eprint(f"    Install: {dep['install']}")
    if optional:
        if required:
            eprint()
        eprint('Optional metadata dependency missing:')
        for dep in optional:
            eprint(f"  - {dep['name']} — {dep['install']}")
            if dep['name'] == 'yt-dlp':
                eprint('    Without yt-dlp: no description, chapters, duration, or upload date.')

def find_existing_transcript(video_id: str, transcripts_dir: Path) -> Optional[Path]:
    if not transcripts_dir.exists():
        return None
    matches = list(transcripts_dir.glob(f'*_[[]{video_id}[]].md'))
    if matches:
        return matches[0]
    for md_file in transcripts_dir.glob('*.md'):
        try:
            with md_file.open(encoding='utf-8', errors='ignore') as handle:
                head = handle.read(512)
            if f'video_id: "{video_id}"' in head:
                return md_file
        except OSError:
            continue
    return None

def get_existing_transcript_date(filepath: Path) -> str:
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        match = re.search('fetched:\\s*"(\\d{4}-\\d{2}-\\d{2})"', content)
        if match:
            return match.group(1)
    except OSError:
        pass
    return 'unknown date'

def overwrite_approved(path: Path, force: bool) -> bool:
    if not path.exists() or force:
        return True
    if not sys.stdin.isatty():
        return False
    try:
        answer = input(f'Output exists: {path}\nOverwrite? [y/N]: ').strip().lower()
    except (EOFError, KeyboardInterrupt):
        answer = 'n'
    return answer in {'y', 'yes'}

def safe_write_text(path: Path, content: str, force: bool=False) -> None:
    if not overwrite_approved(path, force):
        raise RuntimeFailure(f'Existing output preserved: {path}. Use --force to overwrite.', EXIT_DUPLICATE_SKIPPED)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

def extract_video_id(url_or_id: str) -> str:
    candidate = url_or_id.strip()
    if VIDEO_ID_PATTERN.fullmatch(candidate):
        return candidate
    parsed = urlparse(candidate)
    if parsed.scheme.lower() not in {'http', 'https'} or not parsed.hostname:
        raise ValueError(f"Could not extract a YouTube video ID from '{url_or_id}'")
    host = parsed.hostname.lower().rstrip('.')
    path_parts = [part for part in parsed.path.split('/') if part]
    video_id = None
    if host in SHORT_YOUTUBE_HOSTS and path_parts:
        video_id = path_parts[0]
    elif host in YOUTUBE_HOSTS:
        if parsed.path.rstrip('/') == '/watch':
            values = parse_qs(parsed.query).get('v', [])
            video_id = values[0] if values else None
        elif len(path_parts) >= 2 and path_parts[0].lower() in {'embed', 'live', 'shorts', 'v'}:
            video_id = path_parts[1]
    if video_id and VIDEO_ID_PATTERN.fullmatch(video_id):
        return video_id
    raise ValueError(f"Could not extract a YouTube video ID from '{url_or_id}'")

def resolve_output_directory(output: Optional[str], output_dir: Optional[str], environ: Optional[Dict[str, str]]=None) -> Path:
    if output:
        return Path(output).expanduser().parent
    if output_dir:
        return Path(output_dir).expanduser()
    env = os.environ if environ is None else environ
    env_dir = env.get(OUTPUT_DIR_ENV, '').strip()
    if env_dir:
        return Path(env_dir).expanduser()
    return Path.home() / DEFAULT_OUTPUT_DIRNAME

def _format_upload_date(raw: str) -> str:
    if raw and len(raw) == 8 and raw.isdigit():
        return f'{raw[:4]}-{raw[4:6]}-{raw[6:8]}'
    return raw

def fetch_video_metadata(video_id: str, warnings: Optional[List[str]]=None) -> Dict[str, Any]:
    warnings = warnings if warnings is not None else []
    if not shutil.which('yt-dlp'):
        return _fetch_metadata_oembed(video_id, warnings)
    url = f'https://www.youtube.com/watch?v={video_id}'
    try:
        result = subprocess.run(['yt-dlp', '--skip-download', '--dump-json', '--no-warnings', url], capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            message = 'yt-dlp failed; falling back to oEmbed metadata.'
            warnings.append(message)
            eprint(f'Warning: {message}')
            return _fetch_metadata_oembed(video_id, warnings)
        data = json.loads(result.stdout)
        return {'title': data.get('title') or 'Untitled', 'channel': data.get('channel') or data.get('uploader') or 'Unknown', 'description': data.get('description') or '', 'duration': int(data.get('duration') or 0), 'upload_date': _format_upload_date(data.get('upload_date', '')), 'chapters': data.get('chapters') or [], 'metadata_source': 'yt-dlp'}
    except Exception as error:
        message = f'yt-dlp error ({error}); falling back to oEmbed metadata.'
        warnings.append(message)
        eprint(f'Warning: {message}')
        return _fetch_metadata_oembed(video_id, warnings)

def _fetch_metadata_oembed(video_id: str, warnings: Optional[List[str]]=None) -> Dict[str, Any]:
    import requests
    warnings = warnings if warnings is not None else []
    url = f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {'title': data.get('title') or 'Untitled', 'channel': data.get('author_name') or 'Unknown', 'description': '', 'duration': 0, 'upload_date': '', 'chapters': [], 'metadata_source': 'oembed'}
    except Exception as error:
        message = f'oEmbed metadata unavailable ({error}); using empty metadata.'
        warnings.append(message)
        eprint(f'Warning: {message}')
        return {'title': 'Untitled', 'channel': 'Unknown', 'description': '', 'duration': 0, 'upload_date': '', 'chapters': [], 'metadata_source': 'none'}

def select_transcript(transcript_list: Any, requested_language: str, warnings: Optional[List[str]]=None) -> Tuple[Any, str, str]:
    warnings = warnings if warnings is not None else []
    requested_languages = [requested_language]
    if requested_language.lower() != 'en':
        requested_languages.append('en')
    selected = transcript_list.find_transcript(requested_languages)
    actual_language = selected.language_code
    requested_lower = requested_language.lower()
    actual_lower = actual_language.lower()
    if not (actual_lower == requested_lower or actual_lower.startswith(f'{requested_lower}-')):
        message = f"requested captions '{requested_language}' were unavailable; using '{actual_language}' instead."
        warnings.append(message)
        eprint(f'Warning: {message}')
    caption_type = 'auto-generated' if selected.is_generated else 'manual'
    return (selected, actual_language, caption_type)

def normalize_snippet(snippet: Any) -> Dict[str, Any]:
    if isinstance(snippet, dict):
        text = snippet.get('text', '')
        start = snippet.get('start', 0)
        duration = snippet.get('duration', 0)
    else:
        text = getattr(snippet, 'text', '')
        start = getattr(snippet, 'start', 0)
        duration = getattr(snippet, 'duration', 0)
    start_f = float(start or 0)
    duration_f = max(0.0, float(duration or 0))
    return {'text': str(text), 'start': start_f, 'duration': duration_f, 'end': start_f + duration_f}

def normalize_transcript(transcript: Iterable[Any]) -> List[Dict[str, Any]]:
    return [normalize_snippet(snippet) for snippet in transcript]

def parse_time_spec(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        raise ValueError('Time value cannot be empty')
    if ':' not in text:
        try:
            seconds = float(text)
        except ValueError as error:
            raise ValueError(f'Invalid time value: {value}') from error
        if not math.isfinite(seconds) or seconds < 0:
            raise ValueError(f'Invalid time value: {value}')
        return seconds
    parts = text.split(':')
    if len(parts) not in {2, 3}:
        raise ValueError(f'Invalid time value: {value}')
    try:
        numbers = [float(part) for part in parts]
    except ValueError as error:
        raise ValueError(f'Invalid time value: {value}') from error
    if any((not math.isfinite(number) or number < 0 for number in numbers)):
        raise ValueError(f'Invalid time value: {value}')
    if len(numbers) == 2:
        minutes, seconds = numbers
        if seconds >= 60:
            raise ValueError(f'Invalid MM:SS time value: {value}')
        return minutes * 60 + seconds
    hours, minutes, seconds = numbers
    if minutes >= 60 or seconds >= 60:
        raise ValueError(f'Invalid HH:MM:SS time value: {value}')
    return hours * 3600 + minutes * 60 + seconds

def format_timestamp(seconds: float) -> str:
    seconds = max(0.0, float(seconds or 0))
    whole = int(seconds)
    hours = whole // 3600
    minutes = whole % 3600 // 60
    secs = whole % 60
    if hours > 0:
        return f'{hours:02d}:{minutes:02d}:{secs:02d}'
    return f'{minutes:02d}:{secs:02d}'

def normalize_chapters(chapters: Sequence[Dict[str, Any]], duration: int=0) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for index, chapter in enumerate(chapters):
        start = float(chapter.get('start_time') or 0)
        explicit_end = chapter.get('end_time')
        if explicit_end is not None:
            end: Optional[float] = float(explicit_end)
        elif index + 1 < len(chapters):
            end = float(chapters[index + 1].get('start_time') or 0)
        elif duration:
            end = float(duration)
        else:
            end = None
        title = sanitize_inline_text(chapter.get('title', '')) or f'Chapter {index + 1}'
        normalized.append({'index': index + 1, 'title': title, 'start': start, 'end': end, 'start_timestamp': format_timestamp(start), 'end_timestamp': format_timestamp(end) if end is not None else None})
    return normalized

def resolve_chapter(chapters: Sequence[Dict[str, Any]], selector: str, duration: int=0) -> Dict[str, Any]:
    normalized = normalize_chapters(chapters, duration)
    if not normalized:
        raise ValueError('No chapters are available for this video')
    selector_text = str(selector).strip()
    if selector_text.isdigit():
        index = int(selector_text)
        if 1 <= index <= len(normalized):
            return normalized[index - 1]
        raise ValueError(f'Chapter index {index} is out of range (1-{len(normalized)})')
    exact = [chapter for chapter in normalized if chapter['title'].casefold() == selector_text.casefold()]
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        raise ValueError(f'Chapter title is ambiguous: {selector}')
    partial = [chapter for chapter in normalized if selector_text.casefold() in chapter['title'].casefold()]
    if len(partial) == 1:
        return partial[0]
    if len(partial) > 1:
        raise ValueError(f'Chapter selector matches multiple chapters: {selector}')
    raise ValueError(f'Chapter not found: {selector}')

def filter_snippets(snippets: Sequence[Dict[str, Any]], start: Optional[float]=None, end: Optional[float]=None) -> List[Dict[str, Any]]:
    start_bound = 0.0 if start is None else float(start)
    end_bound = None if end is None else float(end)
    if end_bound is not None and end_bound <= start_bound:
        raise ValueError('End time must be greater than start time')
    selected: List[Dict[str, Any]] = []
    for snippet in snippets:
        snippet_start = float(snippet['start'])
        snippet_end = float(snippet.get('end', snippet_start + float(snippet.get('duration', 0))))
        if snippet_end == snippet_start:
            overlaps_start = snippet_start >= start_bound
        else:
            overlaps_start = snippet_end > start_bound
        overlaps_end = end_bound is None or snippet_start < end_bound
        if overlaps_start and overlaps_end:
            selected.append(dict(snippet))
    return selected

def selection_from_args(args: argparse.Namespace, metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if args.chapter:
        if metadata is None:
            raise ValueError('Chapter selection requires metadata')
        chapter = resolve_chapter(metadata.get('chapters', []), args.chapter, metadata.get('duration', 0))
        return {'scope': 'chapter', 'chapter': chapter, 'start': chapter['start'], 'end': chapter['end']}
    start = parse_time_spec(args.start)
    end = parse_time_spec(args.end)
    if start is not None or end is not None:
        start_value = 0.0 if start is None else start
        if end is not None and end <= start_value:
            raise ValueError('--end must be greater than --start')
        return {'scope': 'range', 'chapter': None, 'start': start_value, 'end': end}
    return {'scope': 'full', 'chapter': None, 'start': None, 'end': None}

def chunk_snippets(snippets: Sequence[Dict[str, Any]], chunk_seconds: int=DEFAULT_CHUNK_SECONDS) -> List[Dict[str, Any]]:
    if chunk_seconds <= 0:
        raise ValueError('chunk_seconds must be greater than zero')
    buckets: Dict[int, List[Dict[str, Any]]] = {}
    for snippet in snippets:
        bucket_index = int(float(snippet['start']) // chunk_seconds)
        buckets.setdefault(bucket_index, []).append(dict(snippet))
    chunks: List[Dict[str, Any]] = []
    for bucket_index in sorted(buckets):
        members = buckets[bucket_index]
        window_start = bucket_index * chunk_seconds
        window_end = window_start + chunk_seconds
        text = '\n'.join((member['text'] for member in members))
        actual_start = min((float(member['start']) for member in members))
        actual_end = max((float(member.get('end', member['start'])) for member in members))
        chunks.append({'chunk_id': f'chunk-{window_start:06d}-{window_end:06d}', 'window_start': float(window_start), 'window_end': float(window_end), 'window_start_timestamp': format_timestamp(window_start), 'window_end_timestamp': format_timestamp(window_end), 'content_start': actual_start, 'content_end': actual_end, 'snippet_count': len(members), 'char_count': len(text), 'text': text, 'snippets': [{'text': member['text'], 'start': member['start'], 'duration': member['duration']} for member in members]})
    return chunks

def sanitize_inline_text(text: Any) -> str:
    return ' '.join(str(text).replace('\x00', '').splitlines()).strip()

def sanitize_table_value(text: Any) -> str:
    return sanitize_inline_text(text).replace('|', '\\|')

def yaml_quote(value: Any) -> str:
    return json.dumps(str(value), ensure_ascii=False)

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub('[^\\w\\s-]', '', text)
    text = re.sub('[\\s_]+', '-', text)
    text = re.sub('-+', '-', text)
    return text.strip('-')[:80]

def format_duration(seconds: int) -> str:
    seconds = int(seconds or 0)
    hours = seconds // 3600
    minutes = seconds % 3600 // 60
    secs = seconds % 60
    if hours > 0:
        return f'{hours}h {minutes}m {secs}s'
    return f'{minutes}m {secs}s'

def build_description_section(description: str, chapters: Sequence[Dict[str, Any]]) -> str:
    if not description and (not chapters):
        return ''
    parts = ['\n## Video Description\n']
    if description:
        safe_description = re.sub('^-{3,}$', '\\---', str(description).replace('\x00', ''), flags=re.MULTILINE)
        parts.append(safe_description)
    if chapters:
        parts.append('\n### Chapters\n')
        for chapter in chapters:
            timestamp = format_timestamp(chapter.get('start_time', 0))
            title = sanitize_inline_text(chapter.get('title', ''))
            parts.append(f'- `{timestamp}` {title}')
    return '\n'.join(parts)

def build_selection_frontmatter(selection: Optional[Dict[str, Any]]) -> str:
    if not selection or selection.get('scope') == 'full':
        return ''
    parts = [f"\ntranscript_scope: {yaml_quote(selection['scope'])}"]
    if selection.get('start') is not None:
        parts.append(f"\ntranscript_start_seconds: {yaml_quote(selection['start'])}")
    if selection.get('end') is not None:
        parts.append(f"\ntranscript_end_seconds: {yaml_quote(selection['end'])}")
    chapter = selection.get('chapter')
    if chapter:
        parts.append(f"\ntranscript_chapter_index: {chapter['index']}")
        parts.append(f"\ntranscript_chapter_title: {yaml_quote(chapter['title'])}")
    return ''.join(parts)

def build_markdown(title: str, channel: str, video_id: str, fetched_date: str, source_project: str, language: str, caption_type: str, description_section: str, transcript_text: str, duration: int=0, upload_date: str='', selection: Optional[Dict[str, Any]]=None) -> str:
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    safe_heading = sanitize_inline_text(title) or 'Untitled'
    extra_frontmatter = ''
    if duration:
        extra_frontmatter += f'\nduration: {yaml_quote(format_duration(duration))}'
    if upload_date:
        extra_frontmatter += f'\nupload_date: {yaml_quote(upload_date)}'
    extra_frontmatter += build_selection_frontmatter(selection)
    extra_rows = ''
    if duration:
        extra_rows += f'\n| Duration | {format_duration(duration)} |'
    if upload_date:
        extra_rows += f'\n| Uploaded | {sanitize_table_value(upload_date)} |'
    if selection and selection.get('scope') != 'full':
        extra_rows += f"\n| Scope    | {sanitize_table_value(selection['scope'])} |"
        if selection.get('start') is not None:
            extra_rows += f"\n| From     | {format_timestamp(selection['start'])} |"
        if selection.get('end') is not None:
            extra_rows += f"\n| To       | {format_timestamp(selection['end'])} |"
        if selection.get('chapter'):
            extra_rows += f"\n| Chapter  | {sanitize_table_value(selection['chapter']['title'])} |"
    return f"---\ntitle: {yaml_quote(title)}\nchannel: {yaml_quote(channel)}\nurl: {yaml_quote(video_url)}\nvideo_id: {yaml_quote(video_id)}\nfetched: {yaml_quote(fetched_date)}\nsource_project: {yaml_quote(source_project)}\nlanguage: {yaml_quote(language)}\ncaption_type: {yaml_quote(caption_type)}{extra_frontmatter}\ntags:\n  - yt-transcript\n---\n\n# {safe_heading}\n\n## Video Details\n\n| Field    | Value |\n|----------|-------|\n| URL      | {video_url} |\n| Channel  | {sanitize_table_value(channel)} |{extra_rows}\n| Fetched  | {fetched_date} |\n| Source   | {sanitize_table_value(source_project)} |\n| Language | {sanitize_table_value(f'{language} ({caption_type})')} |\n{description_section}\n\n## Transcript\n\n{transcript_text}\n"

def transcript_text(snippets: Sequence[Dict[str, Any]], timestamps: bool=False) -> str:
    lines = []
    for snippet in snippets:
        if timestamps:
            lines.append(f"[{format_timestamp(snippet['start'])}] {snippet['text']}")
        else:
            lines.append(snippet['text'])
    return '\n'.join(lines)

def json_transcript(snippets: Sequence[Dict[str, Any]]) -> str:
    payload = [{'text': snippet['text'], 'start': snippet['start'], 'duration': snippet['duration']} for snippet in snippets]
    return json.dumps(payload, ensure_ascii=False, indent=2)

def _srt_timestamp(seconds: float) -> str:
    milliseconds = int(round(max(0.0, seconds) * 1000))
    hours, remainder = divmod(milliseconds, 3600000)
    minutes, remainder = divmod(remainder, 60000)
    secs, millis = divmod(remainder, 1000)
    return f'{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}'

def srt_transcript(snippets: Sequence[Dict[str, Any]]) -> str:
    blocks = []
    for index, snippet in enumerate(snippets, start=1):
        start = float(snippet['start'])
        end = float(snippet.get('end', start + float(snippet.get('duration', 0))))
        if end <= start:
            end = start + 0.001
        blocks.append(f"{index}\n{_srt_timestamp(start)} --> {_srt_timestamp(end)}\n{snippet['text']}")
    return '\n\n'.join(blocks) + ('\n' if blocks else '')

def metadata_payload(video_id: str, metadata: Dict[str, Any], include_description: bool=True) -> Dict[str, Any]:
    chapters = normalize_chapters(metadata.get('chapters', []), metadata.get('duration', 0))
    return {'schema_version': METADATA_SCHEMA, 'video_id': video_id, 'url': f'https://www.youtube.com/watch?v={video_id}', 'title': metadata['title'], 'channel': metadata['channel'], 'description': metadata['description'] if include_description else '', 'duration': metadata['duration'], 'upload_date': metadata['upload_date'], 'metadata_source': metadata.get('metadata_source', 'unknown'), 'chapter_count': len(chapters), 'chapters': chapters}

def chapters_payload(video_id: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    return {'schema_version': CHAPTERS_SCHEMA, 'video_id': video_id, 'url': f'https://www.youtube.com/watch?v={video_id}', 'title': metadata['title'], 'metadata_source': metadata.get('metadata_source', 'unknown'), 'chapters': normalize_chapters(metadata.get('chapters', []), metadata.get('duration', 0))}

def chunks_payload(video_id: str, language: str, caption_type: str, selection: Dict[str, Any], chunks: Sequence[Dict[str, Any]], chunk_seconds: int) -> Dict[str, Any]:
    return {'schema_version': CHUNKS_SCHEMA, 'video_id': video_id, 'url': f'https://www.youtube.com/watch?v={video_id}', 'language': language, 'caption_type': caption_type, 'selection': selection, 'chunking': {'strategy': 'absolute-fixed-time-window', 'chunk_seconds': chunk_seconds, 'boundary': '[start,end)', 'assignment': 'snippet-start'}, 'chunks': list(chunks)}

def sha256_text(content: str) -> str:
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def effective_format(mode: str, fmt: str) -> str:
    if mode in {'metadata', 'chapters', 'list'}:
        return 'json'
    return fmt

def infer_media_type(mode: str, fmt: str) -> str:
    if mode in {'metadata', 'chapters', 'list'} or fmt in {'json', 'chunks'}:
        return 'application/json'
    if fmt == 'srt':
        return 'application/x-subrip'
    return 'text/markdown'

def filename_time_token(seconds: Optional[float]) -> str:
    if seconds is None:
        return 'end'
    value = float(seconds)
    if value.is_integer():
        return f'{int(value):06d}'
    rendered = f'{value:.3f}'.rstrip('0').rstrip('.')
    whole, fraction = rendered.split('.', 1)
    return f'{int(whole):06d}p{fraction}'

def selection_filename_suffix(selection: Optional[Dict[str, Any]]) -> str:
    if not selection or selection.get('scope') == 'full':
        return ''
    if selection.get('scope') == 'chapter' and selection.get('chapter'):
        chapter = selection['chapter']
        title_slug = slugify(chapter.get('title', '')) or 'chapter'
        return f".chapter-{int(chapter['index']):02d}-{title_slug[:40]}"
    if selection.get('scope') == 'range':
        return f".range-{filename_time_token(selection.get('start'))}-{filename_time_token(selection.get('end'))}"
    return f".{slugify(str(selection.get('scope', 'selection')))}"

def default_output_path(args: argparse.Namespace, resolved_output_dir: Path, video_id: str, metadata: Optional[Dict[str, Any]], operation: str, selection: Optional[Dict[str, Any]]=None) -> Path:
    if args.output:
        return Path(args.output).expanduser()
    if operation == 'metadata':
        return resolved_output_dir / f'{video_id}.metadata.json'
    if operation == 'chapters':
        return resolved_output_dir / f'{video_id}.chapters.json'
    selection_suffix = selection_filename_suffix(selection)
    if args.fmt == 'json':
        return resolved_output_dir / f'{video_id}{selection_suffix}.json'
    if args.fmt == 'srt':
        return resolved_output_dir / f'{video_id}{selection_suffix}.srt'
    if args.fmt == 'chunks':
        return resolved_output_dir / f'{video_id}{selection_suffix}.chunks.json'
    title = metadata['title'] if metadata else 'untitled'
    return resolved_output_dir / f'{date.today().isoformat()}_{slugify(title)}_[{video_id}]{selection_suffix}.md'

def resolve_manifest_path(manifest_arg: Optional[str], artifact_path: Optional[Path], resolved_output_dir: Path, video_id: str) -> Optional[Path]:
    if manifest_arg is None:
        return None
    if manifest_arg == 'auto':
        if artifact_path is not None:
            return Path(str(artifact_path) + '.manifest.json')
        return resolved_output_dir / f'{video_id}.manifest.json'
    return Path(manifest_arg).expanduser()

def build_manifest(*, started_at: str, completed_at: str, status: str, args: argparse.Namespace, video_id: str, operation: str, artifact_path: Optional[Path], content: Optional[str], manifest_path: Optional[Path], warnings: Sequence[str], selection: Optional[Dict[str, Any]]=None, language: Optional[str]=None, caption_type: Optional[str]=None, metadata: Optional[Dict[str, Any]]=None, original_snippet_count: Optional[int]=None, selected_snippet_count: Optional[int]=None, chunk_count: Optional[int]=None, error: Optional[str]=None) -> Dict[str, Any]:
    output: Dict[str, Any] = {'path': str(artifact_path) if artifact_path is not None else None, 'stdout': bool(args.stdout or (args.machine and operation == 'list')), 'format': effective_format(operation, args.fmt), 'media_type': infer_media_type(operation, args.fmt)}
    if content is not None:
        output.update({'sha256': sha256_text(content), 'bytes': len(content.encode('utf-8'))})
    manifest: Dict[str, Any] = {'schema_version': MANIFEST_SCHEMA, 'status': status, 'started_at': started_at, 'completed_at': completed_at, 'input': {'value': args.video, 'video_id': video_id, 'url': f'https://www.youtube.com/watch?v={video_id}'}, 'operation': {'mode': operation, 'format': effective_format(operation, args.fmt), 'requested_language': args.lang if operation in {'archive', 'transcript', 'list'} else None, 'timestamps': bool(args.timestamps), 'chunk_seconds': args.chunk_seconds if args.fmt == 'chunks' else None}, 'selection': selection, 'transcript': {'actual_language': language, 'caption_type': caption_type, 'original_snippet_count': original_snippet_count, 'selected_snippet_count': selected_snippet_count, 'chunk_count': chunk_count}, 'metadata': None, 'output': output, 'manifest_path': str(manifest_path) if manifest_path is not None else None, 'warnings': list(warnings), 'error': error}
    if metadata is not None:
        manifest['metadata'] = {'source': metadata.get('metadata_source'), 'title': metadata.get('title'), 'channel': metadata.get('channel'), 'duration': metadata.get('duration'), 'upload_date': metadata.get('upload_date'), 'chapter_count': len(metadata.get('chapters', []))}
    return manifest

def build_receipt(*, status: str, operation: str, video_id: Optional[str], artifact_path: Optional[Path]=None, manifest_path: Optional[Path]=None, language: Optional[str]=None, caption_type: Optional[str]=None, warnings: Sequence[str]=(), error: Optional[str]=None, exit_code: int=EXIT_SUCCESS) -> Dict[str, Any]:
    return {'schema_version': RECEIPT_SCHEMA, 'status': status, 'exit_code': exit_code, 'operation': operation, 'video_id': video_id, 'artifact_path': str(artifact_path) if artifact_path is not None else None, 'manifest_path': str(manifest_path) if manifest_path is not None else None, 'language': language, 'caption_type': caption_type, 'warnings': list(warnings), 'error': error}

def emit_receipt(receipt: Dict[str, Any]) -> None:
    print(json.dumps(receipt, ensure_ascii=False, separators=(',', ':')))

def determine_operation(args: argparse.Namespace) -> str:
    if args.metadata_only:
        return 'metadata'
    if args.chapters_only:
        return 'chapters'
    if args.list:
        return 'list'
    if args.fmt == 'text' and (not (args.start or args.end or args.chapter)):
        return 'archive'
    return 'transcript'

def validate_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if args.machine and args.stdout:
        parser.error('--machine and --stdout are mutually exclusive')
    if args.metadata_only and args.chapters_only:
        parser.error('--metadata-only and --chapters-only are mutually exclusive')
    if args.chapter and (args.start is not None or args.end is not None):
        parser.error('--chapter cannot be combined with --start or --end')
    if args.chunk_seconds is not None and args.fmt != 'chunks':
        parser.error('--chunk-seconds requires --format chunks')
    if args.fmt == 'chunks' and args.chunk_seconds is None:
        args.chunk_seconds = DEFAULT_CHUNK_SECONDS
    if args.chunk_seconds is not None and args.chunk_seconds <= 0:
        parser.error('--chunk-seconds must be greater than zero')
    metadata_mode = args.metadata_only or args.chapters_only
    if metadata_mode:
        incompatible = []
        if args.fmt != 'text':
            incompatible.append('--format')
        if args.timestamps:
            incompatible.append('--timestamps')
        if args.start is not None:
            incompatible.append('--start')
        if args.end is not None:
            incompatible.append('--end')
        if args.chapter:
            incompatible.append('--chapter')
        if incompatible:
            parser.error(f"{('--metadata-only' if args.metadata_only else '--chapters-only')} cannot be combined with {', '.join(incompatible)}")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Fetch YouTube transcripts/metadata with agent-native selective output', epilog='Exit codes: 0=success, 1=error, 2=missing deps, 3=existing output preserved')
    parser.add_argument('video', nargs='?', help='YouTube URL or video ID')
    parser.add_argument('--output', '-o', help='Custom output file path (highest precedence)')
    parser.add_argument('--output-dir', help=f'Output directory (overrides ${OUTPUT_DIR_ENV} and ~/{DEFAULT_OUTPUT_DIRNAME}/)')
    parser.add_argument('--timestamps', '-t', action='store_true', help='Include timestamps in Markdown transcript lines')
    parser.add_argument('--lang', '-l', default='en', help='Requested caption language code (default: en)')
    parser.add_argument('--format', '-f', dest='fmt', choices=['text', 'json', 'srt', 'chunks'], default='text', help='Output format: Markdown text, raw transcript JSON, SRT, or deterministic chunks JSON')
    parser.add_argument('--list', action='store_true', help='List available transcript languages')
    parser.add_argument('--source', '-s', default=None, help='Source project name (defaults to cwd name)')
    parser.add_argument('--stdout', action='store_true', help='Print primary payload instead of saving it')
    parser.add_argument('--machine', action='store_true', help='Emit one JSON receipt on stdout; diagnostics remain on stderr')
    parser.add_argument('--manifest', nargs='?', const='auto', default=None, metavar='PATH', help='Write execution manifest JSON; omit PATH for an automatic sidecar')
    parser.add_argument('--metadata-only', action='store_true', help='Fetch metadata only; do not touch transcript endpoints')
    parser.add_argument('--chapters-only', action='store_true', help='Fetch normalized chapters only; do not touch transcript endpoints')
    parser.add_argument('--start', metavar='TIME', help='Start of transcript selection in seconds, MM:SS, or HH:MM:SS')
    parser.add_argument('--end', metavar='TIME', help='End of transcript selection in seconds, MM:SS, or HH:MM:SS; interval is exclusive')
    parser.add_argument('--chapter', metavar='INDEX_OR_TITLE', help='Select one chapter by 1-based index or unique title/substring')
    parser.add_argument('--chunk-seconds', type=int, default=None, metavar='N', help=f'Absolute time-window size for --format chunks (default {DEFAULT_CHUNK_SECONDS})')
    parser.add_argument('--no-description', action='store_true', help='Skip description/chapters section in Markdown')
    parser.add_argument('--force', action='store_true', help='Authorize overwrite / re-fetch of existing output')
    parser.add_argument('--check-deps', action='store_true', help='Check all dependencies and exit')
    return parser

def main(argv: Optional[Sequence[str]]=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    validate_args(args, parser)
    if args.check_deps:
        missing = check_dependencies(require_transcript=True, require_metadata=True)
        required_missing = [item for item in missing if not item.get('optional')]
        exit_code = EXIT_MISSING_DEPS if required_missing else EXIT_SUCCESS
        if args.machine:
            receipt = build_receipt(status='error' if required_missing else 'success', operation='check-deps', video_id=None, warnings=[f"Optional dependency missing: {item['name']}" for item in missing if item.get('optional')], error='Missing required dependencies: ' + ', '.join((item['name'] for item in required_missing)) if required_missing else None, exit_code=exit_code)
            receipt['data'] = {'missing': missing}
            emit_receipt(receipt)
            return exit_code
        if not missing:
            print('All dependencies are installed.')
            return EXIT_SUCCESS
        print_dependency_report(missing)
        return exit_code
    if not args.video:
        parser.error('the following arguments are required: video')
    started_at = utc_now_iso()
    warnings: List[str] = []
    operation = determine_operation(args)
    video_id: Optional[str] = None
    artifact_path: Optional[Path] = None
    manifest_path: Optional[Path] = None
    language: Optional[str] = None
    caption_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    selection: Optional[Dict[str, Any]] = None
    content: Optional[str] = None
    original_snippet_count: Optional[int] = None
    selected_snippet_count: Optional[int] = None
    chunk_count: Optional[int] = None
    resolved_output_dir: Optional[Path] = None
    try:
        try:
            video_id = extract_video_id(args.video)
        except ValueError as error:
            raise RuntimeFailure(str(error), EXIT_ERROR) from error
        resolved_output_dir = resolve_output_directory(args.output, args.output_dir)
        needs = dependency_requirements(operation, args.fmt, chapter=bool(args.chapter))
        missing = check_dependencies(require_transcript=needs['transcript'], require_metadata=needs['metadata'])
        required_missing = [item for item in missing if not item.get('optional')]
        optional_missing = [item for item in missing if item.get('optional')]
        if optional_missing:
            print_dependency_report(optional_missing)
            for item in optional_missing:
                warnings.append(f"Optional dependency missing: {item['name']}")
        if required_missing:
            print_dependency_report(required_missing)
            names = ', '.join((item['name'] for item in required_missing))
            raise RuntimeFailure(f'Missing required dependencies: {names}', EXIT_MISSING_DEPS)
        if operation in {'metadata', 'chapters'}:
            metadata = fetch_video_metadata(video_id, warnings)
            payload = metadata_payload(video_id, metadata, include_description=not args.no_description) if operation == 'metadata' else chapters_payload(video_id, metadata)
            if operation == 'chapters' and (not payload['chapters']) and (metadata.get('metadata_source') != 'yt-dlp'):
                message = 'No chapters available from the current metadata source; yt-dlp is required for chapter extraction when YouTube oEmbed is the fallback.'
                warnings.append(message)
                eprint(f'Warning: {message}')
            content = json.dumps(payload, ensure_ascii=False, indent=2)
            if not args.stdout:
                artifact_path = default_output_path(args, resolved_output_dir, video_id, metadata, operation, selection)
                safe_write_text(artifact_path, content, args.force)
        else:
            from youtube_transcript_api import YouTubeTranscriptApi
            api = YouTubeTranscriptApi()
            try:
                transcript_list = api.list(video_id)
            except Exception as error:
                raise RuntimeFailure(f'Error listing transcripts: {error}') from error
            if operation == 'list':
                rows = []
                for transcript in transcript_list:
                    rows.append({'language_code': transcript.language_code, 'language': transcript.language, 'caption_type': 'auto-generated' if transcript.is_generated else 'manual'})
                content = json.dumps({'video_id': video_id, 'transcripts': rows}, ensure_ascii=False, indent=2)
                manifest_path = resolve_manifest_path(args.manifest, None, resolved_output_dir, video_id)
                if manifest_path is not None:
                    manifest = build_manifest(started_at=started_at, completed_at=utc_now_iso(), status='success', args=args, video_id=video_id, operation=operation, artifact_path=None, content=content, manifest_path=manifest_path, warnings=warnings)
                    safe_write_text(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2), args.force)
                if args.machine:
                    receipt = build_receipt(status='success', operation=operation, video_id=video_id, manifest_path=manifest_path, warnings=warnings)
                    receipt['data'] = {'transcripts': rows}
                    emit_receipt(receipt)
                elif args.stdout:
                    print(content)
                else:
                    for row in rows:
                        kind = 'auto' if row['caption_type'] == 'auto-generated' else 'manual'
                        print(f"  [{row['language_code']}] {row['language']} ({kind})")
                    if manifest_path is not None:
                        print(f'Manifest saved to {manifest_path}')
                return EXIT_SUCCESS
            if operation == 'archive' and (not args.force) and (not args.stdout):
                existing = find_existing_transcript(video_id, resolved_output_dir)
                if existing:
                    fetched_on = get_existing_transcript_date(existing)
                    message = f'Existing note preserved: {existing} (fetched {fetched_on})'
                    warnings.append(message)
                    manifest_path = resolve_manifest_path(args.manifest, existing, resolved_output_dir, video_id)
                    if manifest_path is not None:
                        manifest = build_manifest(started_at=started_at, completed_at=utc_now_iso(), status='duplicate_preserved', args=args, video_id=video_id, operation=operation, artifact_path=existing, content=None, manifest_path=manifest_path, warnings=warnings)
                        safe_write_text(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2), args.force)
                    if args.machine:
                        emit_receipt(build_receipt(status='duplicate_preserved', operation=operation, video_id=video_id, artifact_path=existing, manifest_path=manifest_path, warnings=warnings, exit_code=EXIT_DUPLICATE_SKIPPED))
                    else:
                        eprint(message)
                    return EXIT_DUPLICATE_SKIPPED
            if args.chapter or operation == 'archive':
                metadata = fetch_video_metadata(video_id, warnings)
            try:
                selected_transcript, language, caption_type = select_transcript(transcript_list, args.lang, warnings)
                fetched_transcript = selected_transcript.fetch()
            except Exception as error:
                raise RuntimeFailure(f'Error fetching transcript: {error}') from error
            snippets = normalize_transcript(fetched_transcript)
            original_snippet_count = len(snippets)
            try:
                selection = selection_from_args(args, metadata)
                selected_snippets = filter_snippets(snippets, selection['start'], selection['end'])
            except ValueError as error:
                raise RuntimeFailure(str(error)) from error
            selected_snippet_count = len(selected_snippets)
            if selection['scope'] != 'full' and (not selected_snippets):
                message = 'Transcript selection produced no caption snippets.'
                warnings.append(message)
                eprint(f'Warning: {message}')
            if args.fmt == 'json':
                content = json_transcript(selected_snippets)
            elif args.fmt == 'srt':
                content = srt_transcript(selected_snippets)
            elif args.fmt == 'chunks':
                chunks = chunk_snippets(selected_snippets, args.chunk_seconds)
                chunk_count = len(chunks)
                payload = chunks_payload(video_id, language, caption_type, selection, chunks, args.chunk_seconds)
                content = json.dumps(payload, ensure_ascii=False, indent=2)
            else:
                if metadata is None:
                    metadata = fetch_video_metadata(video_id, warnings)
                description_section = ''
                if not args.no_description:
                    description_section = build_description_section(metadata['description'], metadata['chapters'])
                content = build_markdown(title=metadata['title'], channel=metadata['channel'], video_id=video_id, fetched_date=date.today().isoformat(), source_project=args.source or Path.cwd().name, language=language, caption_type=caption_type, description_section=description_section, transcript_text=transcript_text(selected_snippets, args.timestamps), duration=metadata['duration'], upload_date=metadata['upload_date'], selection=selection)
            if not args.stdout:
                artifact_path = default_output_path(args, resolved_output_dir, video_id, metadata, operation, selection)
                safe_write_text(artifact_path, content, args.force)
        manifest_path = resolve_manifest_path(args.manifest, artifact_path, resolved_output_dir, video_id)
        if manifest_path is not None:
            manifest = build_manifest(started_at=started_at, completed_at=utc_now_iso(), status='success', args=args, video_id=video_id, operation=operation, artifact_path=artifact_path, content=content, manifest_path=manifest_path, warnings=warnings, selection=selection, language=language, caption_type=caption_type, metadata=metadata, original_snippet_count=original_snippet_count, selected_snippet_count=selected_snippet_count, chunk_count=chunk_count)
            safe_write_text(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2), args.force)
        if args.stdout:
            assert content is not None
            print(content)
        elif args.machine:
            emit_receipt(build_receipt(status='success', operation=operation, video_id=video_id, artifact_path=artifact_path, manifest_path=manifest_path, language=language, caption_type=caption_type, warnings=warnings))
        else:
            if artifact_path is not None:
                print(f'Saved to {artifact_path}')
            if manifest_path is not None:
                print(f'Manifest saved to {manifest_path}')
        return EXIT_SUCCESS
    except RuntimeFailure as failure:
        if args.manifest is not None and video_id is not None and (resolved_output_dir is not None) and (manifest_path is None):
            try:
                manifest_path = resolve_manifest_path(args.manifest, artifact_path, resolved_output_dir, video_id)
                if manifest_path is not None:
                    failure_manifest = build_manifest(started_at=started_at, completed_at=utc_now_iso(), status='duplicate_preserved' if failure.exit_code == EXIT_DUPLICATE_SKIPPED else 'error', args=args, video_id=video_id, operation=operation, artifact_path=artifact_path, content=content, manifest_path=manifest_path, warnings=warnings, selection=selection, language=language, caption_type=caption_type, metadata=metadata, original_snippet_count=original_snippet_count, selected_snippet_count=selected_snippet_count, chunk_count=chunk_count, error=failure.message)
                    safe_write_text(manifest_path, json.dumps(failure_manifest, ensure_ascii=False, indent=2), args.force)
            except Exception as manifest_error:
                manifest_path = None
                warnings.append(f'Failure manifest could not be written: {manifest_error}')
                eprint(f'Warning: failure manifest could not be written: {manifest_error}')
        if not args.machine:
            eprint(f'Error: {failure.message}')
        if args.machine:
            emit_receipt(build_receipt(status='error' if failure.exit_code != EXIT_DUPLICATE_SKIPPED else 'duplicate_preserved', operation=operation, video_id=video_id, artifact_path=artifact_path, manifest_path=manifest_path, language=language, caption_type=caption_type, warnings=warnings, error=failure.message, exit_code=failure.exit_code))
        return failure.exit_code
if __name__ == '__main__':
    sys.exit(main())
