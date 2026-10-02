---
doc_id: LDZ-PRC-001
title: LoadZone design precis
project: LoadZone
doc_type: Design precis
version: "0.6"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, components, first-order numbers, safety, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 figures from LDZ-CAL-001; design choices adopted for TRL 3 under LDZ-DDR-001; parametric model and drawing LDZ-DWG-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: "Constructable design (LDZ-DDR-003): base tray and sign brackets; cost against the value-engineering target"
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Decisions of 2026-10-02 carried in (LDZ-DEC-001 items 2 to 7): partner and US915, sealed for life, ASA tray, button heads, legend approval rule, surface puck only and not for plowed streets'
---

# LoadZone design precis

## Summary

LoadZone is a low, battery-powered puck bonded to the road in the middle of each vehicle slot of a loading bay. A 3-axis magnetometer senses the change in the Earth's magnetic field when a vehicle's steel body parks over it, and a LoRaWAN radio from the lab's FieldNode core reports "free" or "occupied" in about 18 s (39 s at worst at SF9). A server turns the reports into bay state, dwell times and an open data feed that maps onto the Curb Data Specification, and, as an option, a solar e-paper sign on an existing pole shows approaching drivers how many slots are free. The TRL 3 calculations (LDZ-CAL-001) give a cell life of 7.7 years at SF9 on two AA-size lithium thionyl chloride cells and a two-slot bay kit estimated at USD 116 in parts against a value-engineering target of USD 120. They also find the weak points: from road level under a parked van a puck reaches a gateway only about 350 m away in a street canyon, so each bay needs a gateway within 300 m (R4 as restated); the road bond is at risk under braking; and the sign is unlit, so it serves drivers by day only (R11 as restated). The design choices below were decided by Amish on 2026-09-25 (LDZ-DDR-001 and LDZ-DDR-002). Writing the prototype build plan (LDZ-BLD-001) made the design constructable without changing what it does (LDZ-DDR-003, open for Amish's review); open items are in the design decisions register (LDZ-DEC-001).

![LoadZone concept](../media/hero.png)

Figure 1. Concept massing model in a two-slot loading bay: the free slot (teal) with its puck, the occupied slot (orange) under a van, and the optional sign on an existing pole, with a 1.75 m person for scale. CONCEPT, NOT FOR FABRICATION.

## How it works

