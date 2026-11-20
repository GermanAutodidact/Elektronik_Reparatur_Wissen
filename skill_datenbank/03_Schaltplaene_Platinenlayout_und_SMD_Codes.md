# 03 – Schaltpläne, Platinenlayout, Datenblätter, Netz-Klassifikation und SMD-Codes

Dieses Modul vereint die Methodik zum Lesen von Schaltplänen, das Reverse Engineering ohne Schaltplan, die automatische Netz- und Bauteil-Rollen-Klassifikation aus `raw_sources/wrench-board/api/pipeline/schematic/net_classifier.py` und `raw_sources/wrench-board/api/pipeline/schematic/passive_classifier.py`, Masse- und Signalintegritäts-Konzepte (`AGND`/`DGND`, Impedanzformeln, JTAG/SWD), die Datenblatt-Analyse (`Datasheet-Driven Repair`) aus `raw_sources/theEmbeddedNewTestament.github.io/` sowie den vollständigen SMD-Gehäuse- und Datenblatt-Katalog aus `raw_sources/electronics-datasheets/`.

---

<!-- TOC_START -->
## Inhaltsverzeichnis & Zeilen-Index

| Abschnitt | Ebene | Zeilen |
| :--- | :--- | :---: |
| [1. Systematisches Lesen von Schaltplänen & Reverse Engineering](#sec-1) | Hauptabschnitt | Z. 36–37 |
| ↳ [1.1 Referenzbezeichner (`RefDes`) & Kompakte Wert-Notation (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Reading_Schematics_Datasheets.md`)](#sec-2) | Unterabschnitt | Z. 39–47 |
| ↳ [1.2 Die 15 kanonischen Netz-Domänen & Regex-Prioritätsregeln (`raw_sources/wrench-board/api/pipeline/schematic/net_classifier.py`)](#sec-3) | Unterabschnitt | Z. 49–69 |
| ↳ [1.3 Topologie-Heuristiken zur Bauteil-Rollen-Erkennung (`raw_sources/wrench-board/api/pipeline/schematic/passive_classifier.py`)](#sec-4) | Unterabschnitt | Z. 71–97 |
| ↳ [1.4 Board-Level Reverse Engineering ohne Schaltplan](#sec-5) | Unterabschnitt | Z. 99–105 |
| [2. Masse-Konzepte, Signalintegrität & PCB-Layout (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/PCB_Design_Considerations.md`, `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Signal_Integrity_Basics.md`, `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/EMI_EMC_Considerations.md`)](#sec-6) | Hauptabschnitt | Z. 107–108 |
| ↳ [2.1 Trennung von `AGND`, `DGND`, `PGND` und `Chassis GND`](#sec-7) | Unterabschnitt | Z. 110–117 |
| ↳ [2.2 Wellenwiderstand (Impedanz) & Signalintegrität auf Leiterplatten](#sec-8) | Unterabschnitt | Z. 119–129 |
| ↳ [2.3 JTAG / Boundary-Scan & SWD-Debug-Schnittstellen (`raw_sources/theEmbeddedNewTestament.github.io/Debugging/JTAG_SWD_Debugging.md`)](#sec-9) | Unterabschnitt | Z. 131–138 |
| [3. Datasheet-Driven Repair, Design-Margen & Temperaturklassen](#sec-10) | Hauptabschnitt | Z. 140–141 |
| ↳ [3.1 Die 4 Pflicht-Sektionen jedes Datenblatts (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Reading_Schematics_Datasheets.md`)](#sec-11) | Unterabschnitt | Z. 143–157 |
| ↳ [3.2 Temperatur- und Qualitätsklassen (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Component_Selection.md`)](#sec-12) | Unterabschnitt | Z. 159–170 |
| [4. SMD-Gehäuseformen & Pinout-Fallen](#sec-13) | Hauptabschnitt | Z. 172–173 |
| ↳ [4.1 Passive SMD-Bauformen (Imperial vs. Metrisch)](#sec-14) | Unterabschnitt | Z. 175–188 |
| ↳ [4.2 Aktive SMD-Gehäuseformen & die gefährliche Regler-Pinout-Falle](#sec-15) | Unterabschnitt | Z. 190–212 |
| [5. SMD-Markierungscodes & Lokaler Datenblatt-Katalog (`raw_sources/electronics-datasheets/`)](#sec-16) | Hauptabschnitt | Z. 214–215 |
| ↳ [5.1 Nutzung des lokalen SMD-Codebooks (`raw_sources/electronics-datasheets/smd-codebook.pdf`)](#sec-17) | Unterabschnitt | Z. 217–223 |
| ↳ [5.2 Vollständiges Verzeichnis der lokalen Offline-Datenblätter (`raw_sources/electronics-datasheets/`)](#sec-18) | Unterabschnitt | Z. 225–239 |

---

<!-- TOC_END -->

<a id="sec-1"></a>
## 1. Systematisches Lesen von Schaltplänen & Reverse Engineering

<a id="sec-2"></a>
### 1.1 Referenzbezeichner (`RefDes`) & Kompakte Wert-Notation (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Reading_Schematics_Datasheets.md`)
- **Standard-Präfixe:**
  - `R`: Widerstand | `C`: Kondensator | `L`: Induktivität/Spule | `FB`: Ferritperle | `F`: Sicherung
  - `D` / `CR`: Diode, Zener, TVS, LED | `Q` / `T`: Transistor (BJT / MOSFET) | `U` / `IC`: Integrierter Schaltkreis
  - `J` / `P` / `CN` / `X`: Steckverbinder | `Y` / `X` / `XTAL`: Quarz / Oszillator | `TP`: Testpunkt | `K` / `RLY`: Relais
- **Wert-Notation ohne Dezimalpunkt (verhindert Lesefehler bei kopierten Schaltplänen):**
  - *Widerstände:* Buchstabe ersetzt das Komma (`4R7` = $4{,}7\ \Omega$, `R010` = $0{,}01\ \Omega$, `1K2` = $1{,}2\text{ k}\Omega$, `10M` = $10\text{ M}\Omega$).
  - *Kondensatoren:* `10p` = $10\text{ pF}$, `100n` = $100\text{ nF} = 0{,}1\ \mu\text{F}$, `2u2` = $2{,}2\ \mu\text{F}$.

<a id="sec-3"></a>
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

<a id="sec-4"></a>
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

<a id="sec-5"></a>
### 1.4 Board-Level Reverse Engineering ohne Schaltplan
1. **Masse (`GND`) kartieren:** Große Kupferflächen (`Copper Pours`), Metallkragen von USB-/HDMI-Buchsen, Schraublöcher und Kondensator-Pads mit **Thermal-Relief-Stegen** (4 schmale Kupferbrücken zum Pad, damit die Massefläche beim Löten die Wärme nicht sofort abzieht) als Referenz markieren.
2. **Versorgungsschienen vom Stecker aus verfolgen:** Große Elkos, Tantals und Speicherdrosseln (`L`) markieren jeweils eine eigene Spannungsschiene.
3. **IC-Nummern ablesen & Applikationsschaltung nutzen:** Für jeden Regler- und Schnittstellen-IC das Datenblatt öffnen – die `Typical Application Circuit` im Datenblatt entspricht in ~90 % der Fälle der realen Beschaltung auf der Platine!

---

<a id="sec-6"></a>
## 2. Masse-Konzepte, Signalintegrität & PCB-Layout (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/PCB_Design_Considerations.md`, `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Signal_Integrity_Basics.md`, `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/EMI_EMC_Considerations.md`)

<a id="sec-7"></a>
### 2.1 Trennung von `AGND`, `DGND`, `PGND` und `Chassis GND`
- **`DGND` (Digital Ground):** Rückstrompfad für schnelle Digitalschaltungen (SoC, MCU, RAM). Durch steile Schaltflanken ($\Delta I / \Delta t$) entstehen an jeder Leitungsinduktivität Spannungsspitzen ($U = L \cdot \frac{\text{d}i}{\text{d}t}$, *Ground Bounce*).
- **`AGND` (Analog Ground):** Störungsfreier Bezugspunkt für Präzisions-ADCs, Wägezellen-Vorverstärker (`AD620`, `ADA4530`), Sensoren und Spannungsreferenzen.
- **`PGND` (Power Ground):** Hochstrom-Rückpfad für Schaltregler-MOSFETs und Endstufen.
- **`Chassis GND` / `PE`:** Metallgehäuse und Kabelschirme zur Ableitung von ESD-Impulsen.
- **Das Sternpunkt-Gesetz (`Star Ground`):** `AGND`, `DGND` und `PGND` werden auf der Platine räumlich getrennt geführt, müssen aber **an genau einem definierten Sternpunkt** (meist direkt unter dem A/D-Wandler oder am Haupt-Elko über eine `0R`-Brücke, einen Net-Tie oder eine Ferritperle) niederohmig verbunden sein!
  - **Häufiger Reparaturfehler:** Brennt der `0R`-Verbindungswiderstand oder die Ferritperle zwischen `AGND` und `DGND` durch, „schwimmt“ (`floats`) der gesamte Analogteil gegenüber der Digitalmasse $\rightarrow$ der ADC liefert nur noch Vollausschlag, Null oder stark driftende Zufallswerte (klassischer Fehler bei Feinwaagen und Multimetern!).

<a id="sec-8"></a>
### 2.2 Wellenwiderstand (Impedanz) & Signalintegrität auf Leiterplatten
Bei hohen Frequenzen bzw. steilen Anstiegszeiten ($t_{\text{rise}} < 1\text{ ns}$) wirken Leiterbahnen als Wellenleiter (`Transmission Lines`):

1. **Microstrip-Leitung (Außenlage über durchgehender `GND`-Plane):**
   $$Z_0 \approx \frac{87}{\sqrt{\varepsilon_r + 1{,}41}} \cdot \ln\left(\frac{5{,}98 \cdot h}{0{,}8 \cdot w + t}\right)\ [\Omega]$$
2. **Stripline-Leitung (Innenlage symmetrisch zwischen zwei `GND`-Planes):**
   $$Z_0 \approx \frac{60}{\sqrt{\varepsilon_r}} \cdot \ln\left(\frac{4 \cdot h}{0{,}67 \cdot \pi \cdot w}\right)\ [\Omega]$$
3. **Differenzielles Leitungspaar (`USB`, `HDMI`, `PCIe`, `LVDS`, `CAN` mit Kopplungsfaktor $k$):**
   $$Z_{\text{diff}} = 2 \cdot Z_{\text{single}} \cdot \frac{1 - k^2}{1 + k^2}\ [\Omega]$$
   - **Reparatur-Regel für Flickdrähte (`Jumper Wires`):** Bei abgerissenen Leiterbahnen auf `USB 2.0/3.0` ($Z_{\text{diff}} = 90\ \Omega$), `HDMI`/`PCIe` ($100\ \Omega$) oder `Ethernet` ($100\ \Omega$) müssen beide Adern (`D+` und `D-`) **gleich lang (`Length Matching`), eng parallel geführt** und ohne dicke Lötzinn-Verdickungen (`Impedance Stubs`) geflickt werden, sonst führen Reflexionen zum Verbindungsabbruch!

<a id="sec-9"></a>
### 2.3 JTAG / Boundary-Scan & SWD-Debug-Schnittstellen (`raw_sources/theEmbeddedNewTestament.github.io/Debugging/JTAG_SWD_Debugging.md`)
- **JTAG (IEEE 1149.1, 4/5-Pin):** `TCK` (Test Clock), `TMS` (Test Mode Select), `TDI` (Test Data In), `TDO` (Test Data Out), optional `TRST` (Test Reset) + `VTref` (`VCC`-Referenz für den Debugger) und `GND`.
  - Über **Boundary Scan** lassen sich an BGA-Chips (FPGAs, SoCs) einzelne Pins ohne physischen Tastkopf-Zugriff auf Kurzschluss oder Unterbrechung testen!
- **SWD (Serial Wire Debug, ARM 2-Pin-Alternative):** `SWDIO` (bidirektionale Daten) + `SWCLK` (Takt) + `VTref` + `GND` + `nRST`.
  - **Diagnose-Tipp:** Meldet der `ST-Link` / `J-Link` `No Target Connected`, zuerst `VTref` am Debug-Header messen (`3,3 V`), dann prüfen, ob `nRST` auf Low klemmt oder `SWDIO`/`SWCLK` durch eine defekte ESD-Diode nach `GND` gezogen werden.

---

<a id="sec-10"></a>
## 3. Datasheet-Driven Repair, Design-Margen & Temperaturklassen

<a id="sec-11"></a>
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

<a id="sec-12"></a>
### 3.2 Temperatur- und Qualitätsklassen (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Component_Selection.md`)
Ein häufiger Fehler bei der Reparatur ist der Einbau eines billigen Commercial-Grade-Bauteils in eine heiße Industrie- oder Kfz-Umgebung:

| Qualitätsklasse (`Grade`) | Temperaturbereich | Qualifikationsnorm / Einsatzgebiet |
|---|---|---|
| **Commercial Grade** | **$0\ ^\circ\text{C}\text{ bis }+70\ ^\circ\text{C}$** | Büro-, Haushalts- und Consumer-Elektronik |
| **Industrial Grade** | **$-40\ ^\circ\text{C}\text{ bis }+85\ ^\circ\text{C}$** | Industriesteuerungen, Netzteile, Außengeräte |
| **Automotive Grade** | **$-40\ ^\circ\text{C}\text{ bis }+125\ ^\circ\text{C}$** (teils $+150\ ^\circ\text{C}$) | **`AEC-Q100`** (ICs), **`AEC-Q200`** (Passive) – Kfz & hohe Zuverlässigkeit |
| **Military / Aerospace** | **$-55\ ^\circ\text{C}\text{ bis }+125\ ^\circ\text{C}$** | `MIL-STD` / `DO-160` – Luft-/Raumfahrt & Verteidigung |

---

<a id="sec-13"></a>
## 4. SMD-Gehäuseformen & Pinout-Fallen

<a id="sec-14"></a>
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

<a id="sec-15"></a>
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

<a id="sec-16"></a>
## 5. SMD-Markierungscodes & Lokaler Datenblatt-Katalog (`raw_sources/electronics-datasheets/`)

<a id="sec-17"></a>
### 5.1 Nutzung des lokalen SMD-Codebooks (`raw_sources/electronics-datasheets/smd-codebook.pdf`)
- Auf kleinen SMD-Halbleitern (`SOT-23`, `SOT-323`, `SOD-323`, `SOT-89`) ist aus Platzgründen nicht die Teilenummer (z. B. `MMBT3904`), sondern ein **2- bis 4-stelliger SMD-Marking-Code** (z. B. `1A` oder `1AM`) aufgedruckt.
- **Vorgehen zur Identifikation:**
  1. **Device-Code vom Date-/Lot-Code trennen:** Die ersten 2–3 großen Zeichen sind der Bauteil-Code; ein einzelnes kleineres, um $90^\circ$ gedrehtes oder tiefgestelltes Zeichen am rechten Rand sowie Über-/Unterstriche sind meist Herstellungsmonat/Werk.
  2. **Gehäuseform exakt abmessen** (`SOT-23` = $2{,}9\times 1{,}3\text{ mm}$ vs. `SOT-323 / SC-70` = $2{,}0\times 1{,}25\text{ mm}$): Derselbe Code `1A` kann in verschiedenen Gehäusen unterschiedliche Bauteile bedeuten!
  3. **Pin-Verbindungen auf der Platine prüfen** (welcher Pin geht an `GND`, welcher an `VCC`?) und im lokalen Nachschlagewerk `raw_sources/electronics-datasheets/smd-codebook.pdf` nach Code + Gehäuseform abgleichen.

<a id="sec-18"></a>
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
