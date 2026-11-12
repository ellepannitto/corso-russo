#!/usr/bin/env python3

import csv
import re
import unicodedata
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path("/Users/ludovica/Documents/corso-russo")
SOURCE_XLSX = ROOT / "vocabolario_italiano_russo_completo.xlsx"
OUTPUT_DIR = ROOT / "anki"

NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return slug or "voce"


def cell_value(cell: ET.Element) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(".//a:t", NS)).strip()
    value = cell.find("a:v", NS)
    return (value.text or "").strip() if value is not None else ""


def worksheet_rows(zf: zipfile.ZipFile, sheet_path: str) -> list[list[str]]:
    root = ET.fromstring(zf.read(sheet_path))
    rows = []
    for row in root.findall(".//a:sheetData/a:row", NS):
        values = [cell_value(cell) for cell in row.findall("a:c", NS)]
        if any(values):
            rows.append(values)
    return rows


def workbook_sheets(zf: zipfile.ZipFile) -> list[tuple[str, str]]:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}

    sheets = []
    for sheet in workbook.find("a:sheets", NS):
        name = sheet.attrib["name"]
        rel_id = sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
        target = rel_map[rel_id]
        if target.startswith("/"):
            target = target.lstrip("/")
        elif not target.startswith("xl/"):
            target = f"xl/{target}"
        sheets.append((name, target))
    return sheets


def build_records(theme_name: str, rows: list[list[str]]) -> list[list[str]]:
    data_rows = rows[1:] if rows and rows[0][:2] == ["Italiano", "Russo"] else rows
    theme_slug = slugify(theme_name)
    records = []

    for idx, row in enumerate(data_rows, start=1):
        italiano = row[0].strip() if len(row) > 0 else ""
        russo = row[1].strip() if len(row) > 1 else ""
        if not italiano or not russo:
            continue

        note = ""
        tags = theme_slug
        record_id = f"{theme_slug}-{idx:03d}-{slugify(italiano)[:40]}".strip("-")
        records.append([record_id, russo, italiano, note, tags])

    return records


def write_tsv(path: Path, records: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["ID", "Front", "Back", "Notes", "Tags"])
        writer.writerows(records)


def main() -> None:
    with zipfile.ZipFile(SOURCE_XLSX) as zf:
        sheets = workbook_sheets(zf)
        for index, (theme_name, sheet_path) in enumerate(sheets, start=1):
            rows = worksheet_rows(zf, sheet_path)
            records = build_records(theme_name, rows)
            output_name = f"{index:02d}-{slugify(theme_name)}.tsv"
            write_tsv(OUTPUT_DIR / output_name, records)
            print(f"{output_name}: {len(records)} carte")


if __name__ == "__main__":
    main()