1. **Sense.** Each puck wakes about once a second and takes a single magnetometer reading. With no vehicle, the reading is the local Earth field plus a fixed offset learned at install. A car or van parked above distorts the field by several microtesla (estimate), mostly in the vertical axis.
2. **Decide.** Firmware compares the field change with an adaptive threshold and requires the new state to hold for about 15 s before accepting it, so traffic passing in the next lane and vehicles pausing briefly do not count. The baseline is re-learned slowly while the slot is free, to follow temperature drift and road works nearby.
3. **Report.** On each confirmed change, and hourly as a heartbeat, the puck sends a 12-byte LoRaWAN uplink: slot state, time since the last change, a confidence value, cell voltage and temperature. If the band is US915, the payload is packed to 11 bytes so that it fits the slowest US915 rate (LDZ-DDR-002). No raw magnetic data leave the device by default.
4. **Aggregate.** A LoRaWAN network server (TwinKit, The Things Network or a city network) passes uplinks to a small open service that keeps bay state, computes occupancy and dwell time, and publishes them in a form that maps onto the Curb Data Specification Events and Metrics APIs ([Open Mobility Foundation](https://www.openmobilityfoundation.org/about-cds/)).
5. **Show (option).** A FieldNode on a nearby pole, running as a LoRaWAN class C device, receives a short downlink when the bay state changes and redraws a 7.5 in e-paper panel set into a "Loading zone" sign: the number of free slots and an arrow. The same state can appear in carriers' routing tools and city maps through the data feed.

![Event flow](../media/flow.png)

Figure 2. Bay event flow, in percent of real occupancy changes (estimates, to be measured in a field trial).

## Main components

Table 1. Components (numbers match `bom/bom.csv` and Figure 3)

| No. | Component | Concept choice |
| --- | --- | --- |
| 1 | Puck dome | Rigid cast polyurethane, high-visibility yellow, 150 mm base diameter, 104 mm crown with a 6 mm radius, 31 mm total height, radio-transparent |
| 2 | Magnetometer | 3-axis, 16-bit, LIS2MDL class, on a small breakout ([STMicroelectronics](https://www.st.com/en/mems-and-sensors/lis2mdl.html)) |
| 3 | Controller and radio | STM32WL-class LoRaWAN module on a small carrier, the same core as FieldNode |
| 4 | Antenna | Flexible PCB antenna for 868 or 915 MHz, fixed inside the dome wall, above the cells |
| 5 | Cells | Two AA-size Li-SOCl2 bobbin cells (about 2.6 Ah each, typical rating) in parallel through one Schottky diode each, with an 85 °C hybrid pulse capacitor to supply transmit current |
| 6 | Base and potting | Printed 150 x 6 mm base tray with a ring that locates the dome, cradles for the cells, standoffs for the board and a rib for the antenna; the dome cavity is fully potted in semi-rigid polyurethane through a fill hole in the tray, and the potting carries wheel loads through to the base (LDZ-DDR-003) |
| 7 | Road-marker epoxy bed | Two-part road-marker epoxy, as used for raised pavement markers, as a 170 mm bed about 3 mm thick (LDZ-DDR-002; a bitumen pad is no longer used) |
| 8 | Sign face (option) | Aluminium composite panel, 450 x 600 mm, "Loading zone" legend and a window for the display |
| 9 | Display (option) | 7.5 in e-paper panel with driver board, behind a polycarbonate window in a sealed housing |
| 10 | Sign brackets (option) | Two aluminium channel brackets bolted to the back of the sign, each with a stainless band clamp for 60 to 90 mm poles (LDZ-DDR-003) |
| 11 | Host FieldNode (option) | Standard FieldNode (6 W panel, LiFePO4 cell, LoRaWAN class C), mounted above the sign and priced once in the FieldNode repo ($126.00) |

![Exploded view](../media/exploded.png)

Figure 3. Exploded view; callout numbers match `bom/bom.csv`. The puck is drawn at 4x scale.

![Cutaway](../media/cutaway.png)

Figure 4. Puck cutaway: potting (grey) fills the dome around the cells (orange), the radio board (teal) and the antenna at the dome's edge; the magnetometer sits on the board behind the section plane.

The parametric model is `cad/src/model.py` (STEP and STL in `cad/step/` and `cad/stl/`), and the general arrangement of the puck is drawing LDZ-DWG-001 at Rev P2 in `cad/drawings/`.

## First-order numbers

All values are from LDZ-CAL-001 v0.2, which the script `docs/04-calcs/sizing.py` reproduces. They are paper estimates, not measurements.

Table 2. Puck energy budget at SF9

| Quantity | Value | Assumption |
| --- | --- | --- |
| Sleep | 0.144 mAh/day | 6 µA: module in stop mode, magnetometer idle, leakage |
| Sampling | 0.480 mAh/day | One reading a second; 10 ms awake at 2 mA (20 µA average) |
| Uplinks | 0.488 mAh/day | 100 state changes and 24 heartbeats, 14.2 mA·s each at SF9 |
| Total | 1.11 mAh/day, 0.406 Ah/year | Sum of the above |
| Usable cell capacity | 3.12 Ah | 2 x 2.6 Ah, derated 40 % for cold, pulse loads and self-discharge |
| Cell life | 7.7 years | 9.6 years at SF7, 6.0 at SF10, 2.8 at SF12; R3 asks for 5 years |

**Airtime.** A 12-byte uplink is on air for 61.7 ms at SF7 and 205.8 ms at SF9. At 124 uplinks a day that is 7.7 s at SF7 and 25.5 s at SF9, within The Things Network's 30 s fair-use limit ([TTN](https://www.thethingsnetwork.org/docs/lorawan/duty-cycle/)), but 51.0 s at SF10. Pucks must therefore sit within SF9 reach of a gateway (R5 at risk).

**Latency.** A 15 s debounce, up to 1 s of sampling and about 2 s of network path give 17.7 s typically; the EU868 duty-cycle wait after a previous uplink raises the worst case to 38.6 s at SF9 and 59.2 s at SF10, within R2's 60 s.

**Pulse supply.** One SF9 uplink draws 9.3 mC, which a capacitor alone would supply with 0.3 V of droop at 31 mF (222 mF at SF12). Fresh cells sit at about 3.67 V, above the module's 3.6 V limit, so one Schottky diode per cell drops the rail to about 3.42 V and stops one cell charging the other.

**Detection.** The Earth's field is roughly 25 to 65 µT, well within the sensor's ±50 gauss (±5,000 µT) range. A line-dipole model calibrated to an assumed 10 µT under a parked van gives 10.6 µT for a car, 7.7 µT for a high-chassis box truck and 3.85 µT for a truck with little low steel, against a 3 µT threshold, while a van in the next lane gives 0.46 µT. The slot-center position sees vehicles anywhere in the slot and ignores neighbors; high-clearance trucks are the weak case, and R1 stays unverified until field data exist.

**Link.** At 11.5 dBm EIRP the SF9 link budget is 141.0 dB. With 10 dB lost at road level and 10 dB to a van overhead, the 3GPP urban microcell street-canyon model leaves -6.0 dB at 1 km out of sight and 2.6 dB in line of sight; the range out of sight is about 350 m with a 10 dB fade margin. The original 1 km target is not reachable, so R4 is restated as a gateway within 300 m of each bay (LDZ-DDR-002), which the 353 m range meets on paper.

**Load.** A 49 kN wheel (half of a 10 t axle) on the 92 mm flat crown gives 7.38 MPa, or 9.59 MPa with a 1.3 dynamic factor: a factor of 5.4 on rigid cast polyurethane and 2.0 on the potting beneath. The bond is the weak point: a braking tire could push 34.3 kN sideways, 1.51 MPa on the bed, against about 1.0 MPa for two-part epoxy on asphalt at 20 °C and much less when hot. A vehicle parked inside the bay lines keeps its tires at least 275 mm from the puck axis, so only maneuvering wheels cross it; R6 is restated on that basis with an epoxy bed (LDZ-DDR-002) and stays at risk.

**Sign.** Class C listening costs 15.2 mW and about 200 e-paper redraws a day add 0.015 Wh; the sign draws 0.42 Wh a day (17.7 mW), well within FieldNode's published allowance of 100 mW. Digits 78 mm high read at about 28 m by day on the MUTCD legibility index, better than the 10 m estimated at TRL 2, but the panel is unlit, and a 0.5 W front light would need 6.0 Wh a day, 2.5 times the allowance, so R11 is restated as a daylight-only target (LDZ-DDR-002) and met on paper. The sign takes about 200 downlinks a day, far above The Things Network's 10, so it needs a private network server such as TwinKit (decided, LDZ-DDR-002). Typical 7.5 in e-paper panels operate from about 0 to 50 °C, so refresh on freezing days is a limit to check.

**Mass and size.** Puck 451 g without the pad (75 g), 150 mm diameter, 31 mm high.

**Cost.** Value-engineering target: USD 120, for the two-puck kit only (LDZ-DDR-001, D6). Estimated cost of the constructable design: USD 116 (USD 4 under the target). The sign option adds USD 101 plus a host FieldNode at USD 126, and the one-off dome casting tooling USD 35 (see `bom/bom.csv`).

## Key design choices

Choices 1 to 7 and 9 to 11 are decided by Amish, 2026-09-25: go with recommendation (LDZ-DDR-001, D1 to D8, and LDZ-DDR-002). Choice 8 follows from choice 2. Choices 12 and 13, and the scope note in choice 1, were decided by Amish on 2026-10-02 (LDZ-DEC-001).

1. **Surface-bonded puck rather than an in-ground (cored) sensor.** No road works for a pilot and easy removal. In-ground units are better protected from plows and theft. Decided by Amish, 2026-10-02 (LDZ-DEC-001, item 7): only the surface puck is offered for now, and it is not for plowed streets; the cored, in-ground version is recorded as a later option.
2. **Magnetometer only, rather than magnetometer plus radar.** Lowest cost and power. A small radar looking up through the dome could confirm detections; it stays an open option if R1 is not met in trials.
3. **One puck per vehicle slot of about 7 m**, rather than one per bay. Bays hold one to three vans; slot-level state lets the sign say "1 free" rather than "space somewhere".
4. **Primary Li-SOCl2 cells rather than rechargeable cells with a solar cell on the puck.** A road-level solar cell is shaded by parked vehicles and soiled by tires. Two AA cells give margin over the 5-year target.
5. **LoRaWAN with the FieldNode core.** Shared firmware, tools and gateways across the lab. The sign, as a class C device, receives state by downlink (D7). At about 200 downlinks a day this needs a private network server such as TwinKit; on The Things Network the sign would have to listen to the pucks directly (LoRa point to point), which also keeps it working when the internet link is down. The sign option therefore requires a private network server or a city network that allows the downlinks (LDZ-DDR-002, O5).
6. **E-paper sign as an option, not the core.** It needs no power to hold an image and is readable in sun, but it is small and unlit, so its target is daylight only (R11) and drivers use the data feed at night. Many drivers may use the data through routing tools instead, which co-design should test.
7. **Open data in a Curb Data Specification form**, so a city can compare LoadZone with carrier and payment data.
8. **Privacy by physics.** The puck senses only a magnetic field, so it cannot identify vehicles or people even if its firmware is changed.
9. **Two-part road-marker epoxy bed** rather than a bitumen pad, for bond strength, with R6 restated around maneuvering wheels (LDZ-DDR-002, O3). Pull-off testing is TRL 4 work and on hold.
10. **A gateway within 300 m of each bay** (R4 restated, LDZ-DDR-002, O2), which also keeps pucks at SF9 or faster for R2, R3 and R5.
11. **Supply and potting details:** one Schottky diode per cell, an 85 °C hybrid pulse capacitor, a fully potted cavity and a 6 mm crown radius (LDZ-DDR-002, O6), and an 11-byte payload if the band is US915 (O7).
12. **Sealed for life** (LDZ-DEC-001, item 3, decided 2026-10-02): the cells cannot be replaced and the firmware changes only over the air; over-the-air updates are planned for TRL 4. The base tray is printed ASA sanded with 80 grit (item 4), and the sign face shows button heads (item 5).
13. **US915 as the default band** (LDZ-DEC-001, item 2, decided 2026-10-02), since the 11-byte payload already fits it.

## Relationship to other lab projects

- **FieldNode** provides the controller and radio core (the STM32WL-class module) for the puck and the complete host node for the sign option, as its README lists LoadZone among adopting projects. LoadZone uses FieldNode's radio currents and its $126.00 core cost (FND-CAL-001); the sign's 17.7 mW fits FieldNode's published 100 mW allowance.
- **TwinKit** is the default gateway and data platform, and the sign option needs it (or another private network server) for its class C downlinks; for the pucks alone, any LoRaWAN network server works.
- **CurbCount** counts people, bicycles and vehicles passing the curb; LoadZone reports who is stopped at it. Both would feed **CityTwin**.
- **CalRig** could check magnetometer offset and noise before installation.

## Safety

> **Safety:** Installing on a road is dangerous. Work only with the road authority's permit, with a trained crew, under the traffic management that local rules require, and with high-visibility clothing. Never install from a live traffic lane without protection.

> **Safety:** Lithium thionyl chloride cells are primary lithium cells. Do not recharge, short, crush, heat or open them; they can vent toxic and corrosive gas and burn. Connect the two cells in parallel only through one diode each so that one cell can never charge the other, fit a fuse, keep the pulse capacitor within its voltage and temperature rating, and recycle spent cells as hazardous waste.

> **Safety:** Two-part road-marker epoxy is chemically hazardous and some grades are applied hot; uncured resin and hardener irritate skin and can sensitize. Follow the maker's safety data sheet, wear gloves and eye protection, and ventilate. Polyurethane casting resins contain isocyanates; cast only with ventilation and suitable respiratory protection.

> **Safety:** The puck is a raised object in the roadway. Keep it low with rounded edges, place it away from bike lanes and crosswalks, and keep it high-visibility. Check after install that it is fully bonded, since a loose puck can be thrown by a tire.

> **Safety:** The sign option is work at height on a street pole. Use a stable platform with a second person present, keep clear of overhead power lines, and use only poles whose owner permits the added wind load. Deburr the aluminium sign panel's edges. The prototype legend is a placeholder: before a sign is mounted on a street, its legend is drawn to the trial city's sign rules (in the US, the MUTCD) and approved by the city traffic engineer (LDZ-DEC-001, item 6).

## Open questions

- [ ] Detection accuracy with magnetometer only, especially for high-clearance trucks: is a radar or second magnetometer needed to meet R1? Awaiting field data.
- [x] Gateway spacing: a gateway within 300 m of each bay (R4 restated, LDZ-DDR-002).
- [x] Bond: two-part road-marker epoxy, with R6 restated (LDZ-DDR-002).
- [x] Sign: daylight-only target, on a private network server (LDZ-DDR-002).
- [x] First trial partner and band (O1). Decided by Amish, 2026-10-02 (LDZ-DEC-001, item 2): the first candidate type to approach, not yet agreed, is a city curb-management or transportation team that has published or piloted the Curb Data Specification, in a city without routine snow plowing; US915 by default, with the 11-byte payload.
- [x] Snow and plows. Decided by Amish, 2026-10-02 (LDZ-DEC-001, item 7): the surface puck is not for plowed streets; a cored, in-ground version is a later option.
