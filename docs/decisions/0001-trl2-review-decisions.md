---
doc_id: LDZ-DDR-001
title: LoadZone TRL 2 review decisions
project: LoadZone
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review recommendations adopted for TRL 3 work under Amish's 2026-09-25 instruction, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for D1 to D8 and O2 to O7. On 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos", so every item with a recommendation is decided by Amish, 2026-09-25: go with recommendation (see LDZ-DDR-002). Item O1 carries no recommendation and remains "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish". Eight carried a recommendation; the ninth (first trial partner and LoRaWAN band) did not. On 2026-09-25 Amish asked for this batch of Design Molecule repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Every item that carried a recommendation is therefore adopted as recommended for TRL 3 work, open for his review. Items without a recommendation stay open. Version 0.1 recorded nothing as decided by Amish. Version 0.2 records his acceptance of 2026-09-25; LDZ-DDR-002 lists what changed.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in LDZ-PRC-001 v0.2, Key design choices. They are not repeated here.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Recommendation | Status |
| --- | --- | --- | --- |
| D1 | Installation | Surface-bonded puck for pilots; a cored in-ground puck stays a later variant | Decided by Amish, 2026-09-25: go with recommendation |
| D2 | Sensing | Magnetometer only for TRL 3; an upward radar stays an option if field data show R1 is missed | Decided by Amish, 2026-09-25: go with recommendation |
| D3 | Granularity | One puck per vehicle slot of about 7 m, at the slot center 1.3 m from the curb face | Decided by Amish, 2026-09-25: go with recommendation |
| D4 | Power | Two AA-size Li-SOCl2 primary cells | Decided by Amish, 2026-09-25: go with recommendation |
| D5 | Housing | Rigid cast polyurethane dome, cavity fully potted in polyurethane, on a flat base | Decided by Amish, 2026-09-25: go with recommendation |
| D6 | Sign option and budget | The sign stays a separate option outside the $120 budget. `budget_usd` is unchanged; the budget is redefined to cover the two-puck bay kit only (R13) | Decided by Amish, 2026-09-25: go with recommendation |
| D7 | Sign data path | LoRaWAN class C downlink from the network server to the sign's host FieldNode | Decided by Amish, 2026-09-25: go with recommendation |
| D8 | Data format | Publish a feed that maps onto the Curb Data Specification Events and Metrics APIs, rather than implementing the specification directly | Decided by Amish, 2026-09-25: go with recommendation |

No reworded pitch or problem line was recommended at TRL 2, so `project.yaml` and `README.md` keep the existing wording. No new `budget_usd` figure was recommended; the $210 and $340 alternatives in the TRL 2 note were options, not the recommendation, and are not applied.

### Items raised at TRL 3

*Table 2. Items raised at TRL 3 and their status after LDZ-DDR-002.*

| # | Item | Status |
| --- | --- | --- |
| O1 | First trial partner (a city curb team, a business district or a carrier) and the LoRaWAN band | Proposed, awaiting Amish. No preference stated at TRL 2. LDZ-CAL-001 uses EU868 figures |
| O2 | R4 link from under a van. LDZ-CAL-001 gives about 350 m in a street canyon at SF9 with a 10 dB fade margin, not 1 km. Options: (a) restate R4 as a gateway within 300 m of the bay, in line of sight where possible; (b) keep 1 km and accept SF12, which breaks R3 and R5; (c) add a relay. Recommendation: (a) | Decided by Amish, 2026-09-25: go with recommendation (a). Applied in LDZ-REQ-001 v0.4 |
| O3 | R6 bond under braking. The upper-bound bond shear (1.51 MPa) exceeds the assumed adhesive-to-asphalt strength. Options: (a) specify two-part road-marker epoxy rather than a bitumen pad; (b) restate R6 with the wheel-path finding that parked wheels straddle the puck; (c) both. Recommendation: (c), with a pull-off test at TRL 4 | Decided by Amish, 2026-09-25: go with recommendation (c). Epoxy bed and restated R6 applied; the pull-off test is TRL 4 and on hold |
| O4 | R11 night legibility. The e-paper sign reads at about 28 m by day but is unlit; a 0.5 W front light needs 2.5 times FieldNode's 100 mW allowance. Options: (a) restate R11 as daylight only; (b) a lit display with its own power; (c) drop the sign in favor of the data feed. Recommendation: (a) | Decided by Amish, 2026-09-25: go with recommendation (a). Applied in LDZ-REQ-001 v0.4 |
| O5 | Sign network. The class C sign takes about 200 downlinks a day, far above The Things Network's 10 a day. Recommendation: the sign option requires a private network server (TwinKit) or a city network that allows it; on The Things Network the sign would need LoRa point to point instead | Decided by Amish, 2026-09-25: go with recommendation |
| O6 | Engineering proposals made at TRL 3: one Schottky diode per cell (parallel cells and the 3.6 V module limit), an 85 °C hybrid pulse capacitor, the fully potted cavity and a 6 mm crown radius | Decided by Amish, 2026-09-25: go with recommendation. Shown in the model and BOM |
| O7 | Payload size. In US915 the slowest 125 kHz rate (SF10) carries at most 11 bytes; the 12-byte payload would not fit there. Recommendation: pack the payload into 11 bytes if the band chosen in O1 is US915 | Decided by Amish, 2026-09-25: go with recommendation (conditional on the band) |

## Consequences

- LDZ-REQ-001, LDZ-PRC-001 and LDZ-PRB-001 moved to v0.3 with this record (and to v0.4 with LDZ-DDR-002): the design choices above are no longer "proposed" in the precis, R6 has a stated load basis, and R13 covers the two-puck kit only.
- The sign option ($97 plus a host FieldNode at $126.00) is costed in the BOM but outside the budget.
- Under LDZ-DDR-002, R4 and R11 are restated and met on paper; R6 is restated and stays at risk until a bond test, which is TRL 4 work and on hold.
- TRL 4 is on hold by Amish's instruction. Nothing in this record starts TRL 4 work.
