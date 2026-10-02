---
doc_id: LDZ-DDR-002
title: LoadZone recommendations accepted
project: LoadZone
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of all recommendations and what changed in the repo
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: O1 decided by Amish on 2026-10-02 as recommended in LDZ-DEC-001
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below marked "Decided" is decided by Amish, 2026-09-25: go with recommendation. The item without a recommendation (O1) was given one in the design decisions register (LDZ-DEC-001, item 2) and decided by Amish on 2026-10-02: "i approve your recommendations for all 555 open decisions."

## Context

After the TRL 3 session, LoadZone had eight items adopted for TRL 3 work pending Amish's review (LDZ-DDR-001, D1 to D8) and six new items raised at TRL 3 (O2 to O7), each with a recommendation. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Where a recommendation offered several options, the recommended option is the decision. Items that carried no recommendation are not decided by this record.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D1 to D8 | LDZ-DDR-001 items: surface-bonded puck; magnetometer only; one puck per 7 m slot; two AA-size Li-SOCl2 cells; cast polyurethane dome over fully potted electronics; sign outside the $120 budget, which covers the two-puck kit only; LoRaWAN class C downlink to the sign; a feed that maps onto the Curb Data Specification | As recommended in LDZ-DDR-001 | LDZ-DDR-001 v0.2 status wording; LDZ-PRC-001 v0.4 "Key design choices" now decided. `budget_usd` stays $120 (D6 redefined the budget's scope rather than its figure); pitch and problem unchanged, since no rewording was recommended |
| O2 | R4 link from under a van | Option (a): restate R4 as a gateway within 300 m of the bay | R4 in LDZ-REQ-001 v0.4 now reads 300 m, not 1 km; LDZ-CAL-001 v0.2 [D3]: 353 m range at SF9 with a 10 dB fade margin, 1.18 times the distance. R4 moves from not met to met on paper. Precis, problem statement, BOM notes, blueprint key figures and a note on LDZ-DWG-001 Rev P2 |
| O3 | R6 bond under braking | Option (c): two-part road-marker epoxy, and R6 restated with the finding that parked wheels straddle the puck | BOM line 7 is now a two-part road-marker epoxy bed (was a bitumen pad or epoxy), price unchanged at $4.00 per puck; `cad/src/model.py` comment, drawing material note and a bond note on LDZ-DWG-001 Rev P2; exploded-view label; R6 restated around a maneuvering wheel crossing the puck. R6 stays at risk: bond shear 1.51 MPa against about 1.0 MPa assumed, factor 0.66 (unchanged). The pull-off test is TRL 4 work and on hold |
| O4 | R11 night legibility | Option (a): a daylight-only legibility target | R11 restated to 25 m by day; about 28 m by day on paper, so R11 moves from not met (night) to met on paper |
| O5 | Sign network | The sign option requires a private network server (TwinKit) or a city network that allows about 200 downlinks a day; on The Things Network it would need LoRa point to point | Stated as a decided constraint in the precis and problem statement; TwinKit class C support listed as a cross-repo action |
| O6 | Engineering proposals | Confirmed: one Schottky diode per cell, an 85 °C hybrid pulse capacitor, a fully potted cavity and a 6 mm crown radius | Already in the model and BOM; wording changed from "awaiting confirmation" to decided. No geometry or cost change |
| O7 | Payload size | Pack the payload into 11 bytes if the band chosen in O1 is US915 | Firmware rule stated in the precis and requirements; LDZ-CAL-001 v0.2 [A2]: 370.7 ms at SF10 for 11 bytes. Figures stay on EU868 until the band is chosen. Writing the firmware is TRL 4 work and on hold |

LDZ-CAL-001 v0.2 also takes FieldNode's published 100 mW sensor allowance (FND-DDR-002) in place of the earlier 115 mW and 100 mW pair; the sign's 17.7 mW is 18 % of it, and R12 stays met on paper.

*Table 2. Item left open by this record, decided on 2026-10-02.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First trial partner (a city curb team, a business district or a carrier) and the LoRaWAN band. No recommendation was made. | **Decided by Amish, 2026-10-02:** first candidate type to approach (not yet agreed), a city curb-management or transportation team that has published or piloted the Curb Data Specification, in a city without routine snow plowing; US915 is the default band, since the 11-byte payload already fits it (LDZ-DEC-001, item 2) |

The suggestion in `docs/REVIEW.md` that CurbCount and LoadZone could share one server and data feed through CityTwin was a suggestion, not a recommendation awaiting decision, and is not adopted.

## Consequences

- Requirement status (LDZ-CAL-001 v0.2): none not met, 3 at risk (R1, R5, R6), 1 not verifiable at TRL 3 (R14), 7 met on paper, 4 met by design. Before: 2 not met (R4, R11), 3 at risk, 1 not verifiable, 5 met on paper, 4 met by design.
- Controlled documents revised: LDZ-PRB-001 v0.4, LDZ-PRC-001 v0.4, LDZ-REQ-001 v0.4, LDZ-CAL-001 v0.2, LDZ-DDR-001 v0.2; drawing LDZ-DWG-001 Rev P2 (notes and material; geometry unchanged).
- Cost: two-puck kit $114.00 against the unchanged $120 `budget_usd`; sign option $97.00 plus a host FieldNode at $126.00, outside the budget.
- Cross-repo actions (other repos not edited): see `docs/REVIEW.md`, session "recommendations accepted".
- TRL 4 remains on hold by Amish's instruction. The bond pull-off and shear test, the field link survey, the magnetometer field log and the firmware payload rule are TRL 4 work and have not been started.
