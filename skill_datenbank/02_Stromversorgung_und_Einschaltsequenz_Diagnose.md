# 02 – Stromversorgung, Einschaltsequenz-Diagnose und Hypothesen-Engine

Dieses Modul enthält die komplette Systematik zur Fehlersuche in Stromversorgungen, Einschaltsequenzen (`Power Sequencing`), Reset-/Takt-/Boot-Schaltungen sowie die vollständige Simulations- und Hypothesen-Logik aus `raw_sources/wrench-board/api/pipeline/schematic/simulator.py`, `raw_sources/wrench-board/api/pipeline/schematic/hypothesize.py`, `raw_sources/wrench-board/api/agent/seed_data/` und `raw_sources/theEmbeddedNewTestament.github.io/`.

---

<!-- TOC_START -->
## Inhaltsverzeichnis & Zeilen-Index

| Abschnitt | Ebene | Zeilen |
| :--- | :--- | :---: |
| [1. Die feste 7-stufige Prüf-Kaskade vom Eingang zur Logik](#sec-1) | Hauptabschnitt | Z. 43–46 |
| ↳ [Stufe 1: Externes Netzteil / Batterie](#sec-2) | Unterabschnitt | Z. 48–51 |
| ↳ [Stufe 2: Eingangsbuchse, Steckverbinder & Netzschalter](#sec-3) | Unterabschnitt | Z. 53–56 |
| ↳ [Stufe 3: Eingangsfilter, Verpolungs- & Überspannungsschutz](#sec-4) | Unterabschnitt | Z. 58–65 |
| ↳ [Stufe 4: Haupt-Spannungsschiene ($V_{\text{IN}}$ / $V_{\text{BUS}}$ / $V_{\text{MAIN}}$ / $V_{\text{BAT}}$)](#sec-5) | Unterabschnitt | Z. 67–72 |
| ↳ [Stufe 5: Linearregler (`LDO` / Standard-Regler wie `78xx`, `LM317`, `AMS1117`)](#sec-6) | Unterabschnitt | Z. 74–82 |
| ↳ [Stufe 6: Schaltregler (`Buck`, `Boost`, `Buck-Boost`, `Flyback`, `PMIC`)](#sec-7) | Unterabschnitt | Z. 84–95 |
| ↳ [Stufe 7: Stützkondensatoren, Filter-Ferrite & Übergang zur Logik](#sec-8) | Unterabschnitt | Z. 97–101 |
| [2. Validierte Diagnose-Playbooks (`raw_sources/wrench-board/api/agent/seed_data/global_playbooks/`)](#sec-9) | Hauptabschnitt | Z. 103–104 |
| ↳ [2.1 Playbook `boot-no-power` (Gerät lässt sich nicht einschalten / Tot)](#sec-10) | Unterabschnitt | Z. 106–117 |
| ↳ [2.2 Playbook `pmic-rail-collapse` (Schiene bricht unter Last ein / Boot-Loop / Reset)](#sec-11) | Unterabschnitt | Z. 119–128 |
| ↳ [2.3 Playbook `usb-no-charge` (Kein Ladestrom über USB)](#sec-12) | Unterabschnitt | Z. 130–141 |
| [3. Power Sequencing, Reset-, Watchdog-, Takt- & Boot-Architektur](#sec-13) | Hauptabschnitt | Z. 143–144 |
| ↳ [3.1 Boot-Phasen-Klassifikation (`raw_sources/wrench-board/api/pipeline/schematic/boot_analyzer.py`)](#sec-14) | Unterabschnitt | Z. 146–151 |
| ↳ [3.2 Reset-Management & Watchdog-Timer (`raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Reset_Management.md` & `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Watchdog_Timers.md`)](#sec-15) | Unterabschnitt | Z. 153–161 |
| ↳ [3.3 Takterzeugung (`raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Clock_Management.md` & `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Clock_Distribution.md`)](#sec-16) | Unterabschnitt | Z. 163–169 |
| ↳ [3.4 Boot-Pins, Strapping-Widerstände & Service-/Flash-Schalter](#sec-17) | Unterabschnitt | Z. 171–176 |
| [4. Thermische Fehlerkaskaden & BGA-Lift-Diagnose](#sec-18) | Hauptabschnitt | Z. 178–179 |
| ↳ [4.1 Die 3 Thermal-Cascade-Archetypen (`raw_sources/wrench-board/api/agent/seed_data/global_patterns/thermal-cascades.md`)](#sec-19) | Unterabschnitt | Z. 181–191 |
| ↳ [4.2 BGA-Lift-Archetyp (Abgerissene Lötkugeln unter BGA-ICs) (`raw_sources/wrench-board/api/agent/seed_data/global_patterns/bga-lift-archetype.md`)](#sec-20) | Unterabschnitt | Z. 193–206 |
| [5. Deterministische Simulations- & Hypothesen-Engine (`raw_sources/wrench-board/api/pipeline/schematic/simulator.py` & `raw_sources/wrench-board/api/pipeline/schematic/hypothesize.py`)](#sec-21) | Hauptabschnitt | Z. 208–209 |
| ↳ [5.1 Schwellwerte & Mathematisches `leaky_short`-Modell (`raw_sources/wrench-board/api/pipeline/schematic/simulator.py`, `raw_sources/wrench-board/api/agent/measurement_memory.py`)](#sec-22) | Unterabschnitt | Z. 211–222 |
| ↳ [5.2 Der 4-Schritt-Kaskaden-Algorithmus (`_cascade` in `raw_sources/wrench-board/api/pipeline/schematic/simulator.py`)](#sec-23) | Unterabschnitt | Z. 224–233 |
| ↳ [5.3 Vollständige 38-zeilige Fehler-Kaskaden-Matrix (`_PASSIVE_CASCADE_TABLE` aus `raw_sources/wrench-board/api/pipeline/schematic/hypothesize.py`)](#sec-24) | Unterabschnitt | Z. 235–288 |
| ↳ [5.4 Hypothesen-Scoring, Tie-Breaking & der 50/50-Discriminator-Algorithmus (`raw_sources/wrench-board/api/pipeline/schematic/hypothesize.py`)](#sec-25) | Unterabschnitt | Z. 290–299 |

---

<!-- TOC_END -->

<a id="sec-1"></a>
## 1. Die feste 7-stufige Prüf-Kaskade vom Eingang zur Logik

Bei jedem Gerät ohne Funktion (`Dead / No Power`) wird **streng sequenziell** vom Stromeingang bis zur Digital-/Analoglogik geprüft (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Reading_Schematics_Datasheets.md`, `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Power_Supply_Design.md`):

<a id="sec-2"></a>
### Stufe 1: Externes Netzteil / Batterie
- **Leerlauf vs. Last:** Ein Netzteil mit gealterten Ausgangselkos zeigt im Leerlauf oft noch die volle Nennspannung (z. B. `12,0 V`), bricht aber bei Lastzuschaltung sofort ein.
- **Restwelligkeit (`Ripple`):** Mit Oszilloskop (AC-Kopplung, `20 MHz`-Bandbreitenfilter) unter Last prüfen. Ripple $> 100\text{–}200\text{ mV}_{\text{pp}}$ stört nachgeschaltete Regler und führt zu erratischen Resets.

<a id="sec-3"></a>
### Stufe 2: Eingangsbuchse, Steckverbinder & Netzschalter
- **Mechanische Defekte:** Gebrochene Lötstellen am Mittelpin von DC-Hohlsteckerbuchsen, aufgebogene Federkontakte, korrodierte oder abgerissene USB-C-Pads, Kabelbruch direkt hinter der Zugentlastung.
- **Masse-Rückpfad prüfen:** Immer auch den Durchgang vom Minuspol des Netzteils bis zur Platinenmasse (`GND`) messen! Ist die Masse-Lötstelle der Buchse gebrochen, misst man gegen das externe Netzteil-Minus überall auf der Platine $+12\text{ V}$, obwohl kein einziger Elektronenfluss stattfindet.

<a id="sec-4"></a>
### Stufe 3: Eingangsfilter, Verpolungs- & Überspannungsschutz
- **Sicherung (`F`) & PPTC:** Auf Durchgang ($\approx 0\ \Omega$) bzw. Spannungsabfall im Betrieb ($< 50\text{ mV}$) prüfen.
- **Verpolungsschutz-Topologien:**
  1. *Seriendiode (`reverse_protection`):* Einfach, hat aber $0{,}2\text{–}0{,}7\text{ V}$ Verlust. Brennt bei Überstrom hochohmig (`open`) durch $\rightarrow$ Ausgangsschiene tot.
  2. *Antiparallele Crowbar-Diode nach `GND` hinter der Sicherung:* Leitet bei Verpolung und löst sofort die Sicherung aus (oft legiert die Diode dabei dauerhaft auf `0 Ω` durch!).
  3. *P-Kanal / N-Kanal Ideal-Diode MOSFET (`inrush_limiter` / `reverse_protection`):* Schaltet über ein RC-Soft-Start-Glied am Gate verzögert ein. Ist der Kanal offen (`open` / `stuck_off`), bleibt die Hauptschiene trotz intakter Eingangsspannung bei `0 V`.
- **Überspannungsschutz (`TVS-Diode` gegen `GND`):** Der häufigste Defekt nach Verwendung eines falschen Netzteils (z. B. `24 V` statt `9 V`). Die TVS-Diode opfert sich durch einen permanenten Legierungskurzschluss (`0,000 V` / $< 1\ \Omega$ gegen `GND`).

<a id="sec-5"></a>
### Stufe 4: Haupt-Spannungsschiene ($V_{\text{IN}}$ / $V_{\text{BUS}}$ / $V_{\text{MAIN}}$ / $V_{\text{BAT}}$)
- Vor dem Einschalten Widerstand ($\Omega$) und Dioden-Signatur (Rot an `GND`) messen.
- **Schutzschaltungs-Verhalten (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Power_Supply_Design.md`):**
  - *Overvoltage Protection (`OVP`):* Crowbar (Thyristor/TVS zieht Schiene hart auf `GND`), Shunt-Regelung, Serien-Abschaltung oder Voltage Clamping.
  - *Overcurrent Protection (`OCP`):* Konstantstrombegrenzung (`Current Limiting`), rückläufige Kennlinie (`Foldback Limiting`), zyklisches Ein-/Ausschalten (**`Hiccup Mode`** – erkennbar am rhythmischen Pulsieren der Schienenspannung und einem leisen Ticken der Induktivitäten!) oder dauerhafte Verriegelung bis zum Power-Cycle (`Latch-Off`).

<a id="sec-6"></a>
### Stufe 5: Linearregler (`LDO` / Standard-Regler wie `78xx`, `LM317`, `AMS1117`)
- **Wirkungsgrad & Thermik (`raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Power_Supply_Design.md` & `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Thermal_Management.md`):**
  $$\eta_{\text{linear}} = \frac{V_{\text{OUT}}}{V_{\text{IN}}} \times 100\ \%, \qquad P_{\text{loss}} = (V_{\text{IN}} - V_{\text{OUT}}) \cdot I_{\text{OUT}}$$
  $$\Delta T = P_{\text{loss}} \cdot R_{\text{th,JA}}, \qquad T_J = T_A + \Delta T$$
- **Typische LDO-Fehlermodi:**
  1. *Ausgang = `0 V` trotz vorhandenem $V_{\text{IN}}$:* Entweder `EN`-Pin (Enable) ist auf `Low`, der LDO ist intern unterbrochen, oder ein harter Kurzschluss am Ausgang zwingt den LDO in den thermischen/Überstrom-Shutdown.
  2. *Durchlegierter Pass-Transistor (**$V_{\text{OUT}} \approx V_{\text{IN}}$**):* Kritischster Fehler! Wenn ein `12 V → 3,3 V` LDO zwischen Eingang und Ausgang durchlegiert, liegen volle `12 V` auf der `3,3 V`-Logikschiene $\rightarrow$ nachgeschaltete Mikrocontroller und Sensoren sind fast immer mitzerstört (siehe `Absolute Maximum Ratings`).
  3. *Hochfrequente Schwingung (Oszillation):* Ältere LDOs (z. B. `AMS1117`, `LM1117`) benötigen für ihre Phasenreserve zwingend einen Ausgangskondensator mit einem **definierten Mindest-ESR** ($0{,}1\text{–}2\ \Omega$, klassisch Tantal/Elko). Ist der Ausgangskondensator ausgetrocknet oder falsch bestückt, schwingt der Regler mit mehreren kHz bis MHz!

<a id="sec-7"></a>
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

<a id="sec-8"></a>
### Stufe 7: Stützkondensatoren, Filter-Ferrite & Übergang zur Logik
- Lokale Entkopplungskondensatoren (`decoupling`, $100\text{ nF}$ direkt an jedem `VCC`-Pin) und Serien-Ferritperlen (`passive_fb`) zu empfindlichen Analog-, Audio- (`DBVDD`, `AVDD`) oder HF-Domänen prüfen.

---

<a id="sec-9"></a>
## 2. Validierte Diagnose-Playbooks (`raw_sources/wrench-board/api/agent/seed_data/global_playbooks/`)

<a id="sec-10"></a>
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

<a id="sec-11"></a>
### 2.2 Playbook `pmic-rail-collapse` (Schiene bricht unter Last ein / Boot-Loop / Reset)
Wenn eine Schiene im Ruhezustand nominal ist, aber beim Start des SoC einbricht (`raw_sources/wrench-board/api/agent/seed_data/global_playbooks/pmic-rail-collapse.json`):

| Schritt | Messziel (`target`) | Messart | Nominalwert | Gültiger Bereich (`pass_range`) | Diagnose-Begründung (`rationale`) |
|---|---|---|---|---|---|
| **1** | `VDDMAIN` (Ruhezustand) | Numerisch (`V`) | `0,80 V` | **`0,78 – 0,82 V`** | Schiene im Ruhezustand (vor SoC-Boot) messen. |
| **2** | `SOC_RESET_N` | Boolean | `true` | **`true`** | Reset wird freigegeben $\rightarrow$ SoC beginnt Strom zu ziehen. |
| **3** | `VDDMAIN_LOADED` (1 s nach Boot) | Numerisch (`V`) | `0,80 V` | **`0,75 – 0,82 V`** | **Spannungseinbruch (`Sag`) $> 50\text{ mV}$** beweist ein schwaches PMIC, defekte Ausgangs-Entkopplungskondensatoren oder einen Kurzschluss, der erst über ein `EN`-Signal zugeschaltet wird. |
| **4** | `PMU_TEMP` (5 s nach Boot) | Numerisch ($^\circ\text{C}$) | `35 °C` | **`25 – 50 °C`** | Wärmebild auf PMIC 5 s nach Einschalten: **$> 60\ ^\circ\text{C}$** deutet auf internen FET-Schaden oder massive Überlast hin. |

<a id="sec-12"></a>
### 2.3 Playbook `usb-no-charge` (Kein Ladestrom über USB)
Diagnose des USB-Ladepfads (`raw_sources/wrench-board/api/agent/seed_data/global_playbooks/usb-no-charge.json`):

| Schritt | Messziel (`target`) | Messart | Nominalwert | Gültiger Bereich (`pass_range`) | Diagnose-Begründung (`rationale`) |
|---|---|---|---|---|---|
| **1** | `VBUS` | Numerisch (`V`) | `5,0 V` | **`4,5 – 5,5 V`** | USB-Eingangsspannung hinter der Buchse prüfen. |
| **2** | `USB_DP` (`D+` Datenleitung) | Numerisch (`V`) | `0,6 V` | **`0,4 – 3,3 V`** | `D+` Ruhespannung prüft, ob die Datenleitungen für die Lade-Signatur/Enumeration frei sind (nicht durch ESD-Diode gegen `GND` geklemmt). |
| **3** | `CHG_EN` | Boolean | `true` | **`true`** | Enable-Signal des Charger-ICs muss aktiv sein. |
| **4** | `VBAT` | Numerisch (`V`) | `3,7 V` | **`3,0 – 4,4 V`** | Fehlt die Ladespannung an der Batterie trotz `VBUS` und `CHG_EN` $\rightarrow$ Charger-IC tot oder `BATFET`-Pfad offen. |

---

<a id="sec-13"></a>
## 3. Power Sequencing, Reset-, Watchdog-, Takt- & Boot-Architektur

<a id="sec-14"></a>
### 3.1 Boot-Phasen-Klassifikation (`raw_sources/wrench-board/api/pipeline/schematic/boot_analyzer.py`)
1. **`always-on`:** Standby-Schienen (z. B. `+3V3_STANDBY`, `LPC_VCC`), Batterie-Management und Supervisor-ICs. Sie laufen an, sobald physikalische Eingangsspannung anliegt, ohne dass ein aktives `EN`-Signal eines Controllers nötig ist (höchstens ein fester Widerstandsteiler an `VIN`).
2. **`sequenced`:** Schienen, die durch einen Sequencer (`sequencer_refdes` = MCU/PMIC/EC/LPC, der $\ge 3$ `*_PWR_EN`-Leitungen steuert) oder eine **Power-Good-Kaskade** (`PG_5V` $\rightarrow$ `EN_3V3` $\rightarrow$ `EN_1V2`) nacheinander freigeschaltet werden.
   - **Wichtige Diagnose-Regel:** Eine Schiene kann volle Eingangsspannung am Regler-IC haben (`power available`), bleibt aber bei `0 V`, weil ihr `enable_net` aus einer vorherigen Boot-Phase fehlt!
3. **`on-demand`:** Schienen, die erst asynchron durch Software/Treiber oder Stecker-Ereignisse eingeschaltet werden (z. B. `PCIE1_PWR`, `USB_VBUS`, Audio-Codec, Display-Backlight `EDP_BL_EN`). Ein Wert von `0 V` direkt nach dem Einschalten ist hier **kein** Hardwaredefekt!

<a id="sec-15"></a>
### 3.2 Reset-Management & Watchdog-Timer (`raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Reset_Management.md` & `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Watchdog_Timers.md`)
- **Reset-Zeitablauf:**
  `Power Applied → Voltage Stabilization (typ. 50–100 ms) → Power Good Check → Reset Release (nRST High) → Clock Settling (typ. 10–50 ms) → Application Start`
- **Reset-Ursachen (`RCC->CSR` Flags bei ARM Cortex-M / STM32):**
  - `PORRSTF` (Power-On / Power-Down Reset), `BORRSTF` (Brownout Reset bei Spannungseinbruch), `PINRSTF` (Externer Reset-Pin `NRST`), `WWDGRSTF` / `IWDGRSTF` (Window-/Independent-Watchdog-Timeout bei Software-Hänger oder fehlendem Takt), `SFTRSTF` (Software-Reset).
- **Hardware-Fehlermuster an der Reset-Leitung (`nRST` / `RESET_N`):**
  1. *Dauer-Reset (`nRST = 0 V` trotz stabiler `VCC`):* Externer Reset-Taster hat Kurzschluss/Feuchtigkeit, Entstörkondensator ($100\text{ nF}$) am Reset-Pin ist kurzgeschlossen, oder ein externer Supervisor-IC hält `nRST` unten, weil eine überwachte Nebenschiene unterhalb ihrer Schwelle liegt.
  2. *Zyklisches Pulsieren am `nRST`-Pin alle paar Millisekunden/Sekunden:* Der Prozessor startet, stürzt aber sofort ab (z. B. wegen defektem Flash/EEPROM, Spannungseinbruch beim PLL-Hochlauf oder nicht gefüttertem Hardware-Watchdog), woraufhin der Watchdog permanent Reset-Impulse auslöst.

<a id="sec-16"></a>
### 3.3 Takterzeugung (`raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Clock_Management.md` & `raw_sources/theEmbeddedNewTestament.github.io/Advanced_Hardware/Clock_Distribution.md`)
- **Taktquellen:**
  - `HSI` / `MSI` / `LSI`: Interne RC-Oszillatoren (starten sofort nach Reset, ungenau $\pm 1\text{–}5\ \%$).
  - `HSE` ($4\text{–}48\text{ MHz}$ Systemquarz) & `LSE` ($32{,}768\text{ kHz}$ Uhrenquarz): Externe Schwingquarze.
  - `PLL` (Phase-Locked Loop): Vervielfacht den Eingangstakt ($f_{\text{out}} = f_{\text{in}} \cdot \frac{N}{M \cdot P}$).
- **Typisches Quarz-Fehlerbild:** Viele Mikrocontroller starten im Bootcode zunächst mit dem internen `HSI`-Takt, schalten dann auf `HSE` + `PLL` um und warten in einer Endlosschleife auf das Ready-Bit (`while (!(RCC->CR & RCC_CR_HSERDY))`). Ist der externe Quarz durch Sturz gebrochen oder einer der beiden Lastkondensatoren (`tank`, typ. $8\text{–}22\text{ pF}$ `C0G`) defekt (`open` oder `short`), bleibt die Firmware exakt in dieser Schleife hängen – das Display bleibt dunkel!

<a id="sec-17"></a>
### 3.4 Boot-Pins, Strapping-Widerstände & Service-/Flash-Schalter
- **Funktionsweise:** Prozessoren (z. B. `STM32` über `BOOT0`/`BOOT1`, `ESP32` über `GPIO0`/`GPIO12`, `i.MX`/SoCs über `BOOT_MODE`-Pins) und Präzisionsmessgeräte (Laborwaagen mit **Service-/Kalibrier-/Flash-Schalter** auf oder nahe der Hauptplatine) tasten beim steigenden Übergang von `nRST` die Strapping-Pegel ab.
- **Praxis-Falle:** Ein versehentlich beim Reinigen/Transport verstellter oder korrodierter **Service-/Flash-Schalter** (bzw. ein hochohmiger `pull_down`-Widerstand an `BOOT0`) legt den Pin auf `High`. Der Prozessor springt in den internen **ROM-Bootloader** und wartet stumm auf serielle Flash-Befehle (`UART`/`USB-DFU`). Alle Spannungen (`12 V`, `5 V`, `3,3 V`) sind zu 100 % vorhanden, kein Bauteil wird heiß, aber das Gerät zeigt keinerlei Anzeige!

---

<a id="sec-18"></a>
## 4. Thermische Fehlerkaskaden & BGA-Lift-Diagnose

<a id="sec-19"></a>
### 4.1 Die 3 Thermal-Cascade-Archetypen (`raw_sources/wrench-board/api/agent/seed_data/global_patterns/thermal-cascades.md`)
> [!WARNING]
> **Anti-Pattern Nr. 1 bei der Wärmebild-Diagnose:** Tausche niemals blind das heißeste Bauteil auf der Platine! Das heißeste Bauteil im eingeschwungenen Zustand ist oft das **Opfer (`Victim`)**, nicht der **Täter (`Culprit`)**. Beobachte die Platine zwingend in den **ersten 5 Sekunden nach dem Einschalten**, identifiziere den **allerersten** Hotspot und verfolge dessen Schiene stromaufwärts und stromabwärts.

1. **Archetyp 1 – Charger-IC defekt $\rightarrow$ Batterie-MOSFET überhitzt:**
   - Ein defekter Ladecontroller treibt unkontrolliert Strom durch einen teilweise leitenden/angeschlagenen Batterie-FET. Der FET wird schneller heiß als das Charger-IC. Prüfe zuerst das Gate-Signal vom Charger-IC zum FET!
2. **Archetyp 2 – Buck-Spulensättigung $\rightarrow$ Nachgeschaltetes IC überhitzt:**
   - Eine Speicherdrossel mit Windungsschluss/Sättigung (oder ein durchlegierter High-Side-FET) regelt nicht mehr ab und drückt überhöhte Spannung in die Ausgangsschiene. Die internen Schutz-/Klemmdioden des nachgeschalteten Verbraucher-ICs leiten diese Überspannung ab und verheizen die Differenzleistung.
3. **Archetyp 3 – PMIC-LDO-Kurzschluss $\rightarrow$ Host-SoC drosselt:**
   - Ein Kurzschluss auf einem LDO-Ausgang des PMIC lässt die Versorgung des SoC einbrechen. Das SoC reduziert sofort seinen Takt und bleibt **kühl**, während das PMIC den Kurzschlussstrom verheizt und **kochend heiß** wird.

<a id="sec-20"></a>
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

<a id="sec-21"></a>
## 5. Deterministische Simulations- & Hypothesen-Engine (`raw_sources/wrench-board/api/pipeline/schematic/simulator.py` & `raw_sources/wrench-board/api/pipeline/schematic/hypothesize.py`)

<a id="sec-22"></a>
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

<a id="sec-23"></a>
### 5.2 Der 4-Schritt-Kaskaden-Algorithmus (`_cascade` in `raw_sources/wrench-board/api/pipeline/schematic/simulator.py`)
1. **Schritt 1 (`effective_dead`):** Vereinigt alle direkt ausgefallenen Bauteile mit allen Bauteilen, die durch Initialfehler (z. B. offenes Serienbauteil oder `UVLO`) bereits `dead` sind.
2. **Schritt 2 (Direkte Verbraucher-Propagation):** Jedes Bauteil, dessen `power_in`-Pin an einer nicht-stabilen Schiene hängt, deren Quell-IC in `effective_dead` liegt, wird als `dead` markiert.
3. **Schritt 3 (Transitive Rail-Abschaltung `dead_rails`):** Eine Schiene wird als `dead` markiert, wenn:
   - sie durch eine offene Ferritperle / einen offenen Serienwiderstand am `enable_net` zwangsabgeschaltet wurde (`_forced_dead_rails`), **oder**
   - ihr Quell-IC (`source_refdes`) nach Schritt 2 (auch transitiv!) in `dead_components` liegt, **oder**
   - ihr Endzustand `shorted` ist, **oder**
   - ihr Endzustand `degraded` mit einer Spannung $< \text{TOLERANCE\_UVLO}$ ($50\ \%$) ist.
4. **Schritt 4 (Verbraucher toter Schienen):** Alle Verbraucher einer in Schritt 3 als `dead` markierten Schiene werden ebenfalls `dead` (sofern sie keinen lebenden Alternativ-Versorgungspin besitzen).

<a id="sec-24"></a>
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

<a id="sec-25"></a>
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
