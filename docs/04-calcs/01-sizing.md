---
doc_id: LDZ-CAL-001
title: LoadZone sizing calculations
project: LoadZone
doc_type: Calculation note
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (airtime, energy and cell life, latency, link, detection, loads, size and mass, sign option, cost) with a status for every requirement
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# LoadZone sizing calculations

On paper, LoadZone meets eleven of its fifteen requirements (seven by calculation, four by design), has three at risk and leaves one that only an installation trial can settle; none is now not met. Version 0.2 applies Amish's decisions of 2026-09-25 (LDZ-DDR-002). **R4**, restated as a gateway within 300 m of the bay, is met on paper: from road level under a parked van a puck reaches about 353 m in a street canyon at SF9 with a 10 dB fade margin (it was not met against the TRL 2 target of 1 km). **R11**, restated as daylight only, is met on paper at about 28 m (it was not met at night). R1 (detection), R5 (airtime at slow data rates) and R6 (bond under braking, now with a two-part epoxy bed) are at risk. The core numbers of the TRL 2 concept stand or improve: cell life is 7.7 years at SF9, the worst-case report time is 38.6 s, and the two-puck kit costs $114.00 against the $120 budget.

Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B2], is the line of the script's output that carries it. Run it from the repo root with `python docs/04-calcs/sizing.py`; it also writes `docs/04-calcs/results.csv`. The script imports `PARAMS`, `derived()` and the part volumes from `cad/src/model.py`, so the geometry here is the geometry in the STEP files and in drawing LDZ-DWG-001. It reads the costs from `bom/bom.csv` and `budget_usd` from `project.yaml`. All values are first-principles estimates; nothing is measured.

> **Safety:** These are paper estimates. They do not show that a puck is safe to leave in a roadway, that the primary lithium cells are safe in a hot road, or that the bond will hold. Bond strength, cell temperature and crush behavior must be checked on hardware before any puck is installed, and only under a road permit with traffic management. See LDZ-PRC-001, Safety.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design unless a source is given.*

