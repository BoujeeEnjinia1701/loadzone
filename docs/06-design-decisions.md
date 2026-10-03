---
doc_id: LDZ-DEC-001
title: LoadZone design decisions register
project: LoadZone
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note, the decision records and the build plan work; budget treated as a value-engineering target
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: Amish approved the recommendations of open items 1 to 10 on 2026-10-02; all moved to decisions made; tray bond line to confirm updated
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: 'Value engineering: host FieldNode priced at USD 139.50 (FND-CAL-001)'
---

# LoadZone design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The display enclosure's real size, its clear lid and its wall thickness | The 4 screw holes, the gland hole and the sign face holes are drawn for about 200 x 140 x 24 mm; move them to suit | LDZ-DDR-003, P8 |
| 2 | The e-paper driver board takes commands from the host FieldNode over a cable about 1 m long, and the pin assignment of the FieldNode sensor port | Sets the cable and connector between the sign and the FieldNode; the FieldNode port pinout is still open in FieldNode | LDZ-DDR-003, P8; FND-DEC-001 |
| 3 | The band clamp range covers the band path for 60 to 90 mm poles (about 250 to 330 mm) | The band runs through the bracket as well as round the pole | LDZ-DDR-003, P7 |
| 4 | The silicone cures against the primer used on the master and core | Some primers stop platinum silicone curing | Build plan, section 3.2 |
| 5 | The potting's peak exotherm for about 175 cm³ against the cells' temperature rating | The potting is poured over live cells | Build plan, safety stop S4 |
| 6 | The magnetic offset of the cells' steel cans at the magnetometer, about 30 mm away | A fixed offset is learned at install; it must not use up the sensor range | LDZ-CAL-001, section 6 |
| 7 | The road-marker epoxy's bond to ASA sanded with 80 grit (decided 2026-10-02; the tray is cast in polyurethane if the TRL 4 pull-off test fails on the tray side) | A second bond line beside the asphalt bond already at risk under R6 | LDZ-DDR-003, A2 |

## Value engineering

Value-engineering target: USD 120 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 116 for the two-puck kit (USD 4 under the target). The sign option (USD 101) and its host FieldNode (USD 139.50, priced in the FieldNode repo) are costed separately, and the one-off dome casting tooling (USD 35) is not part of the per-kit cost. Main cost drivers and savings worth trying:

- The largest lines, for two pucks, are the radio module and board (USD 28), the cell sets with diodes and pulse capacitor (USD 28), the magnetometer breakouts (USD 16), the base trays and potting (USD 12) and the domes (USD 10).
- Making the design constructable added USD 2 to the kit (sealant, screws and mould release in line 12) and USD 4 to the sign option (the channel brackets); the tooling is new.
- Savings worth trying: the magnetometer chip and the radio module on one small carrier board instead of two breakouts (a TRL 4 board design); cells bought in tens; one set of casting tooling shared by every puck made, so its cost falls per puck as more are cast.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D8: surface-bonded puck, magnetometer only, one puck per 7 m slot, two AA-size Li-SOCl2 cells, cast polyurethane dome over fully potted electronics, sign outside the kit cost, class C downlink to the sign, a feed that maps onto the Curb Data Specification | Amish: "i accept all your recommendations, go with them across all repos." | LDZ-DDR-001, LDZ-DDR-002 |
| 2026-09-25 | TRL 3 items O2 to O7: gateway within 300 m (R4), road-marker epoxy bed and R6 restated, daylight-only sign (R11), private network server for the sign, diode per cell, 85 °C pulse capacitor, full potting and 6 mm crown radius, 11-byte payload if US915 | Amish, same instruction | LDZ-DDR-002 |
| 2026-09-30 | Make the design physically buildable as the build plan is drawn | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The resulting changes were accepted on 2026-10-02 (below) | LDZ-DDR-003 |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | This register, Value engineering |
| 2026-10-02 | Open item 1: design for construction accepted: the changes P1 to P8 and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | LDZ-DDR-003, Tables 1 and 2 |
| 2026-10-02 | Open item 2: first trial partner, the first candidate type to approach (not yet agreed), is a city curb-management or transportation team that has published or piloted the Curb Data Specification, in a city without routine snow plowing; US915 is the default band, since the 11-byte payload already fits it | Amish: "i approve your recommendations for all 555 open decisions." | LDZ-DDR-001, O1; LDZ-DDR-002 |
| 2026-10-02 | Open item 3: the puck is sealed for life (cells not replaceable, firmware changed only over the air); over-the-air updates are planned for TRL 4 | Amish: "i approve your recommendations for all 555 open decisions." | LDZ-DDR-003, A1 |
| 2026-10-02 | Open item 4: base tray in printed ASA, sanded with 80 grit, for the first prototype; cast in polyurethane if the TRL 4 pull-off test fails on the tray side | Amish: "i approve your recommendations for all 555 open decisions." | LDZ-DDR-003, A2 |
| 2026-10-02 | Open item 5: button heads on the sign face for the prototype | Amish: "i approve your recommendations for all 555 open decisions." | LDZ-DDR-003, A3 |
| 2026-10-02 | Open item 6: the placeholder legend is kept for now; once the city is chosen the legend is drawn to its sign rules (in the US, the federal sign manual, MUTCD), and the city traffic engineer's approval is obtained before it is mounted on a street | Amish: "i approve your recommendations for all 555 open decisions." | Review note 2026-09-26, item 4 |
| 2026-10-02 | Open item 7: the surface puck only is offered for now and is stated not to be for plowed streets; the cored, in-ground version is recorded as a later option | Amish: "i approve your recommendations for all 555 open decisions." | LDZ-PRC-001, open questions; LDZ-DDR-001, D1 |
| 2026-10-02 | Open item 8: the dome surface detail stays appearance only until the mould is designed for production | Amish: "i approve your recommendations for all 555 open decisions." | Review note 2026-09-26, item 2 |
| 2026-10-02 | Open item 9: the clear amber potting is a render convention unless a clear grade costs no more | Amish: "i approve your recommendations for all 555 open decisions." | Review note 2026-09-26, item 3 |
| 2026-10-02 | Open item 10: the render layout is accepted, and the host FieldNode is mentioned in the caption | Amish: "i approve your recommendations for all 555 open decisions." | Review note 2026-09-26, items 1 and 5 |
