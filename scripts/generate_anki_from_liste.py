#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import html
import hashlib
import io
import re
import sqlite3
import textwrap
import zipfile
from pathlib import Path

import genanki


ROOT = Path("/Users/ludovica/Documents/corso-russo")
LESSONS_DIR = ROOT / "lezioni"
APKG_OUTPUT = ROOT / "anki" / "russo.apkg"
IMPORT_OUTPUT = ROOT / "anki" / "vocabolario-completo.tsv"
IMPORT_HEADER = [
    "#separator:tab",
    "#html:true",
    "#notetype:Russo",
    "#deck:Russo",
    "#tags column:6",
]

MODEL_ID = int(hashlib.sha1(b"Russo v2").hexdigest()[:8], 16)
DECK_ID = int(hashlib.sha1(b"Russo deck v1").hexdigest()[:8], 16)

# Campi, nome e template del tipo di nota sono gli stessi dell'import da TSV:
# template e stile si leggono da anki/template-carte.html (unica fonte).
NOTE_TYPE_NAME = "Russo"
FIELDS = ["ID", "Russo", "Italiano", "FraseRusso", "FraseItaliano"]
TEMPLATE_FILE = Path(__file__).resolve().parent.parent / "anki" / "template-carte.html"
CARD_TYPES = [
    ("Russo → Italiano", "russo-italiano"),
    ("Italiano → Russo", "italiano-russo"),
    ("Frase → Traduzione", "frase-traduzione"),
]


def load_card_templates(path: Path = TEMPLATE_FILE) -> tuple[list[dict[str, str]], str]:
    """Legge fronti, retri e stile dal file di template condiviso con la guida TSV."""
    source = path.read_text(encoding="utf-8")
    blocks = {
        match.group(1): textwrap.dedent(match.group(2)).strip()
        for match in re.finditer(r'<template id="([^"]+)">(.*?)</template>', source, re.DOTALL)
    }
    style = re.search(r"^\s*<style>\n(.*?)^\s*</style>", source, re.DOTALL | re.MULTILINE)
    if not style:
        raise ValueError(f"{path}: blocco <style> mancante")
    templates = []
    for name, prefix in CARD_TYPES:
        try:
            templates.append({"name": name, "qfmt": blocks[f"{prefix}-fronte"], "afmt": blocks[f"{prefix}-retro"]})
        except KeyError as error:
            raise ValueError(f"{path}: template {error.args[0]!r} mancante") from error
    return templates, textwrap.dedent(style.group(1)).strip()


_TEMPLATES, _CSS = load_card_templates()

RUSSO_MODEL = genanki.Model(
    MODEL_ID,
    NOTE_TYPE_NAME,
    fields=[{"name": name} for name in FIELDS],
    templates=_TEMPLATES,
    css=_CSS,
    sort_field_index=FIELDS.index("Russo"),
)


BOLD_RE = re.compile(r"<b>(.*?)</b>", re.DOTALL)


def stable_id(word: str) -> str:
    digest = hashlib.sha1(word.encode("utf-8")).hexdigest()[:10]
    return f"cum-{digest}"


def lesson_label(path: Path) -> str:
    """Etichetta della lezione usata nel tag `lez-...`.

    `lista7` -> "7", `lista21bis.tsv` -> "21bis", `seminario_morte.tsv` -> "seminario_morte".
    """
    stem = path.name.removesuffix(".tsv")
    return stem.removeprefix("lista") if stem.startswith("lista") else stem


def lesson_sort_key(path: Path) -> tuple:
    """Prima le liste numerate (in ordine numerico), poi gli altri file in ordine alfabetico."""
    label = lesson_label(path)
    match = re.match(r"(\d+)(.*)", label) if path.name.startswith("lista") else None
    if match:
        return (0, int(match.group(1)), match.group(2))
    return (1, 0, label)


def _label_sort_key(label: str) -> tuple:
    match = re.match(r"(\d+)(.*)", label)
    return (0, int(match.group(1)), match.group(2)) if match else (1, 0, label)


def lesson_files() -> list[Path]:
    """File di vocabolario in lezioni/: `lista*` e `*.tsv` (esclusi gli appunti senza estensione, come `extra`)."""
    paths = {
        path
        for pattern in ("lista*", "*.tsv")
        for path in LESSONS_DIR.glob(pattern)
        if path.is_file() and not path.name.startswith(".")
    }
    return sorted(paths, key=lesson_sort_key)


