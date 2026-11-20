---
name: elektronik-reparatur-diagnose
description: Vollständiges Regelwerk und Diagnose-Protokoll für Elektronik-Reparatur auf Bauteilebene (Component-Level Repair), In-Circuit-Messungen, Stromversorgungs- und Einschaltsequenz-Diagnose sowie Schaltplan-/SMD-Analyse. Use when diagnosing electronic hardware faults, measuring components in-circuit with multimeter/oscilloscope/ESR meter, tracing power rails and boot sequences, or decoding SMD markings and schematics ("Elektronik reparieren", "Platine messen", "Kurzschluss suchen", "Schaltnetzteil/LDO prüfen", "Feinwaage Diagnose"). Don't use for pure software debugging, web development, or unsafe high-voltage DIY experiments without proper isolation.
metadata:
    version: 2.0-DE
---

# SKILL.md – Haupt-Regelwerk für Elektronik-Reparatur und Hardware-Diagnose

Dieses Regelwerk definiert die verbindlichen Arbeitsgesetze für die KI-gestützte Elektronik-Diagnose und Reparatur auf Bauteilebene (`Board-Level` / `Component-Level Repair`). Es vereint die deterministische Diagnose-Architektur aus `raw_sources/wrench-board/` mit den Hardware-Grundlagen aus `raw_sources/theEmbeddedNewTestament.github.io/`, `raw_sources/Repair/` und `raw_sources/electronics-datasheets/`.

---

<!-- TOC_START -->
## Inhaltsverzeichnis & Zeilen-Index

| Abschnitt | Ebene | Zeilen |
| :--- | :--- | :---: |
| [1. Modul-Router & Aufbau der Wissensdatenbank](#sec-1) | Hauptabschnitt | Z. 42–53 |
| [2. Das Anti-Halluzinations-Gesetz (Zwei-Ebenen-Verteidigung)](#sec-2) | Hauptabschnitt | Z. 55–56 |
| ↳ [2.1 Strikte Verifikationspflicht für Bauteilbezeichnungen (`RefDes`) und Pinouts](#sec-3) | Unterabschnitt | Z. 58–72 |
| ↳ [2.2 Evidence-Gating, Resolution-Kategorien & Konfidenz-Skala (`raw_sources/wrench-board/api/pipeline/prompts.py`)](#sec-4) | Unterabschnitt | Z. 74–89 |
| ↳ [2.3 Die 10 universellen Simulator-Invarianten (`raw_sources/wrench-board/benchmark/weaknesses.md`)](#sec-5) | Unterabschnitt | Z. 91–108 |
| [3. Zerstörungsfreie Prüf-Reihenfolge (Außen vor Innen)](#sec-6) | Hauptabschnitt | Z. 110–129 |
| [4. Mechanik-, ESD- & Elektrischer Sicherheitsschutz zuerst](#sec-7) | Hauptabschnitt | Z. 131–132 |
| ↳ [4.1 Mechanischer Schutz bei Präzisionsmessgeräten (Fein- & Analysenwaagen / EMK-Zellen)](#sec-8) | Unterabschnitt | Z. 134–139 |
| ↳ [4.2 ESD-Schutz (Elektrostatische Entladung)](#sec-9) | Unterabschnitt | Z. 141–144 |
| ↳ [4.3 Elektrische Sicherheit (IEC 61010) & Kondensatorentladung](#sec-10) | Unterabschnitt | Z. 146–152 |
| [5. Werkstatt-Logik vor Handbuch-Theorie & Ersatzteil-Sicherheit](#sec-11) | Hauptabschnitt | Z. 154–155 |
| ↳ [5.1 Reparatur auf Bauteilebene statt Baugruppentausch](#sec-12) | Unterabschnitt | Z. 157–160 |
| ↳ [5.2 Hard Safety Filter für Bauteil-Substitution (`raw_sources/wrench-board/api/stock/safety.py`)](#sec-13) | Unterabschnitt | Z. 162–177 |
| [6. Verbindlicher Diagnose- & Mess-Workflow (`raw_sources/wrench-board/api/agent/manifest.py`)](#sec-14) | Hauptabschnitt | Z. 179–180 |
| ↳ [6.1 Diagnosekette & Hypothesen-Auswertung (`HYPOTHESIZE`)](#sec-15) | Unterabschnitt | Z. 182–188 |
| ↳ [6.2 Präzise Messanweisungen (`MEASURE-TARGET` & `ANTI-GENERIC`)](#sec-16) | Unterabschnitt | Z. 190–196 |
| ↳ [6.3 Bench Anti-Patterns (`raw_sources/wrench-board/api/agent/seed_data/global_patterns/anti-patterns-bench.md`)](#sec-17) | Unterabschnitt | Z. 198–204 |

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
