# KOMPLETTES HANDBUCH: Elektronik-Reparatur und Hardware-Diagnose

> **Master-Ausgabe** – Vollständige, verlustfreie Zusammenführung aller ausgearbeiteten Module ([SKILL.md](SKILL.md) + Module `01` bis `03`) für NotebookLM, Gemini oder die Offline-Werkstatt.

---

# SKILL.md – Haupt-Regelwerk für Elektronik-Reparatur und Hardware-Diagnose

Dieses Regelwerk definiert die verbindlichen Arbeitsgesetze für die KI-gestützte Elektronik-Diagnose und Reparatur auf Bauteilebene (`Board-Level` / `Component-Level Repair`). Es vereint die deterministische Diagnose-Architektur aus `raw_sources/wrench-board/` mit den Hardware-Grundlagen aus `raw_sources/theEmbeddedNewTestament.github.io/`, `raw_sources/Repair/` und `raw_sources/electronics-datasheets/`.

---

<!-- TOC_START -->
## Inhaltsverzeichnis & Zeilen-Index

| Abschnitt | Ebene | Zeilen |
| :--- | :--- | :---: |
| [1. Modul-Router & Aufbau der Wissensdatenbank](#sec-1) | Hauptabschnitt | Z. 102–113 |
| [2. Das Anti-Halluzinations-Gesetz (Zwei-Ebenen-Verteidigung)](#sec-2) | Hauptabschnitt | Z. 115–116 |
| ↳ [2.1 Strikte Verifikationspflicht für Bauteilbezeichnungen (`RefDes`) und Pinouts](#sec-3) | Unterabschnitt | Z. 118–132 |
| ↳ [2.2 Evidence-Gating, Resolution-Kategorien & Konfidenz-Skala (`raw_sources/wrench-board/api/pipeline/prompts.py`)](#sec-4) | Unterabschnitt | Z. 134–149 |
| ↳ [2.3 Die 10 universellen Simulator-Invarianten (`raw_sources/wrench-board/benchmark/weaknesses.md`)](#sec-5) | Unterabschnitt | Z. 151–168 |
| [3. Zerstörungsfreie Prüf-Reihenfolge (Außen vor Innen)](#sec-6) | Hauptabschnitt | Z. 170–189 |
| [4. Mechanik-, ESD- & Elektrischer Sicherheitsschutz zuerst](#sec-7) | Hauptabschnitt | Z. 191–192 |
| ↳ [4.1 Mechanischer Schutz bei Präzisionsmessgeräten (Fein- & Analysenwaagen / EMK-Zellen)](#sec-8) | Unterabschnitt | Z. 194–199 |
| ↳ [4.2 ESD-Schutz (Elektrostatische Entladung)](#sec-9) | Unterabschnitt | Z. 201–204 |
| ↳ [4.3 Elektrische Sicherheit (IEC 61010) & Kondensatorentladung](#sec-10) | Unterabschnitt | Z. 206–212 |
| [5. Werkstatt-Logik vor Handbuch-Theorie & Ersatzteil-Sicherheit](#sec-11) | Hauptabschnitt | Z. 214–215 |
| ↳ [5.1 Reparatur auf Bauteilebene statt Baugruppentausch](#sec-12) | Unterabschnitt | Z. 217–220 |
| ↳ [5.2 Hard Safety Filter für Bauteil-Substitution (`raw_sources/wrench-board/api/stock/safety.py`)](#sec-13) | Unterabschnitt | Z. 222–237 |
| [6. Verbindlicher Diagnose- & Mess-Workflow (`raw_sources/wrench-board/api/agent/manifest.py`)](#sec-14) | Hauptabschnitt | Z. 239–240 |
| ↳ [6.1 Diagnosekette & Hypothesen-Auswertung (`HYPOTHESIZE`)](#sec-15) | Unterabschnitt | Z. 242–248 |
| ↳ [6.2 Präzise Messanweisungen (`MEASURE-TARGET` & `ANTI-GENERIC`)](#sec-16) | Unterabschnitt | Z. 250–256 |
| ↳ [6.3 Bench Anti-Patterns (`raw_sources/wrench-board/api/agent/seed_data/global_patterns/anti-patterns-bench.md`)](#sec-17) | Unterabschnitt | Z. 258–273 |
| [1. Physik und Messmodi des Multimeters In-Circuit](#sec-18) | Hauptabschnitt | Z. 275–276 |
| ↳ [1.1 Widerstandsmessung ($\Omega$) vs. Durchgangsprüfung vs. Diodentest](#sec-19) | Unterabschnitt | Z. 278–285 |
| ↳ [1.2 Einflüsse der Schaltungsumgebung (Parallelschaltung, Ladekurven, Restladung)](#sec-20) | Unterabschnitt | Z. 287–294 |
| ↳ [1.3 Relativmessung gegen Masse (`Red-Probe-on-Ground` / Dioden-Signatur)](#sec-21) | Unterabschnitt | Z. 296–307 |
| [2. Exakte Prüftabellen für alle Bauteilklassen In-Circuit](#sec-22) | Hauptabschnitt | Z. 309–310 |
| ↳ [2.1 SMD-Sicherungen (`F`) & Polyswitches (`PPTC`)](#sec-23) | Unterabschnitt | Z. 312–328 |
| ↳ [2.2 Dioden, Gleichrichter, Schottky-, Zener- & TVS-Schutzdioden](#sec-24) | Unterabschnitt | Z. 330–343 |
| ↳ [2.3 Widerstände (SMD & THT) & vollständige Code-Entschlüsselung](#sec-25) | Unterabschnitt | Z. 345–389 |
| ↳ [2.4 Keramikkondensatoren (`MLCC`) & Elektrolytkondensatoren (`Elko` / `Tantal` / `Polymer`)](#sec-26) | Unterabschnitt | Z. 391–425 |
| ↳ [2.5 Spulen, Induktivitäten (`L`), Ferritperlen (`FB`) & Übertrager](#sec-27) | Unterabschnitt | Z. 427–436 |
| ↳ [2.6 Bipolartransistoren (`BJT`: NPN / PNP) & MOSFETs (N-Kanal / P-Kanal)](#sec-28) | Unterabschnitt | Z. 438–462 |
| [3. Oszilloskop-, Logic-Analyzer- & I/O-Diagnose In-Circuit](#sec-29) | Hauptabschnitt | Z. 464–465 |
| ↳ [3.1 Oszilloskop-Regeln & Formeln (`raw_sources/theEmbeddedNewTestament.github.io/Debugging/Oscilloscope_Measurements.md`)](#sec-30) | Unterabschnitt | Z. 467–482 |
| ↳ [3.2 Logic Analyzer & Digitale Bus-Prüfung (`raw_sources/theEmbeddedNewTestament.github.io/Debugging/Logic_Analyzer_Usage.md`, `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Digital_IO_Programming.md`, `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Analog_IO.md`)](#sec-31) | Unterabschnitt | Z. 484–494 |
| [4. Löttechnik, Sektionale Inbetriebnahme & Fallstudien (`aKaReZa75/Repair`)](#sec-32) | Hauptabschnitt | Z. 496–497 |
| ↳ [4.1 Sektionale Bestückungs- & Prüf-Reihenfolge (`raw_sources/Repair/Videos.md`)](#sec-33) | Unterabschnitt | Z. 499–505 |
| ↳ [4.2 Lötwerkzeuge, Temperaturprofile & IPC-A-610D-Qualität (`raw_sources/Repair/Soldering_Tools.md` & `raw_sources/Repair/aKaReZa 38 - Repair, Soldering Tools/IPC-A-610D.pdf`)](#sec-34) | Unterabschnitt | Z. 507–519 |
| ↳ [4.3 Reparatur-Fallstudie: Defektes Multimeter (`Victor VC97` / EEPROM-Diagnose aus `raw_sources/Repair/Videos.md`)](#sec-35) | Unterabschnitt | Z. 521–535 |
| [1. Die feste 7-stufige Prüf-Kaskade vom Eingang zur Logik](#sec-36) | Hauptabschnitt | Z. 537–540 |
| ↳ [Stufe 1: Externes Netzteil / Batterie](#sec-37) | Unterabschnitt | Z. 542–545 |
| ↳ [Stufe 2: Eingangsbuchse, Steckverbinder & Netzschalter](#sec-38) | Unterabschnitt | Z. 547–550 |
| ↳ [Stufe 3: Eingangsfilter, Verpolungs- & Überspannungsschutz](#sec-39) | Unterabschnitt | Z. 552–559 |
| ↳ [Stufe 4: Haupt-Spannungsschiene ($V_{\text{IN}}$ / $V_{\text{BUS}}$ / $V_{\text{MAIN}}$ / $V_{\text{BAT}}$)](#sec-40) | Unterabschnitt | Z. 561–566 |
| ↳ [Stufe 5: Linearregler (`LDO` / Standard-Regler wie `78xx`, `LM317`, `AMS1117`)](#sec-41) | Unterabschnitt | Z. 568–576 |
| ↳ [Stufe 6: Schaltregler (`Buck`, `Boost`, `Buck-Boost`, `Flyback`, `PMIC`)](#sec-42) | Unterabschnitt | Z. 578–589 |
| ↳ [Stufe 7: Stützkondensatoren, Filter-Ferrite & Übergang zur Logik](#sec-43) | Unterabschnitt | Z. 591–595 |
| [2. Validierte Diagnose-Playbooks (`raw_sources/wrench-board/api/agent/seed_data/global_playbooks/`)](#sec-44) | Hauptabschnitt | Z. 597–598 |
| ↳ [2.1 Playbook `boot-no-power` (Gerät lässt sich nicht einschalten / Tot)](#sec-45) | Unterabschnitt | Z. 600–611 |
| ↳ [2.2 Playbook `pmic-rail-collapse` (Schiene bricht unter Last ein / Boot-Loop / Reset)](#sec-46) | Unterabschnitt | Z. 613–622 |
| ↳ [2.3 Playbook `usb-no-charge` (Kein Ladestrom über USB)](#sec-47) | Unterabschnitt | Z. 624–635 |
| [3. Power Sequencing, Reset-, Watchdog-, Takt- & Boot-Architektur](#sec-48) | Hauptabschnitt | Z. 637–638 |
| ↳ [3.1 Boot-Phasen-Klassifikation (`raw_sources/wrench-board/api/pipeline/schematic/boot_analyzer.py`)](#sec-49) | Unterabschnitt | Z. 640–645 |
| ↳ [3.2 Reset-Management & Watchdog-Timer (`raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Reset_Management.md` & `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Watchdog_Timers.md`)](#sec-50) | Unterabschnitt | Z. 647–655 |
| ↳ [3.3 Takterzeugung (`raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Clock_Management.md` & `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Clock_Distribution.md`)](#sec-51) | Unterabschnitt | Z. 657–663 |
| ↳ [3.4 Boot-Pins, Strapping-Widerstände & Service-/Flash-Schalter](#sec-52) | Unterabschnitt | Z. 665–670 |
| [4. Thermische Fehlerkaskaden & BGA-Lift-Diagnose](#sec-53) | Hauptabschnitt | Z. 672–673 |
| ↳ [4.1 Die 3 Thermal-Cascade-Archetypen (`raw_sources/wrench-board/api/agent/seed_data/global_patterns/thermal-cascades.md`)](#sec-54) | Unterabschnitt | Z. 675–685 |
| ↳ [4.2 BGA-Lift-Archetyp (Abgerissene Lötkugeln unter BGA-ICs) (`raw_sources/wrench-board/api/agent/seed_data/global_patterns/bga-lift-archetype.md`)](#sec-55) | Unterabschnitt | Z. 687–700 |
| [5. Deterministische Simulations- & Hypothesen-Engine (`raw_sources/wrench-board/api/pipeline/schematic/simulator.py` & `raw_sources/wrench-board/api/pipeline/schematic/hypothesize.py`)](#sec-56) | Hauptabschnitt | Z. 702–703 |
| ↳ [5.1 Schwellwerte & Mathematisches `leaky_short`-Modell (`raw_sources/wrench-board/api/pipeline/schematic/simulator.py`, `raw_sources/wrench-board/api/agent/measurement_memory.py`)](#sec-57) | Unterabschnitt | Z. 705–716 |
| ↳ [5.2 Der 4-Schritt-Kaskaden-Algorithmus (`_cascade` in `raw_sources/wrench-board/api/pipeline/schematic/simulator.py`)](#sec-58) | Unterabschnitt | Z. 718–727 |
| ↳ [5.3 Vollständige 38-zeilige Fehler-Kaskaden-Matrix (`_PASSIVE_CASCADE_TABLE` aus `raw_sources/wrench-board/api/pipeline/schematic/hypothesize.py`)](#sec-59) | Unterabschnitt | Z. 729–782 |
| ↳ [5.4 Hypothesen-Scoring, Tie-Breaking & der 50/50-Discriminator-Algorithmus (`raw_sources/wrench-board/api/pipeline/schematic/hypothesize.py`)](#sec-60) | Unterabschnitt | Z. 784–802 |
| [1. Systematisches Lesen von Schaltplänen & Reverse Engineering](#sec-61) | Hauptabschnitt | Z. 804–805 |
| ↳ [1.1 Referenzbezeichner (`RefDes`) & Kompakte Wert-Notation (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Reading_Schematics_Datasheets.md`)](#sec-62) | Unterabschnitt | Z. 807–815 |
| ↳ [1.2 Die 15 kanonischen Netz-Domänen & Regex-Prioritätsregeln (`raw_sources/wrench-board/api/pipeline/schematic/net_classifier.py`)](#sec-63) | Unterabschnitt | Z. 817–837 |
| ↳ [1.3 Topologie-Heuristiken zur Bauteil-Rollen-Erkennung (`raw_sources/wrench-board/api/pipeline/schematic/passive_classifier.py`)](#sec-64) | Unterabschnitt | Z. 839–865 |
| ↳ [1.4 Board-Level Reverse Engineering ohne Schaltplan](#sec-65) | Unterabschnitt | Z. 867–873 |
| [2. Masse-Konzepte, Signalintegrität & PCB-Layout (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/PCB_Design_Considerations.md`, `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Signal_Integrity_Basics.md`, `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/EMI_EMC_Considerations.md`)](#sec-66) | Hauptabschnitt | Z. 875–876 |
| ↳ [2.1 Trennung von `AGND`, `DGND`, `PGND` und `Chassis GND`](#sec-67) | Unterabschnitt | Z. 878–885 |
| ↳ [2.2 Wellenwiderstand (Impedanz) & Signalintegrität auf Leiterplatten](#sec-68) | Unterabschnitt | Z. 887–897 |
| ↳ [2.3 JTAG / Boundary-Scan & SWD-Debug-Schnittstellen (`raw_sources/theEmbeddedNewTestament.github.io/Debugging/JTAG_SWD_Debugging.md`)](#sec-69) | Unterabschnitt | Z. 899–906 |
| [3. Datasheet-Driven Repair, Design-Margen & Temperaturklassen](#sec-70) | Hauptabschnitt | Z. 908–909 |
| ↳ [3.1 Die 4 Pflicht-Sektionen jedes Datenblatts (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Reading_Schematics_Datasheets.md`)](#sec-71) | Unterabschnitt | Z. 911–925 |
| ↳ [3.2 Temperatur- und Qualitätsklassen (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Component_Selection.md`)](#sec-72) | Unterabschnitt | Z. 927–938 |
| [4. SMD-Gehäuseformen & Pinout-Fallen](#sec-73) | Hauptabschnitt | Z. 940–941 |
| ↳ [4.1 Passive SMD-Bauformen (Imperial vs. Metrisch)](#sec-74) | Unterabschnitt | Z. 943–956 |
| ↳ [4.2 Aktive SMD-Gehäuseformen & die gefährliche Regler-Pinout-Falle](#sec-75) | Unterabschnitt | Z. 958–980 |
| [5. SMD-Markierungscodes & Lokaler Datenblatt-Katalog (`raw_sources/electronics-datasheets/`)](#sec-76) | Hauptabschnitt | Z. 982–983 |
| ↳ [5.1 Nutzung des lokalen SMD-Codebooks (`raw_sources/electronics-datasheets/smd-codebook.pdf`)](#sec-77) | Unterabschnitt | Z. 985–991 |
| ↳ [5.2 Vollständiges Verzeichnis der lokalen Offline-Datenblätter (`raw_sources/electronics-datasheets/`)](#sec-78) | Unterabschnitt | Z. 993–1007 |

---

<!-- TOC_END -->

<a id="sec-1"></a>
## 1. Modul-Router & Aufbau der Wissensdatenbank

Nutze je nach Diagnosephase gezielt die folgenden Fachmodule im selben Verzeichnis:

1. **[00_INDEX_UND_KONTROLLLISTE.md](00_INDEX_UND_KONTROLLLISTE.md):** Vollständiges Quellen-Inventar aller ausgewerteten Repositories und Dateien.
2. **[01_In_Circuit_Messen_und_Bauteilpruefung.md](01_In_Circuit_Messen_und_Bauteilpruefung.md):** Physik der Multimeter-Modi ($\Omega$, Durchgang, Diodentest), Parallelschaltungs- und Ladeeffekte, `Red-Probe-on-Ground`, Prüftabellen für Sicherungen, Dioden/TVS, Widerstände (inkl. kompletter EIA-96-Tabelle), MLCC/Elkos (inkl. ESR-Richtwerttabelle), Spulen/Ferrite, BJT/MOSFET, Oszilloskop-/Logic-Analyzer-Praxis sowie Löt-Reihenfolge und IPC-A-610D-Kriterien.
3. **[02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md):** 7-stufige Prüf-Kaskade vom Netzteil bis zur Logik, validierte Playbooks (`boot-no-power`, `pmic-rail-collapse`, `usb-no-charge`), Power Sequencing, Reset/Quarz/Watchdog/Boot-Schalter, 3 Thermal-Cascade-Archetypen, BGA-Lift-Diagnoseprotokoll, `leaky_short`-Formel, 38-zeilige `_PASSIVE_CASCADE_TABLE` und 50/50-Discriminator-Algorithmus.
4. **[03_Schaltplaene_Platinenlayout_und_SMD_Codes.md](03_Schaltplaene_Platinenlayout_und_SMD_Codes.md):** Schaltplanlesen, Reverse Engineering ohne Schaltplan, 15 kanonische Netz-Domänen, Topologie-Heuristiken zur Bauteil-Rollen-Erkennung, Masse-Konzepte (`AGND`/`DGND`/`PGND`/Sternpunkt), Impedanz- und Signalintegritätsformeln, Datenblatt-Analyse (`Absolute Maximum Ratings`, Derating, Temperaturklassen), SMD-Gehäuseformen und lokaler Datenblatt-Katalog (`raw_sources/electronics-datasheets/smd-codebook.pdf`).
5. **[KOMPLETTES_HANDBUCH_ELEKTRONIK_DIAGNOSE.md](KOMPLETTES_HANDBUCH_ELEKTRONIK_DIAGNOSE.md):** Verlustfreie Gesamtausgabe aller Module in einer Datei (automatisch generiert und geprüft über [scripts/build_handbuch.py](scripts/build_handbuch.py)).

---

<a id="sec-2"></a>
## 2. Das Anti-Halluzinations-Gesetz (Zwei-Ebenen-Verteidigung)

<a id="sec-3"></a>
### 2.1 Strikte Verifikationspflicht für Bauteilbezeichnungen (`RefDes`) und Pinouts
- **NIEMALS** Bauteilbezeichnungen (`Reference Designators` / `RefDes` wie `R12`, `D4`, `U1`, `C3257`, `Q5200`), Pin-Nummern, Netznamen, Nominalspannungen oder Testpunkte aus dem Trainingsgedächtnis erraten oder erfinden (`raw_sources/wrench-board/CLAUDE.md`, `raw_sources/wrench-board/api/agent/manifest.py`).
- Jede genannte `RefDes` muss aus einer verifizierten Quelle stammen:
  1. Hochgeladene Fotos / Mikroskop-Aufnahmen mit lesbarem Platinenaufdruck (`Silkscreen`)
  2. Verifizierter Schaltplan (`Schematic PDF`) oder Boardview-Datei (`.brd`, `.kicad_pcb`, `.fz`, `.tvw`, `.bdv`, `.asc`, `.cad`)
  3. Vom Techniker ausdrücklich genannte und bestätigte Bezeichnung
- **Markierungspflicht bei Unbekanntheit:** Ist ein Bauteil auf einem Foto nicht eindeutig beschriftet oder fehlt der Schaltplan, muss es zwingend als **`[Unbekanntes Bauteil - Foto/Code nötig]`** markiert werden.
- **Zwei-Schichten-Abwehr (`raw_sources/wrench-board/api/agent/sanitize.py` & `raw_sources/wrench-board/api/board/validator.py`):**
  1. **Ebene 1 (Tool-Disziplin):** Jedes Bauteil wird vor Nennung gegen das bekannte Board-Inventar geprüft (`is_valid_refdes`, `resolve_part`, `resolve_net`, `resolve_pin`). Existiert ein Bezeichner nicht, wird `{found: false, closest_matches: [...]}` (über Präfix-Match bzw. Levenshtein-Nachbarn `suggest_similar`) geliefert – die KI muss nachfragen, statt zu raten.
  2. **Ebene 2 (Post-hoc-Sanitizer):** Ausgehender Text wird per Regex `REFDES_RE = \b[A-Z]{1,3}\d{1,4}\b` gescannt. Nicht verifizierte Tokens werden automatisch als `⟨?U999⟩` (und unbekannte Spender-Boards via `_DONOR_ID_RE = \b[a-z0-9][a-z0-9-]*-donor-\d{4}-\d{3}\b` als `⟨?donor:invalid⟩`) gekapselt.
  3. **Ausnahmen (`PROTOCOL_BLOCKLIST` & `_DEVICE_MODEL_RE`):** Vierstellige Apple-Modellnummern (`^A\d{4}$`, z. B. `A2337`, `A1989`) sowie folgende 115 Bus- und Schnittstellen-Bezeichner sind **keine** `RefDes`:
     - *USB / UART / I2C / I2S / SPI / QSPI:* `USB1`–`USB4`, `USB30`, `USB31`, `USB40`, `UART0`–`UART9`, `I2C0`–`I2C9`, `I2S0`–`I2S9`, `SPI0`–`SPI9`, `QSPI0`–`QSPI9`
     - *High-Speed / Storage / Memory:* `PCI0`–`PCI9`, `PCIE0`–`PCIE9`, `PCIE16`, `PCIE32`, `SAT0`–`SAT9`, `SATA0`–`SATA9`, `DDR0`–`DDR9`, `LPDDR2`–`LPDDR5`, `LPDDR4X`, `SDIO0`–`SDIO4`, `EMMC0`–`EMMC4`, `SD0`–`SD9`
     - *Display / Video / Debug / Control:* `HDM1`–`HDM3`, `HDMI0`–`HDMI9`, `DP1`–`DP9`, `VGA0`–`VGA9`, `LVDS0`–`LVDS9`, `MIPI0`–`MIPI4`, `CSI0`–`CSI4`, `DSI0`–`DSI4`, `JTAG0`–`JTAG4`, `CAN0`–`CAN9`, `GPI0`–`GPI9`, `GPIO0`–`GPIO9`, `HDCP1`, `HDCP2`

<a id="sec-4"></a>
### 2.2 Evidence-Gating, Resolution-Kategorien & Konfidenz-Skala (`raw_sources/wrench-board/api/pipeline/prompts.py`)
- **Zulässige Evidenz-Arten für Bauteil-Zuordnungen (`MAPPER_SYSTEM`):**
  1. `literal_refdes_in_quote`: Die Quelle nennt die `RefDes` wörtlich neben der Funktion (z. B. *„der LPC-Controller U14 wacht nicht auf“*).
  2. `mpn_match_in_quote`: Die Quelle nennt die exakte Hersteller-Teilenummer (`MPN`), die im Schaltplan diesem Bauteil zugeordnet ist (z. B. Quelle nennt `LM2677`, Schaltplan hat `U7 = LM2677SX-5`).
  - **Verboten:** Reine Topologie-Rückschlüsse (*„U7 erzeugt +5V und der Bericht erwähnt eine tote 5V-Schiene“*) oder funktionale Ähnlichkeit (*„es gibt nur einen Buck-Regler“*) gelten **nicht** als verifizierte Bauteil-Zuordnung!
- **Resolution-Kategorien bei Erfahrungsberichten (`SCOUT_SYSTEM`):**
  - `hardware_fix_verified`: Bauteil wurde ersetzt/nachgelötet und das Symptom verschwand nachweislich.
  - `hardware_ruled_out`: Hardware wurde durchgemessen (alle Rails stabil, keine Kurzschlüsse) und als Ursache ausgeschlossen (Fehler lag in Firmware/Konfiguration) – wichtig als **Differenzialdiagnose**, damit der Techniker denselben Hardware-Check vorab durchführt.
  - `ambiguous`: Symptom und Messpfad sind dokumentiert, Endlösung blieb offen.
- **Konfidenz-Skala für Diagnoseregeln (`CLINICIEN_TASK` & `raw_sources/wrench-board/api/agent/validation.py`):**
  - **`0.80 – 0.90` (`high`):** Mindestens 2 unabhängige Quellen oder Vorher-/Nachher-Messungen bestätigen exakt diese Reparatur.
  - **`0.60 – 0.80` (`medium`):** Eine fundierte Quelle mit klaren Messwerten oder eindeutige Schaltungstopologie + Messbefund.
  - **`0.50 – 0.60` (`low`):** Physikalisch plausibel, aber dünn belegt – nur als Prüfvorschlag, niemals als direkte Auslöt-Anweisung!
  - **`< 0.50`:** Verwerfen (keine Regel aus bloßer Spekulation bilden).
- **Validierte Reparatur-Abschlussmodi (`FixMode`):** `dead`, `alive`, `anomalous`, `hot`, `shorted`, `passive_swap`.

<a id="sec-5"></a>
### 2.3 Die 10 universellen Simulator-Invarianten (`raw_sources/wrench-board/benchmark/weaknesses.md`)
Jede kausale Fehler-Hypothese muss diese 10 physikalischen Gesetze erfüllen:

| ID | Physikalische Invariante | Verhindert folgendes Fehlverhalten |
|---|---|---|
| **INV-1** | `cascade_dead_*` ist immer eine echte Teilmenge des realen Schaltungsgraphen | Halluzinierte `RefDes` oder erfundene Spannungsschienen |
| **INV-2** | `failures=[]` (kein Bauteildefekt) erzeugt eine komplett leere Fehlerkaskade | Geister-Ausfälle im Normalbetrieb |
| **INV-3** | Jeder Folgetod (`cascade death`) hat eine echte physikalische Ursache (direkter Defekt, tote Versorgungsschiene, kurzgeschlossene Quelle oder offenes Serienbauteil stromaufwärts) | **Self-Dead-Gaming:** Bauteile als „tot“ markieren, obwohl ihr Ausfall keinen beobachtbaren Effekt hat |
| **INV-4** | Fällt das Quell-IC (`source_refdes`) einer Schiene aus, fällt zwingend auch die erzeugte Schiene (`cascade_dead_rails`) aus | Gebrochene Transitivität bei der Spannungsausbreitung |
| **INV-5** | Fällt eine Spannungsschiene aus, fallen alle Verbraucher (`consumers`) dieser Schiene aus – außer sie besitzen einen aktiven alternativen `power_in`-Pfad | Übersehene Folgeschäden nach Rail-Ausfall |
| **INV-6** | Strikter Determinismus auf dem gesamten Fehlerpfad | Schwankende oder zufällige Diagnose-Rankings |
| **INV-7** | Externe Eingangsschienen ohne eigenes Quell-IC auf dem Board (`VIN`, `VBUS`, Batterie) können durch interne IC-Ausfälle nicht „abgeschaltet“ (ohl/off) werden (wohl aber durch Kurzschluss heruntergezogen werden) | Falsche Rückwärts-Kausalität auf externe Netzteile |
| **INV-8** | Round-Trip-Konsistenz: `hypothesize(simulate(refdes, mode))` muss das Paar `(refdes, mode)` für beobachtbare Fehler in den Top-5 rekonstruieren | Asymmetrie zwischen Vorwärts-Physik und Rückwärts-Diagnose |
| **INV-9** | Jede nicht-leere Fehlerkaskade führt zu einem Verdict $\in \{\text{cascade}, \text{blocked}, \text{degraded}\}$ (niemals `completed`) | Versteckte Fehler bei scheinbar erfolgreichem Boot |
| **INV-10** | `hypothesize(empty_observation)` liefert keine Hypothesen mit positivem Score | Erfinden von Verdächtigen ohne Messwerte |

---

<a id="sec-6"></a>
## 3. Zerstörungsfreie Prüf-Reihenfolge (Außen vor Innen)

Bevor ein Gehäuse geöffnet, ein Kalibrier-/Garantiesiegel gebrochen oder eine Platine ausgebaut wird, ist **zwingend** diese Reihenfolge einzuhalten:

1. **Äußere Sicht-, Geruchs- und Schalterprüfung:**
   - Netzteil, Netzkabel, Stecker und Gerätebuchse auf verbogene Kontakte, Korrosion, Wackelkontakt, Risse oder Schmorspuren prüfen.
   - Alle externen Schalterstellungen prüfen (Netzschalter, Transportsicherung, Service-/Kalibrier-/Boot-Schalter).
2. **Externes Netzteil isoliert prüfen:**
   - Leerlaufspannung ($U_0$) und Spannung unter bekannter Prüflast ($U_{\text{Last}}$) sowie Polarität (Hohlstecker: Innenleiter `+` vs. Außenleiter `-`) messen.
3. **Eingangsmessung am geschlossenen Gerät (stromlos!):**
   - Widerstand ($\Omega$) und Diodentest ($\rightarrow\vert-$) in beiden Polaritäten zwischen Stromeingang (`+`) und Gehäuse-/Buchsen-Masse (`GND`) messen.
   - Ein Wert von $0\text{–}2\ \Omega$ in beiden Richtungen beweist sofort von außen einen harten Eingangskurzschluss (z. B. durchlegierte `TVS-Diode` oder Verpolungsschutzdiode).
4. **Kontrollierte Stromeinspeisung über Labornetzteil:**
   - Statt des ungeschützten Originalnetzteils ein Labornetzteil mit **strikter Strombegrenzung** (`100–300 mA` bei Logikplatinen) anschließen:
     - **`0,000 A`:** Offener Eingangspfad (Kabel, Buchse, Sicherung `F1`, Netzschalter, Serien-Induktivität).
     - **Sofortiger Anschlag im `CC`-Modus (Constant Current) bei $< 1\text{ V}$:** Harter Kurzschluss auf der Haupteingangsschiene.
     - **Kurzer Strompuls, dann `0 A` oder zyklisches Pulsieren:** Schutzabschaltung (`Hiccup-Mode`) durch Kurzschluss auf einer nachgeschalteten Sekundärschiene.

---

<a id="sec-7"></a>
## 4. Mechanik-, ESD- & Elektrischer Sicherheitsschutz zuerst

<a id="sec-8"></a>
### 4.1 Mechanischer Schutz bei Präzisionsmessgeräten (Fein- & Analysenwaagen / EMK-Zellen)
- **Zwingende Warnung vor dem Öffnen:** Präzisionswaagen mit **monolithischer EMK-Wägezelle (Elektromagnetische Kraftkompensation)** oder empfindlichen DMS-Biegebalken dürfen niemals ungesichert geöffnet, gekippt oder auf den Kopf gestellt werden:
  1. **Waagschale, Unterbau und Windschutz vorab komplett abnehmen** und Transportsicherung (falls vorhanden) verriegeln.
  2. **Absolutes Stoß- und Druckverbot am Aufnahmedorn:** Niemals auf den Schalenaufnahmedorn drücken, daran ziehen oder beim Lösen von Gehäuseschrauben ein Drehmoment einleiten – die hauchdünnen monolithischen Parallelogramm-Biegegelenke verbiegen oder brechen sofort (wirtschaftlicher Totalschaden).
  3. **Luftspalt-Sauberkeit:** Beim Löten an der Elektronikplatine das Wäystem abdecken, damit keine Lötzinnperlen, Drahtreste oder magnetischen Partikel in den Permanentmagnet-Luftspalt der Tauchspule fallen.

<a id="sec-9"></a>
### 4.2 ESD-Schutz (Elektrostatische Entladung)
- Vor dem Berühren offener Platinen ESD-Handgelenkband und ESD-Matte (über $1\text{ M}\Omega$ Schutzwiderstand geerdet) anlegen.
- Moderne CMOS-SoCs, FPGAs (`raw_sources/electronics-datasheets/FPGA/`), Operationsverstärker mit Femtoampere-Eingang (`ADA4530`) und ungeschützte MOSFET-Gates erleiden bereits ab $< 100\text{ V}$ latente Gate-Oxiddurchbrüche.

<a id="sec-10"></a>
### 4.3 Elektrische Sicherheit (IEC 61010) & Kondensatorentladung
- **Widerstands-, Durchgangs-, Kapazitäts-, ESR- und Diodenmessungen** dürfen **ausschließlich an komplett spannungsfreien und entladenen Schaltungen** durchgeführt werden!
- **Entladepflicht:** Primär-Elkos in Schaltnetzteilen (`320–400 V DC`!) und große Bulk-Elkos speichern lebensgefährliche bzw. bauteilzerstörende Ladung. Vor jeder Messung über einen Leistungswiderstand (z. B. $1\text{–}4{,}7\text{ k}\Omega / 5\text{ W}$) entladen und mit dem Multimeter im `DC V`-Modus auf **$< 1\text{ V}$** kontrollieren.
- **Netztrennung bei Oszilloskop-Messungen:** Der Masseclip (`GND`) eines Standard-Oszilloskops ist direkt mit dem Schutzleiter (`PE`) verbunden! Messungen auf der Primärseite von Schaltnetzteilen niemals mit geerdetem Standard-Tastkopf ohne Trenntrafo bzw. differentiellen Hochspannungstastkopf durchführen (Kurzschluss über `PE`!).

---

<a id="sec-11"></a>
## 5. Werkstatt-Logik vor Handbuch-Theorie & Ersatzteil-Sicherheit

<a id="sec-12"></a>
### 5.1 Reparatur auf Bauteilebene statt Baugruppentausch
- Empfiehl niemals den pauschalen Austausch einer gesamten Platine, wenn der Fehler auf ein konkretes Bauteil (Sicherung, TVS-Diode, LDO, Schaltregler-IC, MLCC, Elko, Lötstelle) eingegrenzt werden kann.
- **Kein Bauteiltausch auf Verdacht:** Jedes Bauteil wird erst ausgelötet, wenn eine Messung den Defekt belegt oder (bei parallelen Kondensatoren auf einer kurzgeschlossenen Schiene) die Eingrenzung dies erfordert.

<a id="sec-13"></a>
### 5.2 Hard Safety Filter für Bauteil-Substitution (`raw_sources/wrench-board/api/stock/safety.py`)
Beim Ersatz defekter Bauteile (insbesondere aus Spender-Platinen / Donor Boards) gilt die strikte Sicherheitsklassifikation `ROLE_TO_SAFETY` (Fail-Safe: jede unbekannte Rolle `role=None` ist zwingend `exact_only`!):

| Bauteilklasse | Funktionale Rolle (`role`) | Sicherheitsklasse (`SafetyClass`) | Werkstatt-Regel für den Ersatz |
|---|---|---|---|
| **Widerstand (`passive_r`)** | `feedback`, `current_sense`, `damping` | **`exact_only`** | Exakter Widerstandswert, Toleranz ($\le 1\ \%$) und Bauform zwingend erforderlich (bestimmt Reglerspannung, Überstromabschaltung und Signalintegrität). |
| **Widerstand (`passive_r`)** | `series`, `pull_up`, `pull_down` | **`tolerant_with_warning`** | Leichte Abweichung (z. B. $4{,}7\text{ k}\Omega$ statt $10\text{ k}\Omega$ bei Pull-up) im Notfall mit Hinweis zulässig. |
| **Kondensator (`passive_c`)** | `tank`, `ac_coupling`, `filter` | **`exact_only`** | Exakte Kapazität und Dielektrikum (`C0G`/`NP0` am Quarz, definierte Grenzfrequenz im LC-Filter) zwingend! |
| **Kondensator (`passive_c`)** | `decoupling`, `bulk`, `bypass` | **`tolerant_with_warning`** | Gleiche oder leicht höhere Kapazität zulässig, **Spannungsfestigkeit muss zwingend $\ge$ Original** sein! |
| **Ferritperle (`passive_fb`)** | `filter` | **`tolerant_with_warning`** | Ähnliche Impedanz @ 100 MHz zulässig, **Nennstrom (DC Current Rating) muss $\ge$ Original** sein! |
| **Diode (`passive_d`)** | `flyback`, `rectifier`, `esd`, `reverse_protection`, `signal_clamp` | **`exact_only`** | Exakter Typ (Schottky vs. Ultrafast vs. TVS, Sperrspannung, Flussspannung, Schaltzeit, Kapazität) zwingend! |
| **Transistor (`passive_q`)** | `load_switch`, `level_shifter`, `inrush_limiter`, `flyback_switch`, `cell_protection`, `cell_balancer` | **`exact_only`** | Exakter Typ (N/P-Kanal, $V_{GS(\text{th})}$, $R_{DS(\text{on})}$, $Q_g$, Gehäuse) zwingend! |
| **Aktive ICs & Stecker** | `ic`, `connector` | **`exact_only`** | Nur identische `MPN` (Hersteller-Teilenummer) und Pinbelegung zulässig! |

---

<a id="sec-14"></a>
## 6. Verbindlicher Diagnose- & Mess-Workflow (`raw_sources/wrench-board/api/agent/manifest.py`)

<a id="sec-15"></a>
### 6.1 Diagnosekette & Hypothesen-Auswertung (`HYPOTHESIZE`)
Jede Diagnose durchläuft den Zyklus:
`SYMPTOM → TOPOLOGIE / SCHALTPLAN → HYPOTHESE → GEZIELTE EINZELMESSUNG → AUSWERTUNG → NÄCHSTER SCHRITT`

- **Einzelner Spitzenkandidat (Score $\ge 2\times$ Platz 2):** Hypothese mit physikalischem Mechanismus benennen (nicht nur *„C156 Kurzschluss“*, sondern *„Plattenschluss von MLCC C156 zieht Schiene +3V3 auf GND“*) und sofort die verifizierende Messung (`MEASURE-TARGET`) anfordern.
- **Gleichstand mehrerer Kandidaten (`Top-N Tie`):** Nicht 5 Bauteile blind zum Auslöten auflisten, sondern über `discriminating_targets` genau den Messpunkt wählen, der die Kandidatenmenge **50/50 halbiert** (Details in [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md)).

<a id="sec-16"></a>
### 6.2 Präzise Messanweisungen (`MEASURE-TARGET` & `ANTI-GENERIC`)
- **Niemals** vage Anweisungen geben wie *„Miss mal U1“* oder generische Textbausteine (*„Prüfe mit Wärmebildkamera, suche nach Verfärbungen“*), ohne zu wissen, welche Werkzeuge der Techniker hat.
- **Immer genau EINE präzise Messung pro Schritt vorschlagen**, bestehend aus:
  1. **Pin-Rolle & Ziel:** Welcher exakte Pin an welchem Bauteil (z. B. `power_in` an Pin 3 von `U1` auf Schiene `+5V` gegen `GND`; oder `signal_out` / `clock_out` für Signalprüfung).
  2. **Messgerät & Modus:** z. B. Multimeter im $\Omega$-Modus (stromlos), Diodentest (Rot auf `GND`), DC-Voltmeter (im Betrieb) oder Oszilloskop.
  3. **Erwartungswert & Entscheidungsregel:** z. B. *„Sollwert stromlos: $9\text{–}50\text{ k}\Omega$. Bei $< 1\ \Omega$: harter Kurzschluss auf der Schiene oder in U1.“*

<a id="sec-17"></a>
### 6.3 Bench Anti-Patterns (`raw_sources/wrench-board/api/agent/seed_data/global_patterns/anti-patterns-bench.md`)
1. **Keine volle Nennspannung auf eine kurzgeschlossene Schiene geben:** Immer ein Labornetzteil mit Strombegrenzung (`100–300 mA`) nutzen – bei vollem Strom brennt die Leiterbahn weg, bevor der Hotspot lokalisiert ist.
2. **Bei Smartphone-/PMIC-Diagnose niemals den Akku ersatzlos weglassen:** Der Akku wirkt als riesiger Pufferkondensator; ohne ihn führen schnelle Lasttransienten am PMIC zu Schutzabschaltungen, die einen falschen Fehler vortäuschen.
3. **Kein Heißluft-Reflow neben ungeschützten Polymer-Elkos:** Polymer-Kondensatoren sterben oberhalb von $250\ ^\circ\text{C}$ oft lautlos (ohne Aufblähen) und legen die Schiene beim nächsten Einschalten lahm (mit Kapton-Tape/Hitzeschild schützen oder vorab abnehmen).
4. **Kein BGA-Abheben ohne Unterhitze (`Preheater`):** Ein steiler Temperaturgradient von oben reißt Pads und Leiterbahnen unter dem BGA ab.
5. **Keine hochohmigen Knoten mit einem 1-MΩ-Oszilloskop-Tastkopf messen:** Auf `10 MΩ` (`10:1`) umschalten oder aktiven Tastkopf nutzen, sonst verschiebt der Tastkopf den Arbeitspunkt (z. B. am Quarz oder Feedback-Teiler).
6. **Dem Diodenmodus unterhalb von `0,4 V` nicht zur Kurzschluss-Unterscheidung vertrauen:** Darunter greifen interne Schutzschaltungen vieler Multimeter – für Sub-Ohm-Kurzschlüsse immer den $\Omega$-Bereich (ideal: **4-Leiter-Milliohm-Messung**) verwenden.

---

# 01 – In-Circuit-Messen, Bauteilprüfung, Oszilloskop-Praxis und Löttechnik

Dieses Modul beschreibt die physikalischen Grundlagen und exakten Prüfprozeduren für das Messen elektronischer Bauteile im **eingelöteten Zustand (`In-Circuit`)** ohne Auslöten, ergänzt um Oszilloskop- und Logic-Analyzer-Diagnose sowie die Löt- und Instandsetzungspraxis aus `raw_sources/Repair/`, `raw_sources/theEmbeddedNewTestament.github.io/` und `raw_sources/wrench-board/`.

---

<a id="sec-18"></a>
## 1. Physik und Messmodi des Multimeters In-Circuit

<a id="sec-19"></a>
### 1.1 Widerstandsmessung ($\Omega$) vs. Durchgangsprüfung vs. Diodentest

| Messmodus | Prüfspannung / Prüfstrom | Anzeige | Wann nutzen? | Typische Falle In-Circuit |
|---|---|---|---|---|
| **Widerstand ($\Omega$)** | Sehr kleine Prüfspannung (**$< 0{,}3\text{ V}$**, meist $0{,}1\text{–}0{,}25\text{ V}$) | $\Omega$, $\text{k}\Omega$, $\text{M}\Omega$ oder `OL` | Widerstände, Sicherungen, Spulen-DCR, Sub-Ohm-Kurzschlüsse gegen `GND` | Halbleiterstrecken (Silizium $\approx 0{,}6\text{ V}$) werden bei $< 0{,}3\text{ V}$ **nicht** leitend $\rightarrow$ zeigen fälschlich `OL`! |
| **Durchgangsprüfung (Buzzer)** | Prüfspannung meist $0{,}5\text{–}3{,}0\text{ V}$, akustischer Schwellwert | Piepton + $\Omega$ / `V` | Leiterbahnverfolgung, Sicherungen, Schalter, Stecker, Kabel | Piept bei vielen Multimetern bis **$30\text{–}50\ \Omega$**! Moderne CPU/GPU/SoC-`VCORE`-Rails haben regulär $1\text{–}10\ \Omega$ $\rightarrow$ **kein** Kurzschluss! |
| **Diodentest ($\rightarrow\vert-$)** | Konstantstromquelle (**$\approx 0{,}5\text{–}2\text{ mA}$**), Leerlaufspannung **$2{,}0\text{–}3{,}3\text{ V}$** | Flussspannung $U_F$ in **Volt** (`0.540 V`) oder `OL` | Dioden, TVS, Transistoren, MOSFETs, IC-Pins gegen `GND` (`Red-Probe-on-Ground`) | Unter **$0{,}4\text{ V}$** greifen Multimeter-Schutzschaltungen (`raw_sources/wrench-board/api/agent/seed_data/global_patterns/anti-patterns-bench.md`) $\rightarrow$ für Sub-Ohm-Schlüsse 4-Leiter-$\Omega$ nutzen! |

<a id="sec-20"></a>
### 1.2 Einflüsse der Schaltungsumgebung (Parallelschaltung, Ladekurven, Restladung)
1. **Parallele Pfade:** Im eingelöteten Zustand misst man niemals das Bauteil isoliert, sondern immer das Bauteil **parallel zum gesamten Restnetzwerk** der Platine:
   $$\frac{1}{R_{\text{gemessen}}} = \frac{1}{R_{\text{Bauteil}}} + \frac{1}{R_{\text{Parallelpfad}}} \implies R_{\text{gemessen}} \le R_{\text{Nennwert}}$$
   - **Goldene Widerstands-Regel:** Ist ein gemessener Widerstandswert **kleiner** als der Nennwert, kann der Widerstand völlig intakt sein (ein paralleler Pfad zieht den Wert herunter). Ist der gemessene Wert jedoch **größer** als der Nennwert + Toleranz (z. B. `15 kΩ` statt `10 kΩ`), ist der Widerstand **zu 100 % defekt** (hochohmig geworden oder Haarriss).
2. **Ladekurven von Kondensatoren:** Beim Anlegen der Messspitzen an eine Spannungsschiene lädt der Prüfstrom des Multimeters die Stütz- und Ausgangskondensatoren auf. Der angezeigte Widerstandswert startet nahe $0\ \Omega$ (scheinbarer Kurzschluss) und **steigt kontinuierlich an**, bis die Kondensatoren geladen sind. Erst der **stabile Endwert** nach dem Einschwingen ist gültig!
3. **Restladungen (Sicherheit & Messfehler):** Restspannungen auf Elkos verfälschen jede $\Omega$- und Diodenmessung (oft negative Werte oder Dauerpiepen) und zerstören den Messeingang des Multimeters. **Platine immer stromlos machen, Elkos entladen und im `DC V`-Modus auf $< 1\text{ V}$ prüfen!**
4. **Parasitäre Body- und Substrat-Dioden:** In ICs und MOSFETs liegen zwischen `GND` und den Versorgungspins bzw. zwischen Source und Drain interne Dioden. Im $\Omega$- oder Diodenmodus erhält man daher beim Vertauschen von Rot und Schwarz unterschiedliche Messwerte.

<a id="sec-21"></a>
### 1.3 Relativmessung gegen Masse (`Red-Probe-on-Ground` / Dioden-Signatur)
In der Board-Level-Reparatur wird zur schnellen Prüfung von Spannungsschienen und IC-Pins die **umgekehrte Diodenmessung** verwendet:
- **Rote Messspitze (`+`) fest an Masse (`GND`)**, **schwarze Messspitze (`-`) an den zu prüfenden Pin / Kondensator**.
- **Physikalischer Grund:** Nahezu jeder IC-Pin besitzt interne ESD-Schutz- und Substratdioden, deren **Anode an `GND`** und deren **Kathode am Signal-/Versorgungspin** liegt. Legt man **Rot (`+`) an `GND`** und **Schwarz (`-`) an den Pin**, wird diese interne Diode in **Flussrichtung** bestromt und man misst direkt ihre Flussspannung $U_F$.
- **Bewertung der Dioden-Signatur:**
  - **`0,000 – 0,020 V` (in beide Richtungen):** Harter Kurzschluss gegen `GND`.
  - **`0,020 – 0,150 V`:** Entweder sehr niederohmige Hochstrom-Schiene (z. B. GPU/CPU-Core – mit $\Omega$-Messung gegenprüfen!) oder Fast-Kurzschluss (`leaky_short`).
  - **`0,250 – 0,750 V`:** Normale, gesunde Halbleiter-Signatur (Bestätigung, dass der Pin mit dem IC-Die verbunden ist und keinen Kurzschluss nach `GND` hat).
  - **`OL` (Open Loop / unendlich):** Leiterbahn unterbrochen, Lötstelle/BGA-Ball abgerissen (`bga-lift`), Serien-Ferritperle offen oder Pin ist intern nicht mit einer GND-ESD-Diode beschaltet.

---

<a id="sec-22"></a>
## 2. Exakte Prüftabellen für alle Bauteilklassen In-Circuit

<a id="sec-23"></a>
### 2.1 SMD-Sicherungen (`F`) & Polyswitches (`PPTC`)

| Prüfschritt | Messmodus | Sollwert (Intakt) | Fehlerbild & Bedeutung |
|---|---|---|---|
| **Widerstand** | $\Omega$ (4-Leiter oder 2-Leiter nach Nullabgleich der Messleitungen) | **$0{,}0\text{–}0{,}5\ \Omega$** (Schmelzsicherung typ. $< 0{,}2\ \Omega$; kleiner PPTC bis $1\text{–}2\ \Omega$) | **`OL` / $\text{M}\Omega$:** Sicherung durchgebrannt (offen). **Erhöhter Widerstand ($> 2\text{–}5\ \Omega$) bei PPTC:** Polyswitch ist nach Überstromauslösung hochohmig geblieben $\rightarrow$ Spannung bricht erst unter Last zusammen! |
| **Diodentest** | $\rightarrow\vert-$ | **`0,000 – 0,005 V`** | **`OL`:** Sicherung unterbrochen. |
| **Live-Spannung (im Betrieb)** | `DC V` (beide Seiten gegen `GND`) | $U_{\text{Eingang}} \approx U_{\text{Ausgang}}$ ($\Delta U < 50\text{ mV}$) | $U_{\text{Eingang}} = \text{Nennspannung}$, $U_{\text{Ausgang}} = 0\text{ V}$ $\rightarrow$ Sicherung offen. |

> [!CAUTION]
> **Goldene Sicherungs-Regel:** Eine durchgebrannte Sicherung **NIEMALS** sofort überbrücken oder ersetzen! Zuerst zwingend stromlos auf der **Lastseite (Ausgangsseite) der Sicherung gegen `GND`** den Widerstand ($\Omega$) und Diodenwert messen. Liegt dort ein Kurzschluss ($< 5\ \Omega$) vor, ist die Sicherung nur das Symptom eines nachgeschalteten Defekts (meist `TVS-Diode`, `MLCC` oder Schaltregler-MOSFET).

**Gängige SMD-Sicherungscodes:**
- `0` / `000`: $0\ \Omega$-Widerstand (oft als Sollbruchstelle/Sicherung eingesetzt)
- Littelfuse / Bourns Buchstabencodes: `D` ($0{,}25\text{ A}$), `E` ($0{,}375\text{ A}$), `F` ($0{,}5\text{ A}$), `G` ($0{,}75\text{ A}$), `H` ($1{,}0\text{ A}$), `J` ($1{,}25\text{ A}$), `K` ($1{,}5\text{ A}$), `L` ($1{,}75\text{ A}$), `N` ($2{,}0\text{ A}$), `O` ($2{,}5\text{ A}$), `P` ($3{,}0\text{ A}$), `R` ($3{,}5\text{ A}$), `S` ($4{,}0\text{ A}$), `T` ($5{,}0\text{ A}$), `W` ($7{,}0\text{ A}$).

---

<a id="sec-24"></a>
### 2.2 Dioden, Gleichrichter, Schottky-, Zener- & TVS-Schutzdioden

Immer in **beiden Polaritäten** im **Diodentest ($\rightarrow\vert-$)** prüfen (Anode = ohne Strich, Kathode = mit Ring/Balken):

| Diodentyp | Flussrichtung (`+` an Anode, `-` an Kathode) | Sperrrichtung (`+` an Kathode, `-` an Anode) | Typische Fehlerbilder In-Circuit |
|---|---|---|---|
| **Silizium-Gleichrichter / Schaltdiode (z. B. `1N4007`, `1N4148`, `UF4007`)** | **`0,55 – 0,75 V`** | **`OL`** (oder Parallelwiderstand der Schaltung) | `0,000 V` in beide Richtungen = **Legierungskurzschluss**. `OL` in beide Richtungen = **Unterbrechung**. |
| **Schottky-Diode (z. B. `1N5819`, `SS14`, `SBL2045`, `BAT54`)** | **`0,15 – 0,35 V`** | **`OL`** (Achtung: im heißen Zustand merklicher Sperrstrom normal!) | $U_F < 0{,}08\text{ V}$ oder in beide Richtungen identisch niedrig = **Kurzschluss / thermischer Durchbruch**. |
| **Zener-Diode (z. B. `1N47xx`, `BZX84`)** | **`0,55 – 0,75 V`** | **`OL`** (solange $U_Z > \text{Multimeter-Leerlaufspannung } \approx 3\text{ V}$) | `0,000 V` beidseitig = **Kurzschluss** (zieht Referenz- oder Gate-Spannung auf $0\text{ V}$). |
| **TVS-Diode unidirektional (z. B. `SMAJ5.0A`, `SMBJ12A`)** | **`0,55 – 0,75 V`** (Anode an `GND`, Kathode an Rail) | **`OL`** | **Häufigster Defekt nach Überspannung / falschem Netzteil:** Legiert auf **`0,000 V` in beide Richtungen** durch und klemmt die Eingangsschiene dauerhaft auf `GND`. |
| **TVS-Diode bidirektional (z. B. `SMAJ12CA`, ohne Kathodenstrich)** | **`OL`** | **`OL`** | Zeigt im intakten Zustand in **beide** Richtungen `OL`! Misst man Durchgang oder $< 0{,}5\text{ V}$, ist sie durchgeschlagen. |

---

<a id="sec-25"></a>
### 2.3 Widerstände (SMD & THT) & vollständige Code-Entschlüsselung

- **In-Circuit-Prüfregel:** Im $\Omega$-Modus in beiden Polaritäten messen.
  - $R_{\text{gemessen}} \approx R_{\text{Nennwert}}$: Widerstand intakt.
  - $R_{\text{gemessen}} < R_{\text{Nennwert}}$: Paralleler Schaltungspfad vorhanden (normal).
  - **$R_{\text{gemessen}} > R_{\text{Nennwert}} \times (1 + \text{Toleranz})$:** Widerstand **sicher defekt** (hochohmig / offen)!
- **Kritische Rollen (`raw_sources/wrench-board/api/pipeline/schematic/passive_classifier.py`):**
  - `feedback` (Spannungsteiler am Regler-Pin `FB`): Wird einer der Widerstände hochohmig (`open`), läuft der Regler in **Überspannung** oder schaltet ab.
  - `current_sense` (Shunt $< 1\ \Omega$, z. B. `R010`, `R050`, `R100`): Driftet er durch Überlast nach oben, löst die Überstromabschaltung (`OCP`) fälschlich schon bei geringer Last aus; brennt er offen durch (`open`), ist die nachfolgende Schiene tot.

#### 2.3.1 3-stellige & 4-stellige SMD-Codes sowie R-Notation
- **3-stellig (E24, $\pm 5\ \%$):** `AB C` $\rightarrow$ $\text{Wert} = (AB) \times 10^C\ \Omega$.
  - `100` = $10 \times 10^0 = 10\ \Omega$ *(NICHT $100\ \Omega$!)* | `101` = $100\ \Omega$ | `102` = $1\text{ k}\Omega$ | `472` = $4{,}7\text{ k}\Omega$ | `103` = $10\text{ k}\Omega$ | `104` = $100\text{ k}\Omega$ | `105` = $1\text{ M}\Omega$ | `0` oder `000` = $0\ \Omega$-Brücke.
- **4-stellig (E96, $\pm 1\ \%$):** `ABC D` $\rightarrow$ $\text{Wert} = (ABC) \times 10^D\ \Omega$.
  - `1000` = $100 \times 10^0 = 100\ \Omega$ | `1001` = $1\text{ k}\Omega$ | `4701` = $4{,}7\text{ k}\Omega$ | `1002` = $10\text{ k}\Omega$ | `4992` = $49{,}9\text{ k}\Omega$.
- **R- / K- / M-Notation (Dezimalkomma für Werte $< 10\ \Omega$ bzw. Shunts):**
  - `4R7` = $4{,}7\ \Omega$ | `0R22` oder `R22` = $0{,}22\ \Omega$ | `R010` = $0{,}010\ \Omega = 10\text{ m}\Omega$ | `2K2` = $2{,}2\text{ k}\Omega$.

#### 2.3.2 Vollständige EIA-96 Tabelle (Präzisionswiderstände $\pm 1\ \%$ in Bauform `0603`)
Format: **2 Ziffern (Basiswert `01`–`96`) + 1 Buchstabe (Multiplikator)**, z. B. `01C` = $100 \times 100 = 10\text{ k}\Omega$, `68X` = $499 \times 0{,}1 = 49{,}9\ \Omega$.

**Multiplikator-Buchstaben:**
- `Z` = $\times 0{,}001$ | `Y` oder `R` = $\times 0{,}01$ | `X` oder `S` = $\times 0{,}1$ | `A` = $\times 1$ | `B` oder `H` = $\times 10$ | `C` = $\times 100$ | `D` = $\times 1\,000$ | `E` = $\times 10\,000$ | `F` = $\times 100\,000$

| Code | Basiswert | Code | Basiswert | Code | Basiswert | Code | Basiswert | Code | Basiswert | Code | Basiswert |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **01** | 100 | **17** | 147 | **33** | 215 | **49** | 316 | **65** | 464 | **81** | 681 |
| **02** | 102 | **18** | 150 | **34** | 221 | **50** | 324 | **66** | 475 | **82** | 698 |
| **03** | 105 | **19** | 154 | **35** | 226 | **51** | 332 | **67** | 487 | **83** | 715 |
| **04** | 107 | **20** | 158 | **36** | 232 | **52** | 340 | **68** | 499 | **84** | 732 |
| **05** | 110 | **21** | 162 | **37** | 237 | **53** | 348 | **69** | 511 | **85** | 750 |
| **06** | 113 | **22** | 165 | **38** | 243 | **54** | 357 | **70** | 523 | **86** | 768 |
| **07** | 115 | **23** | 169 | **39** | 249 | **55** | 365 | **71** | 536 | **87** | 787 |
| **08** | 118 | **24** | 174 | **40** | 255 | **56** | 374 | **72** | 549 | **88** | 806 |
| **09** | 121 | **25** | 178 | **41** | 261 | **57** | 383 | **73** | 562 | **89** | 825 |
| **10** | 124 | **26** | 182 | **42** | 267 | **58** | 392 | **74** | 576 | **90** | 845 |
| **11** | 127 | **27** | 187 | **43** | 274 | **59** | 402 | **75** | 590 | **91** | 866 |
| **12** | 130 | **28** | 191 | **44** | 280 | **60** | 412 | **76** | 604 | **92** | 887 |
| **13** | 133 | **29** | 196 | **45** | 287 | **61** | 422 | **77** | 619 | **93** | 909 |
| **14** | 137 | **30** | 200 | **46** | 294 | **62** | 432 | **78** | 634 | **94** | 931 |
| **15** | 140 | **31** | 205 | **47** | 301 | **63** | 442 | **79** | 649 | **95** | 953 |
| **16** | 143 | **32** | 210 | **48** | 309 | **64** | 453 | **80** | 665 | **96** | 976 |

---

<a id="sec-26"></a>
### 2.4 Keramikkondensatoren (`MLCC`) & Elektrolytkondensatoren (`Elko` / `Tantal` / `Polymer`)

#### 2.4.1 MLCC (Multi-Layer Ceramic Capacitors) & 5-stufiges Kurzschluss-Jagdprotokoll (`raw_sources/wrench-board/api/agent/seed_data/global_patterns/short-to-gnd.md`)
- **Dielektrika:** `C0G`/`NP0` (hochgradig stabil für Quarze `tank` und HF-Filter; selten Kurzschluss), `X7R`/`X5R`/`Y5V` (hohe Packungsdichte für `decoupling`/`bulk`, anfällig für **Flex-Cracking** = Mikrorisse durch Platinenbiegung bei Sturz, Schraubspannung oder Steckerbelastung).
- **Wichtiges Anti-Pattern:** Vertraue niemals einem MLCC, nur weil er unter dem 10×-Mikroskop äußerlich unversehrt aussieht – Risse liegen meist im Inneren der Keramikschichten nahe den Löt-Terminals!
- **Verbindliche 5-stufige Diagnose-Reihenfolge bei Kurzschluss einer Schiene gegen `GND`:**
  1. Widerstand ($\Omega$) und Diodenmodus (rote Spitze an `GND`) auf der Schiene messen und Wert notieren ($< 5\ \Omega$ = Kurzschluss-Verdacht).
  2. Niedrige Spannung (**niemals höher als die Nennspannung der Schiene!**) mit Strombegrenzung (**`300 mA` Cap**) einspeisen.
  3. Thermischen Hotspot mit Wärmebildkamera, Kältespray oder einem Film aus **99 % Isopropanol** lokalisieren (der defekte MLCC verdampft den Alkohol als Erster).
  4. Verdächtige Kondensatoren **einzeln nacheinander** abnehmen und nach jedem Bauteil den Widerstand gegen `GND` erneut messen.
  5. Normalisiert sich der Wert nach dem Abnehmen eines Kondensators $\rightarrow$ neuen MLCC gleicher Kapazität und $\ge$ Spannungsfestigkeit einlöten. Bleibt der Kurzschluss nach Abnahme aller Kondensatoren bestehen $\rightarrow$ Last-IC oder Regler-IC ist intern durchgeschlagen.

#### 2.4.2 Elektrolyt-, Tantal- & Polymer-Kondensatoren + In-Circuit ESR-Prüfung
- **Alu-Elkos:** Trocknen durch Wärme (nahe Kühlkörpern/Schaltdrosseln) aus $\rightarrow$ Kapazität sinkt, **ESR (`Equivalent Series Resistance`)** steigt stark an, oder Elektrolyt tritt unten am Gummistopfen aus (fischiger Geruch beim Löten, ätzende Korrosion an Leiterbahnen und Durchkontaktierungen!).
- **Tantal-Elkos (gelbe oder schwarze SMD-Quader, Balken = `+` / Anode!):** Extrem empfindlich gegen Überspannungsspitzen und Verpolung; schlagen schlagartig mit **hartem Kurzschluss (`0–2 Ω`)** oder Brandfleck durch.
- **In-Circuit ESR-Messung:** Erfolgt mit einem ESR-Meter bei **$100\text{ kHz}$** und einer Prüfspannung **$< 100\text{ mV}_{\text{pp}}$**. Da $100\text{ mV}$ weit unter der Schwellenspannung von Halbleitern ($0{,}3\text{–}0{,}7\text{ V}$) liegt, kann der `ESR` direkt im eingelöteten Zustand gemessen werden!

**Typische ESR-Maximalwerte für Standard-Aluminium-Elkos (bei $20\ ^\circ\text{C}$, $100\text{ kHz}$):**

| Kapazität | 10 V | 16 V | 25 V | 35 V | 50 V | 63 V | 100 V | 250–400 V |
|---|---|---|---|---|---|---|---|---|
| **1 µF** | – | – | – | – | $5{,}0\text{–}15\ \Omega$ | $4{,}0\text{–}12\ \Omega$ | $3{,}0\text{–}10\ \Omega$ | $10\text{–}25\ \Omega$ |
| **4,7 µF** | – | – | $3{,}0\text{–}8{,}0\ \Omega$ | $2{,}5\text{–}6{,}0\ \Omega$ | $2{,}0\text{–}5{,}0\ \Omega$ | $1{,}5\text{–}4{,}0\ \Omega$ | $1{,}2\text{–}3{,}5\ \Omega$ | $4{,}0\text{–}10\ \Omega$ |
| **10 µF** | – | $2{,}0\text{–}5{,}0\ \Omega$ | $1{,}5\text{–}4{,}0\ \Omega$ | $1{,}0\text{–}3{,}0\ \Omega$ | $0{,}8\text{–}2{,}5\ \Omega$ | $0{,}8\text{–}2{,}0\ \Omega$ | $0{,}6\text{–}1{,}5\ \Omega$ | $2{,}0\text{–}6{,}0\ \Omega$ |
| **22 µF** | $2{,}0\text{–}4{,}5\ \Omega$ | $1{,}5\text{–}3{,}5\ \Omega$ | $1{,}0\text{–}2{,}5\ \Omega$ | $0{,}8\text{–}2{,}0\ \Omega$ | $0{,}6\text{–}1{,}5\ \Omega$ | $0{,}5\text{–}1{,}2\ \Omega$ | $0{,}4\text{–}1{,}0\ \Omega$ | $1{,}0\text{–}3{,}0\ \Omega$ |
| **47 µF** | $1{,}5\text{–}3{,}0\ \Omega$ | $1{,}0\text{–}2{,}5\ \Omega$ | $0{,}8\text{–}2{,}0\ \Omega$ | $0{,}6\text{–}1{,}5\ \Omega$ | $0{,}5\text{–}1{,}2\ \Omega$ | $0{,}4\text{–}1{,}0\ \Omega$ | $0{,}3\text{–}0{,}8\ \Omega$ | $0{,}6\text{–}1{,}8\ \Omega$ |
| **100 µF** | $0{,}8\text{–}2{,}0\ \Omega$ | $0{,}6\text{–}1{,}5\ \Omega$ | $0{,}4\text{–}1{,}2\ \Omega$ | $0{,}3\text{–}0{,}9\ \Omega$ | $0{,}25\text{–}0{,}7\ \Omega$ | $0{,}2\text{–}0{,}6\ \Omega$ | $0{,}15\text{–}0{,}5\ \Omega$ | $0{,}3\text{–}1{,}0\ \Omega$ |
| **220 µF** | $0{,}4\text{–}1{,}0\ \Omega$ | $0{,}3\text{–}0{,}8\ \Omega$ | $0{,}25\text{–}0{,}6\ \Omega$ | $0{,}2\text{–}0{,}5\ \Omega$ | $0{,}15\text{–}0{,}4\ \Omega$ | $0{,}12\text{–}0{,}35\ \Omega$ | $0{,}1\text{–}0{,}3\ \Omega$ | $0{,}2\text{–}0{,}6\ \Omega$ |
| **470 µF** | $0{,}25\text{–}0{,}7\ \Omega$ | $0{,}2\text{–}0{,}5\ \Omega$ | $0{,}15\text{–}0{,}4\ \Omega$ | $0{,}12\text{–}0{,}3\ \Omega$ | $0{,}1\text{–}0{,}25\ \Omega$ | $0{,}08\text{–}0{,}2\ \Omega$ | $0{,}06\text{–}0{,}15\ \Omega$ | $0{,}15\text{–}0{,}4\ \Omega$ |
| **1000 µF** | $0{,}15\text{–}0{,}4\ \Omega$ | $0{,}1\text{–}0{,}3\ \Omega$ | $0{,}08\text{–}0{,}2\ \Omega$ | $0{,}06\text{–}0{,}15\ \Omega$ | $0{,}05\text{–}0{,}12\ \Omega$ | $0{,}04\text{–}0{,}1\ \Omega$ | $0{,}03\text{–}0{,}08\ \Omega$ | – |

*(In Schaltnetzteilen und auf Mainboards verbaute **Low-ESR-** und **Polymer-Elkos** müssen noch deutlich niedriger liegen, typisch **$0{,}01\text{–}0{,}08\ \Omega$**.)*

---

<a id="sec-27"></a>
### 2.5 Spulen, Induktivitäten (`L`), Ferritperlen (`FB`) & Übertrager

| Bauteil | $\Omega$-Messung (DCR) | Fehlerbilder & Diagnose |
|---|---|---|
| **Ferritperle (`FB`, `passive_fb`)** | **$0{,}01\text{–}0{,}5\ \Omega$** | Verbindet Haupt-Rail mit gefilterter Sub-Rail (z. B. `+3V3` $\rightarrow$ `DBVDD` / `PCIE1_PWR_FILT`). Brennt bei nachgeschaltetem Überstrom **hochohmig (`OL` / `open`)** durch $\rightarrow$ Sub-Rail ist tot (`0 V`), Haupt-Rail bleibt stabil. |
| **Speicherdrossel (Buck/Boost `L`)** | **$0{,}01\text{–}2{,}0\ \Omega$** | **`OL`:** Wicklungsbruch oder abgerissenes Lötpad (häufig nach Sturz wegen hoher Bauteilmasse!). **Windungsschluss / Kernsättigung:** Im $\Omega$-Modus **nicht** erkennbar! Erfordert **LCR-Meter** ($L$ und Güte $Q$ bei $100\text{ kHz}$) oder **Ringing-Test** (gedämpfte Schwingung mit Oszilloskop prüfen). |
| **Übertrager / Trafo** | Primär/Sekundär getrennt: $\text{DCR}_{\text{prim}}$ vs. $\text{DCR}_{\text{sek}}$; zwischen Primär und Sekundär zwingend **`OL` ($> 10\text{ M}\Omega$)** | Unterbrechung einer Wicklung (`OL` oder eingebaute Thermosicherung offen) oder Isolationsdurchschlag. |

---

<a id="sec-28"></a>
### 2.6 Bipolartransistoren (`BJT`: NPN / PNP) & MOSFETs (N-Kanal / P-Kanal)

#### 2.6.1 Bipolartransistor (BJT) im Diodentest
Ersatzmodell für den statischen Test: Zwei Dioden mit gemeinsamem Basis-Anschluss:
- **NPN (z. B. `2N3904`, `2N2222`, `BC547`):**
  - Rot (`+`) an **Basis (`B`)**, Schwarz (`-`) an **Kollektor (`C`)** $\rightarrow$ **`0,55 – 0,75 V`**
  - Rot (`+`) an **Basis (`B`)**, Schwarz (`-`) an **Emitter (`E`)** $\rightarrow$ **`0,55 – 0,75 V`** (meist $2\text{–}10\text{ mV}$ höher als `B-C` wegen höherer Emitter-Dotierung!)
  - Alle anderen 4 Kombinationen (`-` an `B`, sowie `C-E` in beide Richtungen) $\rightarrow$ **`OL`**.
- **PNP (z. B. `2N3906`, `2SB156`, `BC557`):**
  - Schwarz (`-`) an **Basis (`B`)**, Rot (`+`) an **Kollektor (`C`)** und **Emitter (`E`)** $\rightarrow$ jeweils **`0,55 – 0,75 V`**. Alle anderen 4 Kombinationen $\rightarrow$ **`OL`**.

#### 2.6.2 MOSFET (N-Kanal / P-Kanal) im Diodentest
1. **Schritt 1 – Gate entladen:** Vor der Messung Gate (`G`) und Source (`S`) kurz mit einer Metallpinzette überbrücken.
2. **Schritt 2 – Gate-Oxidisolation prüfen:** Zwischen **Gate (`G`) und Source (`S`)** sowie zwischen **Gate (`G`) und Drain (`D`)** muss das Multimeter in **beide Richtungen `OL`** anzeigen (es sei denn, in der Schaltung liegt ein externer Gate-Source-Ableitwiderstand z. B. $10\text{–}100\text{ k}\Omega$ parallel). Ein Wert nahe $0\text{ V}$ / $< 10\ \Omega$ bedeutet **Gate-Oxiddurchbruch (MOSFET defekt)**.
3. **Schritt 3 – Interne Body-Diode zwischen Source (`S`) und Drain (`D`) prüfen:**
   - **N-Kanal MOSFET (z. B. `2N7002`, `2SK2043`, `IRFZ44N`):**
     - Rot (`+`) an **Source (`S`)**, Schwarz (`-`) an **Drain (`D`)** $\rightarrow$ **`0,40 – 0,70 V`** (Body-Diode in Flussrichtung).
     - Rot (`+`) an **Drain (`D`)**, Schwarz (`-`) an **Source (`S`)** $\rightarrow$ **`OL`** (sofern Gate entladen ist!).
   - **P-Kanal MOSFET (häufig als High-Side `load_switch` / `inrush_limiter`):**
     - Rot (`+`) an **Drain (`D`)**, Schwarz (`-`) an **Source (`S`)** $\rightarrow$ **`0,40 – 0,70 V`**.
     - Rot (`+`) an **Source (`S`)**, Schwarz (`-`) an **Drain (`D`)** $\rightarrow$ **`OL`**.
4. **Die Gate-Auflade-Falle:** Misst man beim N-Kanal-MOSFET zuerst mit Rot (`+`) am Gate und Schwarz (`-`) an Source, lädt die Prüfspannung ($2{,}5\text{–}3\text{ V}$) die Gate-Source-Kapazität $C_{\text{iss}}$ über die Schwellenspannung $V_{GS(\text{th})}$ auf. Der Kanal **schaltet leitend durch** und zeigt anschließend zwischen Drain und Source in beide Richtungen `0,000 V`! Nach Kurzschließen von `G-S` sperrt er wieder (`OL`).

---

<a id="sec-29"></a>
## 3. Oszilloskop-, Logic-Analyzer- & I/O-Diagnose In-Circuit

<a id="sec-30"></a>
### 3.1 Oszilloskop-Regeln & Formeln (`raw_sources/theEmbeddedNewTestament.github.io/Debugging/Oscilloscope_Measurements.md`)
- **Zusammenhang zwischen Bandbreite und Anstiegszeit ($10\ \%\text{–}90\ \%$):**
  $$\text{Bandwidth (BW)} = \frac{0{,}35}{t_{\text{rise}}}$$
- **Mindest-Bandbreite nach Signaltyp:**
  - **Digitalsignale / Takte:** **$3\text{–}5\times f_{\text{clock}}$** (um die 3. und 5. Harmonische der Rechteckflanke sauber abzubilden).
  - **Analogsignale:** **$2\text{–}3\times f_{\text{max}}$**.
  - **Schaltnetzteil-Ripple & Switching-Spikes:** **$10\times f_{\text{switching}}$** (für Ripple-Messungen auf Power-Rails zusätzlich `20 MHz`-Bandbreitenbegrenzung am Kanal aktivieren, um eingestreutes HF-Rauschen auszublenden!).
- **Tastkopf-Disziplin (`Common Pitfalls`):**
  1. **10:1-Tastkopf (`10 MΩ`, $\approx 10\text{–}15\text{ pF}$)** statt 1:1-Tastkopf (`1 MΩ`, $\approx 100\text{ pF}$) verwenden, um Quarze und hochohmige Schaltungsknoten nicht kapazitiv/ohmsch zu belasten.
  2. **Tastkopf-Kompensation vorab am 1-kHz-Kalibrierausgang prüfen:** Abgerundete Ecken = unterkompensiert; Überschwinger = überkompensiert.
  3. **Kurze Massefeder (`Ground Spring`) statt langem Massekabel mit Krokodilklemme:** Ein $15\text{ cm}$ langes Massekabel bildet eine Induktivität ($\approx 150\text{ nH}$), die bei schnellen Schaltflanken künstliches Überschwingen (`Ringing`) auf dem Bildschirm erzeugt und wie eine elektromagnetische Antenne wirkt!
- **Trigger-Modi gezielt einsetzen:**
  - `Auto`: Erzwingt Bildaufbau auch ohne Trigger (gut zum Prüfen, ob überhaupt ein DC-Pegel da ist).
  - `Normal`: Löst **nur** bei echtem Trigger-Ereignis aus (unverzichtbar für seltene Glitches oder Bus-Pakete).
  - `Single`: Einmalige Aufzeichnung (`Single-Shot`) zum Einfrieren des **Einschaltmoments (`Power-Up-Sequence`)** oder eines Spannungsabfalls (`Brownout` / `Rail Sag`).

<a id="sec-31"></a>
### 3.2 Logic Analyzer & Digitale Bus-Prüfung (`raw_sources/theEmbeddedNewTestament.github.io/Debugging/Logic_Analyzer_Usage.md`, `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Digital_IO_Programming.md`, `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Analog_IO.md`)
- **Abtastrate:** Mindestens **$4\text{–}10\times$ höchste Busfrequenz** (z. B. $\ge 4\text{ MS/s}$ für $400\text{ kHz}$ I2C Fast-Mode; $\ge 50\text{–}100\text{ MS/s}$ für SPI).
- **Typische Hardware-Fehlerbilder auf Digitalbussen (I2C / SPI / UART):**
  - **I2C-Leitung (`SDA` oder `SCL`) klemmt dauerhaft auf `0 V` (`Stuck Low`):** Entweder ein Busteilnehmer-IC hat einen internen ESD-Diodenschluss nach `GND`, ein Slave hält `SDA` im abgebrochenen Clock-Zyklus fest, oder der externe Pull-up-Widerstand ($2{,}2\text{–}10\text{ k}\Omega$ nach `VCC`) ist offen (`open`).
  - **I2C-Flanken steigen extrem langsam (sägezahnförmig) an:** Pull-up-Widerstand zu hochohmig oder zu hohe Buskapazität.
  - **Taster-/Schalter-Fehlfunktionen (`Switch Debouncing`):** Mechanische Taster prellen $1\text{–}20\text{ ms}$; ist der RC-Entprellkondensator kurzgeschlossen (`short`), sieht der GPIO dauerhaft den aktiven Pegel (z. B. Dauer-Reset oder Dauer-Tastendruck).
- **Analogeingänge (`ADC`):**
  - Stimmen alle ADC-Messwerte eines Geräts proportional nicht, zuerst die analoge Referenzspannung **`VREF` / `AVDD`** und deren Stützkondensatoren gegen **`AGND`** prüfen!

---

<a id="sec-32"></a>
## 4. Löttechnik, Sektionale Inbetriebnahme & Fallstudien (`aKaReZa75/Repair`)

<a id="sec-33"></a>
### 4.1 Sektionale Bestückungs- & Prüf-Reihenfolge (`raw_sources/Repair/Videos.md`)
Beim Aufbau oder der Komplettsanierung einer Mikrocontroller-/Embedded-Platine wird **niemals alles auf einmal** eingelötet, sondern in validierten Stufen:
1. **Stufe 1 – Stromeingang & Spannungsregler:** Buchse, Sicherung, Schutzdiode sowie `12 V`-, `5 V`- und `3,3 V`- (bzw. `4,0 V`-GSM-)Regler samt Eingangs-/Ausgangskondensatoren einlöten.
2. **Stufe 2 – Pflicht-Zwischentest (ohne MCU!):** Spannung anlegen und **alle Ausgangsschienen nachmessen**. Erst wenn `5,0 V` und `3,3 V` exakt stimmen, darf der Mikrocontroller bestückt werden (verhindert den Tod der MCU durch einen falsch gelöteten Regler!).
3. **Stufe 3 – Kernlogik (MCU & Takt):** Mikrocontroller (`STM32F103C8`, `ATmega328P`), Quarz + Lastkondensatoren, Reset-Beschaltung und `SWD`/`JTAG`/`ISP`-Header einlöten $\rightarrow$ Stromaufnahme und Debugger-Verbindung (`ST-Link` / `J-Link`) testen.
4. **Stufe 4 – Kommunikation & Peripherie:** USB-Buchse, USB-UART-Wandler (`CH340`), Relais, Displays, SIM-Slot und HF-empfindliche GSM-Module (`Quectel M66`) bestücken und im Gesamtsystem testen.

<a id="sec-34"></a>
### 4.2 Lötwerkzeuge, Temperaturprofile & IPC-A-610D-Qualität (`raw_sources/Repair/Soldering_Tools.md` & `raw_sources/Repair/aKaReZa 38 - Repair, Soldering Tools/IPC-A-610D.pdf`)
- **Lötspitzen-Auswahl:**
  - `900M-T-K` (Messer-/Klingenform) und `900M-T-2C` (abgeschrägter Zylinder): Ideal für Drag-Soldering (Ziehlöten) an `SOIC`/`QFP`-ICs mit Flussmittel.
  - `900M-T-3.2D` (Meißelform): Hohe Wärmeübertragung für große Masse-Pads, Steckverbinder und THT-Bauteile.
- **Lot, Flussmittel & Temperaturen:**
  - **Bleihaltiges Lot (`Sn63/Pb37` / Lotpaste `183 °C`):** Eutektischer Schmelzpunkt bei $183\ ^\circ\text{C}$, Lötspitze $320\text{–}350\ ^\circ\text{C}$ – ideal für schonendes Rework empfindlicher Platinen.
  - **Bleifreies Lot (`SAC305`):** Schmelzpunkt $217\text{–}221\ ^\circ\text{C}$, Lötspitze $360\text{–}380\ ^\circ\text{C}$.
  - **Heißluft-Rework:** Unterhitze (`Preheater`) auf **$130\text{–}150\ ^\circ\text{C}$**, Heißluftdüse auf **$330\text{–}380\ ^\circ\text{C}$** bei mittlerem Luftstrom; benachbarte Kunststoffstecker, Mikrofone und Polymer-Elkos zwingend mit **Kapton-Tape (Polyimid)** abkleben!
  - **Reinigung:** Flussmittelreste (`RMA-223-UV`) nach dem Löten immer mit **99 % Isopropanol** (oder `Kontakt 600`) und antistatischem ESD-Pinsel entfernen, da verbleibende Rückstände unter feuchten Bedingungen Kriechströme an hochohmigen Knoten verursachen.
- **Abnahmekriterien nach `IPC-A-610D`:**
  - **Gute SMD-/THT-Lötstelle:** Konkaver Meniskus (Hohlkehle), glatte Oberfläche, Benetzungswinkel $< 90^\circ$, Bauteilanschlusskontur noch erkennbar.
  - **Typische Lötfehler:** *Kalte Lötstelle* (matt-krümelig, hochohmig/Wackelkontakt), *Tombstoning* (Grabsteineffekt bei `0402`/`0603` durch ungleichmäßige Pad-Erwärmung), *Solder Bridging* (Zinnbrücke zwischen Fine-Pitch-Pins), *Lifted Pad* (abgerissenes Kupferpad durch Hebeln vor vollständigem Aufschmelzen!).

<a id="sec-35"></a>
### 4.3 Reparatur-Fallstudie: Defektes Multimeter (`Victor VC97` / EEPROM-Diagnose aus `raw_sources/Repair/Videos.md`)
- **Symptom:** Nach versehentlicher Spannungsmessung im Widerstands-/Diodenbereich funktionieren Widerstands-, Kapazitäts-, Dioden- und Durchgangsmessung nicht mehr oder zeigen völligen Unsinn, während Spannungsmessung noch geht.
- **Diagnose- & Reparaturweg:**
  1. **Eingangs-Schutzkette prüfen:** Im Multimeter sitzen hinter der `V/Ω/Hz`-Buchse ein **PTC-Thermistor** ($1\text{–}1{,}5\text{ k}\Omega$) sowie antiparallele **Schutz-Transistoren** (oft als niederohmige Zener-/Klemmdioden geschaltete `NPN`-Transistoren wie `S9013`/`2N3904`). Bei Überspannung schlagen diese Klemmtransistoren auf Kurzschluss durch und klemmen den Messeingang fest $\rightarrow$ auslöten und prüfen!
  2. **Kalibrier-EEPROM (`AT24C02` / `24C02`, SOIC-8) prüfen:** Durch Spannungsspitzen oder Unterspannung beim Einschalten korrumpiert häufig der Inhalt des externen I2C-EEPROMs.
  3. **Instandsetzung:** Klemmtransistoren/PTC ersetzen und das `AT24C02`-EEPROM mit einem intakten Referenz-Dump (`raw_sources/Repair/aKaReZa 26 - Repair, VC97 EEPROM IC/VC97_EEPROM_BackUP.bin`) neu flashen.

---

# 02 – Stromversorgung, Einschaltsequenz-Diagnose und Hypothesen-Engine

Dieses Modul enthält die komplette Systematik zur Fehlersuche in Stromversorgungen, Einschaltsequenzen (`Power Sequencing`), Reset-/Takt-/Boot-Schaltungen sowie die vollständige Simulations- und Hypothesen-Logik aus `raw_sources/wrench-board/api/pipeline/schematic/simulator.py`, `raw_sources/wrench-board/api/pipeline/schematic/hypothesize.py`, `raw_sources/wrench-board/api/agent/seed_data/` und `raw_sources/theEmbeddedNewTestament.github.io/`.

---

<a id="sec-36"></a>
## 1. Die feste 7-stufige Prüf-Kaskade vom Eingang zur Logik

Bei jedem Gerät ohne Funktion (`Dead / No Power`) wird **streng sequenziell** vom Stromeingang bis zur Digital-/Analoglogik geprüft (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Reading_Schematics_Datasheets.md`, `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Power_Supply_Design.md`):

<a id="sec-37"></a>
### Stufe 1: Externes Netzteil / Batterie
- **Leerlauf vs. Last:** Ein Netzteil mit gealterten Ausgangselkos zeigt im Leerlauf oft noch die volle Nennspannung (z. B. `12,0 V`), bricht aber bei Lastzuschaltung sofort ein.
- **Restwelligkeit (`Ripple`):** Mit Oszilloskop (AC-Kopplung, `20 MHz`-Bandbreitenfilter) unter Last prüfen. Ripple $> 100\text{–}200\text{ mV}_{\text{pp}}$ stört nachgeschaltete Regler und führt zu erratischen Resets.

<a id="sec-38"></a>
### Stufe 2: Eingangsbuchse, Steckverbinder & Netzschalter
- **Mechanische Defekte:** Gebrochene Lötstellen am Mittelpin von DC-Hohlsteckerbuchsen, aufgebogene Federkontakte, korrodierte oder abgerissene USB-C-Pads, Kabelbruch direkt hinter der Zugentlastung.
- **Masse-Rückpfad prüfen:** Immer auch den Durchgang vom Minuspol des Netzteils bis zur Platinenmasse (`GND`) messen! Ist die Masse-Lötstelle der Buchse gebrochen, misst man gegen das externe Netzteil-Minus überall auf der Platine $+12\text{ V}$, obwohl kein einziger Elektronenfluss stattfindet.

<a id="sec-39"></a>
### Stufe 3: Eingangsfilter, Verpolungs- & Überspannungsschutz
- **Sicherung (`F`) & PPTC:** Auf Durchgang ($\approx 0\ \Omega$) bzw. Spannungsabfall im Betrieb ($< 50\text{ mV}$) prüfen.
- **Verpolungsschutz-Topologien:**
  1. *Seriendiode (`reverse_protection`):* Einfach, hat aber $0{,}2\text{–}0{,}7\text{ V}$ Verlust. Brennt bei Überstrom hochohmig (`open`) durch $\rightarrow$ Ausgangsschiene tot.
  2. *Antiparallele Crowbar-Diode nach `GND` hinter der Sicherung:* Leitet bei Verpolung und löst sofort die Sicherung aus (oft legiert die Diode dabei dauerhaft auf `0 Ω` durch!).
  3. *P-Kanal / N-Kanal Ideal-Diode MOSFET (`inrush_limiter` / `reverse_protection`):* Schaltet über ein RC-Soft-Start-Glied am Gate verzögert ein. Ist der Kanal offen (`open` / `stuck_off`), bleibt die Hauptschiene trotz intakter Eingangsspannung bei `0 V`.
- **Überspannungsschutz (`TVS-Diode` gegen `GND`):** Der häufigste Defekt nach Verwendung eines falschen Netzteils (z. B. `24 V` statt `9 V`). Die TVS-Diode opfert sich durch einen permanenten Legierungskurzschluss (`0,000 V` / $< 1\ \Omega$ gegen `GND`).

<a id="sec-40"></a>
### Stufe 4: Haupt-Spannungsschiene ($V_{\text{IN}}$ / $V_{\text{BUS}}$ / $V_{\text{MAIN}}$ / $V_{\text{BAT}}$)
- Vor dem Einschalten Widerstand ($\Omega$) und Dioden-Signatur (Rot an `GND`) messen.
- **Schutzschaltungs-Verhalten (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Power_Supply_Design.md`):**
  - *Overvoltage Protection (`OVP`):* Crowbar (Thyristor/TVS zieht Schiene hart auf `GND`), Shunt-Regelung, Serien-Abschaltung oder Voltage Clamping.
  - *Overcurrent Protection (`OCP`):* Konstantstrombegrenzung (`Current Limiting`), rückläufige Kennlinie (`Foldback Limiting`), zyklisches Ein-/Ausschalten (**`Hiccup Mode`** – erkennbar am rhythmischen Pulsieren der Schienenspannung und einem leisen Ticken der Induktivitäten!) oder dauerhafte Verriegelung bis zum Power-Cycle (`Latch-Off`).

<a id="sec-41"></a>
### Stufe 5: Linearregler (`LDO` / Standard-Regler wie `78xx`, `LM317`, `AMS1117`)
- **Wirkungsgrad & Thermik (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Power_Supply_Design.md` & `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Thermal_Management.md`):**
  $$\eta_{\text{linear}} = \frac{V_{\text{OUT}}}{V_{\text{IN}}} \times 100\ \%, \qquad P_{\text{loss}} = (V_{\text{IN}} - V_{\text{OUT}}) \cdot I_{\text{OUT}}$$
  $$\Delta T = P_{\text{loss}} \cdot R_{\text{th,JA}}, \qquad T_J = T_A + \Delta T$$
- **Typische LDO-Fehlermodi:**
  1. *Ausgang = `0 V` trotz vorhandenem $V_{\text{IN}}$:* Entweder `EN`-Pin (Enable) ist auf `Low`, der LDO ist intern unterbrochen, oder ein harter Kurzschluss am Ausgang zwingt den LDO in den thermischen/Überstrom-Shutdown.
  2. *Durchlegierter Pass-Transistor (**$V_{\text{OUT}} \approx V_{\text{IN}}$**):* Kritischster Fehler! Wenn ein `12 V → 3,3 V` LDO zwischen Eingang und Ausgang durchlegiert, liegen volle `12 V` auf der `3,3 V`-Logikschiene $\rightarrow$ nachgeschaltete Mikrocontroller und Sensoren sind fast immer mitzerstört (siehe `Absolute Maximum Ratings`).
  3. *Hochfrequente Schwingung (Oszillation):* Ältere LDOs (z. B. `AMS1117`, `LM1117`) benötigen für ihre Phasenreserve zwingend einen Ausgangskondensator mit einem **definierten Mindest-ESR** ($0{,}1\text{–}2\ \Omega$, klassisch Tantal/Elko). Ist der Ausgangskondensator ausgetrocknet oder falsch bestückt, schwingt der Regler mit mehreren kHz bis MHz!

<a id="sec-42"></a>
### Stufe 6: Schaltregler (`Buck`, `Boost`, `Buck-Boost`, `Flyback`, `PMIC`)
- **Topologien (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Power_Supply_Design.md`):**
  - *Buck (Abwärtswandler):* $V_{\text{OUT}} < V_{\text{IN}}$ (Induktivität speichert Energie während der High-Side-On-Zeit und gibt sie über den Ausgang an die Last ab).
  - *Boost (Aufwärtswandler):* $V_{\text{OUT}} > V_{\text{IN}}$ (für Display-Backlights, OLED, Batterie-Systeme; Induktivität liegt am Eingang, Diode/Sync-FET zum Ausgang).
  - *Buck-Boost:* $V_{\text{OUT}}$ kann größer oder kleiner als $V_{\text{IN}}$ sein.
  - *Flyback (Sperrwandler):* Galvanisch getrennt über Übertrager/Transformator (klassisch für AC/DC-Netzteilmodule).
- **Kritische Prüfstellen am Buck-/Boost-Regler:**
  1. `VIN` / `PVIN` (Leistungseingang) und `EN` / `SHDN` (Freigabesignal).
  2. **Switch-Node (`SW` / `LX` / `PHASE`) vor der Speicherdrossel `L`:** Mit dem Oszilloskop muss ein sauberes Pulsweiten-Rechtecksignal ($100\text{ kHz}\text{–}3\text{ MHz}$) zwischen $0\text{ V}$ und $V_{\text{IN}}$ sichtbar sein. Am **Ausgang hinter der Spule `L`** muss eine glatte Gleichspannung ($V_{\text{OUT}}$) anliegen.
  3. **Bootstrap-Kondensator (`C_BOOT`, zwischen `SW` und `BST`/`BOOT`-Pin):** Typisch $10\text{–}100\text{ nF}$. Ist er offen oder kurzgeschlossen, kann der High-Side-N-Kanal-MOSFET nicht über $V_{\text{IN}}$ angesteuert werden $\rightarrow$ Regler startet nicht oder bricht unter Last zusammen.
  4. **Feedback-Spannungsteiler ($R_{FB1}$ von $V_{\text{OUT}}$ nach `FB`, $R_{FB2}$ von `FB` nach `GND`):** Bestimmt die Ausgangsspannung über $V_{\text{OUT}} = V_{\text{REF}} \cdot (1 + R_{FB1}/R_{FB2})$.

<a id="sec-43"></a>
### Stufe 7: Stützkondensatoren, Filter-Ferrite & Übergang zur Logik
- Lokale Entkopplungskondensatoren (`decoupling`, $100\text{ nF}$ direkt an jedem `VCC`-Pin) und Serien-Ferritperlen (`passive_fb`) zu empfindlichen Analog-, Audio- (`DBVDD`, `AVDD`) oder HF-Domänen prüfen.

---

<a id="sec-44"></a>
## 2. Validierte Diagnose-Playbooks (`raw_sources/wrench-board/api/agent/seed_data/global_playbooks/`)

<a id="sec-45"></a>
### 2.1 Playbook `boot-no-power` (Gerät lässt sich nicht einschalten / Tot)
Kanonische 6-Schritt-Isolationskaskade (`raw_sources/wrench-board/api/agent/seed_data/global_playbooks/boot-no-power.json`):

| Schritt | Messziel (`target`) | Messart | Nominalwert | Gültiger Bereich (`pass_range`) | Diagnose-Begründung (`rationale`) |
|---|---|---|---|---|---|
| **1** | `VBUS` (Eingang) | Numerisch (`V`) | `5,0 V` | **`4,5 – 5,5 V`** | Externe Stromversorgung verifizieren, bevor die Platine verdächtigt wird. |
| **2** | `F1` (Eingangssicherung) | Numerisch ($\Omega$ / Diode) | `0 Ω` | **`0 – 5 Ω`** | Durchgang der Eingangssicherung prüfen. Offen (`OL`) $\rightarrow$ Sicherung ausgelöst (Folgekurzschluss prüfen!). |
| **3** | `VBAT_MAIN` (Hauptschiene) | Numerisch (`V`) | `3,7 V` | **`3,0 – 4,4 V`** | Batterie-/Haupt-Systemschiene prüfen. Ist sie tot, hat das PMIC keine Referenz-/Eingangsspannung. |
| **4** | `PMU_ENABLE` (Power-On) | Boolean (Pegel) | `true` (Aktiv) | **`true`** | Prüfen, ob das Einschaltsignal (Power-Button $\rightarrow$ PMIC) tatsächlich ausgelöst wird. |
| **5** | `VDDMAIN` (1. Digital-Rail) | Numerisch (`V`) | `0,8 V` | **`0,75 – 0,85 V`** | Erste vom PMIC erzeugte Digitalschiene. Fehlt sie $\rightarrow$ PMIC defekt oder Kurzschluss auf der Sekundärschiene. |
| **6** | `SOC_RESET_N` (CPU-Reset) | Boolean (Pegel) | `true` (High) | **`true`** | Reset muss vom PMIC freigegeben (deasserted) werden, sobald alle Primär-Rails stabil sind. |

<a id="sec-46"></a>
### 2.2 Playbook `pmic-rail-collapse` (Schiene bricht unter Last ein / Boot-Loop / Reset)
Wenn eine Schiene im Ruhezustand nominal ist, aber beim Start des SoC einbricht (`raw_sources/wrench-board/api/agent/seed_data/global_playbooks/pmic-rail-collapse.json`):

| Schritt | Messziel (`target`) | Messart | Nominalwert | Gültiger Bereich (`pass_range`) | Diagnose-Begründung (`rationale`) |
|---|---|---|---|---|---|
| **1** | `VDDMAIN` (Ruhezustand) | Numerisch (`V`) | `0,80 V` | **`0,78 – 0,82 V`** | Schiene im Ruhezustand (vor SoC-Boot) messen. |
| **2** | `SOC_RESET_N` | Boolean | `true` | **`true`** | Reset wird freigegeben $\rightarrow$ SoC beginnt Strom zu ziehen. |
| **3** | `VDDMAIN_LOADED` (1 s nach Boot) | Numerisch (`V`) | `0,80 V` | **`0,75 – 0,82 V`** | **Spannungseinbruch (`Sag`) $> 50\text{ mV}$** beweist ein schwaches PMIC, defekte Ausgangs-Entkopplungskondensatoren oder einen Kurzschluss, der erst über ein `EN`-Signal zugeschaltet wird. |
| **4** | `PMU_TEMP` (5 s nach Boot) | Numerisch ($^\circ\text{C}$) | `35 °C` | **`25 – 50 °C`** | Wärmebild auf PMIC 5 s nach Einschalten: **$> 60\ ^\circ\text{C}$** deutet auf internen FET-Schaden oder massive Überlast hin. |

<a id="sec-47"></a>
### 2.3 Playbook `usb-no-charge` (Kein Ladestrom über USB)
Diagnose des USB-Ladepfads (`raw_sources/wrench-board/api/agent/seed_data/global_playbooks/usb-no-charge.json`):

| Schritt | Messziel (`target`) | Messart | Nominalwert | Gültiger Bereich (`pass_range`) | Diagnose-Begründung (`rationale`) |
|---|---|---|---|---|---|
| **1** | `VBUS` | Numerisch (`V`) | `5,0 V` | **`4,5 – 5,5 V`** | USB-Eingangsspannung hinter der Buchse prüfen. |
| **2** | `USB_DP` (`D+` Datenleitung) | Numerisch (`V`) | `0,6 V` | **`0,4 – 3,3 V`** | `D+` Ruhespannung prüft, ob die Datenleitungen für die Lade-Signatur/Enumeration frei sind (nicht durch ESD-Diode gegen `GND` geklemmt). |
| **3** | `CHG_EN` | Boolean | `true` | **`true`** | Enable-Signal des Charger-ICs muss aktiv sein. |
| **4** | `VBAT` | Numerisch (`V`) | `3,7 V` | **`3,0 – 4,4 V`** | Fehlt die Ladespannung an der Batterie trotz `VBUS` und `CHG_EN` $\rightarrow$ Charger-IC tot oder `BATFET`-Pfad offen. |

---

<a id="sec-48"></a>
## 3. Power Sequencing, Reset-, Watchdog-, Takt- & Boot-Architektur

<a id="sec-49"></a>
### 3.1 Boot-Phasen-Klassifikation (`raw_sources/wrench-board/api/pipeline/schematic/boot_analyzer.py`)
1. **`always-on`:** Standby-Schienen (z. B. `+3V3_STANDBY`, `LPC_VCC`), Batterie-Management und Supervisor-ICs. Sie laufen an, sobald physikalische Eingangsspannung anliegt, ohne dass ein aktives `EN`-Signal eines Controllers nötig ist (höchstens ein fester Widerstandsteiler an `VIN`).
2. **`sequenced`:** Schienen, die durch einen Sequencer (`sequencer_refdes` = MCU/PMIC/EC/LPC, der $\ge 3$ `*_PWR_EN`-Leitungen steuert) oder eine **Power-Good-Kaskade** (`PG_5V` $\rightarrow$ `EN_3V3` $\rightarrow$ `EN_1V2`) nacheinander freigeschaltet werden.
   - **Wichtige Diagnose-Regel:** Eine Schiene kann volle Eingangsspannung am Regler-IC haben (`power available`), bleibt aber bei `0 V`, weil ihr `enable_net` aus einer vorherigen Boot-Phase fehlt!
3. **`on-demand`:** Schienen, die erst asynchron durch Software/Treiber oder Stecker-Ereignisse eingeschaltet werden (z. B. `PCIE1_PWR`, `USB_VBUS`, Audio-Codec, Display-Backlight `EDP_BL_EN`). Ein Wert von `0 V` direkt nach dem Einschalten ist hier **kein** Hardwaredefekt!

<a id="sec-50"></a>
### 3.2 Reset-Management & Watchdog-Timer (`raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Reset_Management.md` & `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Watchdog_Timers.md`)
- **Reset-Zeitablauf:**
  `Power Applied → Voltage Stabilization (typ. 50–100 ms) → Power Good Check → Reset Release (nRST High) → Clock Settling (typ. 10–50 ms) → Application Start`
- **Reset-Ursachen (`RCC->CSR` Flags bei ARM Cortex-M / STM32):**
  - `PORRSTF` (Power-On / Power-Down Reset), `BORRSTF` (Brownout Reset bei Spannungseinbruch), `PINRSTF` (Externer Reset-Pin `NRST`), `WWDGRSTF` / `IWDGRSTF` (Window-/Independent-Watchdog-Timeout bei Software-Hänger oder fehlendem Takt), `SFTRSTF` (Software-Reset).
- **Hardware-Fehlermuster an der Reset-Leitung (`nRST` / `RESET_N`):**
  1. *Dauer-Reset (`nRST = 0 V` trotz stabiler `VCC`):* Externer Reset-Taster hat Kurzschluss/Feuchtigkeit, Entstörkondensator ($100\text{ nF}$) am Reset-Pin ist kurzgeschlossen, oder ein externer Supervisor-IC hält `nRST` unten, weil eine überwachte Nebenschiene unterhalb ihrer Schwelle liegt.
  2. *Zyklisches Pulsieren am `nRST`-Pin alle paar Millisekunden/Sekunden:* Der Prozessor startet, stürzt aber sofort ab (z. B. wegen defektem Flash/EEPROM, Spannungseinbruch beim PLL-Hochlauf oder nicht gefüttertem Hardware-Watchdog), woraufhin der Watchdog permanent Reset-Impulse auslöst.

<a id="sec-51"></a>
### 3.3 Takterzeugung (`raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Clock_Management.md` & `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Clock_Distribution.md`)
- **Taktquellen:**
  - `HSI` / `MSI` / `LSI`: Interne RC-Oszillatoren (starten sofort nach Reset, ungenau $\pm 1\text{–}5\ \%$).
  - `HSE` ($4\text{–}48\text{ MHz}$ Systemquarz) & `LSE` ($32{,}768\text{ kHz}$ Uhrenquarz): Externe Schwingquarze.
  - `PLL` (Phase-Locked Loop): Vervielfacht den Eingangstakt ($f_{\text{out}} = f_{\text{in}} \cdot \frac{N}{M \cdot P}$).
- **Typisches Quarz-Fehlerbild:** Viele Mikrocontroller starten im Bootcode zunächst mit dem internen `HSI`-Takt, schalten dann auf `HSE` + `PLL` um und warten in einer Endlosschleife auf das Ready-Bit (`while (!(RCC->CR & RCC_CR_HSERDY))`). Ist der externe Quarz durch Sturz gebrochen oder einer der beiden Lastkondensatoren (`tank`, typ. $8\text{–}22\text{ pF}$ `C0G`) defekt (`open` oder `short`), bleibt die Firmware exakt in dieser Schleife hängen – das Display bleibt dunkel!

<a id="sec-52"></a>
### 3.4 Boot-Pins, Strapping-Widerstände & Service-/Flash-Schalter
- **Funktionsweise:** Prozessoren (z. B. `STM32` über `BOOT0`/`BOOT1`, `ESP32` über `GPIO0`/`GPIO12`, `i.MX`/SoCs über `BOOT_MODE`-Pins) und Präzisionsmessgeräte (Laborwaagen mit **Service-/Kalibrier-/Flash-Schalter** auf oder nahe der Hauptplatine) tasten beim steigenden Übergang von `nRST` die Strapping-Pegel ab.
- **Praxis-Falle:** Ein versehentlich beim Reinigen/Transport verstellter oder korrodierter **Service-/Flash-Schalter** (bzw. ein hochohmiger `pull_down`-Widerstand an `BOOT0`) legt den Pin auf `High`. Der Prozessor springt in den internen **ROM-Bootloader** und wartet stumm auf serielle Flash-Befehle (`UART`/`USB-DFU`). Alle Spannungen (`12 V`, `5 V`, `3,3 V`) sind zu 100 % vorhanden, kein Bauteil wird heiß, aber das Gerät zeigt keinerlei Anzeige!

---

<a id="sec-53"></a>
## 4. Thermische Fehlerkaskaden & BGA-Lift-Diagnose

<a id="sec-54"></a>
### 4.1 Die 3 Thermal-Cascade-Archetypen (`raw_sources/wrench-board/api/agent/seed_data/global_patterns/thermal-cascades.md`)
> [!WARNING]
> **Anti-Pattern Nr. 1 bei der Wärmebild-Diagnose:** Tausche niemals blind das heißeste Bauteil auf der Platine! Das heißeste Bauteil im eingeschwungenen Zustand ist oft das **Opfer (`Victim`)**, nicht der **Täter (`Culprit`)**. Beobachte die Platine zwingend in den **ersten 5 Sekunden nach dem Einschalten**, identifiziere den **allerersten** Hotspot und verfolge dessen Schiene stromaufwärts und stromabwärts.

1. **Archetyp 1 – Charger-IC defekt $\rightarrow$ Batterie-MOSFET überhitzt:**
   - Ein defekter Ladecontroller treibt unkontrolliert Strom durch einen teilweise leitenden/angeschlagenen Batterie-FET. Der FET wird schneller heiß als das Charger-IC. Prüfe zuerst das Gate-Signal vom Charger-IC zum FET!
2. **Archetyp 2 – Buck-Spulensättigung $\rightarrow$ Nachgeschaltetes IC überhitzt:**
   - Eine Speicherdrossel mit Windungsschluss/Sättigung (oder ein durchlegierter High-Side-FET) regelt nicht mehr ab und drückt überhöhte Spannung in die Ausgangsschiene. Die internen Schutz-/Klemmdioden des nachgeschalteten Verbraucher-ICs leiten diese Überspannung ab und verheizen die Differenzleistung.
3. **Archetyp 3 – PMIC-LDO-Kurzschluss $\rightarrow$ Host-SoC drosselt:**
   - Ein Kurzschluss auf einem LDO-Ausgang des PMIC lässt die Versorgung des SoC einbrechen. Das SoC reduziert sofort seinen Takt und bleibt **kühl**, während das PMIC den Kurzschlussstrom verheizt und **kochend heiß** wird.

<a id="sec-55"></a>
### 4.2 BGA-Lift-Archetyp (Abgerissene Lötkugeln unter BGA-ICs) (`raw_sources/wrench-board/api/agent/seed_data/global_patterns/bga-lift-archetype.md`)
- **Signatur:**
  - Sporadische Boot-Ausfälle, stark temperaturabhängig (Gerät läuft nur kalt oder nur warm).
  - Leichter Fingerdruck auf das IC stabilisiert das Gerät vorübergehend.
  - Schnelle differenzielle Busse (`PCIe`, `DDR`, `MIPI`) zeigen Bitfehler oder fallen aus.
- **Typische Ursachen:** Sturzschaden (oft mit kleiner Gehäusedelle nahe dem BGA), zu hohe Temperatur beim Reflow eines Nachbar-ICs (Lot-Voids reißen unter Spannung auf), oder **Underfill-Alterung** bei Geräten $> 3\text{ Jahre}$.
- **Verbindliche 3-stufige Diagnose-Reihenfolge:**
  1. **Finger-Press-Test:** Im eingeschalteten Zustand sanft mit dem Finger auf das verdächtige BGA-IC drücken. Verschwindet das Symptom (oder bootet das Gerät), ist ein BGA-Kontaktproblem belegt.
  2. **Kältespray-Test (`Cold Spray`):** Verdächtige ICs einzeln abkühlen. Kehrt der Fehler exakt beim Wiedererwärmen zurück, ist die thermische Ausdehnung unter dem BGA bestätigt.
  3. **Temperature-Soak ($50\ ^\circ\text{C}$ für 5 Minuten):** Platine gleichmäßig auf $50\ ^\circ\text{C}$ durchwärmen. Tritt der Fehler nur im warmen Zustand auf, dehnt sich das Substrat vom gelifteten BGA-Pad weg.
- **Anti-Pattern:** Ein bloßes Re-Balling ohne Prüfung der Pads unter dem Mikroskop nach dem Abnehmen hält nur kurz, wenn darunter ein Lötstopplack-Riss oder ein angerissenes Kupferpad (`Pad Lift` / `Trace Fracture`) vorliegt!

---

<a id="sec-56"></a>
## 5. Deterministische Simulations- & Hypothesen-Engine (`raw_sources/wrench-board/api/pipeline/schematic/simulator.py` & `raw_sources/wrench-board/api/pipeline/schematic/hypothesize.py`)

<a id="sec-57"></a>
### 5.1 Schwellwerte & Mathematisches `leaky_short`-Modell (`raw_sources/wrench-board/api/pipeline/schematic/simulator.py`, `raw_sources/wrench-board/api/agent/measurement_memory.py`)
- **Spannungstoleranz-Schwellen (`raw_sources/wrench-board/api/pipeline/schematic/engine_params.json`):**
  - `TOLERANCE_OK = 0.90` ($\ge 90\ \%$ von $V_{\text{nom}}$ $\rightarrow$ Verbraucher `on` / Schiene `alive` bis $110\ \%$)
  - `TOLERANCE_UVLO = 0.50` ($50\ \%\text{–}90\ \%$ von $V_{\text{nom}}$ $\rightarrow$ Verbraucher `degraded` / Schiene `anomalous`; $< 50\ \%$ $\rightarrow$ **Under-Voltage Lockout (`UVLO`)**, Verbraucher schaltet ab `dead`!)
  - `CLASSIFY_RAIL_DEAD_THRESHOLD_V = 0.05 V` ($< 50\text{ mV}$ absolut $\rightarrow$ Schiene `dead`, mit Hinweis auf Kurzschluss $\rightarrow$ `shorted`)
  - `CLASSIFY_IC_HOT_CELSIUS = 65.0 °C` ($\ge 65\ ^\circ\text{C}$ $\rightarrow$ Bauteil `hot`)
- **Spannungsteiler-Formel für leckende Kondensatoren (`leaky_short` mit Leckwiderstand $R_{\text{leak}}$ in $\Omega$):**
  Ein Kondensator mit endlichem Leckwiderstand $R_{\text{leak}}$ zieht zusätzlichen Leckstrom, während die $N$ angeschlossenen Verbraucher der Schiene ihren Nennstrom ziehen (geschätzt mit `LEAKY_SHORT_PER_CONSUMER_MA = 50.0 mA` pro Verbraucher):
  $$I_{\text{nom,total}} = \frac{50{,}0\text{ mA} \cdot \max(1, N_{\text{consumers}})}{1000}\ [\text{A}], \qquad R_{\text{eff,consumers}} = \frac{V_{\text{nom}}}{I_{\text{nom,total}}}$$
  $$V_{\text{rail,pct}} = \frac{R_{\text{leak}}}{R_{\text{leak}} + R_{\text{eff,consumers}}} \in [0, 1]$$
  Fällt $V_{\text{rail,pct}}$ durch einen niedrigen Leckwiderstand $R_{\text{leak}}$ unter `TOLERANCE_UVLO` ($0{,}50$), sterben alle nachgeschalteten Verbraucher durch `UVLO`!

<a id="sec-58"></a>
### 5.2 Der 4-Schritt-Kaskaden-Algorithmus (`_cascade` in `raw_sources/wrench-board/api/pipeline/schematic/simulator.py`)
1. **Schritt 1 (`effective_dead`):** Vereinigt alle direkt ausgefallenen Bauteile mit allen Bauteilen, die durch Initialfehler (z. B. offenes Serienbauteil oder `UVLO`) bereits `dead` sind.
2. **Schritt 2 (Direkte Verbraucher-Propagation):** Jedes Bauteil, dessen `power_in`-Pin an einer nicht-stabilen Schiene hängt, deren Quell-IC in `effective_dead` liegt, wird als `dead` markiert.
3. **Schritt 3 (Transitive Rail-Abschaltung `dead_rails`):** Eine Schiene wird als `dead` markiert, wenn:
   - sie durch eine offene Ferritperle / einen offenen Serienwiderstand am `enable_net` zwangsabgeschaltet wurde (`_forced_dead_rails`), **oder**
   - ihr Quell-IC (`source_refdes`) nach Schritt 2 (auch transitiv!) in `dead_components` liegt, **oder**
   - ihr Endzustand `shorted` ist, **oder**
   - ihr Endzustand `degraded` mit einer Spannung $< \text{TOLERANCE\_UVLO}$ ($50\ \%$) ist.
4. **Schritt 4 (Verbraucher toter Schienen):** Alle Verbraucher einer in Schritt 3 als `dead` markierten Schiene werden ebenfalls `dead` (sofern sie keinen lebenden Alternativ-Versorgungspin besitzen).

<a id="sec-59"></a>
### 5.3 Vollständige 38-zeilige Fehler-Kaskaden-Matrix (`_PASSIVE_CASCADE_TABLE` aus `raw_sources/wrench-board/api/pipeline/schematic/hypothesize.py`)

| # | Bauteil-Typ (`kind`) | Funktionale Rolle (`role`) | Fehlermodus (`mode`) | Vorhergesagte Fehlerkaskade (`Cascade Handler`) |Visibility-Multiplikator |
|---|---|---|---|---|---|
| 1 | `passive_r` | `series` | `open` | Nachgeschaltete Schiene & alle ihre Verbraucher tot (`_cascade_series_open`; auf `enable_net`: Regler schaltet nie ein!) | `1.0` |
| 2 | `passive_r` | `series` | `short` | Kein Ausfall / Schiene lebt weiter (`_cascade_passive_alive`) | `1.0` |
| 3 | `passive_r` | `feedback` | `open` | Teiler offen $\rightarrow$ Regler läuft in **Überspannung** (`shorted_rails`), Verbraucher `anomalous` (`_cascade_feedback_open_overvolt`) | `1.0` |
| 4 | `passive_r` | `feedback` | `short` | Teiler kurzgeschlossen $\rightarrow$ Regler schaltet Ausgang ab, Schiene tot (`_cascade_feedback_short_undervolt`) | `1.0` |
| 5 | `passive_r` | `pull_up` | `open` | Signalleitung floatet $\rightarrow$ angeschlossene Signal-Konsumenten `anomalous` (`_cascade_pull_up_open`) | **`0.5`** |
| 6 | `passive_r` | `pull_up` | `short` | Schiene hart mit Signalleitung verbunden / Bus blockiert $\rightarrow$ Rail-Loss (`_cascade_pull_up_short`) | `1.0` |
| 7 | `passive_r` | `pull_down` | `open` | Signalleitung floatet $\rightarrow$ Signal-Konsumenten `anomalous` (`_cascade_pull_up_open`) | **`0.5`** |
| 8 | `passive_r` | `pull_down` | `short` | Kein Rail-Ausfall (`_cascade_passive_alive`) | `1.0` |
| 9 | `passive_r` | `current_sense` | `open` | Strompfad unterbrochen $\rightarrow$ nachgeschaltete Schiene & Verbraucher tot (`_cascade_series_open`) | `1.0` |
| 10 | `passive_r` | `current_sense` | `short` | Shunt überbrückt $\rightarrow$ Schiene lebt, aber Strommessung fehlt (`_cascade_passive_alive`) | `1.0` |
| 11 | `passive_r` | `damping` | `open` | Keine statische Rail-Kaskade (`_cascade_passive_alive`) | `1.0` |
| 12 | `passive_r` | `damping` | `short` | Keine statische Rail-Kaskade (`_cascade_passive_alive`) | `1.0` |
| 13 | `passive_c` | `decoupling` | `open` | Lokale Entkopplung fehlt $\rightarrow$ zugehöriges IC `anomalous` durch Ripple (`_cascade_decoupling_open`) | **`0.5`** |
| 14 | `passive_c` | `decoupling` | `short` | Plattenschluss $\rightarrow$ Schiene `shorted`, Quell-IC `hot`, Folgeschienen `dead` (`_cascade_decoupling_short`) | `1.0` |
| 15 | `passive_c` | `decoupling` | `leaky_short` | Schiene bricht Richtung `GND` ein (`_cascade_decoupling_leaky`) | `1.0` |
| 16 | `passive_c` | `bulk` | `open` | Stützkapazität fehlt $\rightarrow$ versorgtes IC `anomalous` (`_cascade_decoupling_open`) | **`0.5`** |
| 17 | `passive_c` | `bulk` | `short` | Schiene `shorted`, Quell-IC `hot`, Folgeschienen `dead` (`_cascade_decoupling_short`) | `1.0` |
| 18 | `passive_c` | `bulk` | `leaky_short` | Schiene bricht ein (`_cascade_decoupling_leaky`) | `1.0` |
| 19 | `passive_c` | `filter` | `open` | Erhöhter Ripple auf geregelter Schiene $\rightarrow$ IC `anomalous` (`_cascade_filter_cap_open`) | **`0.5`** |
| 20 | `passive_c` | `filter` | `short` | Schiene `shorted`, Quell-IC `hot`, Folgeschienen `dead` (`_cascade_decoupling_short`) | `1.0` |
| 21 | `passive_c` | `ac_coupling` | `open` | AC-Signalpfad unterbrochen $\rightarrow$ Signalempfänger `anomalous` (`_cascade_signal_path_open`) | `1.0` |
| 22 | `passive_c` | `ac_coupling` | `short` | DC-Offset gelangt ungehindert in den Ausgang $\rightarrow$ Empfänger `anomalous` (`_cascade_signal_path_dc`) | `1.0` |
| 23 | `passive_c` | `tank` (Quarz) | `open` | Quarz-Lastkapazität fehlt $\rightarrow$ Oszillator-IC `anomalous` / Frequenzdrift (`_cascade_tank_open`) | `1.0` |
| 24 | `passive_c` | `tank` (Quarz) | `short` | Quarz-Pin nach `GND` kurzgeschlossen $\rightarrow$ Oszillator-IC komplett `dead` (`_cascade_tank_short`) | `1.0` |
| 25 | `passive_c` | `bypass` | `open` | Referenz-/Analog-Bypass fehlt $\rightarrow$ IC `anomalous` (`_cascade_decoupling_open`) | `1.0` |
| 26 | `passive_c` | `bypass` | `short` | Schiene `shorted`, Quell-IC `hot` (`_cascade_decoupling_short`) | `1.0` |
| 27 | `passive_fb` | `filter` | `open` | Durchgebrannte Ferritperle $\rightarrow$ gefilterte Ausgangsschiene & Verbraucher tot (`_cascade_filter_open`) | `1.0` |
| 28 | `passive_fb` | `filter` | `short` | Kein Ausfall (nur HF-Filterwirkung reduziert, `_cascade_passive_alive`) | `1.0` |
| 29 | `passive_d` | `flyback` | `open` | Freilaufdiode offen $\rightarrow$ Induktionsspannungsspitzen (`Kickback`) stören/schädigen Verbraucher (`_cascade_flyback_open`) | `1.0` |
| 30 | `passive_d` | `flyback` | `short` | Dauerstrompfad $\rightarrow$ Schiene `shorted`, Quell-IC `hot`, Folgeschienen `dead` (`_cascade_flyback_short`) | `1.0` |
| 31 | `passive_d` | `rectifier` | `open` | Gleichrichter offen $\rightarrow$ Ausgangsschiene tot (`_cascade_rectifier_open`) | `1.0` |
| 32 | `passive_d` | `rectifier` | `short` | Eingangsschiene wird auf Ausgang gezogen/kurzgeschlossen, Quell-IC `hot` (`_cascade_rectifier_short`) | `1.0` |
| 33 | `passive_d` | `esd` | `open` | Schaltung läuft normal weiter, aber ohne ESD-Schutz (`_cascade_passive_alive`) | `1.0` |
| 34 | `passive_d` | `esd` | `short` | ESD-Diode durchlegiert $\rightarrow$ Signalleitung fest auf `GND` geklemmt, Empfänger `anomalous` (`_cascade_signal_to_ground`) | `1.0` |
| 35 | `passive_d` | `reverse_protection` | `open` | Verpolungsschutzdiode durchgebrannt $\rightarrow$ nachfolgende Schiene tot (`_cascade_series_open`) | `1.0` |
| 36 | `passive_d` | `reverse_protection` | `short` | Schiene läuft weiter (kein Verpolungsschutz mehr, `_cascade_passive_alive`) | `1.0` |
| 37 | `passive_d` | `signal_clamp` | `open` | Kein direkter Ausfall (`_cascade_passive_alive`) | `1.0` |
| 38 | `passive_d` | `signal_clamp` | `short` | Signalleitung geklemmt $\rightarrow$ Empfänger `anomalous` (`_cascade_signal_to_ground`) | `1.0` |

**Ergänzende Transistor-/MOSFET-Rollen (`passive_q`, Phase 4.5 & 4.6 aus `raw_sources/wrench-board/api/pipeline/schematic/hypothesize.py`):**

| `passive_q` Rolle (`role`) | Modus `open` / `stuck_off` (Kanal sperrt dauerhaft) | Modus `short` / `stuck_on` (Drain-Source-Kurzschluss) |
|---|---|---|
| **`load_switch`** (High-Side-Schalter mit `EN`-Gate) | Nachgeschaltete Schiene & Verbraucher tot (`_cascade_q_load_dead`) | Nachgeschaltete Schiene **dauerhaft an (`always_on_rails` / `stuck_on`)**, Verbraucher im Standby aktiv (`_cascade_q_load_stuck_on`) |
| **`level_shifter`** (Pegelwandler z. B. `3V3 ↔ 1V8`) | Bus-Signal wird nicht übertragen $\rightarrow$ Empfänger `anomalous` (`_cascade_q_shifter_signal_broken`) | Bus-Signal klemmt auf einem festen Pegel $\rightarrow$ Empfänger `anomalous` (`_cascade_q_shifter_signal_stuck`) |
| **`inrush_limiter`** (Soft-Start am `VIN`-Eingang) | Nachgeschalteter Hauptregler bekommt keinen Strom $\rightarrow$ tot (`_cascade_q_inrush_rail_dead`) | Schiene startet ohne Soft-Start direkt durch (`_cascade_passive_alive`) |
| **`flyback_switch`** (Schalt-FET am `SW`/`LX`-Knoten eines SMPS) | Schaltregler taktet nicht mehr $\rightarrow$ Ausgangsschiene hinter der Spule `L` ist tot (`_cascade_q_flyback_switch_dead`) | Dauerstrom durch die Induktivität `L` $\rightarrow$ **Eingangsschiene (`PVIN`/`VIN`) kurzgeschlossen**, Quell-IC `hot` (`_cascade_q_flyback_switch_short`) |
| **`cell_protection`** (BMS-Schutz-FET zwischen `BATn` und `BATnFUSED`/`PROT`/`OUT`/`PACK`) | Geschützte Pack-Schiene verliert Spannung, Zell-Tap bleibt live (`_cascade_q_cell_protection_dead`) | Schutzfunktion überbrückt, Schiene bleibt im Normalbetrieb unauffällig (`_cascade_passive_alive`) |
| **`cell_balancer`** (Passiver BMS-Balancing-FET + Bleed-R an `BATn`) | Keine Rail-Kaskade; betroffene Einzelzelle driftet im BMS-Telemetrie-Log (`_cascade_passive_alive`) | Entlädt die betroffene Einzelzelle dauerhaft über den Bleed-Widerstand (`_cascade_passive_alive`) |

<a id="sec-60"></a>
### 5.4 Hypothesen-Scoring, Tie-Breaking & der 50/50-Discriminator-Algorithmus (`raw_sources/wrench-board/api/pipeline/schematic/hypothesize.py`)
1. **Scoring-Formel (`_score_candidate` mit `PENALTY_WEIGHTS = (10, 2)`):**
   $$\text{TP} = (\text{tp}_{\text{comps}} \cdot \text{tp}_{\text{mult}}) + \text{tp}_{\text{rails}}, \qquad \text{FP} = \text{fp}_{\text{comps}} + \text{fp}_{\text{rails}}, \qquad \text{FN} = \text{fn}_{\text{comps}} + \text{fn}_{\text{rails}}$$
   $$\text{Score} = \text{TP} - 10 \cdot \text{FP} - 2 \cdot \text{FN}$$
   - Ein **Widerspruch (`FP`, Gewicht `-10`)** – d. h. die Hypothese sagt vorher, dass eine Schiene tot ist, der Techniker hat sie aber als `alive` gemessen – bestraft eine Hypothese $5\times$ härter als ein **noch nicht erklärtes Symptom (`FN`, Gewicht `-2`)**!
2. **Tie-Break-Prior (`_failure_prior_rank`):**
   - Erklären mehrere Kandidaten auf derselben Schiene einen Kurzschluss mit exakt gleichem Score (z. B. 10 Entkopplungs-MLCCs und 1 teures SoC), gewinnen **passive Bauteile (`kind` beginnt mit `passive`) immer den Tie-Break vor aktiven ICs**, weil ein gerissener MLCC in der Praxis ungleich häufiger die Ursache ist als ein interner IC-Schluss.
3. **Der 50/50-Discriminator-Algorithmus (`_compute_discriminators`):**
   - Liegen $n$ Spitzen-Hypothesen innerhalb von `score_tolerance = 0.01` gleichauf, sucht der Algorithmus nach einer noch nicht gemessenen Schiene oder einem Bauteil (`target`), das in **einigen, aber nicht allen** ($0 < \text{hits} < n$) der führenden Fehlerkaskaden als defekt vorhergesagt wird.
   - Die Ziele werden nach minimalem Abstand zur Hälfte $\left|\text{hits} - \frac{n}{2}\right|$ sortiert: **Eine einzige Messung an diesem Discriminator-Punkt halbiert die Anzahl der verdächtigen Ursachen!**

---

# 03 – Schaltpläne, Platinenlayout, Datenblätter, Netz-Klassifikation und SMD-Codes

Dieses Modul vereint die Methodik zum Lesen von Schaltplänen, das Reverse Engineering ohne Schaltplan, die automatische Netz- und Bauteil-Rollen-Klassifikation aus `raw_sources/wrench-board/api/pipeline/schematic/net_classifier.py` und `raw_sources/wrench-board/api/pipeline/schematic/passive_classifier.py`, Masse- und Signalintegritäts-Konzepte (`AGND`/`DGND`, Impedanzformeln, JTAG/SWD), die Datenblatt-Analyse (`Datasheet-Driven Repair`) aus `raw_sources/theEmbeddedNewTestament.github.io/` sowie den vollständigen SMD-Gehäuse- und Datenblatt-Katalog aus `raw_sources/electronics-datasheets/`.

---

<a id="sec-61"></a>
## 1. Systematisches Lesen von Schaltplänen & Reverse Engineering

<a id="sec-62"></a>
### 1.1 Referenzbezeichner (`RefDes`) & Kompakte Wert-Notation (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Reading_Schematics_Datasheets.md`)
- **Standard-Präfixe:**
  - `R`: Widerstand | `C`: Kondensator | `L`: Induktivität/Spule | `FB`: Ferritperle | `F`: Sicherung
  - `D` / `CR`: Diode, Zener, TVS, LED | `Q` / `T`: Transistor (BJT / MOSFET) | `U` / `IC`: Integrierter Schaltkreis
  - `J` / `P` / `CN` / `X`: Steckverbinder | `Y` / `X` / `XTAL`: Quarz / Oszillator | `TP`: Testpunkt | `K` / `RLY`: Relais
- **Wert-Notation ohne Dezimalpunkt (verhindert Lesefehler bei kopierten Schaltplänen):**
  - *Widerstände:* Buchstabe ersetzt das Komma (`4R7` = $4{,}7\ \Omega$, `R010` = $0{,}01\ \Omega$, `1K2` = $1{,}2\text{ k}\Omega$, `10M` = $10\text{ M}\Omega$).
  - *Kondensatoren:* `10p` = $10\text{ pF}$, `100n` = $100\text{ nF} = 0{,}1\ \mu\text{F}$, `2u2` = $2{,}2\ \mu\text{F}$.

<a id="sec-63"></a>
### 1.2 Die 15 kanonischen Netz-Domänen & Regex-Prioritätsregeln (`raw_sources/wrench-board/api/pipeline/schematic/net_classifier.py`)
Beim Analysieren eines Schaltplans wird jedes Netz einer von 15 funktionalen Domänen zugeordnet. Die **Prüfreihenfolge** ist entscheidend, damit z. B. ein Enable-Signal wie `5V_PWR_EN` nicht fälschlich als `5V`-Spannungsschiene oder `PCIE1_CLK_P` nicht als generischer Takt klassifiziert wird:

| Prio | Domäne (`domain`) | Erkennungs-Muster (Regex / Namenskonvention) | Typische elektrische Eigenschaft (Intakt) |
|---|---|---|---|
| **1** | `ground` | `^(GND\|AGND\|DGND\|PGND\|SGND)(_[A-Z0-9]+)?$` | $0{,}00\text{ V}$ Bezugspotenzial (`< 0,5 Ω` zum Sternpunkt) |
| **2** | `hdmi` | `^HDMI_`, `^TMDS_`, `_CEC$`, `_DDC_`, `^DDC_` | Differenzielle TMDS-Paare, `5 V` DDC/HPD |
| **3** | `usb` | `^USB_`, `USB_DP`, `USB_DM`, `USB_OC`, `USB_VBUS` | `D+/D-` differenziell $90\ \Omega$, `VBUS` $5\text{ V}$ (bzw. USB-PD bis $20\text{ V}$) |
| **4** | `pcie` | `^PCIE_`, `^PCIE\d+_` | High-Speed differenziell + `100 MHz` `REFCLK` |
| **5** | `ethernet` | `^ETH_`, `^RGMII_`, `^MII_`, `^MDIO_`, `^PHY_` | RGMII/MII-Signale + Übertrager |
| **6** | `display` | `^EDP_`, `^DSI_`, `_DSI_`, `^LCD_`, `BACKLIGHT_`, `_BL$`, `LVDS_` | MIPI-DSI / eDP / LVDS + Backlight-Boost-Schiene |
| **7** | `storage` | `^SD_`, `_SD_`, `^EMMC_`, `^SDHC_`, `^MMC_` | `3,3 V` / `1,8 V` CMD/CLK/DAT0..7 |
| **8** | `audio` | `^DAC_`, `^ADC_`, `^I2S_`, `^SPDIF`, `MICBIAS`, `AUDIO_`, `LRCLK`, `BCLK` | I2S-Digitalbus + rauscharme Analog-Rails |
| **9** | `debug` | `^JTAG_`, `^SWD_`, `^UART_`, `^DEBUG_`, `TDO`, `TDI`, `TCK`, `TMS`, `SWDIO`, `SWCLK` | `3,3 V` / `1,8 V` Logik (oft mit Pull-up/Pull-down) |
| **10** | `control` | `^I2C_`, `^SPI_`, `^SDA$`, `^SCL$`, `_SDA$`, `_SCL$` | Open-Drain mit Pull-up (I2C) bzw. Push-Pull (SPI) |
| **11** | `power_seq` | `_PWR_EN$`, `_PG$`, `_EN$`, `POWER_GOOD`, `^PG_`, `^EN_` | **Steuersignale!** Logikpegel (`1,8 V`/`3,3 V`), **keine** Lastschiene! |
| **12** | `reset` | `^RESET$`, `^RESET_`, `_RST$`, `^XRESET$`, `^POR_`, `RESET_N$`, `NRESET$` | Meist aktiv-low (`0 V` = Reset aktiv, `3,3 V`/`1,8 V` = Run) |
| **13** | `power_rail` | `^\+?\d+V\d*`, `VIN`, `VOUT`, `VCC`, `VDD`, `VBUS`, `AVDD`, `DBVDD`, `DCVDD`, `SPKVDD`, `INTVCC`, `BAT\d*`, `PVIN` | Echte DC-Versorgungsschienen (mit Suffixen `_STANDBY`, `_AUX`, `_IN`, `_OUT`) |
| **14** | `clock` | `^CLK_`, `_CLK$`, `XTAL_`, `OSC_`, `REFCLK` | Periodisches Taktsignal (mit `10:1`-Tastkopf prüfen!) |
| **15** | `misc` | Alle übrigen internen Koppel-Netze | Kontextabhängig über verbundene IC-Pins prüfen |

<a id="sec-64"></a>
### 1.3 Topologie-Heuristiken zur Bauteil-Rollen-Erkennung (`raw_sources/wrench-board/api/pipeline/schematic/passive_classifier.py`)
Auch ohne Bauteilwert im Schaltplan oder beim Reverse Engineering auf der Platine lässt sich die exakte funktionale Rolle (`role`) eines Bauteils deterministisch aus seinen Pin-Verbindungen ableiten:

1. **Widerstände (`passive_r`):**
   - **`feedback`:** Ein Pin liegt am `FB`- (`feedback_in`-)Pin eines Regler-ICs, der andere an einer Power-Rail oder `GND`.
   - **`pull_up`:** Pin 1 liegt an einer Power-Rail (`+3V3`, `+1V8`), Pin 2 an einem Signalnetz (nicht `GND`, keine Rail).
   - **`pull_down`:** Pin 1 liegt an einem Signalnetz (oder einer Rail), Pin 2 an `GND`.
   - **`series`:** Pin 1 liegt an einer Power-Rail, Pin 2 führt direkt zum `power_in`-Pin eines ICs oder zu einer abgeleiteten Sub-Rail.
   - **`current_sense`:** Niederohmiger Widerstand ($< 1\ \Omega$) in Serie auf einer Hauptstromschiene, meist mit zwei Sense-Leitungen zu einem Regler/INA-Messverstärker.
   - **`damping`:** Beide Pins liegen an Signalnetzen (weder Power-Rail noch `GND`, oft $10\text{–}33\ \Omega$ in Takt-/USB-/SPI-Leitungen).
2. **Kondensatoren (`passive_c`):**
   - **`decoupling` / `bulk`:** Pin 1 an Power-Rail, Pin 2 an `GND`, räumlich direkt am `VCC`-Pin eines Verbraucher-ICs (`decoupling` typ. $100\text{ nF}$–$1\ \mu\text{F}$; `bulk` $> 10\ \mu\text{F}$).
   - **`filter`:** Zwischen einer geregelten Ausgangsschiene und `GND` direkt hinter einem Regler/LC-Filter.
   - **`ac_coupling`:** Beide Pins liegen an Signalnetzen (weder Power-Rail noch `GND`; z. B. PCIe/HDMI/Audio-Koppelkondensatoren).
   - **`tank`:** Pin 1 an `GND`, Pin 2 am `clock_out` / `XTAL`-Pin eines Quarzes oder Oszillators (typ. $8\text{–}22\text{ pF}$).
3. **Dioden (`passive_d`):**
   - **`flyback`:** Liegt exakt parallel zu den beiden Netzen einer Speicherdrossel (`L`) bzw. zwischen `SW` und `GND`/`VOUT`.
   - **`esd`:** Ein Pin an `GND`, der andere an einem Signalnetz (am Stecker/Port).
   - **`rectifier` / `reverse_protection`:** Liegt zwischen zwei Power-Rails (Wandlung bzw. Verpolungsschutz in Serie zum Eingang).
4. **Transistoren / MOSFETs (`passive_q` – Prioritäts-Entscheidungsbaum):**
   - **Regel 0 (`flyback_switch`):** Ein Pin liegt an einem Schaltknoten (`SW`, `LX`, `PHASE`), ein weiterer an `GND` oder einer Eingangs-Rail (`VIN`, `PVIN`, `+12V`, `BAT`).
   - **Regel 0.5 (`cell_protection`):** Mindestens 2 verschiedene Batterie-Netze (`^BAT|VBAT|CHGBAT|CELL\d*(FUSED|PROT|RAW|OUT|PACK)?$`), **kein** Pin an `GND`.
   - **Regel 0.6 (`cell_balancer`):** Exakt dasselbe `BAT`-Netz an $\ge 2$ Pins (durch zusammengefassten Bleed-Widerstand), kein fremdes Steuernetz.
   - **Regel 1 (`inrush_limiter`):** Liegt zwischen einer Haupteingangsschiene (`VIN`, `BAT`, `+12V`, `+24V`) und einer internen Schiene mit Verbrauchern; Gate an einem RC-Glied / `SOFT_START`.
   - **Regel 2 (`load_switch`):** Liegt zwischen zwei Power-Rails (Source = Upstream, Drain = Downstream); Gate an einem Steuernetz mit `EN`, `_PWR_EN`, `POWER` oder `_CTRL`.
   - **Regel 3 (`level_shifter`):** Liegt zwischen zwei Signalnetzen unterschiedlicher Spannungsdomänen (z. B. `I2C_SDA_3V3` und `I2C_SDA_1V8`), Gate liegt fest an der niedrigeren Versorgungsschiene.

<a id="sec-65"></a>
### 1.4 Board-Level Reverse Engineering ohne Schaltplan
1. **Masse (`GND`) kartieren:** Große Kupferflächen (`Copper Pours`), Metallkragen von USB-/HDMI-Buchsen, Schraublöcher und Kondensator-Pads mit **Thermal-Relief-Stegen** (4 schmale Kupferbrücken zum Pad, damit die Massefläche beim Löten die Wärme nicht sofort abzieht) als Referenz markieren.
2. **Versorgungsschienen vom Stecker aus verfolgen:** Große Elkos, Tantals und Speicherdrosseln (`L`) markieren jeweils eine eigene Spannungsschiene.
3. **IC-Nummern ablesen & Applikationsschaltung nutzen:** Für jeden Regler- und Schnittstellen-IC das Datenblatt öffnen – die `Typical Application Circuit` im Datenblatt entspricht in ~90 % der Fälle der realen Beschaltung auf der Platine!

---

<a id="sec-66"></a>
## 2. Masse-Konzepte, Signalintegrität & PCB-Layout (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/PCB_Design_Considerations.md`, `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Signal_Integrity_Basics.md`, `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/EMI_EMC_Considerations.md`)

<a id="sec-67"></a>
### 2.1 Trennung von `AGND`, `DGND`, `PGND` und `Chassis GND`
- **`DGND` (Digital Ground):** Rückstrompfad für schnelle Digitalschaltungen (SoC, MCU, RAM). Durch steile Schaltflanken ($\Delta I / \Delta t$) entstehen an jeder Leitungsinduktivität Spannungsspitzen ($U = L \cdot \frac{\text{d}i}{\text{d}t}$, *Ground Bounce*).
- **`AGND` (Analog Ground):** Störungsfreier Bezugspunkt für Präzisions-ADCs, Wägezellen-Vorverstärker (`AD620`, `ADA4530`), Sensoren und Spannungsreferenzen.
- **`PGND` (Power Ground):** Hochstrom-Rückpfad für Schaltregler-MOSFETs und Endstufen.
- **`Chassis GND` / `PE`:** Metallgehäuse und Kabelschirme zur Ableitung von ESD-Impulsen.
- **Das Sternpunkt-Gesetz (`Star Ground`):** `AGND`, `DGND` und `PGND` werden auf der Platine räumlich getrennt geführt, müssen aber **an genau einem definierten Sternpunkt** (meist direkt unter dem A/D-Wandler oder am Haupt-Elko über eine `0R`-Brücke, einen Net-Tie oder eine Ferritperle) niederohmig verbunden sein!
  - **Häufiger Reparaturfehler:** Brennt der `0R`-Verbindungswiderstand oder die Ferritperle zwischen `AGND` und `DGND` durch, „schwimmt“ (`floats`) der gesamte Analogteil gegenüber der Digitalmasse $\rightarrow$ der ADC liefert nur noch Vollausschlag, Null oder stark driftende Zufallswerte (klassischer Fehler bei Feinwaagen und Multimetern!).

<a id="sec-68"></a>
### 2.2 Wellenwiderstand (Impedanz) & Signalintegrität auf Leiterplatten
Bei hohen Frequenzen bzw. steilen Anstiegszeiten ($t_{\text{rise}} < 1\text{ ns}$) wirken Leiterbahnen als Wellenleiter (`Transmission Lines`):

1. **Microstrip-Leitung (Außenlage über durchgehender `GND`-Plane):**
   $$Z_0 \approx \frac{87}{\sqrt{\varepsilon_r + 1{,}41}} \cdot \ln\left(\frac{5{,}98 \cdot h}{0{,}8 \cdot w + t}\right)\ [\Omega]$$
2. **Stripline-Leitung (Innenlage symmetrisch zwischen zwei `GND`-Planes):**
   $$Z_0 \approx \frac{60}{\sqrt{\varepsilon_r}} \cdot \ln\left(\frac{4 \cdot h}{0{,}67 \cdot \pi \cdot w}\right)\ [\Omega]$$
3. **Differenzielles Leitungspaar (`USB`, `HDMI`, `PCIe`, `LVDS`, `CAN` mit Kopplungsfaktor $k$):**
   $$Z_{\text{diff}} = 2 \cdot Z_{\text{single}} \cdot \frac{1 - k^2}{1 + k^2}\ [\Omega]$$
   - **Reparatur-Regel für Flickdrähte (`Jumper Wires`):** Bei abgerissenen Leiterbahnen auf `USB 2.0/3.0` ($Z_{\text{diff}} = 90\ \Omega$), `HDMI`/`PCIe` ($100\ \Omega$) oder `Ethernet` ($100\ \Omega$) müssen beide Adern (`D+` und `D-`) **gleich lang (`Length Matching`), eng parallel geführt** und ohne dicke Lötzinn-Verdickungen (`Impedance Stubs`) geflickt werden, sonst führen Reflexionen zum Verbindungsabbruch!

<a id="sec-69"></a>
### 2.3 JTAG / Boundary-Scan & SWD-Debug-Schnittstellen (`raw_sources/theEmbeddedNewTestament.github.io/Debugging/JTAG_SWD_Debugging.md`)
- **JTAG (IEEE 1149.1, 4/5-Pin):** `TCK` (Test Clock), `TMS` (Test Mode Select), `TDI` (Test Data In), `TDO` (Test Data Out), optional `TRST` (Test Reset) + `VTref` (`VCC`-Referenz für den Debugger) und `GND`.
  - Über **Boundary Scan** lassen sich an BGA-Chips (FPGAs, SoCs) einzelne Pins ohne physischen Tastkopf-Zugriff auf Kurzschluss oder Unterbrechung testen!
- **SWD (Serial Wire Debug, ARM 2-Pin-Alternative):** `SWDIO` (bidirektionale Daten) + `SWCLK` (Takt) + `VTref` + `GND` + `nRST`.
  - **Diagnose-Tipp:** Meldet der `ST-Link` / `J-Link` `No Target Connected`, zuerst `VTref` am Debug-Header messen (`3,3 V`), dann prüfen, ob `nRST` auf Low klemmt oder `SWDIO`/`SWCLK` durch eine defekte ESD-Diode nach `GND` gezogen werden.

---

<a id="sec-70"></a>
## 3. Datasheet-Driven Repair, Design-Margen & Temperaturklassen

<a id="sec-71"></a>
### 3.1 Die 4 Pflicht-Sektionen jedes Datenblatts (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Reading_Schematics_Datasheets.md`)
1. **`Pin Configuration & Functions`:** Identifiziere Pin 1, Versorgung (`VCC`/`VDD`/`PVIN`), Masse (`GND`/`PGND`/`Exposed Pad`), Freigabe (`EN`/`SHDN`), Feedback (`FB`/`ADJ`), Schaltausgang (`SW`/`LX`) und Status (`PG`/`FAULT`).
2. **`Absolute Maximum Ratings` (Die Zerstörungsgrenze):**
   - Überschreitet eine Spannung (auch nur kurzzeitig durch einen defekten Vorregler!) das *Absolute Maximum Rating*, ist das Bauteil physikalisch durchgeschlagen.
   - **Industrielle Design-Margen (Derating-Regeln für zuverlässigen Ersatz):**
     - **Spannung:** Mindestens **$20\text{–}30\ \%$ Sicherheitsabstand** unter Maximum (bei sicherheitskritischen Systemen und Elkos/Tantals **$30\text{–}50\ \%$**!).
     - **Dauerstrom:** Maximal **$50\ \%$** des absoluten Grenzstroms im Dauerbetrieb.
     - **Leistung:** Maximal **$70\ \%$** der Nennverlustleistung.
     - **Temperatur:** Mindestens **$20\ ^\circ\text{C}$** Abstand unter $T_{J,\text{max}}$ ($125\ ^\circ\text{C}$ bzw. $150\ ^\circ\text{C}$).
3. **`Electrical Characteristics` & Feedback-Formel:**
   - Suche nach **`Feedback Voltage` ($V_{\text{FB}}$ / $V_{\text{REF}}$)**. Damit lässt sich an jedem einstellbaren LDO oder Schaltregler die Soll-Ausgangsspannung aus den beiden eingelöteten SMD-Widerständen ($R_1$ von `VOUT` nach `FB`, $R_2$ von `FB` nach `GND`) berechnen:
     $$V_{\text{OUT}} = V_{\text{REF}} \cdot \left(1 + \frac{R_1}{R_2}\right)$$
     *(Gängige Referenzspannungen: `LM317` / `AMS1117-ADJ` = $1{,}25\text{ V}$; klassische Buck-Regler = $0{,}80\text{ V}$ oder $0{,}60\text{ V}$.)*
4. **`Typical Application Circuit`:** Liefert die exakten Bauteilwerte für fehlende/abgerissene SMD-Nachbarbauteile.

<a id="sec-72"></a>
### 3.2 Temperatur- und Qualitätsklassen (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Component_Selection.md`)
Ein häufiger Fehler bei der Reparatur ist der Einbau eines billigen Commercial-Grade-Bauteils in eine heiße Industrie- oder Kfz-Umgebung:

| Qualitätsklasse (`Grade`) | Temperaturbereich | Qualifikationsnorm / Einsatzgebiet |
|---|---|---|
| **Commercial Grade** | **$0\ ^\circ\text{C}\text{ bis }+70\ ^\circ\text{C}$** | Büro-, Haushalts- und Consumer-Elektronik |
| **Industrial Grade** | **$-40\ ^\circ\text{C}\text{ bis }+85\ ^\circ\text{C}$** | Industriesteuerungen, Netzteile, Außengeräte |
| **Automotive Grade** | **$-40\ ^\circ\text{C}\text{ bis }+125\ ^\circ\text{C}$** (teils $+150\ ^\circ\text{C}$) | **`AEC-Q100`** (ICs), **`AEC-Q200`** (Passive) – Kfz & hohe Zuverlässigkeit |
| **Military / Aerospace** | **$-55\ ^\circ\text{C}\text{ bis }+125\ ^\circ\text{C}$** | `MIL-STD` / `DO-160` – Luft-/Raumfahrt & Verteidigung |

---

<a id="sec-73"></a>
## 4. SMD-Gehäuseformen & Pinout-Fallen

<a id="sec-74"></a>
### 4.1 Passive SMD-Bauformen (Imperial vs. Metrisch)

| Imperial-Code | Metrisch (mm) | Abmessungen ($L \times B$) | Typische Nennleistung (Widerstand) | Typische Maximalspannung |
|---|---|---|---|---|
| **01005** | 0402 | $0{,}4 \times 0{,}2\text{ mm}$ | $0{,}031\text{ W}$ ($1/32\text{ W}$) | $15\text{ V}$ |
| **0201** | 0603 | $0{,}6 \times 0{,}3\text{ mm}$ | $0{,}05\text{ W}$ ($1/20\text{ W}$) | $25\text{ V}$ |
| **0402** | 1005 | $1{,}0 \times 0{,}5\text{ mm}$ | $0{,}063\text{ W}$ ($1/16\text{ W}$) | $50\text{ V}$ |
| **0603** | 1608 | $1{,}6 \times 0{,}8\text{ mm}$ | $0{,}10\text{ W}$ ($1/10\text{ W}$) | $75\text{ V}$ |
| **0805** | 2012 | $2{,}0 \times 1{,}25\text{ mm}$ | $0{,}125\text{ W}$ ($1/8\text{ W}$) | $150\text{ V}$ |
| **1206** | 3216 | $3{,}2 \times 1{,}6\text{ mm}$ | $0{,}25\text{ W}$ ($1/4\text{ W}$) | $200\text{ V}$ |
| **1210** | 3225 | $3{,}2 \times 2{,}5\text{ mm}$ | $0{,}50\text{ W}$ ($1/2\text{ W}$) | $200\text{ V}$ |
| **2010** | 5025 | $5{,}0 \times 2{,}5\text{ mm}$ | $0{,}75\text{ W}$ ($3/4\text{ W}$) | $200\text{ V}$ |
| **2512** | 6332 | $6{,}3 \times 3{,}2\text{ mm}$ | $1{,}00\text{ W}$ ($1\text{ W}$) | $200\text{–}500\text{ V}$ |

<a id="sec-75"></a>
### 4.2 Aktive SMD-Gehäuseformen & die gefährliche Regler-Pinout-Falle

| Gehäuseform | Pin-Anzahl | Typische Bauteile | Pin-1-Zählung & Kritische Pinout-Fallen |
|---|---|---|---|
| **SOD-123 / SOD-323 / SOD-523** | 2 | Kleinsignal-, Schottky- & Zener-Dioden | Markierungsbalken = **Kathode (`-`)**. |
| **SMA / SMB / SMC (`DO-214`)** | 2 | Gleichrichter, Freilauf- & TVS-Dioden | `SMA` ($4{,}3\times 2{,}6\text{ mm}$), `SMB` ($4{,}3\times 3{,}6\text{ mm}$), `SMC` ($6{,}9\times 5{,}9\text{ mm}$). Balken = Kathode. |
| **SOT-23-3 (`TO-236`)** | 3 | BJT, MOSFET (`2N7002`), Doppeldiode (`BAV99`), LDO | Unten links = Pin 1, unten rechts = Pin 2, oben Mitte = Pin 3. **Standard BJT/MOSFET:** `1 = Basis/Gate`, `2 = Emitter/Source`, `3 = Kollektor/Drain`. |
| **SOT-23-5 / SOT-23-6** | 5 / 6 | LDOs, kleine Buck-Regler, Einzel-OpAmps | Punkt/Laser-Linie markiert Pin 1; Zählung **gegen den Uhrzeigersinn**. |
| **SOT-89 / SOT-223** | 3 + Kühl-Tab | Linearregler (`AMS1117`, `78L05`, `78M05`), Mittelstrom-BJT | Der große Kühl-Tab oben ist elektrisch immer mit dem mittleren Pin (**Pin 2**) verbunden! |
| **TO-252 (`DPAK`) / TO-263 (`D2PAK`)** | 2/3 + Tab | Leistungs-MOSFETs, Schaltregler, LDOs | Mittlerer Stummelpin fehlt oft, weil der große verlötete Kühl-Tab bereits **Pin 2 (`Drain` bzw. `GND`/`VOUT`)** ist. |
| **SOIC-8 / TSSOP / MSOP** | 8–28 | OpAmps (`LM358`, `AD620`), EEPROMs (`AT24C02`, `AT93C46`), Buck-Controller | Abgeschrägte Längskante, Kerbe oder Punkt markiert Pin 1. |
| **QFP / LQFP / TQFP** | 32–144+ | Mikrocontroller (`STM32F103C8`, `ATmega328P`), CPLDs | Punkt in einer Ecke = Pin 1; Zählung ringsum gegen den Uhrzeigersinn. |
| **QFN / DFN / WLCSP / BGA** | 6–500+ | PMICs, moderne SoCs, Sensoren (`VL53L0X`, `BMP180`) | Lötflächen unter dem Gehäuse; mittleres **Thermal Pad** bei QFN meist zwingend mit `GND` verlöten! |

> [!WARNING]
> **Die tödliche Spannungsregler-Pinout-Falle bei `SOT-223` / `SOT-89` / `TO-252`:**
> Linearregler verschiedener Familien im selben Gehäuse haben **komplett vertauschte Pins**! Prüfe vor dem Einlöten immer auf der Platine, welcher Pin Durchgang zu `GND` hat:
> - **`AMS1117` / `LM1117` / `LD1117` / `LM317`:** `Pin 1 = GND / ADJ` · **`Pin 2 (Tab) = VOUT`** · `Pin 3 = VIN`
> - **`7805` / `78M05` / `L78xx` (DPAK/TO-220):** `Pin 1 = VIN` · **`Pin 2 (Tab) = GND`** · `Pin 3 = VOUT`
> - **`78L05` (SOT-89 / TO-92):** `Pin 1 = VOUT` · **`Pin 2 (Tab) = GND`** · `Pin 3 = VIN`

---

<a id="sec-76"></a>
## 5. SMD-Markierungscodes & Lokaler Datenblatt-Katalog (`raw_sources/electronics-datasheets/`)

<a id="sec-77"></a>
### 5.1 Nutzung des lokalen SMD-Codebooks (`raw_sources/electronics-datasheets/smd-codebook.pdf`)
- Auf kleinen SMD-Halbleitern (`SOT-23`, `SOT-323`, `SOD-323`, `SOT-89`) ist aus Platzgründen nicht die Teilenummer (z. B. `MMBT3904`), sondern ein **2- bis 4-stelliger SMD-Marking-Code** (z. B. `1A` oder `1AM`) aufgedruckt.
- **Vorgehen zur Identifikation:**
  1. **Device-Code vom Date-/Lot-Code trennen:** Die ersten 2–3 großen Zeichen sind der Bauteil-Code; ein einzelnes kleineres, um $90^\circ$ gedrehtes oder tiefgestelltes Zeichen am rechten Rand sowie Über-/Unterstriche sind meist Herstellungsmonat/Werk.
  2. **Gehäuseform exakt abmessen** (`SOT-23` = $2{,}9\times 1{,}3\text{ mm}$ vs. `SOT-323 / SC-70` = $2{,}0\times 1{,}25\text{ mm}$): Derselbe Code `1A` kann in verschiedenen Gehäusen unterschiedliche Bauteile bedeuten!
  3. **Pin-Verbindungen auf der Platine prüfen** (welcher Pin geht an `GND`, welcher an `VCC`?) und im lokalen Nachschlagewerk `raw_sources/electronics-datasheets/smd-codebook.pdf` nach Code + Gehäuseform abgleichen.

<a id="sec-78"></a>
### 5.2 Vollständiges Verzeichnis der lokalen Offline-Datenblätter (`raw_sources/electronics-datasheets/`)
Nach Aktivierung von `git config core.longpaths true` stehen im lokalen Archiv `raw_sources/electronics-datasheets/` über **330 Original-Datenblätter** in 15 Fachordnern offline bereit:

| Ordner in `raw_sources/electronics-datasheets/` | Anzahl Dateien | Wichtigste enthaltene Bauteilfamilien & Referenz-PDFs |
|---|---|---|
| **`smd-codebook.pdf`** | 1 | Komplettes SMD-Code-Nachschlagewerk (Codes, Typen, Gehäuse, Pinouts) |
| **`Diodes/`** (+ `Bridges/`) | 46 | Standard-Gleichrichter (`1N4001–1N4007`, `1N5400–1N5408`, `6A10`, `RL201–RL207`), Kleinsignal (`1N4148`), Zener 1W/5W (`1N4728–1N4764`, `1N5333B–1N5388B`), Schottky (`1N5711`, `1N5844`, `SBL2000`, `SBL2045CT`, `B20H100G`), Fast/Ultrafast (`1N4933–1N4937`, `UF4000`, `UF5400`, `BYV95`, `BYW95`, `PR1001–PR3007`), Brückengleichrichter (`GBL005–GBL10`, `2KBP08M`) |
| **`ICs/`** | 141 | Logik-Gatter (`74AC00/04/14`, `74HC245/595/4050`, `74LVC00A/14A`, `CD4017/4042`), Präzisions-/Instrumenten-OpAmps (`AD620`, `AD712`, `ADA4530`, `LM358`, `LM324`, `TL072/082`, `NE5532`), Komparatoren (`AD790`, `LM339`, `LM393`), Spannungsregler & Referenzen (`AN78XX`, `LM317`, `TL431`, `UC3842/3843`), Speicher (`AT45DB041B` Flash, `AT93C46` EEPROM), Schnittstellen (`ADM232`, `MAX232`), Timer (`NE555`) |
| **`Transistors, FETs, Thyristors/`** | 117 | Standard-BJT (`2N2222`, `2N3904`, `BC547/557`, `TIP122`), Japanische Transistoren (`2SB156`, `2SC1050`, `2SC4517`, `2SD1427`, `2SD2137`), SMD-Digital-/Dual-Transistoren (`EMZ1/IMZ1A/UMZ1N`), N-/P-Kanal MOSFETs (`2N7002`, `2SK2043` 600V, `IRFZ44N`, `IRF540`), Thyristoren & Triacs (`BT136`, `BTA16`) |
| **`Sensors/`** | 13 | Hall-Effekt-Sensoren (`A1301/A1302`, `A3141–A3144`, `A3503`, `SS49e`), Drucksensor (`BMP180`), Optische Sensoren (`TCRT5000`, `VL53L0X`/`VL53L1X` Time-of-Flight, `Agilent AEDS-962x` Encoder), Typ-K-Thermoelement |
| **`MCUs/`** | 3 | `ATmega48A/88A/168A/328P` (komplettes AVR-Handbuch), `ATtiny25/45/85`, `STM32F103C8` (ARM Cortex-M3) |
| **`Displays/`** | 6 | 7-Segment-Anzeigen (`LN524RA/GA`, `TLR4172`), `ILI9341` 2.4" SPI-TFT-Display + Adafruit-GFX-Referenz |
| **`FPGA/`** & **`CPLD/`** | 6 | Intel/Altera Cyclone 10 LP (`CYC1000` User Guide, Schaltplan & Arrow USB Programmer Troubleshooting Guide), MAX 7000 (`EPM7032–EPM7256`) |
| **`Bluetooth/`** & **`Radio/`** | 4 | `BLK-MD-BC04-B` Bluetooth-Modul + AT-Befehlssatz, `RBT-001`, `nRF24L01` 2.4-GHz-Transceiver |
| **`LEDs/`**, **`Laser/`**, **`Photodiodes/`**, **`Motors/`**, **`Magnetron/`** | 11 | `5050-RGB-LED`, `M140` 445nm Laserdiode + Pinout, `FDS025` Photodiode, `PM35L-048`/`PM55L-048` Schrittmotoren, `2M319J` Mikrowellen-Magnetron |
