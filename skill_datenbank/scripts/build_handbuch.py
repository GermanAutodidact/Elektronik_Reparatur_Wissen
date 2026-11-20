#!/usr/bin/env python3
"""Deterministischer Generator & Validator für KOMPLETTES_HANDBUCH_ELEKTRONIK_DIAGNOSE.md.

Führt SKILL.md (ohne YAML-Frontmatter) sowie die Fachmodule 01 bis 03 verlustfrei
zu einer Gesamtausgabe zusammen. Unterstützt --check und --self-test.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

sys.dont_write_bytecode = True

MODULES: list[tuple[str, str]] = [
    ("SKILL.md", "Teil 1: Haupt-Regelwerk für die KI (SKILL.md)"),
    ("01_In_Circuit_Messen_und_Bauteilpruefung.md", "Teil 2: In-Circuit-Messen, Bauteilprüfung, Oszilloskop-Praxis und Löttechnik"),
    ("02_Stromversorgung_und_Einschaltsequenz_Diagnose.md", "Teil 3: Stromversorgung, Einschaltsequenz-Diagnose und Hypothesen-Engine"),
    ("03_Schaltplaene_Platinenlayout_und_SMD_Codes.md", "Teil 4: Schaltpläne, Platinenlayout, Datenblätter, Netz-Klassifikation und SMD-Codes"),
]

TARGET_NAME = "KOMPLETTES_HANDBUCH_ELEKTRONIK_DIAGNOSE.md"


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        return re.sub(r"^---\n.*?\n---\n+", "", text, count=1, flags=re.S)
    return text


def strip_auto_toc(text: str) -> str:
    return re.sub(
        r"<!--\s*TOC\s*START\s*-->.*?<!--\s*TOC\s*END\s*-->\n*",
        "",
        text,
        flags=re.S,
    )


def build_handbook_text(skill_dir: pathlib.Path) -> str:
    header = [
        "# KOMPLETTES HANDBUCH: Elektronik-Reparatur und Hardware-Diagnose\n\n",
        "> **Master-Ausgabe** – Vollständige, verlustfreie Zusammenführung aller ausgearbeiteten Module ([SKILL.md](SKILL.md) + Module `01` bis `03`) für NotebookLM, Gemini oder die Offline-Werkstatt.\n\n",
        "---\n\n",
    ]
    blocks: list[str] = []
    for filename, _title in MODULES:
        path = skill_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Pflichtmodul fehlt: {path}")
        raw = path.read_text(encoding="utf-8")
        cleaned = strip_auto_toc(strip_frontmatter(raw)).strip()
        blocks.append(cleaned + "\n")
    return "".join(header) + "\n---\n\n".join(blocks)


def run_self_test(skill_dir: pathlib.Path) -> int:
    required = ["00_INDEX_UND_KONTROLLLISTE.md"] + [m[0] for m in MODULES]
    for req in required:
        p = skill_dir / req
        if not p.exists() or p.stat().st_size < 1000:
            print(f"[FAIL] Datei fehlt oder ist zu klein: {p}", file=sys.stderr)
            return 1
    rendered = build_handbook_text(skill_dir)
    for token in ("INV-10", "EIA-96", "_PASSIVE_CASCADE_TABLE", "smd-codebook.pdf"):
        if token not in rendered:
            print(f"[FAIL] Pflicht-Fachbegriff '{token}' fehlt im generierten Handbuch!", file=sys.stderr)
            return 1
    print(f"[OK] Self-Test erfolgreich ({len(rendered)} Zeichen validiert).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Erzeugt KOMPLETTES_HANDBUCH_ELEKTRONIK_DIAGNOSE.md")
    parser.add_argument("--check", action="store_true", help="Prüft nur, ob das Handbuch aktuell ist")
    parser.add_argument("--self-test", action="store_true", help="Führt den internen Selbsttest aus")
    args = parser.parse_args()

    skill_dir = pathlib.Path(__file__).resolve().parent.parent
    if args.self_test:
        return run_self_test(skill_dir)

    expected = build_handbook_text(skill_dir)
    target = skill_dir / TARGET_NAME

    if args.check:
        if not target.exists():
            print(f"[FAIL] {target} existiert nicht.", file=sys.stderr)
            return 1
        current = strip_auto_toc(target.read_text(encoding="utf-8"))
        if current.strip() != expected.strip():
            print(f"[FAIL] {target} ist nicht synchron mit den Einzelmodulen.", file=sys.stderr)
            return 1
        print(f"[OK] {TARGET_NAME} ist synchron.")
        return 0

    target.write_text(expected, encoding="utf-8")
    print(f"[OK] {target} geschrieben ({len(expected)} Zeichen).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
