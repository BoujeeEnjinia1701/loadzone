---
doc_id: LDZ-DEC-001
title: LoadZone design decisions register
project: LoadZone
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note, the decision records and the build plan work; budget treated as a value-engineering target
---

# LoadZone design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design-for-construction changes P1 to P8 (base tray with locating ring, fill and vents; cradles, standoffs and rib; cells and antenna moved inward; casting tooling; programming hold point; channel brackets with band clamps; screwed display housing with a gland) | Accept; accept with changes; reject | Accept: none changes what LoadZone does, its pitch or its safety case | The whole build plan | LDZ-DDR-003, Table 1 |
| 2 | First trial partner and LoRaWAN band | A city curb team, a business district or a carrier; EU868 or US915 | None yet | Antenna band (BOM line 4); US915 means the 11-byte payload rule | LDZ-DDR-001, O1; LDZ-DDR-002 |
| 3 | Sealed-for-life puck: cells not replaceable, firmware changed only over the air | (a) accept and plan over-the-air updates for TRL 4; (b) a sealed service port | (a) | Steps 3 to 5; the programming hold point is the last access | LDZ-DDR-003, A1 |
| 4 | Material of the base tray, which the epoxy bed bonds to | (a) printed ASA, sanded; (b) cast polyurethane in a second mould | (a) for the first prototype, (b) if the TRL 4 pull-off test fails on the tray side | Section 3.5; tooling if (b) | LDZ-DDR-003, A2 |
| 5 | Fixings showing on the printed face of the sign | (a) button heads; (b) studs bonded to the back of the panel | (a) for the prototype | Sections 3.9 to 3.11 | LDZ-DDR-003, A3 |
| 6 | Sign legend and artwork | Placeholder legend; the local traffic sign rules of the trial city | Set to the trial city's rules once item 2 is decided | Sign face (BOM line 8) | Review note 2026-09-26, item 4 |
| 7 | Snow and ploughs: surface puck or a cored, in-ground variant where roads are ploughed | Surface puck only; a cored variant for ploughed climates | None yet | Not part of the TRL 3 build | LDZ-PRC-001, open questions; LDZ-DDR-001, D1 |
| 8 | Dome surface detail in the appearance model (anti-skid grooves, parting line, badge recess cut into the 4 mm wall) | Appearance only; add to the mould master | Appearance only until the mould is designed for production | None in the prototype: the mould master has a plain dome | Review note 2026-09-26, item 2 |
| 9 | Potting colour shown clear amber in the renders | Render convention; buy a clear grade | Render convention unless a clear grade suits the cost target | Potting (BOM line 6) | Review note 2026-09-26, item 3 |
| 10 | Render layout (kerb and sign drawn closer to the puck) and the host FieldNode left out of the renders | Accept for the renders; redraw to scale | Accept, and mention the FieldNode in the caption | None (renders only) | Review note 2026-09-26, items 1 and 5 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The display enclosure's real size, its clear lid and its wall thickness | The 4 screw holes, the gland hole and the sign face holes are drawn for about 200 x 140 x 24 mm; move them to suit | LDZ-DDR-003, P8 |
| 2 | The e-paper driver board takes commands from the host FieldNode over a cable about 1 m long, and the pin assignment of the FieldNode sensor port | Sets the cable and connector between the sign and the FieldNode; the FieldNode port pinout is still open in FieldNode | LDZ-DDR-003, P8; FND-DEC-001 |
| 3 | The band clamp range covers the band path for 60 to 90 mm poles (about 250 to 330 mm) | The band runs through the bracket as well as round the pole | LDZ-DDR-003, P7 |
| 4 | The silicone cures against the primer used on the master and core | Some primers stop platinum silicone curing | Build plan, section 3.2 |
| 5 | The potting's peak exotherm for about 175 cm³ against the cells' temperature rating | The potting is poured over live cells | Build plan, safety stop S4 |
| 6 | The magnetic offset of the cells' steel cans at the magnetometer, about 30 mm away | A fixed offset is learned at install; it must not use up the sensor range | LDZ-CAL-001, section 6 |
| 7 | The road-marker epoxy's bond to sanded ASA | A second bond line beside the asphalt bond already at risk under R6 | LDZ-DDR-003, A2 |

## Value engineering

Value-engineering target: USD 120 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 116 for the two-puck kit (USD 4 under the target). The sign option (USD 101) and its host FieldNode (USD 126, priced in the FieldNode repo) are costed separately, and the one-off dome casting tooling (USD 35) is not part of the per-kit cost. Main cost drivers and savings worth trying:

- The largest lines, for two pucks, are the radio module and board (USD 28), the cell sets with diodes and pulse capacitor (USD 28), the magnetometer breakouts (USD 16), the base trays and potting (USD 12) and the domes (USD 10).
- Making the design constructable added USD 2 to the kit (sealant, screws and mould release in line 12) and USD 4 to the sign option (the channel brackets); the tooling is new.
- Savings worth trying: the magnetometer chip and the radio module on one small carrier board instead of two breakouts (a TRL 4 board design); cells bought in tens; one set of casting tooling shared by every puck made, so its cost falls per puck as more are cast.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D8: surface-bonded puck, magnetometer only, one puck per 7 m slot, two AA-size Li-SOCl2 cells, cast polyurethane dome over fully potted electronics, sign outside the kit cost, class C downlink to the sign, a feed that maps onto the Curb Data Specification | Amish: "i accept all your recommendations, go with them across all repos." | LDZ-DDR-001, LDZ-DDR-002 |
| 2026-09-25 | TRL 3 items O2 to O7: gateway within 300 m (R4), road-marker epoxy bed and R6 restated, daylight-only sign (R11), private network server for the sign, diode per cell, 85 °C pulse capacitor, full potting and 6 mm crown radius, 11-byte payload if US915 | Amish, same instruction | LDZ-DDR-002 |
| 2026-09-30 | Make the design physically buildable as the build plan is drawn | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The resulting changes await his review (open decision 1) | LDZ-DDR-003 |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register, Value engineering |