| Input | Value | Basis |
| --- | --- | --- |
| Traffic | 100 state changes a day per puck plus hourly heartbeats: 124 uplinks | LDZ-REQ-001 R3 |
| Payload | 12 bytes plus 13 bytes of LoRaWAN overhead, 125 kHz, CR 4/5; packed to 11 bytes if the band is US915 | LDZ-PRC-001; LDZ-DDR-002 |
| Radio currents | 45 mA transmit at +14 dBm, 4.6 mA receive, 8 mA controller awake 0.5 s per uplink, two 0.1 s receive windows | Same as FND-CAL-001 |
| Sleep and sampling | 6 µA sleep; one reading a second, 10 ms awake at 2 mA | LDZ-PRC-001 v0.2 |
| Cells | 2 x 2.6 Ah in parallel, derated 40 % for cold, pulse loads, self-discharge and end-of-life voltage | ER14505 class, typical rating |
| Fair use | 30 s of uplink airtime and 10 downlinks per node per day on The Things Network | [TTN](https://www.thethingsnetwork.org/docs/lorawan/duty-cycle/), checked 2026-09-25 |
| Duty cycle | 1 % on the EU868 default sub-band; 10 % on the RX2 sub-band | EU868 regional rules |
| Link | Puck antenna -2 dBi once potted; 10 dB road-level loss; 10 dB (typical) to 20 dB (worst) for a van overhead; gateway 10 m high, 2 dBi, 2 dB feeder loss; 6 dB noise figure | Estimates; FND-CAL-001 for the gateway side |
| Path loss | 3GPP TR 38.901 urban microcell street canyon (UMi), Table 7.4.1-1, at 868 MHz with the user height at its 1.5 m floor; the road-level loss covers the lower antenna | Standard model, used outside its height range |
| Detection | A vehicle is a line of vertical induced dipoles along its length; 10 µT under the middle of a parked van (calibration); 3 µT threshold, 10 times the magnetometer's 0.3 µT RMS noise | Assumption; only a field log can set these |
| Loads | Half of a 10 t single axle (49 kN), x1.3 dynamic; friction 0.7; rigid cast polyurethane 40 MPa and semi-rigid potting 15 MPa in compression; two-part road-marker epoxy to asphalt shear 1.0 MPa at 20 °C, 0.2 MPa at 50 °C | Typical values, to be checked against chosen materials |
| Vehicles | Bay 2.6 m wide; van 2.0 m wide, 1.75 m track, 225 mm tires; car 1.8 m, 1.55 m, 200 mm | Typical dimensions |
| Sign | Class C receiver on at 15.2 mW; 200 redraws a day at 26.4 mW for 5 s plus the controller; 90 % rail efficiency; 7.5 in panel with a 97.9 mm active height, digits 80 % of it | Typical 7.5 in panel data |
| Legibility | 30 ft of distance per inch of letter height (0.36 m per mm) | MUTCD, section 2A.13 |

## 2. Airtime (R5)

A 12-byte uplink is on air for 61.7 ms at SF7, 205.8 ms at SF9 and 1,482.8 ms at SF12 [A1]. At 124 uplinks a day that is 7.7 s at SF7, 14.0 s at SF8 and 25.5 s at SF9, all within the 30 s fair-use limit, but 51.0 s at SF10 and 183.9 s at SF12 [A1]. At SF10 even the state changes alone exceed the limit: 73 uplinks a day is the most that fits. **R5 is at risk**: met at SF7 to SF9, not met at SF10 and slower. The TRL 2 note used FieldNode's longer 20-byte airtime and gave 31 s at SF9; with the 12-byte payload SF9 fits with hourly heartbeats, so the 2 h heartbeat fallback is no longer needed at SF9. If the band chosen in O1 is US915, the payload is packed to 11 bytes, the most the slowest US915 125 kHz rate (SF10) carries; an 11-byte uplink is on air for 370.7 ms at SF10 [A2]. This firmware rule is decided (LDZ-DDR-002); the figures in this note stay on EU868 until the band is chosen. A private gateway (TwinKit) is bound only by the 1 % duty cycle, which allows far more.

## 3. Energy and cell life (R3)

At SF9 a puck uses 1.11 mAh a day: 0.144 mAh asleep, 0.480 mAh for sampling (20 µA average) and 0.488 mAh for 124 uplinks at 14.2 mA·s each [B1, B2]. That is 0.406 Ah a year against 3.12 Ah usable, **a life of 7.7 years, and R3 is met** [B2, B3]. Sampling and uplinks each take about 44 % of the budget [B3], so a slower sampling rate is the first lever if life must grow. Life is 9.6 years at SF7, 6.0 years at SF10 and 2.8 years at SF12 [B2], so pucks far from a gateway fail R3 as well as R5.

**Pulse supply.** One SF9 uplink draws 9.3 mC; if the capacitor supplied it alone with 0.3 V of droop it would need 31 mF, and 222 mF at SF12 [B4]. Bobbin Li-SOCl2 cells cannot deliver 45 mA pulses well, so the capacitor is essential. Ordinary supercapacitors are often rated only to 60 to 70 °C, below the road-surface target, so the BOM now calls for an 85 °C hybrid pulse capacitor.

**Supply voltage.** Fresh Li-SOCl2 cells sit at about 3.67 V open circuit, above the 3.6 V recommended maximum of STM32WL-class modules. One Schottky diode per cell brings this to 3.42 V and also stops one cell charging the other, which primary lithium cells must never do [B5]. This is an engineering proposal (LDZ-DDR-001, O6).

## 4. Report latency (R2)

A new state must hold for 15 s, sampling adds up to 1 s and the network path about 2 s, so a report reaches the server in 17.7 s typically [C1]. The worst case adds the EU868 duty-cycle wait after the previous uplink: 20.4 s at SF9, for 38.6 s in all, and 59.2 s at SF10 [C1]. **R2 is met at SF10 or faster**; at SF11 (100.3 s) and SF12 (166.3 s) it is not.

## 5. Link from road level (R4)

With 11.5 dBm EIRP the link budget at SF9 is 141.0 dB [D1, D2]. The UMi model gives 127.0 dB of non-line-of-sight path loss at 1 km to a 10 m gateway, and 118.4 dB in line of sight [D1]. Adding 10 dB for an antenna at road level and 10 dB for a van overhead leaves **-6.0 dB at 1 km out of sight and 2.6 dB in line of sight; with the worst vehicle loss, -16.0 dB** [D2]. The range out of sight is 678 m with no fade margin and 353 m with 10 dB [D2]. SF12 would reach 576 m with the fade margin [D2] but breaks R3 and R5. The 1 km target of versions up to LDZ-REQ-001 v0.3 is not met. Under LDZ-DDR-002 (O2) R4 is restated as a gateway within 300 m of the bay; 353 m is 1.18 times that distance [D3], so **R4 is met on paper**, with a thin margin that a field survey must confirm. The UMi model is used below its 1.5 m height floor; the 10 dB road-level loss is the estimate that covers this and only a field survey can settle it.

## 6. Detection (R1)

With the line-dipole model calibrated to 10 µT under a parked van, a car gives 10.6 µT, a small car pushed to one end of the 7 m slot 10.5 µT, a high-chassis box truck 7.7 µT and a box truck with little steel low down 3.85 µT, just 1.28 times the 3 µT threshold [E1]. A van passing in the next lane gives 0.46 µT and a van parked in the next slot 0.08 µT, both well below the threshold [E1]. The geometry therefore favors the slot-center position (D3): vehicles anywhere in the slot are seen, and neighbors are not. The margins rest on the 10 µT calibration, which is an assumption. **R1 is at risk and not verifiable at TRL 3**; high-clearance trucks are the weak case, and a short field log under parked vehicles would settle it.

## 7. Loads and bond (R6)

The load basis is now set: half of a 10 t single axle, 49.0 kN static, or 63.8 kN with a 1.3 dynamic factor for slow maneuvering [F1]. If the whole wheel bears on the 92 mm flat crown, the stress is 7.38 MPa static and 9.59 MPa dynamic; spread over the base it is 2.78 MPa [F1]. That gives factors of 5.4 (static) and 4.2 (dynamic) on rigid cast polyurethane, but only 2.0 and 1.6 on the potting under the crown [F2]. The bond is weaker: with a friction coefficient of 0.7 the tire can push 34.3 kN sideways, 1.51 MPa over the 170 mm pad, against an assumed adhesive-to-asphalt strength of 1.0 MPa at 20 °C (factor 0.66) and 0.2 MPa at 50 °C (0.13) [F3]. The bed is now two-part road-marker epoxy rather than a bitumen pad (LDZ-DDR-002, O3), so the 1.0 MPa figure is the epoxy-to-asphalt value, in which the asphalt surface usually governs. These are upper bounds, since a truck tire deflects around a 31 mm puck and rarely brakes on it. Wheel geometry helps: a van or car parked inside the bay lines keeps its nearest tire edge at least 462 mm (van) or 275 mm (car) from the puck axis, against a 75 mm puck radius, so parked wheels straddle the puck and only maneuvering wheels cross it [F4]. R6 is restated with this finding (LDZ-DDR-002, O3): the load case is a maneuvering wheel crossing the puck, and the slot-center placement keeps it out of parked wheel paths. **R6 is still at risk** on debonding under braking; crushing is met on paper. The pull-off and shear test on asphalt that would settle it is TRL 4 work and on hold.

## 8. Size and mass (R7)

The model gives a puck 31.0 mm high on a 150 mm base, a 170 mm pad, a 104 mm crown and a 6 mm crown radius [G1]. **R7 is met.** From the model volumes the puck weighs 451 g without its pad, and the pad 75 g [G2]; the TRL 2 estimate of 0.35 kg is corrected, because the cavity is now fully potted.

## 9. Sign option (R11, R12)

**Power (R12).** The class C receiver draws 15.2 mW, or 0.364 Wh a day, and 200 redraws add 0.015 Wh; with 90 % rail efficiency the sign draws 0.424 Wh a day, or 17.7 mW [H1]. That is 18 % of FieldNode's allowance of 100 mW, which FieldNode now publishes (FND-DDR-002) [H2]. **R12 is met on paper.** The sign takes about 200 downlinks a day, against The Things Network's limit of 10 [H5], so D7 works only on a private network server such as TwinKit, where the downlinks use 33 s a day, or 0.38 % of the RX2 sub-band allowance [H5]. This is decided: the sign option requires a private network server or a city network that allows it (LDZ-DDR-002, O5). Typical 7.5 in e-paper panels are rated for about 0 to 50 °C in operation, so the sign may not refresh on freezing days; this is a limit to confirm with the panel chosen.

**Legibility (R11).** Digits 78 mm high on the 97.9 mm panel read at about 28.2 m by day at full contrast, using the MUTCD legibility index of 0.36 m per mm; 69 mm digits would be enough for 25 m [H4]. E-paper contrast is lower than a printed sign's, so the daytime figure is optimistic. The panel is unlit, and a 0.5 W front light for 12 h a night would add 6.0 Wh a day, 2.5 times the 100 mW allowance [H3]. Under LDZ-DDR-002 (O4) R11 is restated as a daylight-only target of 25 m, so **R11 is met on paper**; at night drivers rely on the data feed.

## 10. Cost (R13)

The two-puck kit costs **$114.00 against `budget_usd` $120**, a margin of $6.00; one puck costs $54.00 [I1]. Under D6 the budget covers the two-puck kit only. The sign option costs $97.00, and its host FieldNode $126.00 (priced in the FieldNode BOM), for $337.00 per bay with the sign [I1]. **R13 is met on paper**, with a thin margin on indicative prices.

## 11. Requirement status

*Table 2. Requirement status from this note. The same rows are in `docs/04-calcs/results.csv`.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R1 | Detect slot state | Van 10.0 µT, high-chassis truck 7.7 µT, weak-steel truck 3.85 µT, next lane 0.46 µT against 3 µT | 97 % correct over a day | **At risk** (not verifiable at TRL 3) |
| R5 | Fair-use airtime | 7.7 s at SF7, 25.5 s at SF9, 51.0 s at SF10, 183.9 s at SF12 | 30 s a day or less | **At risk** (not met at SF10 to SF12) |
| R6 | Survive traffic | Crown 7.4 MPa, factor 5.4 on PU and 2.0 on potting; epoxy bond shear 1.51 MPa, factor 0.66 at 20 °C | 49 kN maneuvering wheel crossing the puck, no cracking or debonding; parked wheels straddle it | **At risk** (debond under braking) |
| R14 | Quick install | Bonded pad, no road cutting | 15 min per puck | Not verifiable at TRL 3 |
| R2 | Report quickly | 17.7 s typical; 38.6 s worst at SF9, 59.2 s at SF10 | 60 s or less | Met on paper (SF10 or faster) |
| R3 | Battery life | 7.7 years at SF9; 2.8 years at SF12 | 5 years or more | Met on paper |
| R4 | Reach a gateway from road level | 353 m NLOS range with a van over and 10 dB fade margin at SF9 | Gateway within 300 m in a street canyon (restated) | Met on paper |
| R7 | Low profile | 31 mm high, 150 mm diameter, 6 mm crown radius, yellow | 35 mm or less, rounded | Met on paper |
| R11 | Sign legible (option) | About 28 m by day at full contrast; unlit at night | 25 m by day (restated, daylight only) | Met on paper |
| R12 | Sign power (option) | 0.42 Wh a day (17.7 mW) against 100 mW | Within the FieldNode allowance | Met on paper (private network only) |
| R13 | Low cost | $114.00 for two pucks | $120 or less | Met on paper |
| R8 | Weather and temperature | Parts rated -40 to +85 °C with an 85 °C pulse capacitor; fully potted | IP68; -25 to +70 °C | Met by design (sealing not verifiable at TRL 3) |
| R9 | Privacy | Magnetometer only; state, timer, confidence, voltage, temperature | No images, audio or identifiers | Met by design |
| R10 | Open data | CDS Events `park_start`, `park_end`, `scheduled_report`, `comms_lost`, `comms_restored`; Metrics for occupancy and dwell | Maps onto CDS Events and Metrics | Met by design |
| R15 | Tamper resistance | No external fasteners; removal flagged by a field and orientation step | No screws; removal reported | Met by design |

Counts: none not met, 3 at risk, 1 not verifiable at TRL 3, 7 met on paper, 4 met by design [K]. In version 0.1: 2 not met (R4, R11), 3 at risk, 1 not verifiable, 5 met on paper, 4 met by design.

The Curb Data Specification event types used for R10 were checked against the specification's Events API on 2026-09-25 ([Open Mobility Foundation, CDS Events](https://github.com/openmobilityfoundation/curb-data-specification/blob/main/events/README.md)).

## 12. Checks against the TRL 2 figures

*Table 3. TRL 2 claims (LDZ-PRC-001 v0.2) against this note.*

| TRL 2 claim | This note | Action |
| --- | --- | --- |
| About 20 s to report | 17.7 s typical, 38.6 s worst at SF9 | Precis updated |
| About 1.2 mAh a day, about 7 years | 1.11 mAh a day, 7.7 years at SF9 | Precis updated |
| 72 ms at SF7, 247 ms at SF9; 9 s and 31 s a day | 61.7 ms and 205.8 ms for 12 bytes; 7.7 s and 25.5 s a day | Corrected; R5 now met at SF9 |
| A vehicle overhead leaves room for a gateway a few hundred meters away | 353 m with a 10 dB fade margin | Stands; R4 restated to 300 m and met on paper (LDZ-DDR-002) |
| 2.8 MPa over the base; printed housing would fail | 2.78 MPa over the base, 7.38 MPa at the crown; cast PU adopted | Precis updated; bond is the new risk |
| Sign legible at about 10 m | About 28 m by day at full contrast | Corrected; R11 restated to daylight only and met on paper (LDZ-DDR-002) |
| Sign about 0.4 Wh a day | 0.42 Wh a day drawn | Stands |
| Puck about 0.35 kg | 451 g without pad | Corrected |
| Two-puck kit about $110 | $114.00 with the diodes and 85 °C capacitor | Corrected |
