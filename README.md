# Elektronik-Reparatur & Hardware-Diagnose – Wissensdatenbank & KI-Skill (`v2.0-DE`)

Vollständiges, verlustfrei auf Deutsch ausgearbeitetes Nachschlagewerk und mehrteiliger KI-Skill für **Elektronik-Reparatur auf Bauteilebene (`Component-Level Repair`)**, **In-Circuit-Messtechnik**, **Stromversorgungs- und Einschaltsequenz-Diagnose** sowie **Schaltplan-, Layout- und SMD-Code-Analyse**.

---

## 📂 Struktur der Wissensdatenbank (`skill_datenbank/`)

| Datei | Beschreibung |
|---|---|
| [skill_datenbank/00_INDEX_UND_KONTROLLLISTE.md](skill_datenbank/00_INDEX_UND_KONTROLLLISTE.md) | Vollständiges Quellen-Inventar aller ausgewerteten Repositories, Kapitel und Übertragungs-Status |
| [skill_datenbank/SKILL.md](skill_datenbank/SKILL.md) | Haupt-Regelwerk für die KI: Zwei-Ebenen-Anti-Halluzinations-Gesetz, 10 Simulator-Invarianten (`INV-1`–`INV-10`), zerstörungsfreie Prüf-Reihenfolge, Mechanik-/ESD-Schutz (monolithische EMK-Wägezellen), Hard-Safety-Substitution & Diagnose-Workflow |
| [skill_datenbank/01_In_Circuit_Messen_und_Bauteilpruefung.md](skill_datenbank/01_In_Circuit_Messen_und_Bauteilpruefung.md) | In-Circuit-Messphysik ($\Omega$ vs. Durchgang vs. Diodentest), Parallelschaltung, Ladekurven, `Red-Probe-on-Ground`, Prüftabellen (Sicherungen, Dioden/TVS, Widerstände inkl. kompletter EIA-96-Tabelle, MLCC/Elkos inkl. ESR-Richtwerttabelle, Spulen/Ferrite, BJT/MOSFET), Oszilloskop-/Logic-Analyzer-Praxis, Löt-Reihenfolge & IPC-A-610D |
| [skill_datenbank/02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](skill_datenbank/02_Stromversorgung_und_Einschaltsequenz_Diagnose.md) | 7-stufige Prüf-Kaskade vom Netzteil bis zur Logik, validierte Playbooks (`boot-no-power`, `pmic-rail-collapse`, `usb-no-charge`), Power Sequencing, Reset/Quarz/Watchdog/Boot-Schalter, 3 Thermal-Cascade-Archetypen, BGA-Lift-Protokoll, `leaky_short`-Formel, 38-zeilige `_PASSIVE_CASCADE_TABLE` & 50/50-Discriminator-Algorithmus |
| [skill_datenbank/03_Schaltplaene_Platinenlayout_und_SMD_Codes.md](skill_datenbank/03_Schaltplaene_Platinenlayout_und_SMD_Codes.md) | Schaltplanlesen & Reverse Engineering ohne Schaltplan, 15 kanonische Netz-Domänen, Topologie-Heuristiken zur Bauteil-Rollen-Erkennung, Masse-Konzepte (`AGND`/`DGND`/`PGND`/Sternpunkt), Impedanzformeln, Datenblatt-Analyse (`Absolute Maximum Ratings`, Derating, Temperaturklassen), SMD-Gehäuseformen & Datenblatt-Katalog (`smd-codebook.pdf`) |
| [skill_datenbank/KOMPLETTES_HANDBUCH_ELEKTRONIK_DIAGNOSE.md](skill_datenbank/KOMPLETTES_HANDBUCH_ELEKTRONIK_DIAGNOSE.md) | Verlustfreie Gesamtausgabe (Module `SKILL.md` + `01` bis `03`) in einer einzigen Master-Datei für NotebookLM / Gemini |
| [skill_datenbank/scripts/build_handbuch.py](skill_datenbank/scripts/build_handbuch.py) | Deterministischer Generator & Validator (`--check`, `--self-test`) für das Gesamthandbuch |
| [skill_datenbank/evals/cases.json](skill_datenbank/evals/cases.json) | Evaluations-Testfälle (Positiv-, Negativ- und Adversarial-Cases) |

---

## 🛠️ Quell-Repositories (`raw_sources/`) herunterladen

Um die vier Original-Quell-Repositories (`Junkz3/wrench-board`, `theEmbeddedGeorge/theEmbeddedNewTestament.github.io`, `aKaReZa75/Repair`, `Vitorbnc/electronics-datasheets` inkl. `smd-codebook.pdf`) lokal in `raw_sources/` bereitzustellen, führe im Projektverzeichnis folgendes PowerShell-Skript aus:

```powershell
.\setup_raw_sources.ps1
```

## ✅ Verifikation & Selbsttest

```bash
python skill_datenbank/scripts/build_handbuch.py --self-test
python skill_datenbank/scripts/build_handbuch.py --check
```
