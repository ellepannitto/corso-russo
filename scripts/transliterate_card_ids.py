#!/usr/bin/env python3
"""Rigenera i card_id delle lezioni usando la traslitterazione della parola russa
al posto degli hash sha1 (es. cum-9e7f48584c -> kot)."""

import re
from pathlib import Path

ROOT = Path("/Users/ludovica/Documents/corso-russo")
LESSONS_DIR = ROOT / "lezioni"

TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "io",
    "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "h", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch",
    "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}


def lesson_number(path: Path) -> int:
    return int(path.name.removeprefix("lista"))


def transliterate(word: str) -> str:
    slug = "".join(TRANSLIT.get(ch, ch) for ch in word.lower())
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug


def build_id_map() -> dict[str, str]:
    """Un id per parola russa distinta, univoco su tutto il corpus."""
    seen_ru: dict[str, str] = {}
    used_ids: dict[str, int] = {}

    for path in sorted(LESSONS_DIR.glob("lista*"), key=lesson_number):
        for raw in path.read_text(encoding="utf-8").splitlines():
            if not raw.strip():
                continue
            fields = raw.split("\t")
            ru = fields[0]
            if ru in seen_ru:
                continue

            base = transliterate(ru) or "parola"
            count = used_ids.get(base, 0)
            new_id = base if count == 0 else f"{base}-{count + 1}"
            used_ids[base] = count + 1
            seen_ru[ru] = new_id

    return seen_ru


def migrate_file(path: Path, id_map: dict[str, str]) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    new_lines: list[str] = []
    changed = 0

    for raw in lines:
        if not raw.strip():
            new_lines.append(raw)
            continue

        fields = raw.split("\t")
        ru = fields[0]
        new_id = id_map[ru]

        if len(fields) == 4:
            ru, it, theme, old_id = fields
            if old_id == new_id:
                new_lines.append(raw)
                continue
            new_lines.append("\t".join([ru, it, theme, new_id]))
            changed += 1
        else:
            ru, it, theme = fields
            new_lines.append("\t".join([ru, it, theme, new_id]))
            changed += 1

    if changed:
        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    return changed


def main() -> None:
    id_map = build_id_map()
    total_changed = 0

    for path in sorted(LESSONS_DIR.glob("lista*"), key=lesson_number):
        changed = migrate_file(path, id_map)
        total_changed += changed
        if changed:
            print(f"{path.name}: {changed} id aggiornati")

    print(f"Totale: {total_changed} id aggiornati su {len(id_map)} parole distinte")


if __name__ == "__main__":
    main()
