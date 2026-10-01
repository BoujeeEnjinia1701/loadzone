---
doc_id: LDZ-REQ-001
title: LoadZone requirements
project: LoadZone
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-10-01'
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
  change: First measurable requirements for TRL 2, with status against the concept
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from LDZ-CAL-001; R6 load basis set; R13 redefined to the two-puck kit (LDZ-DDR-001 D6)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Constructable design (LDZ-DDR-003); R13 reported against the value-engineering target
---

# LoadZone requirements

These are the requirements for the concept, checked by calculation at TRL 3 in LDZ-CAL-001 v0.3 on the constructable design of LDZ-DDR-003, which changes no requirement status. On 2026-09-25 Amish accepted the recommendations (LDZ-DDR-002), so this version restates three targets: R4 is now a gateway within 300 m of the bay rather than 1 km; R6 is restated with the finding that the wheels of a vehicle parked inside the bay lines straddle the puck, and the bond is two-part road-marker epoxy; and R11 is a daylight-only target. R13 covers the two-puck bay kit only, with the sign option costed separately (LDZ-DDR-001 D6, now decided); its figure is a value-engineering target, not a spending limit (Amish, 2026-10-01). R12 uses FieldNode's published 100 mW allowance.

Table 1. Requirements

| ID | Requirement | Target | Status at TRL 3 (LDZ-CAL-001) | Verification |
| --- | --- | --- | --- | --- |
| R1 | Detect the state of each vehicle slot | 97 % or more of slot states correct over a day, for cars, vans and box trucks, with traffic passing in the next lane | **At risk**, not verifiable at TRL 3: a line-dipole model puts a van at 10.0 µT, a weak-steel box truck at 3.85 µT and next-lane traffic at 0.46 µT against a 3 µT threshold, on an assumed calibration | Field trial against a manual count or time-lapse survey (TRL 5) |
| R2 | Report changes quickly | Slot state at the server within 60 s of a vehicle arriving or leaving | Met on paper at SF10 or faster: 17.7 s typical, 38.6 s worst at SF9, 59.2 s at SF10 | Timing calculation (TRL 3) |
| R3 | Long battery life | 5 years or more at 100 state changes a day plus hourly heartbeats | Met on paper: 7.7 years at SF9 on two AA-size Li-SOCl2 cells derated 40 %; 2.8 years at SF12 | Power budget calculation (TRL 3) |
| R4 | Reach a gateway from road level | Uplinks received by a gateway within 300 m of the bay in a street canyon, with a van parked over the puck (restated from 1 km, LDZ-DDR-002) | Met on paper: 353 m out of sight at SF9 with a 10 dB fade margin, 1.18 times the distance | Link budget (TRL 3), then field survey |
| R5 | Stay within network fair use | 30 s or less of uplink airtime per puck per day ([TTN fair use](https://www.thethingsnetwork.org/docs/lorawan/duty-cycle/)) | **At risk**: 25.5 s a day at SF9, but 51.0 s at SF10 and 183.9 s at SF12 | Airtime calculation (TRL 3) |
| R6 | Survive traffic | Withstand a maneuvering wheel crossing the puck at 49 kN (half of a 10 t single axle), 64 kN with a 1.3 dynamic factor, and repeated drive-overs by loaded trucks, without cracking or debonding, on a two-part road-marker epoxy bed. The puck sits at the slot center so that the wheels of a vehicle parked inside the bay lines straddle it (restated, LDZ-DDR-002) | **At risk**: crushing met on paper (factor 5.4 on the cast dome, 2.0 on the potting); parked wheels clear the puck by at least 275 mm; bond shear under braking 1.51 MPa against about 1.0 MPa assumed for epoxy on asphalt | Load calculation (TRL 3), then load and pull-off test (TRL 4, on hold) |
| R7 | Safe, low profile | Height 35 mm or less above the road, rounded edges, high-visibility color | Met on paper: 31 mm high, 150 mm diameter, 6 mm crown radius, yellow dome | Parametric model and drawing LDZ-DWG-001 |
| R8 | Weather and temperature | Sealed to IP68; operate from -25 to +70 °C road surface temperature; resist salt, oil and fuel | Met by design: parts rated -40 to +85 °C with an 85 °C pulse capacitor; fully potted. Sealing not verifiable at TRL 3 | Datasheet review (TRL 3), then immersion test |
| R9 | Privacy by design | Only slot state, timestamps and device health leave the device; no images, audio or vehicle identifiers | Met by design: a magnetometer cannot read plates or faces | Design review |
| R10 | Open data | Bay state available through an open API that maps onto the Curb Data Specification Events and Metrics APIs ([Open Mobility Foundation](https://www.openmobilityfoundation.org/about-cds/)) | Met by design: events map onto `park_start`, `park_end`, `scheduled_report`, `comms_lost` and `comms_restored` | Design review (TRL 3) |
| R11 | Sign legible to drivers (option) | Free-slot count legible at 25 m by day (daylight only, restated, LDZ-DDR-002); at night drivers use the data feed | Met on paper: about 28 m by day at full contrast with 78 mm digits | Legibility calculation (TRL 3) |
| R12 | Sign power (option) | Sign runs within the host FieldNode's sensor energy allowance | Met on paper: 0.42 Wh a day (17.7 mW) against FieldNode's published 100 mW; needs a private network for its 200 downlinks a day (LDZ-DDR-002, O5) | Power budget (TRL 3) |
| R13 | Low cost | Two-puck bay kit in parts at quantity 1 against a value-engineering target of USD 120; the sign option and its host FieldNode are costed separately and excluded | Met on paper: estimated USD 116.00, USD 4.00 under the target. Sign option USD 101.00 plus a FieldNode at USD 126.00 | Priced BOM |
| R14 | Quick install without road works | One puck bonded in 15 min or less by a two-person crew; removable without damaging the road | Not verifiable at TRL 3 | Install trial (TRL 4 or later) |
| R15 | Tamper and theft resistant | No external screws; removal needs a heat gun or scraper; device reports removal | Met by design: bonded, no fasteners; removal flagged by a sudden field and orientation change | Design review (TRL 3) |

## Requirements at risk at TRL 3

No requirement is now not met. Before LDZ-DDR-002, R4 (1 km) and R11 (night) were not met; both are restated and met on paper.

- **R1 (detection)** is at risk for high-clearance trucks and rests on an assumed signal; only field data can settle it.
- **R5 (airtime)** is not met at SF10 or slower; R2 and R3 also fail at SF11 and SF12, so pucks must be placed within SF9 reach of a gateway, which the 300 m gateway distance in R4 supports.
- **R6 (traffic)** is at risk on debonding under braking, even with the epoxy bed; a pull-off and shear test on asphalt would settle it, but that is TRL 4 work and on hold.

## Assumptions

- A vehicle slot is about 7 m long and the puck sits near its center, 1.3 m from the curb face (estimates; bay layouts vary by city).
- Loading bay turnover of up to 50 vehicles a slot a day, or 100 state changes, based on most delivery stops lasting 30 minutes or less ([Urban Freight Lab, 2019](https://urbanfreightlab.com/publications/the-final-50-feet-of-the-urban-goods-delivery-system-tracking-curb-use-in-seattle/)).
- Each 12-byte LoRaWAN uplink costs about 14.2 mA·s at SF9 with FieldNode's radio currents (LDZ-CAL-001). If the band is US915, the payload is packed to 11 bytes (LDZ-DDR-002); the band is still open.
- The wheel load is half of a 10 t single axle (49 kN); a vehicle parked inside the bay lines straddles the puck, so wheel loads come from maneuvering (LDZ-CAL-001, section 7).
