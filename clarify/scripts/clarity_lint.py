#!/usr/bin/env python3
"""Deterministic lint for Brazilian-Portuguese clarity risks.

This tool flags surface-level risks. It does not prove comprehension,
semantic accuracy, or source fidelity. Use it before human/model review.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:[-’'][A-Za-zÀ-ÖØ-öø-ÿ0-9]+)*")
SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9])")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
URL_RE = re.compile(r"https?://\S+")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+")
LIST_PREFIX_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)")
NUMBERED_STEP_RE = re.compile(r"^\s*\d+[.)]\s+")
ACRONYM_RE = re.compile(r"\b[A-ZÁÉÍÓÚÇ][A-ZÁÉÍÓÚÇ0-9-]{1,9}\b")
PERCENT_RE = re.compile(r"\b\d+(?:[.,]\d+)?\s*%")

IMPERATIVE_STEMS = {
    "abra",
    "acesse",
    "ative",
    "atualize",
    "aguarde",
    "clique",
    "conecte",
    "confirme",
    "configure",
    "crie",
    "desative",
    "desconecte",
    "escolha",
    "exclua",
    "execute",
    "gere",
    "informe",
    "insira",
    "mantenha",
    "monitore",
    "publique",
    "registre",
    "remova",
    "revise",
    "salve",
    "selecione",
    "valide",
    "verifique",
}

VAGUE_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\badequad[oa]s?\b", "Substitua por um critério observável ou um limite explícito."),
    (r"\bbrevemente\b", "Informe um prazo ou evento de conclusão."),
    (r"\boportunamente\b", "Informe quem decide e quando."),
    (r"\bsempre que possível\b", "Defina a condição em que é obrigatório ou opcional."),
    (r"\bquando necessário\b", "Defina o gatilho que torna a ação necessária."),
    (r"\bde forma eficiente\b", "Defina a métrica de eficiência."),
    (r"\bgerar valor\b", "Defina o resultado observável: receita, custo, tempo, qualidade ou risco."),
    (r"\botimizar\b", "Informe qual variável deve melhorar e quais restrições não podem piorar."),
    (r"\betc\.?\b", "Verifique se a lista precisa ser completa para a decisão ou execução."),
)

NOMINALIZATION_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\brealizar\s+(?:a\s+|o\s+)?configura(?:ção|ções)\b", "Use “configurar”."),
    (r"\befetuar\s+(?:a\s+|o\s+)?valida(?:ção|ções)\b", "Use “validar”."),
    (r"\bproceder\s+(?:à|a|ao)\s+implementa(?:ção|ções)\b", "Use “implementar”."),
    (r"\bfazer\s+(?:a\s+|o\s+)?utiliza(?:ção|ções)\b", "Use “usar”."),
    (r"\brealizar\s+(?:a\s+|o\s+)?anális(?:e|es)\b", "Use “analisar”."),
    (r"\befetuar\s+(?:o\s+|a\s+)?envio\b", "Use “enviar”."),
    (r"\brealizar\s+(?:o\s+|a\s+)?monitoramento\b", "Use “monitorar”."),
    (r"\brealizar\s+(?:a\s+|o\s+)?exclusão\b", "Use “excluir”."),
    (r"\bpromover\s+(?:a\s+|o\s+)?integração\b", "Use “integrar” quando a ação for o sentido pretendido."),
    (r"\boperacionaliza(?:ção|ções)\b", "Nomeie a ação concreta, o responsável e o resultado observável."),
    (r"\botimiza(?:ção|ções)\b", "Nomeie a variável, o baseline e a restrição que definem a melhoria."),
)

PASSIVE_RE = re.compile(
    r"\b(?:é|são|foi|foram|será|serão|deve\s+ser|devem\s+ser)\s+"
    r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:ado|ada|ados|adas|ido|ida|idos|idas)\b",
    re.IGNORECASE,
)

DEFAULT_ACRONYM_ALLOWLIST = {
    "AI",
    "IA",
    "PT-BR",
    "R$",
    "OK",
}


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    line: int
    message: str
    excerpt: str
    suggestion: str


@dataclass(frozen=True)
class Metrics:
    characters: int
    words: int
    sentences: int
    paragraphs: int
    headings: int
    list_items: int
    average_sentence_words: float
    maximum_sentence_words: int
    long_sentences: int
    long_paragraphs: int


def read_text(path: str) -> tuple[str, str]:
    if path == "-":
        return sys.stdin.read(), "<stdin>"
    file_path = Path(path)
    return file_path.read_text(encoding="utf-8"), str(file_path)


def strip_fenced_code(text: str) -> str:
    output: list[str] = []
    in_fence = False
    fence_token = ""
    for line in text.splitlines(keepends=True):
        match = FENCE_RE.match(line)
        if match:
            token = match.group(1)
            if not in_fence:
                in_fence = True
                fence_token = token
            elif token == fence_token:
                in_fence = False
                fence_token = ""
            output.append("\n" if line.endswith("\n") else "")
            continue
        output.append(("\n" if line.endswith("\n") else "") if in_fence else line)
    return "".join(output)


def normalize_markdown(text: str) -> str:
    text = strip_fenced_code(text)
    text = INLINE_CODE_RE.sub("", text)
    text = MARKDOWN_LINK_RE.sub(r"\1", text)
    text = URL_RE.sub("", text)
    return text


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, max(0, offset)) + 1


def excerpt(value: str, limit: int = 180) -> str:
    compact = re.sub(r"\s+", " ", value).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def iter_sentences(text: str) -> Iterable[tuple[str, int]]:
    cursor = 0
    for paragraph_match in re.finditer(r"\S(?:.*?\S)?(?=\n\s*\n|\Z)", text, re.DOTALL):
        paragraph = paragraph_match.group(0)
        paragraph_offset = paragraph_match.start()
        local_cursor = 0
        for sentence in SENTENCE_BOUNDARY_RE.split(paragraph):
            sentence = sentence.strip()
            if not sentence:
                continue
            found = paragraph.find(sentence, local_cursor)
            if found < 0:
                found = local_cursor
            offset = paragraph_offset + found
            yield sentence, offset
            local_cursor = found + len(sentence)
        cursor = paragraph_match.end()
    _ = cursor


def iter_paragraphs(text: str) -> Iterable[tuple[str, int]]:
    for match in re.finditer(r"\S(?:.*?\S)?(?=\n\s*\n|\Z)", text, re.DOTALL):
        paragraph = match.group(0).strip()
        if paragraph:
            yield paragraph, match.start()


def looks_like_expanded_acronym(text: str, acronym: str, offset: int) -> bool:
    before = text[max(0, offset - 160) : offset]
    after = text[offset + len(acronym) : offset + len(acronym) + 160]
    escaped = re.escape(acronym)

    if re.search(rf"\({escaped}\)", text[max(0, offset - 4) : offset + len(acronym) + 4]):
        # Acronym appears in parentheses after a plausible multi-word expansion.
        prefix = before.rsplit("(", 1)[0]
        return len(words(prefix[-100:])) >= 2

    if after.lstrip().startswith("(") and ")" in after[:120]:
        inside = after[after.find("(") + 1 : after.find(")")]
        if len(words(inside)) >= 2:
            return True

    # Search for an explicit “sigla X” or a prior parenthetical expansion.
    if re.search(rf"(?:sigla|abreviação)\s+{escaped}\b", before, re.IGNORECASE):
        return True
    if re.search(rf"\([^)]+\b{escaped}\b[^)]*\)", before + acronym, re.IGNORECASE):
        return True
    return False


def load_terms(path: str | None) -> dict[str, list[str]]:
    if not path:
        return {}
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("The terms file must be a JSON object: canonical term -> aliases array.")
    result: dict[str, list[str]] = {}
    for canonical, aliases in payload.items():
        if not isinstance(canonical, str) or not isinstance(aliases, list):
            raise ValueError("Invalid terms mapping.")
        result[canonical] = [str(item) for item in aliases]
    return result


def analyze(
    text: str,
    *,
    max_sentence_words: int,
    max_paragraph_words: int,
    terms: dict[str, list[str]],
) -> tuple[Metrics, list[Issue]]:
    normalized = normalize_markdown(text).rstrip()
    issues: list[Issue] = []

    sentence_lengths: list[int] = []
    long_sentence_count = 0
    for sentence, offset in iter_sentences(normalized):
        count = len(words(sentence))
        if count == 0:
            continue
        sentence_lengths.append(count)
        if count > max_sentence_words:
            long_sentence_count += 1
            severity = "high" if count > max(max_sentence_words + 15, 50) else "medium"
            issues.append(
                Issue(
                    severity,
                    "CL001",
                    line_number(normalized, offset),
                    f"Frase com {count} palavras; investigue dependências e orações encaixadas.",
                    excerpt(sentence),
                    "Separe proposições independentes, mas preserve condições e escopo técnico.",
                )
            )

    long_paragraph_count = 0
    for paragraph, offset in iter_paragraphs(normalized):
        if HEADING_RE.match(paragraph) or all(LIST_PREFIX_RE.match(line) for line in paragraph.splitlines() if line.strip()):
            continue
        count = len(words(paragraph))
        if count > max_paragraph_words:
            long_paragraph_count += 1
            issues.append(
                Issue(
                    "medium",
                    "CL002",
                    line_number(normalized, offset),
                    f"Parágrafo com {count} palavras e provável mistura de funções.",
                    excerpt(paragraph),
                    "Separe definição, mecanismo, exemplo, exceção ou ação em blocos próprios.",
                )
            )

    for pattern, suggestion in NOMINALIZATION_PATTERNS:
        for match in re.finditer(pattern, normalized, re.IGNORECASE):
            issues.append(
                Issue(
                    "low",
                    "CL003",
                    line_number(normalized, match.start()),
                    "Construção nominal pode esconder a ação principal.",
                    excerpt(match.group(0)),
                    suggestion,
                )
            )

    for match in PASSIVE_RE.finditer(normalized):
        issues.append(
            Issue(
                "low",
                "CL004",
                line_number(normalized, match.start()),
                "Construção passiva pode esconder responsabilidade.",
                excerpt(match.group(0)),
                "Nomeie o ator quando responsabilidade ou sequência importar.",
            )
        )

    for pattern, suggestion in VAGUE_PATTERNS:
        for match in re.finditer(pattern, normalized, re.IGNORECASE):
            issues.append(
                Issue(
                    "low",
                    "CL005",
                    line_number(normalized, match.start()),
                    "Expressão vaga pode impedir decisão ou execução consistente.",
                    excerpt(match.group(0)),
                    suggestion,
                )
            )

    lines = normalized.splitlines()
    running_offset = 0
    for line_index, line in enumerate(lines, start=1):
        if NUMBERED_STEP_RE.match(line):
            lower = line.lower()
            count = sum(1 for verb in IMPERATIVE_STEMS if re.search(rf"\b{re.escape(verb)}\b", lower))
            if count >= 2 and ("," in line or re.search(r"\s+e\s+", lower)):
                issues.append(
                    Issue(
                        "medium",
                        "CL006",
                        line_index,
                        f"Etapa procedural contém pelo menos {count} ações imperativas.",
                        excerpt(line),
                        "Separe ações que exigem decisão, verificação ou recuperação independentes.",
                    )
                )
        running_offset += len(line) + 1
    _ = running_offset

    first_occurrence: dict[str, int] = {}
    for match in ACRONYM_RE.finditer(normalized):
        acronym = match.group(0)
        if acronym in DEFAULT_ACRONYM_ALLOWLIST or acronym.isdigit():
            continue
        first_occurrence.setdefault(acronym, match.start())
    for acronym, offset in sorted(first_occurrence.items(), key=lambda item: item[1]):
        if not looks_like_expanded_acronym(normalized, acronym, offset):
            issues.append(
                Issue(
                    "low",
                    "CL007",
                    line_number(normalized, offset),
                    f"Sigla potencialmente não definida no primeiro uso: {acronym}.",
                    acronym,
                    "Expanda ou explique a sigla no primeiro uso relevante para a audiência.",
                )
            )

    for sentence, offset in iter_sentences(normalized):
        if PERCENT_RE.search(sentence):
            lower = sentence.lower()
            context_markers = (" de ", " para ", "ponto percentual", "em cada", "entre ", "base", "total")
            if not any(marker in lower for marker in context_markers):
                issues.append(
                    Issue(
                        "low",
                        "CL008",
                        line_number(normalized, offset),
                        "Percentual pode estar sem baseline, denominador ou comparação suficiente.",
                        excerpt(sentence),
                        "Informe valor inicial/final, denominador, período e diferença absoluta quando material.",
                    )
                )

    lowered = normalized.lower()
    for canonical, aliases in terms.items():
        variants = [canonical, *aliases]
        present = [term for term in variants if re.search(rf"(?<!\w){re.escape(term.lower())}(?!\w)", lowered)]
        if len(present) > 1:
            first = min(lowered.find(term.lower()) for term in present)
            issues.append(
                Issue(
                    "medium",
                    "CL009",
                    line_number(normalized, first),
                    f"Possível deriva terminológica para o conceito “{canonical}”: {', '.join(present)}.",
                    ", ".join(present),
                    "Use o termo canônico de forma consistente ou explique por que os termos representam papéis distintos.",
                )
            )

    # De-duplicate exact issue signatures.
    deduped: list[Issue] = []
    seen: set[tuple[str, str, int, str]] = set()
    for issue in sorted(issues, key=lambda item: (item.line, item.code, item.message)):
        signature = (issue.severity, issue.code, issue.line, issue.excerpt)
        if signature not in seen:
            deduped.append(issue)
            seen.add(signature)

    text_words = words(normalized)
    paragraph_count = sum(1 for _ in iter_paragraphs(normalized))
    heading_count = sum(1 for line in lines if HEADING_RE.match(line))
    list_item_count = sum(1 for line in lines if LIST_PREFIX_RE.match(line))
    metrics = Metrics(
        characters=len(normalized),
        words=len(text_words),
        sentences=len(sentence_lengths),
        paragraphs=paragraph_count,
        headings=heading_count,
        list_items=list_item_count,
        average_sentence_words=round(sum(sentence_lengths) / len(sentence_lengths), 2) if sentence_lengths else 0.0,
        maximum_sentence_words=max(sentence_lengths, default=0),
        long_sentences=long_sentence_count,
        long_paragraphs=long_paragraph_count,
    )
    return metrics, deduped


def format_text(source: str, metrics: Metrics, issues: Sequence[Issue]) -> str:
    counts = {severity: sum(issue.severity == severity for issue in issues) for severity in ("high", "medium", "low")}
    lines = [
        "CLARIFY LINT",
        f"Source: {source}",
        "",
        "Metrics:",
        f"  words: {metrics.words}",
        f"  sentences: {metrics.sentences}",
        f"  average sentence words: {metrics.average_sentence_words}",
        f"  maximum sentence words: {metrics.maximum_sentence_words}",
        f"  paragraphs: {metrics.paragraphs}",
        f"  headings: {metrics.headings}",
        f"  list items: {metrics.list_items}",
        "",
        f"Issues: {len(issues)} (high={counts['high']}, medium={counts['medium']}, low={counts['low']})",
    ]
    if not issues:
        lines.append("  No surface-level lint issues detected.")
    for issue in issues:
        lines.extend(
            [
                "",
                f"[{issue.severity.upper()}] {issue.code} — line {issue.line}",
                f"  {issue.message}",
                f"  Excerpt: {issue.excerpt}",
                f"  Suggestion: {issue.suggestion}",
            ]
        )
    lines.extend(
        [
            "",
            "Note: this linter cannot verify source fidelity, causal correctness, mental-model quality, or comprehension.",
        ]
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lint Brazilian-Portuguese content for surface clarity risks.")
    parser.add_argument("path", nargs="?", default="-", help="UTF-8 Markdown/text file or '-' for stdin.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when medium or high issues exist.")
    parser.add_argument("--max-sentence-words", type=int, default=35)
    parser.add_argument("--max-paragraph-words", type=int, default=120)
    parser.add_argument("--terms", help="JSON mapping canonical terms to aliases.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        text, source = read_text(args.path)
        term_map = load_terms(args.terms)
        metrics, issues = analyze(
            text,
            max_sentence_words=args.max_sentence_words,
            max_paragraph_words=args.max_paragraph_words,
            terms=term_map,
        )
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    if args.format == "json":
        payload = {
            "source": source,
            "metrics": asdict(metrics),
            "issues": [asdict(issue) for issue in issues],
            "limitations": [
                "Surface lint does not prove source fidelity.",
                "Surface lint does not prove comprehension or transfer.",
                "Heuristics may produce false positives and require semantic review.",
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(format_text(source, metrics, issues))

    if args.strict and any(issue.severity in {"high", "medium"} for issue in issues):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