def is_header(raw: str) -> bool:
    return raw.split("\t")[0].strip().lower() == "russo"


def parse_row(raw: str, path: Path, line_number: int) -> tuple[str, str, str, str | None, str, str]:
    fields = raw.split("\t")

    if len(fields) == 3:
        ru, it, theme = fields
        return ru, it, theme, None, "", ""

    if len(fields) == 4:
        ru, it, theme, card_id = fields
        if not card_id.strip():
            raise ValueError(f"{path}:{line_number}: card_id vuoto")
        return ru, it, theme, card_id, "", ""

    if len(fields) == 6:
        ru, it, theme, card_id, example_ru, example_it = fields
        if not card_id.strip():
            raise ValueError(f"{path}:{line_number}: card_id vuoto")
        if not example_ru.strip() or not example_it.strip():
            raise ValueError(f"{path}:{line_number}: frase russa e traduzione sono obbligatorie")
        return ru, it, theme, card_id, example_ru, example_it

    raise ValueError(
        f"{path}:{line_number}: attese 3, 4 o 6 colonne, trovate {len(fields)}"
    )


def highlight_word(sentence: str, word: str) -> str:
    """Render explicit **targets**, or highlight the exact headword automatically.

    Explicit targets handle inflections and ambiguous words without guessing.
    All source text is escaped; only the generated highlight spans are HTML.
    """
    if not sentence:
        return ""

    def span(text: str) -> str:
        return f'<span class="target-word">{html.escape(text)}</span>'

    if "**" not in sentence and ("<b>" in sentence or "</b>" in sentence):
        # Forma esplicita con <b>...</b>, usata nei file delle lezioni.
        if "<b>" in BOLD_RE.sub("", sentence) or "</b>" in BOLD_RE.sub("", sentence):
            raise ValueError("tag <b> non bilanciati nella frase")
        result = []
        end = 0
        for match in BOLD_RE.finditer(sentence):
            target = match.group(1)
            if not target.strip() or target != target.strip():
                raise ValueError("testo evidenziato vuoto o con spazi ai bordi")
            result.extend([html.escape(sentence[end:match.start()]), span(target)])
            end = match.end()
        result.append(html.escape(sentence[end:]))
        return "".join(result)

    if "**" in sentence:
        parts = sentence.split("**")
        if len(parts) % 2 == 0 or "***" in sentence:
            raise ValueError("marcatori ** non bilanciati o ambigui nella frase")
        if any(not part.strip() or part != part.strip() for part in parts[1::2]):
            raise ValueError("testo evidenziato vuoto o con spazi ai bordi")
        return "".join(span(part) if i % 2 else html.escape(part)
                       for i, part in enumerate(parts))

    # In headwords such as 'сколько стоит?', '?' is not part of the expression.
    target = word.rstrip("?!.,…")
    if not target:
        raise ValueError("lemma vuoto per l'evidenziazione")
    pattern = re.compile(rf"(?<!\w){re.escape(target)}(?!\w)", re.IGNORECASE)
    matches = list(pattern.finditer(sentence))
    if not matches:
        raise ValueError(
            f"nessuna occorrenza di {word!r}: indica la forma nella frase con **...**"
        )
    result = []
    end = 0
    for match in matches:
        result.extend([html.escape(sentence[end:match.start()]), span(match.group())])
        end = match.end()
    result.append(html.escape(sentence[end:]))
    return "".join(result)


def _fix_apkg_user_version(apkg_path: Path) -> None:
    """Set SQLite user_version=11 so newer AnkiDroid (Rust backend) can import the file."""
    with zipfile.ZipFile(apkg_path, "r") as zin:
        names = zin.namelist()
        db_name = "collection.anki21" if "collection.anki21" in names else "collection.anki2"
        db_bytes = zin.read(db_name)
        other_files = {n: zin.read(n) for n in names if n != db_name}

    db_path = apkg_path.parent / "_tmp_collection.anki2"
    db_path.write_bytes(db_bytes)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA user_version = 11")
    conn.commit()
    conn.close()

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zout:
        zout.write(db_path, db_name)
        for name, data in other_files.items():
            zout.writestr(name, data)
    db_path.unlink()
    apkg_path.write_bytes(buf.getvalue())


