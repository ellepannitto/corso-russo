#!/usr/bin/env python3

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path("/Users/ludovica/Documents/corso-russo")
LESSONS_DIR = ROOT / "lezioni"
DEFAULT_SOURCES = [
    ROOT / "anki" / "A1.tsv",
    ROOT / "anki" / "vocabolario.tsv",
]


def lesson_number(path: Path) -> int:
    return int(path.name.removeprefix("lista"))


def choose_source(explicit_source: str | None) -> Path:
    if explicit_source:
        return Path(explicit_source)

    for candidate in DEFAULT_SOURCES:
        if candidate.exists():
            return candidate

    raise FileNotFoundError("Nessun TSV sorgente trovato in anki/")


def stable_id(word: str) -> str:
    digest = hashlib.sha1(word.encode("utf-8")).hexdigest()[:10]
    return f"cum-{digest}"


def load_id_map(source: Path) -> tuple[dict[str, str], set[str]]:
    by_front: dict[str, str] = {}
    ambiguous: set[str] = set()

    with source.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            card_id = (row.get("ID") or "").strip()
            front = (row.get("Front") or "").strip()
            if not card_id or not front:
                continue

            previous = by_front.get(front)
            if previous and previous != card_id:
                ambiguous.add(front)
                continue

            by_front[front] = card_id

    for front in ambiguous:
        by_front.pop(front, None)

    return by_front, ambiguous


def migrate_file(path: Path, id_map: dict[str, str], fill_missing: bool) -> dict[str, object]:
    lines = path.read_text(encoding="utf-8").splitlines()
    new_lines: list[str] = []
    changed = 0
    preserved = 0
    filled = 0
    missing: list[tuple[int, str]] = []
    invalid: list[tuple[int, int]] = []

    for line_number, raw in enumerate(lines, start=1):
        if not raw.strip():
            new_lines.append(raw)
            continue

        fields = raw.split("\t")

        if len(fields) == 4:
            preserved += 1
            new_lines.append(raw)
            continue

        if len(fields) != 3:
            invalid.append((line_number, len(fields)))
            new_lines.append(raw)
            continue

        front, back, theme = fields
        card_id = id_map.get(front)
        if not card_id:
            if fill_missing:
                card_id = stable_id(front)
                new_lines.append("\t".join([front, back, theme, card_id]))
                filled += 1
                changed += 1
                continue
            missing.append((line_number, front))
            new_lines.append(raw)
            continue

        new_lines.append("\t".join([front, back, theme, card_id]))
        changed += 1

    if changed:
        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    return {
        "changed": changed,
        "preserved": preserved,
        "filled": filled,
        "missing": missing,
        "invalid": invalid,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aggiunge card_id alle lezioni usando un TSV Anki esistente."
    )
    parser.add_argument(
        "--source",
        help="TSV sorgente con colonne ID e Front. Default: anki/A1.tsv, poi anki/vocabolario.tsv",
    )
    parser.add_argument(
        "--fill-missing",
        action="store_true",
        help="Assegna un card_id generato ai termini senza match nel TSV sorgente.",
    )
    args = parser.parse_args()

    source = choose_source(args.source)
    id_map, ambiguous_fronts = load_id_map(source)

    total_changed = 0
    total_preserved = 0
    total_filled = 0
    total_missing = 0
    total_invalid = 0

    print(f"Sorgente: {source}")
    print(f"Front univoci caricati: {len(id_map)}")
    if ambiguous_fronts:
        print(f"Front ambigui ignorati nel TSV sorgente: {len(ambiguous_fronts)}")

    for path in sorted(LESSONS_DIR.glob("lista*"), key=lesson_number):
        result = migrate_file(path, id_map, args.fill_missing)
        total_changed += int(result["changed"])
        total_preserved += int(result["preserved"])
        total_filled += int(result["filled"])
        total_missing += len(result["missing"])
        total_invalid += len(result["invalid"])

        if (
            result["changed"]
            or result["preserved"]
            or result["missing"]
            or result["invalid"]
        ):
            print(
                f"{path.name}: aggiunte={result['changed']} gia_presenti={result['preserved']} "
                f"riempiti={result['filled']} senza_match={len(result['missing'])} "
                f"formato_non_valido={len(result['invalid'])}"
            )

        for line_number, field_count in result["invalid"]:
            print(f"  - {path.name}:{line_number}: {field_count} colonne")

        for line_number, front in result["missing"][:10]:
            print(f"  - {path.name}:{line_number}: nessun ID trovato per {front!r}")
        if len(result["missing"]) > 10:
            print(f"  - {path.name}: altri {len(result['missing']) - 10} senza match")

    print(
        f"Totale: aggiunte={total_changed} gia_presenti={total_preserved} "
        f"riempiti={total_filled} senza_match={total_missing} formato_non_valido={total_invalid}"
    )


if __name__ == "__main__":
    main()
