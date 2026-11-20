# 01 – In-Circuit-Messen, Bauteilprüfung, Oszilloskop-Praxis und Löttechnik

Dieses Modul beschreibt die physikalischen Grundlagen und exakten Prüfprozeduren für das Messen elektronischer Bauteile im **eingelöteten Zustand (`In-Circuit`)** ohne Auslöten, ergänzt um Oszilloskop- und Logic-Analyzer-Diagnose sowie die Löt- und Instandsetzungspraxis aus `raw_sources/Repair/`, `raw_sources/theEmbeddedNewTestament.github.io/` und `raw_sources/wrench-board/`.

---

<!-- TOC_START -->
## Inhaltsverzeichnis & Zeilen-Index

| Abschnitt | Ebene | Zeilen |
| :--- | :--- | :---: |
| [1. Physik und Messmodi des Multimeters In-Circuit](#sec-1) | Hauptabschnitt | Z. 36–37 |
| ↳ [1.1 Widerstandsmessung ($\Omega$) vs. Durchgangsprüfung vs. Diodentest](#sec-2) | Unterabschnitt | Z. 39–46 |
| ↳ [1.2 Einflüsse der Schaltungsumgebung (Parallelschaltung, Ladekurven, Restladung)](#sec-3) | Unterabschnitt | Z. 48–55 |
| ↳ [1.3 Relativmessung gegen Masse (`Red-Probe-on-Ground` / Dioden-Signatur)](#sec-4) | Unterabschnitt | Z. 57–68 |
| [2. Exakte Prüftabellen für alle Bauteilklassen In-Circuit](#sec-5) | Hauptabschnitt | Z. 70–71 |
| ↳ [2.1 SMD-Sicherungen (`F`) & Polyswitches (`PPTC`)](#sec-6) | Unterabschnitt | Z. 73–89 |
| ↳ [2.2 Dioden, Gleichrichter, Schottky-, Zener- & TVS-Schutzdioden](#sec-7) | Unterabschnitt | Z. 91–104 |
| ↳ [2.3 Widerstände (SMD & THT) & vollständige Code-Entschlüsselung](#sec-8) | Unterabschnitt | Z. 106–150 |
| ↳ [2.4 Keramikkondensatoren (`MLCC`) & Elektrolytkondensatoren (`Elko` / `Tantal` / `Polymer`)](#sec-9) | Unterabschnitt | Z. 152–186 |
| ↳ [2.5 Spulen, Induktivitäten (`L`), Ferritperlen (`FB`) & Übertrager](#sec-10) | Unterabschnitt | Z. 188–197 |
| ↳ [2.6 Bipolartransistoren (`BJT`: NPN / PNP) & MOSFETs (N-Kanal / P-Kanal)](#sec-11) | Unterabschnitt | Z. 199–223 |
| [3. Oszilloskop-, Logic-Analyzer- & I/O-Diagnose In-Circuit](#sec-12) | Hauptabschnitt | Z. 225–226 |
| ↳ [3.1 Oszilloskop-Regeln & Formeln (`raw_sources/theEmbeddedNewTestament.github.io/Debugging/Oscilloscope_Measurements.md`)](#sec-13) | Unterabschnitt | Z. 228–243 |
| ↳ [3.2 Logic Analyzer & Digitale Bus-Prüfung (`raw_sources/theEmbeddedNewTestament.github.io/Debugging/Logic_Analyzer_Usage.md`, `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Digital_IO_Programming.md`, `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Analog_IO.md`)](#sec-14) | Unterabschnitt | Z. 245–255 |
| [4. Löttechnik, Sektionale Inbetriebnahme & Fallstudien (`aKaReZa75/Repair`)](#sec-15) | Hauptabschnitt | Z. 257–258 |
| ↳ [4.1 Sektionale Bestückungs- & Prüf-Reihenfolge (`raw_sources/Repair/Videos.md`)](#sec-16) | Unterabschnitt | Z. 260–266 |
| ↳ [4.2 Lötwerkzeuge, Temperaturprofile & IPC-A-610D-Qualität (`raw_sources/Repair/Soldering_Tools.md` & `raw_sources/Repair/aKaReZa 38 - Repair, Soldering Tools/IPC-A-610D.pdf`)](#sec-17) | Unterabschnitt | Z. 268–280 |
| ↳ [4.3 Reparatur-Fallstudie: Defektes Multimeter (`Victor VC97` / EEPROM-Diagnose aus `raw_sources/Repair/Videos.md`)](#sec-18) | Unterabschnitt | Z. 282–287 |

---

<!-- TOC_END -->

<a id="sec-1"></a>
## 1. Physik und Messmodi des Multimeters In-Circuit

<a id="sec-2"></a>
### 1.1 Widerstandsmessung ($\Omega$) vs. Durchgangsprüfung vs. Diodentest

| Messmodus | Prüfspannung / Prüfstrom | Anzeige | Wann nutzen? | Typische Falle In-Circuit |
|---|---|---|---|---|
| **Widerstand ($\Omega$)** | Sehr kleine Prüfspannung (**$< 0{,}3\text{ V}$**, meist $0{,}1\text{–}0{,}25\text{ V}$) | $\Omega$, $\text{k}\Omega$, $\text{M}\Omega$ oder `OL` | Widerstände, Sicherungen, Spulen-DCR, Sub-Ohm-Kurzschlüsse gegen `GND` | Halbleiterstrecken (Silizium $\approx 0{,}6\text{ V}$) werden bei $< 0{,}3\text{ V}$ **nicht** leitend $\rightarrow$ zeigen fälschlich `OL`! |
| **Durchgangsprüfung (Buzzer)** | Prüfspannung meist $0{,}5\text{–}3{,}0\text{ V}$, akustischer Schwellwert | Piepton + $\Omega$ / `V` | Leiterbahnverfolgung, Sicherungen, Schalter, Stecker, Kabel | Piept bei vielen Multimetern bis **$30\text{–}50\ \Omega$**! Moderne CPU/GPU/SoC-`VCORE`-Rails haben regulär $1\text{–}10\ \Omega$ $\rightarrow$ **kein** Kurzschluss! |
| **Diodentest ($\rightarrow\vert-$)** | Konstantstromquelle (**$\approx 0{,}5\text{–}2\text{ mA}$**), Leerlaufspannung **$2{,}0\text{–}3{,}3\text{ V}$** | Flussspannung $U_F$ in **Volt** (`0.540 V`) oder `OL` | Dioden, TVS, Transistoren, MOSFETs, IC-Pins gegen `GND` (`Red-Probe-on-Ground`) | Unter **$0{,}4\text{ V}$** greifen Multimeter-Schutzschaltungen (`raw_sources/wrench-board/api/agent/seed_data/global_patterns/anti-patterns-bench.md`) $\rightarrow$ für Sub-Ohm-Schlüsse 4-Leiter-$\Omega$ nutzen! |

<a id="sec-3"></a>
### 1.2 Einflüsse der Schaltungsumgebung (Parallelschaltung, Ladekurven, Restladung)
1. **Parallele Pfade:** Im eingelöteten Zustand misst man niemals das Bauteil isoliert, sondern immer das Bauteil **parallel zum gesamten Restnetzwerk** der Platine:
   $$\frac{1}{R_{\text{gemessen}}} = \frac{1}{R_{\text{Bauteil}}} + \frac{1}{R_{\text{Parallelpfad}}} \implies R_{\text{gemessen}} \le R_{\text{Nennwert}}$$
   - **Goldene Widerstands-Regel:** Ist ein gemessener Widerstandswert **kleiner** als der Nennwert, kann der Widerstand völlig intakt sein (ein paralleler Pfad zieht den Wert herunter). Ist der gemessene Wert jedoch **größer** als der Nennwert + Toleranz (z. B. `15 kΩ` statt `10 kΩ`), ist der Widerstand **zu 100 % defekt** (hochohmig geworden oder Haarriss).
2. **Ladekurven von Kondensatoren:** Beim Anlegen der Messspitzen an eine Spannungsschiene lädt der Prüfstrom des Multimeters die Stütz- und Ausgangskondensatoren auf. Der angezeigte Widerstandswert startet nahe $0\ \Omega$ (scheinbarer Kurzschluss) und **steigt kontinuierlich an**, bis die Kondensatoren geladen sind. Erst der **stabile Endwert** nach dem Einschwingen ist gültig!
3. **Restladungen (Sicherheit & Messfehler):** Restspannungen auf Elkos verfälschen jede $\Omega$- und Diodenmessung (oft negative Werte oder Dauerpiepen) und zerstören den Messeingang des Multimeters. **Platine immer stromlos machen, Elkos entladen und im `DC V`-Modus auf $< 1\text{ V}$ prüfen!**
4. **Parasitäre Body- und Substrat-Dioden:** In ICs und MOSFETs liegen zwischen `GND` und den Versorgungspins bzw. zwischen Source und Drain interne Dioden. Im $\Omega$- oder Diodenmodus erhält man daher beim Vertauschen von Rot und Schwarz unterschiedliche Messwerte.

<a id="sec-4"></a>
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

<a id="sec-5"></a>
## 2. Exakte Prüftabellen für alle Bauteilklassen In-Circuit

<a id="sec-6"></a>
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

<a id="sec-7"></a>
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

<a id="sec-8"></a>
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

<a id="sec-9"></a>
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

<a id="sec-10"></a>
### 2.5 Spulen, Induktivitäten (`L`), Ferritperlen (`FB`) & Übertrager

| Bauteil | $\Omega$-Messung (DCR) | Fehlerbilder & Diagnose |
|---|---|---|
| **Ferritperle (`FB`, `passive_fb`)** | **$0{,}01\text{–}0{,}5\ \Omega$** | Verbindet Haupt-Rail mit gefilterter Sub-Rail (z. B. `+3V3` $\rightarrow$ `DBVDD` / `PCIE1_PWR_FILT`). Brennt bei nachgeschaltetem Überstrom **hochohmig (`OL` / `open`)** durch $\rightarrow$ Sub-Rail ist tot (`0 V`), Haupt-Rail bleibt stabil. |
| **Speicherdrossel (Buck/Boost `L`)** | **$0{,}01\text{–}2{,}0\ \Omega$** | **`OL`:** Wicklungsbruch oder abgerissenes Lötpad (häufig nach Sturz wegen hoher Bauteilmasse!). **Windungsschluss / Kernsättigung:** Im $\Omega$-Modus **nicht** erkennbar! Erfordert **LCR-Meter** ($L$ und Güte $Q$ bei $100\text{ kHz}$) oder **Ringing-Test** (gedämpfte Schwingung mit Oszilloskop prüfen). |
| **Übertrager / Trafo** | Primär/Sekundär getrennt: $\text{DCR}_{\text{prim}}$ vs. $\text{DCR}_{\text{sek}}$; zwischen Primär und Sekundär zwingend **`OL` ($> 10\text{ M}\Omega$)** | Unterbrechung einer Wicklung (`OL` oder eingebaute Thermosicherung offen) oder Isolationsdurchschlag. |

---

<a id="sec-11"></a>
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

<a id="sec-12"></a>
## 3. Oszilloskop-, Logic-Analyzer- & I/O-Diagnose In-Circuit

<a id="sec-13"></a>
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

<a id="sec-14"></a>
### 3.2 Logic Analyzer & Digitale Bus-Prüfung (`raw_sources/theEmbeddedNewTestament.github.io/Debugging/Logic_Analyzer_Usage.md`, `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Digital_IO_Programming.md`, `raw_sources/theEmbeddedNewTestament.github.io/Hardware_Fundamentals/Analog_IO.md`)
- **Abtastrate:** Mindestens **$4\text{–}10\times$ höchste Busfrequenz** (z. B. $\ge 4\text{ MS/s}$ für $400\text{ kHz}$ I2C Fast-Mode; $\ge 50\text{–}100\text{ MS/s}$ für SPI).
- **Typische Hardware-Fehlerbilder auf Digitalbussen (I2C / SPI / UART):**
  - **I2C-Leitung (`SDA` oder `SCL`) klemmt dauerhaft auf `0 V` (`Stuck Low`):** Entweder ein Busteilnehmer-IC hat einen internen ESD-Diodenschluss nach `GND`, ein Slave hält `SDA` im abgebrochenen Clock-Zyklus fest, oder der externe Pull-up-Widerstand ($2{,}2\text{–}10\text{ k}\Omega$ nach `VCC`) ist offen (`open`).
  - **I2C-Flanken steigen extrem langsam (sägezahnförmig) an:** Pull-up-Widerstand zu hochohmig oder zu hohe Buskapazität.
  - **Taster-/Schalter-Fehlfunktionen (`Switch Debouncing`):** Mechanische Taster prellen $1\text{–}20\text{ ms}$; ist der RC-Entprellkondensator kurzgeschlossen (`short`), sieht der GPIO dauerhaft den aktiven Pegel (z. B. Dauer-Reset oder Dauer-Tastendruck).
- **Analogeingänge (`ADC`):**
  - Stimmen alle ADC-Messwerte eines Geräts proportional nicht, zuerst die analoge Referenzspannung **`VREF` / `AVDD`** und deren Stützkondensatoren gegen **`AGND`** prüfen!

---

<a id="sec-15"></a>
## 4. Löttechnik, Sektionale Inbetriebnahme & Fallstudien (`aKaReZa75/Repair`)

<a id="sec-16"></a>
### 4.1 Sektionale Bestückungs- & Prüf-Reihenfolge (`raw_sources/Repair/Videos.md`)
Beim Aufbau oder der Komplettsanierung einer Mikrocontroller-/Embedded-Platine wird **niemals alles auf einmal** eingelötet, sondern in validierten Stufen:
1. **Stufe 1 – Stromeingang & Spannungsregler:** Buchse, Sicherung, Schutzdiode sowie `12 V`-, `5 V`- und `3,3 V`- (bzw. `4,0 V`-GSM-)Regler samt Eingangs-/Ausgangskondensatoren einlöten.
2. **Stufe 2 – Pflicht-Zwischentest (ohne MCU!):** Spannung anlegen und **alle Ausgangsschienen nachmessen**. Erst wenn `5,0 V` und `3,3 V` exakt stimmen, darf der Mikrocontroller bestückt werden (verhindert den Tod der MCU durch einen falsch gelöteten Regler!).
3. **Stufe 3 – Kernlogik (MCU & Takt):** Mikrocontroller (`STM32F103C8`, `ATmega328P`), Quarz + Lastkondensatoren, Reset-Beschaltung und `SWD`/`JTAG`/`ISP`-Header einlöten $\rightarrow$ Stromaufnahme und Debugger-Verbindung (`ST-Link` / `J-Link`) testen.
4. **Stufe 4 – Kommunikation & Peripherie:** USB-Buchse, USB-UART-Wandler (`CH340`), Relais, Displays, SIM-Slot und HF-empfindliche GSM-Module (`Quectel M66`) bestücken und im Gesamtsystem testen.

<a id="sec-17"></a>
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

<a id="sec-18"></a>
### 4.3 Reparatur-Fallstudie: Defektes Multimeter (`Victor VC97` / EEPROM-Diagnose aus `raw_sources/Repair/Videos.md`)
- **Symptom:** Nach versehentlicher Spannungsmessung im Widerstands-/Diodenbereich funktionieren Widerstands-, Kapazitäts-, Dioden- und Durchgangsmessung nicht mehr oder zeigen völligen Unsinn, während Spannungsmessung noch geht.
- **Diagnose- & Reparaturweg:**
  1. **Eingangs-Schutzkette prüfen:** Im Multimeter sitzen hinter der `V/Ω/Hz`-Buchse ein **PTC-Thermistor** ($1\text{–}1{,}5\text{ k}\Omega$) sowie antiparallele **Schutz-Transistoren** (oft als niederohmige Zener-/Klemmdioden geschaltete `NPN`-Transistoren wie `S9013`/`2N3904`). Bei Überspannung schlagen diese Klemmtransistoren auf Kurzschluss durch und klemmen den Messeingang fest $\rightarrow$ auslöten und prüfen!
  2. **Kalibrier-EEPROM (`AT24C02` / `24C02`, SOIC-8) prüfen:** Durch Spannungsspitzen oder Unterspannung beim Einschalten korrumpiert häufig der Inhalt des externen I2C-EEPROMs.
  3. **Instandsetzung:** Klemmtransistoren/PTC ersetzen und das `AT24C02`-EEPROM mit einem intakten Referenz-Dump (`raw_sources/Repair/aKaReZa 26 - Repair, VC97 EEPROM IC/VC97_EEPROM_BackUP.bin`) neu flashen.