def collect_notes() -> dict[str, dict[str, object]]:
    """Legge tutte le liste e unisce le righe con lo stesso ID in un'unica nota."""
    by_note: dict[str, dict[str, object]] = {}

    for path in lesson_files():
        lesson = lesson_label(path)

        for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not raw.strip() or (line_number == 1 and is_header(raw)):
                continue

            ru, it, theme, explicit_id, example_ru, example_it = parse_row(raw, path, line_number)
            # Validate every example before opening/replacing either output file.
            try:
                example_ru = highlight_word(example_ru, ru)
            except ValueError as error:
                raise ValueError(f"{path}:{line_number}: {error}") from error
            note_key = explicit_id or ru
            entry = by_note.setdefault(
                note_key,
                {
                    "id": explicit_id or stable_id(ru),
                    "russian": ru,
                    "italian": [],
                    "examples": [],
                    "themes": set(),
                    "lessons": set(),
                },
            )

            if entry["russian"] != ru:
                raise ValueError(
                    f"{path}:{line_number}: la nota '{note_key}' ha piu' front diversi: "
                    f"{entry['russian']!r} e {ru!r}"
                )

            italian = entry["italian"]
            if it not in italian:
                italian.append(it)
            if example_ru and (example_ru, example_it) not in entry["examples"]:
                entry["examples"].append((example_ru, example_it))
            # La colonna categoria puo' contenere piu' temi separati da virgola
            # (es. "verbi,cibo-e-bevande"): ognuno diventa un tag.
            entry["themes"].update(t.strip() for t in theme.split(",") if t.strip())
            entry["lessons"].add(lesson)

    return by_note


def note_tags(entry: dict[str, object]) -> list[str]:
    theme_tags = sorted(entry["themes"])
    lesson_tags = [f"lez-{lesson}" for lesson in sorted(entry["lessons"], key=_label_sort_key)]
    return theme_tags + lesson_tags


def note_fields(entry: dict[str, object]) -> list[str]:
    """Valori dei campi, nell'ordine di FIELDS: ID, Russo, Italiano, FraseRusso, FraseItaliano."""
    # Una sola frase per nota: se la parola ha più esempi (da liste diverse)
    # si tiene il primo, così sulla carta frase e traduzione restano abbinate.
    example_ru, example_it = entry["examples"][0] if entry["examples"] else ("", "")
    return [
        entry["id"],
        entry["russian"],
        " / ".join(entry["italian"]),
        example_ru,
        html.escape(example_it),
    ]


def write_import_tsv(by_note: dict[str, dict[str, object]], path: Path = IMPORT_OUTPUT) -> None:
    """TSV pronto per l'import in Anki (senza apkg): una riga per nota, con direttive di intestazione.

    Colonne: ID, Russo, Italiano, FraseRusso, FraseItaliano, Tags. La riga senza frase
    ha le due colonne della frase vuote: il tipo di nota genera solo le prime due carte.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\n".join(IMPORT_HEADER) + "\n")
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        for entry in sorted(by_note.values(), key=lambda e: (e["russian"].lower(), e["id"])):
            writer.writerow(note_fields(entry) + [" ".join(note_tags(entry))])
    print(f"{path.name}: {len(by_note)} note")


def main() -> None:
    """Genera il pacchetto russo.apkg (stesso tipo di nota dell'import da TSV)."""
    by_note = collect_notes()
    deck = genanki.Deck(DECK_ID, "Russo")

    for entry in sorted(by_note.values(), key=lambda e: (e["russian"].lower(), e["id"])):
        deck.add_note(genanki.Note(
            model=RUSSO_MODEL,
            fields=note_fields(entry),
            tags=note_tags(entry),
            guid=entry["id"],
        ))

    APKG_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(deck).write_to_file(APKG_OUTPUT)
    _fix_apkg_user_version(APKG_OUTPUT)
    print(f"{APKG_OUTPUT.name}: {len(deck.notes)} note, 3 template (russo→italiano, italiano→russo, frase→traduzione)")


def cli(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Genera i file Anki dalle liste in lezioni/.")
    parser.add_argument(
        "--solo-tsv",
        action="store_true",
        help="genera solo anki/vocabolario-completo.tsv (per l'import da TSV), senza toccare russo.apkg",
    )
    args = parser.parse_args(argv)
    if args.solo_tsv:
        write_import_tsv(collect_notes())
        return
    main()
    write_import_tsv(collect_notes())


if __name__ == "__main__":
    cli()
