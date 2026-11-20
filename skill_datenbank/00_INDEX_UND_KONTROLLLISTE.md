# 00 – Index und Kontrollliste der Elektronik-Reparatur-Wissensdatenbank

- **Erstellt / Aktualisiert:** 2026-11-20
- **Projektverzeichnis:** `Elektronik_Reparatur_Wissen/`
- **Ziel:** Verlustfreie, vollständige Übertragung aller fachlichen Regeln, Messwerte, Bauteilverhalten, Prüf-Kaskaden, Formeln, Tabellen und Sicherheitswarnungen ins Deutsche.

---

<!-- TOC_START -->
## Inhaltsverzeichnis & Zeilen-Index

| Abschnitt | Ebene | Zeilen |
| :--- | :--- | :---: |
| [1. Übersicht der Zieldateien in `skill_datenbank/`](#sec-1) | Hauptabschnitt | Z. 27–39 |
| [2. Quellen-Bestandsaufnahme & Übertragungs-Kontrollliste](#sec-2) | Hauptabschnitt | Z. 41–42 |
| ↳ [2.1 `raw_sources/wrench-board/`](#sec-3) | Unterabschnitt | Z. 44–90 |
| ↳ [2.2 `raw_sources/theEmbeddedNewTestament.github.io/`](#sec-4) | Unterabschnitt | Z. 92–112 |
| ↳ [2.3 `raw_sources/Repair/` (`aKaReZa75/Repair`)](#sec-5) | Unterabschnitt | Z. 114–120 |
| ↳ [2.4 `raw_sources/electronics-datasheets/` (`Vitorbnc/electronics-datasheets`)](#sec-6) | Unterabschnitt | Z. 122–126 |
| ↳ [2.5 `https://repair.wiki` (Status: Blockiert)](#sec-7) | Unterabschnitt | Z. 128–130 |

---

<!-- TOC_END -->

<a id="sec-1"></a>
## 1. Übersicht der Zieldateien in `skill_datenbank/`

| Nr. | Zieldatei | Inhalt / Schwerpunkt |
|---|---|---|
| 0 | [00_INDEX_UND_KONTROLLLISTE.md](00_INDEX_UND_KONTROLLLISTE.md) | Vollständige Bestandsaufnahme aller Quellen + Übertragungs-Status |
| 1 | [SKILL.md](SKILL.md) | Haupt-Regelwerk für die KI (Anti-Halluzinations-Gesetze, 10 Simulator-Invarianten `INV-1`–`INV-10`, zerstörungsfreie Prüf-Reihenfolge, Mechanik-/ESD-Schutz, Hard-Safety-Substitution, Diagnose-Workflow & Modul-Router) |
| 2 | [01_In_Circuit_Messen_und_Bauteilpruefung.md](01_In_Circuit_Messen_und_Bauteilpruefung.md) | In-Circuit-Messphysik ($\Omega$ vs. Durchgang vs. Diodentest), Parallelschaltung, Ladekurven, Red-Probe-on-Ground, Prüftabellen (Sicherungen, Dioden/TVS, Widerstände inkl. EIA-96, MLCC/Elkos inkl. ESR, Spulen/Ferrite, BJT/MOSFET), Oszilloskop-/Logic-Analyzer-Messtechnik, Löt-Reihenfolge & IPC-A-610D |
| 3 | [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md) | 7-stufige Prüf-Kaskade, Playbooks (`boot-no-power`, `pmic-rail-collapse`, `usb-no-charge`), Power Sequencing, Reset/Quarz/Watchdog/Boot-Schalter, 3 Thermal-Cascade-Archetypen, BGA-Lift-Protokoll, `leaky_short`-Formel, 38-zeilige `_PASSIVE_CASCADE_TABLE` & 50/50-Discriminator-Algorithmus |
| 4 | [03_Schaltplaene_Platinenlayout_und_SMD_Codes.md](03_Schaltplaene_Platinenlayout_und_SMD_Codes.md) | Schaltplanlesen & Reverse Engineering ohne Schaltplan, 15 kanonische Netz-Domänen (`net_classifier`), Bauteil-Rollen-Heuristiken (`passive_classifier`), Masse-Konzepte (`AGND`/`DGND`/`PGND`), Impedanz- & Signalintegritätsformeln, Datenblatt-Analyse & Derating, SMD-Gehäuseformen & kompletter Datenblatt-Katalog (`smd-codebook.pdf` + 15 Bauteil-Ordner) |
| 5 | [KOMPLETTES_HANDBUCH_ELEKTRONIK_DIAGNOSE.md](KOMPLETTES_HANDBUCH_ELEKTRONIK_DIAGNOSE.md) | Verlustfreie Gesamtausgabe (Datei 1 bis 4) in einem Master-Dokument (deterministisch erzeugt via [scripts/build_handbuch.py](scripts/build_handbuch.py)) |

---

<a id="sec-2"></a>
## 2. Quellen-Bestandsaufnahme & Übertragungs-Kontrollliste

<a id="sec-3"></a>
### 2.1 `raw_sources/wrench-board/`

- [x] `raw_sources/wrench-board/CLAUDE.md` → [SKILL.md](SKILL.md)
  - Hard rules (No hallucinated component IDs, two-layer defense: tool discipline + post-hoc sanitizer `⟨?U999⟩`)
  - Architecture: Deterministic engines (`raw_sources/wrench-board/api/pipeline/schematic/simulator.py`, `raw_sources/wrench-board/api/pipeline/schematic/hypothesize.py`), Diagnostic runtime, Board parsing & validator (`is_valid_refdes`, `resolve_part`, `resolve_net`, `resolve_pin`, `suggest_similar`)
- [x] `raw_sources/wrench-board/.claude/skills/microsolder-evolve/SKILL.md` → [SKILL.md](SKILL.md)
  - Read-only oracle & anti-gaming rules (Goodhart's Law), knob layer (`raw_sources/wrench-board/api/pipeline/schematic/engine_params.json`) vs. algorithmic changes, `score = 0.6 × self_MRR + 0.4 × cascade_recall`
- [x] `raw_sources/wrench-board/.claude/skills/microsolder-evolve-monitor/SKILL.md` → [SKILL.md](SKILL.md)
  - Klassifikation von Fix-Mustern (`✅ Vrai fix` mit realer physikalischer Kaskade vs. `⚠️ Convention défendable` vs. `❌ Gaming-suspect` Self-Dead ohne Upstream-Ursache)
- [x] `raw_sources/wrench-board/api/agent/sanitize.py` → [SKILL.md](SKILL.md)
  - `REFDES_RE` (`\b[A-Z]{1,3}\d{1,4}\b`), `PROTOCOL_BLOCKLIST` (115 Bus-/Protokoll-Tokens), `_DEVICE_MODEL_RE` (`^A\d{4}$`), `sanitize_agent_text` (`⟨?token⟩`), `_validate_donor_ids` (`⟨?donor:invalid⟩`)
- [x] `raw_sources/wrench-board/api/agent/manifest.py` → [SKILL.md](SKILL.md) & [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md)
  - System-Prompt-Gesetze: `ANTI-HALLUCINATION RULE`, `ARROWS` (Kausalketten Hop-für-Hop), `STYLE`, `HYPOTHESIZE` (Modi für IC, Passive R/C/D/FB, Q, Rails), `MEASURE-TARGET` (pin-spezifisch mit Rolle `power_in`/`signal_out`/`clock_out` statt vage), `ANTI-GENERIC`, `PROTOCOL` (max. 12 Schritte, Confirmation-Gate), `STOCK AWARENESS`
- [x] `raw_sources/wrench-board/api/agent/validation.py` → [SKILL.md](SKILL.md)
  - `FixMode` (`dead`, `alive`, `anomalous`, `hot`, `shorted`, `passive_swap`), `AgentConfidence` (`high`, `medium`, `low`), `ValidatedFix`, `RepairOutcome`
- [x] `raw_sources/wrench-board/api/agent/measurement_memory.py` → [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md)
  - `auto_classify` Schwellwerte (`CLASSIFY_RAIL_ALIVE_LOW = 0.90`, `CLASSIFY_RAIL_ALIVE_HIGH = 1.10`, `CLASSIFY_RAIL_DEAD_THRESHOLD_V = 0.05`, `CLASSIFY_RAIL_ANOMALOUS_LOW = 0.50`, `CLASSIFY_IC_HOT_CELSIUS = 65.0`, Standby-Erkennung für `stuck_on`)
- [x] `raw_sources/wrench-board/api/stock/safety.py` → [SKILL.md](SKILL.md) & [01_In_Circuit_Messen_und_Bauteilpruefung.md](01_In_Circuit_Messen_und_Bauteilpruefung.md)
  - `ROLE_TO_SAFETY` (`exact_only` vs. `tolerant_with_warning`, Disambiguierung von `filter` bei Kondensator vs. Ferritperle, Fail-Safe-Regel `role=None -> exact_only`)
- [x] `raw_sources/wrench-board/api/pipeline/prompts.py` → [SKILL.md](SKILL.md)
  - Evidence-Gating (`literal_refdes_in_quote`, `mpn_match_in_quote`, Verbot von Topologie-Spekulation als Beleg), Resolution-Kategorien (`hardware_fix_verified`, `hardware_ruled_out`, `ambiguous`), Confidence-Stufen (`0.80–0.90`, `0.60–0.80`, `0.50–0.60`, `<0.50 drop`)
- [x] `raw_sources/wrench-board/api/agent/seed_data/global_patterns/anti-patterns-bench.md` → [SKILL.md](SKILL.md) & [01_In_Circuit_Messen_und_Bauteilpruefung.md](01_In_Circuit_Messen_und_Bauteilpruefung.md)
  - Power-on sequencing (100–300 mA Limit, niemals Batterie bei Smartphone-PMIC-Diagnose weglassen), Rework hygiene (Polymer-Elkos > 250 °C, BGA-Preheating), Measurement discipline (10 MΩ Scope-Tastkopf, Diodenmodus < 0,4 V nicht vertrauen → 4-Leiter-Ohmmeter)
- [x] `raw_sources/wrench-board/api/agent/seed_data/global_patterns/bga-lift-archetype.md` → [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md)
  - Signature, Common scenarios (Drop event, Reflow over-temp, Underfill aging > 3 Jahre), Diagnostic order (1. Finger-Press-Test im Betrieb, 2. Kältespray-Test, 3. 50 °C Temperature-Soak für 5 min), Anti-pattern
- [x] `raw_sources/wrench-board/api/agent/seed_data/global_patterns/short-to-gnd.md` → [01_In_Circuit_Messen_und_Bauteilpruefung.md](01_In_Circuit_Messen_und_Bauteilpruefung.md) & [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md)
  - Signature (< 100 mV, CC-Limit, < 5 Ω im Diodenmodus mit Rot an GND), Common offenders (X5R/X7R MLCC Flex-Cracking, Load-ICs, PMIC), 5-stufige Diagnostic order, Anti-patterns
- [x] `raw_sources/wrench-board/api/agent/seed_data/global_patterns/thermal-cascades.md` → [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md)
  - 3 Cascade archetypes (1. Charger IC fail → battery FET overheats; 2. Buck coil saturation → adjacent IC heats; 3. PMIC LDO short → host SoC throttles/stays cool, PMIC gets hot), Diagnostic order (erster Hotspot innerhalb 5 s), Anti-pattern
- [x] `raw_sources/wrench-board/api/agent/seed_data/global_playbooks/boot-no-power.json` → [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md)
  - 6-stufige Prüf-Kaskade (`VBUS` 5.0 V [4.5–5.5 V] → `F1` 0 Ω [0–5 Ω] → `VBAT_MAIN` 3.7 V [3.0–4.4 V] → `PMU_ENABLE` true → `VDDMAIN` 0.8 V [0.75–0.85 V] → `SOC_RESET_N` true)
- [x] `raw_sources/wrench-board/api/agent/seed_data/global_playbooks/pmic-rail-collapse.json` → [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md)
  - 4-stufiges Protokoll bei Rail-Einbruch unter Last (`VDDMAIN` Ruhe [0.78–0.82 V] → `SOC_RESET_N` true → `VDDMAIN_LOADED` 1 s nach Boot [0.75–0.82 V], Sag > 50 mV → `PMU_TEMP` nach 5 s [25–50 °C], > 60 °C = interner Defekt)
- [x] `raw_sources/wrench-board/api/agent/seed_data/global_playbooks/usb-no-charge.json` → [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md)
  - 4-stufiges USB-Ladeprotokoll (`VBUS` 5.0 V [4.5–5.5 V] → `USB_DP` Idle 0.6 V [0.4–3.3 V] → `CHG_EN` true → `VBAT` 3.7 V [3.0–4.4 V])
- [x] `raw_sources/wrench-board/api/pipeline/schematic/simulator.py` & `raw_sources/wrench-board/api/pipeline/schematic/engine_params.json` → [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md)
  - `TOLERANCE_OK = 0.9`, `TOLERANCE_UVLO = 0.5`, `LEAKY_SHORT_PER_CONSUMER_MA = 50.0`
  - `SimulationEngine`: Failure-Modi (`dead`, `shorted`, `leaky_short`, `regulating_low`, `open`), Spannungsteiler-Formel für `leaky_short`, Enable-Net-Union (`rail.enable_net` $\cup$ `enable_in`-Pins), Unique-Passive-Supply-Prüfung (`_is_unique_passive_supply`), 4-Schritt-Kaskaden-Transitivität (`_cascade`)
- [x] `raw_sources/wrench-board/api/pipeline/schematic/hypothesize.py` → [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md)
  - `_PASSIVE_CASCADE_TABLE` (alle 38 Einträge für `passive_r`, `passive_c`, `passive_fb`, `passive_d`, `passive_q`), F1-Soft-Penalty-Scoring (`PENALTY_WEIGHTS = (10, 2)`, `_SCORE_VISIBILITY` 0.5× Dampening), Tie-Break-Prior (Passive vor ICs), 2-Fault-Pruning (`TOP_K_SINGLE = 20`, `MAX_PAIRS = 100`) & 50/50-Discriminator-Algorithmus (`_compute_discriminators`)
- [x] `raw_sources/wrench-board/api/pipeline/schematic/boot_analyzer.py` → [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md)
  - Boot-Phasen-Klassifikation (`always-on`, `sequenced`, `on-demand`), `enable_net`, Power-Good-Ketten (`PG_5V` → `EN_3V3`), `sequencer_refdes` (steuert $\ge 3$ EN-Leitungen), `UNTRACED REFDES`-Filterung
- [x] `raw_sources/wrench-board/api/pipeline/schematic/net_classifier.py` & `raw_sources/wrench-board/api/pipeline/schematic/passive_classifier.py` → [03_Schaltplaene_Platinenlayout_und_SMD_Codes.md](03_Schaltplaene_Platinenlayout_und_SMD_Codes.md)
  - 15 kanonische Netz-Domänen samt Regex-Prioritätsregeln & deterministische Topologie-Heuristiken für Widerstände, Kondensatoren, Dioden, Ferritperlen und Transistoren (`flyback_switch`, `cell_protection`, `cell_balancer`, `inrush_limiter`, `load_switch`, `level_shifter`)
- [x] `raw_sources/wrench-board/benchmark/weaknesses.md` → [SKILL.md](SKILL.md)
  - Alle 10 universellen Simulator-Invarianten (`INV-1` bis `INV-10`) & Anti-Pattern `Self-dead conventions`

<a id="sec-4"></a>
### 2.2 `raw_sources/theEmbeddedNewTestament.github.io/`

- [x] `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Reading_Schematics_Datasheets.md` → [03_Schaltplaene_Platinenlayout_und_SMD_Codes.md](03_Schaltplaene_Platinenlayout_und_SMD_Codes.md)
  - Schematic vs. Layout, Component Symbols, Power & Ground (`VCC/VDD`, `VSS/VEE`, `AGND/DGND`), Value Notation (`1K2`, `4R7`, `100n`, `2u2`), Reference Designators, Datasheet Analysis (`Absolute Maximum Ratings`, Design-Margen 20–30 % Spannung / 50 % Strom / 20 °C Temperatur / 70 % Leistung, `Recommended Operating Conditions`), Practical Schematic Reading (Power-First, Voltage Divider, RC Filter), Troubleshooting
- [x] `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Power_Supply_Design.md` → [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md)
  - Linear vs. Switching Topologies (Buck, Boost, Buck-Boost, Flyback), Wirkungsgrad ($\eta = V_{\text{out}}/V_{\text{in}}$) & Thermik ($P = (V_{\text{in}} - V_{\text{out}}) \cdot I_{\text{out}}$, $\Delta T = P \cdot R_{\text{th}}$), Feedback-Kompensation (Type II/III), Schutzschaltungen (`OVP` Crowbar/Clamping, `OCP` Current Limiting/Foldback/Hiccup/Latch-Off), Power Integrity
- [x] `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/PCB_Design_Considerations.md` → [03_Schaltplaene_Platinenlayout_und_SMD_Codes.md](03_Schaltplaene_Platinenlayout_und_SMD_Codes.md)
  - Layer Stack, Impedanzformeln (Microstrip, Stripline, Differential Pairs), Ground & Power Planes, Return Paths, Ground Segmentation (`AGND/DGND`), Design for Testing (Testpunkte, JTAG/Boundary Scan TAP-Controller)
- [x] `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Component_Selection.md` → [01_In_Circuit_Messen_und_Bauteilpruefung.md](01_In_Circuit_Messen_und_Bauteilpruefung.md) & [03_Schaltplaene_Platinenlayout_und_SMD_Codes.md](03_Schaltplaene_Platinenlayout_und_SMD_Codes.md)
  - Temperaturklassen (Commercial $0\text{..}70\ ^\circ\text{C}$, Industrial $-40\text{..}85\ ^\circ\text{C}$, Automotive AEC-Q100 $-40\text{..}125\ ^\circ\text{C}$, Military $-55\text{..}125\ ^\circ\text{C}$), Derating, MTBF/MTTF/Badewannenkurve, Ausfallmechanismen (EOS, ESD, Thermal Runaway, Whisker/Elektromigration)
- [x] `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Signal_Integrity_Basics.md`, `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Signal_Integrity_EMC.md` & `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/EMI_EMC_Considerations.md` → [03_Schaltplaene_Platinenlayout_und_SMD_Codes.md](03_Schaltplaene_Platinenlayout_und_SMD_Codes.md)
  - Reflexionen, Übersprechen (Crosstalk), Terminierung, Time Domain Reflectometry (TDR), Gleichtakt-/Gegentaktstörungen, EMV-Filterung
- [x] `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Thermal_Management.md` & `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Clock_Distribution.md` → [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md)
  - Wärmeleitung/Konvektion/Strahlung, thermische Widerstandsnetzwerke ($R_{\text{th,JC}}$, $R_{\text{th,CA}}$), Quarz- und PLL-Taktverteilung, Jitter & Skew
- [x] `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Power_Management.md`, `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Reset_Management.md`, `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Clock_Management.md` & `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Watchdog_Timers.md` → [02_Stromversorgung_und_Einschaltsequenz_Diagnose.md](02_Stromversorgung_und_Einschaltsequenz_Diagnose.md)
  - Power Modes (Active, Idle, Light/Deep Sleep, Standby), Reset-Quellen (`RCC->CSR`: POR, WDT, Software, Pin, Brownout) & Timing, Clock Sources (`HSI`, `HSE`, `LSI`, `LSE`, `PLL`), Hardware-Watchdog (`IWDG`/`WWDG`)
- [x] `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Analog_IO.md` & `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Digital_IO_Programming.md` → [01_In_Circuit_Messen_und_Bauteilpruefung.md](01_In_Circuit_Messen_und_Bauteilpruefung.md)
  - ADC-Eingangsimpedanz, Referenzspannungen, Anti-Aliasing, GPIO-Schutzbeschaltung, Open-Drain vs. Push-Pull, Taster-Entprellung (RC-Debouncing)
- [x] `raw_sources/theEmbeddedNewTestament.github.io/Debugging/Oscilloscope_Measurements.md`, `raw_sources/theEmbeddedNewTestament.github.io/Debugging/Logic_Analyzer_Usage.md` & `raw_sources/theEmbeddedNewTestament.github.io/Debugging/JTAG_SWD_Debugging.md` → [01_In_Circuit_Messen_und_Bauteilpruefung.md](01_In_Circuit_Messen_und_Bauteilpruefung.md) & [03_Schaltplaene_Platinenlayout_und_SMD_Codes.md](03_Schaltplaene_Platinenlayout_und_SMD_Codes.md)
  - Oszilloskop-Bandbreite ($\text{BW} = 0{,}35 / t_{\text{rise}}$), Abtastrate, Trigger-Modi, FFT, Tastkopf-Belastung; Logic-Analyzer-Abtasttheorem & Protokolldekodierung (I2C/SPI/UART); JTAG (`TCK`, `TMS`, `TDI`, `TDO`, `TRST`) & SWD (`SWDIO`, `SWCLK`)

<a id="sec-5"></a>
### 2.3 `raw_sources/Repair/` (`aKaReZa75/Repair`)

- [x] `raw_sources/Repair/README.md` & `raw_sources/Repair/Videos.md` → [01_In_Circuit_Messen_und_Bauteilpruefung.md](01_In_Circuit_Messen_und_Bauteilpruefung.md)
  - Praxis-Reparaturfälle: Victor VC97 Multimeter-Instandsetzung (Widerstands-/Kapazitäts-/Dioden-/Durchgangs-Messpfad & `AT24C02` EEPROM-Backup `raw_sources/Repair/aKaReZa 26 - Repair, VC97 EEPROM IC/VC97_EEPROM_BackUP.bin`), LED-Leuchtmittel-Diagnose (Vorheizplatte, LED-/Zener-Tester), Bestückungs- und Inbetriebnahme-Reihenfolge (`12V → 5V → 3.3V → MCU → CH340/USB → GSM/HF`)
- [x] `raw_sources/Repair/Soldering_Tools.md` & `raw_sources/Repair/aKaReZa 38 - Repair, Soldering Tools/IPC-A-610D.pdf` → [SKILL.md](SKILL.md) & [01_In_Circuit_Messen_und_Bauteilpruefung.md](01_In_Circuit_Messen_und_Bauteilpruefung.md)
  - Löt- und Rework-Werkzeuge (Spitzen `900M-T-2C`/`T-K`/`T-3.2D`, Heißluft, Preheater, 183 °C Sn63/Pb37 Lotpaste, RMA-223-UV Flux, Kapton-Tape, Kontakt-600, 99 % Isopropanol, Ultraschallbad) & Lötstellen-Inspektion nach IPC-A-610D

<a id="sec-6"></a>
### 2.4 `raw_sources/electronics-datasheets/` (`Vitorbnc/electronics-datasheets`)

- [x] `raw_sources/electronics-datasheets/smd-codebook.pdf` & alle 15 Bauteil-Ordner (`Bluetooth/`, `CPLD/`, `Diodes/`, `Displays/`, `FPGA/`, `ICs/`, `LEDs/`, `Laser/`, `MCUs/`, `Magnetron/`, `Motors/`, `Photodiodes/`, `Radio/`, `Sensors/`, `Transistors, FETs, Thyristors/`) → [03_Schaltplaene_Platinenlayout_und_SMD_Codes.md](03_Schaltplaene_Platinenlayout_und_SMD_Codes.md)
  - Vollständiger Offline-Datenblatt-Katalog (über 330 PDFs) nach Reparatur des Windows-Longpath-Checkouts (`core.longpaths=true`) ausgewertet und katalogisiert.

<a id="sec-7"></a>
### 2.5 `https://repair.wiki` (Status: Blockiert)

- [ ] **NICHT AUTOMATISIERBAR:** `https://repair.wiki` liefert beim Abruf eine Cloudflare Anti-Bot-Challenge (`challenges.cloudflare.com` / "Just a moment...") aus (dokumentiert in `raw_sources/repair_wiki_BLOCKED_INFO.md`). Gemäß Sicherheitsrichtlinien wurde das Gate nicht umgangen; alle In-Circuit-Messgrundlagen und Prüftabellen sind vollständig in [01_In_Circuit_Messen_und_Bauteilpruefung.md](01_In_Circuit_Messen_und_Bauteilpruefung.md) ausgearbeitet.
