---
doc_id: LDZ-REQ-001
title: LoadZone requirements
project: LoadZone
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# LoadZone requirements

These are first-pass requirements for the concept. Targets are proposals for review, awaiting Amish, and will be checked by calculation at TRL 3 and by test at TRL 4 or later. "Status" gives the position of the TRL 2 concept on first-order estimates.

Table 1. Requirements

| ID | Requirement | Target | Status at TRL 2 | Verification |
| --- | --- | --- | --- | --- |
| R1 | Detect the state of each vehicle slot | 97 % or more of slot states correct over a day, for cars, vans and box trucks, with traffic passing in the next lane | Unverified; magnetometer-only detection may be fooled by adjacent-lane traffic and by high-clearance trucks | Field trial against a manual count or time-lapse survey (TRL 5) |
| R2 | Report changes quickly | Slot state at the server within 60 s of a vehicle arriving or leaving | Met by estimate: 15 s debounce plus under 5 s to send | Timing calculation (TRL 3) |
| R3 | Long battery life | 5 years or more at 100 state changes a day plus hourly heartbeats | Met by estimate: about 7 years on two AA-size Li-SOCl2 cells | Power budget calculation (TRL 3) |
| R4 | Reach a gateway from road level | Uplinks received by a gateway 1 km away in a street canyon, with a van parked over the puck | Unverified; a vehicle overhead may add 10 to 20 dB of loss (estimate) | Link budget (TRL 3), then field test |
| R5 | Stay within network fair use | 30 s or less of uplink airtime per puck per day ([TTN fair use](https://www.thethingsnetwork.org/docs/lorawan/duty-cycle/)) | Partly met: about 9 s a day at SF7 and about 31 s at SF9, so at SF9 or slower the heartbeat must drop to every 2 h | Airtime calculation (TRL 3) |
| R6 | Survive traffic | Withstand a 50 kN static wheel load and repeated drive-overs by loaded trucks without cracking or debonding (target, basis to be set at TRL 3) | Not met for a printed prototype housing; cast polyurethane over potted electronics is proposed but unverified | Load calculation (TRL 3), then load test |
| R7 | Safe, low profile | Height 35 mm or less above the road, rounded edges, high-visibility color | Met in the massing model: 31 mm high, 150 mm diameter, yellow dome | Massing model and design review |
| R8 | Weather and temperature | Sealed to IP68; operate from -25 to +70 °C road surface temperature; resist salt, oil and fuel | Unverified; cell and sensor ratings to be checked against +70 °C | Datasheet review (TRL 3) |
| R9 | Privacy by design | Only slot state, timestamps and device health leave the device; no images, audio or vehicle identifiers | Met by design: a magnetometer cannot read plates or faces | Design review |
| R10 | Open data | Bay state available through an open API that maps onto the Curb Data Specification Events and Metrics APIs ([Open Mobility Foundation](https://www.openmobilityfoundation.org/about-cds/)) | Met in concept; mapping not yet written | Design review (TRL 3) |
| R11 | Sign legible to drivers (option) | Free-slot count legible at 25 m by day and night | Not met: a 7.5 in e-paper panel gives about 80 mm digits, legible at about 10 m by day (estimate), and it is unlit at night | Legibility calculation (TRL 3) |
| R12 | Sign power (option) | Sign runs within the host FieldNode's sensor energy allowance of about 2.75 Wh a day | Met by estimate: about 0.4 Wh a day without night lighting | Power budget (TRL 3) |
| R13 | Low cost | Two-puck bay kit $120 or less in parts at quantity 1 | Met: about $110. With the sign option, about $207 plus a host FieldNode (about $126), which exceeds the budget | Priced BOM |
| R14 | Quick install without road works | One puck bonded in 15 min or less by a two-person crew; removable without damaging the road | Unverified | Install trial (TRL 4 or later) |
| R15 | Tamper and theft resistant | No external screws; removal needs a heat gun or scraper; device reports removal | Unverified; removal detection from a sudden field and orientation change is proposed | Design review (TRL 3) |

## Requirements not met at TRL 2

- **R6 (traffic loads)** is not met by a printed housing and is unverified for cast polyurethane.
- **R11 (sign legibility)** is not met with a 7.5 in e-paper panel; a larger panel, a lit display or relying on a map layer instead are open options.
- **R13 (cost)** is met for the two-puck kit but not with the sign option.
- **R5 (airtime)** is met only at fast data rates unless the heartbeat interval is lengthened.
- **R1 and R4** are the main technical risks and cannot be confirmed without field data.

## Assumptions

- A vehicle slot is about 7 m long and the puck sits near its center, 1.3 m from the curb face (estimates; bay layouts vary by city).
- Loading bay turnover of up to 50 vehicles a slot a day, or 100 state changes, based on most delivery stops lasting 30 minutes or less ([Urban Freight Lab, 2019](https://urbanfreightlab.com/publications/the-final-50-feet-of-the-urban-goods-delivery-system-tracking-curb-use-in-seattle/)).
- Each LoRaWAN uplink costs about 16 mA·s at SF9, as estimated in FieldNode's design precis.
- Wheel load of 50 kN is a placeholder for a loaded truck's heaviest single wheel; the governing load case is to be set at TRL 3.
