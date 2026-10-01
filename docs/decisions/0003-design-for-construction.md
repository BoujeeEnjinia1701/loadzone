---
doc_id: LDZ-DDR-003
title: LoadZone design for construction
project: LoadZone
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. The changes in Table 1 and Table 2 were made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are "Proposed, awaiting Amish".

## Context

On 2026-09-30 Amish asked for every repo to get an illustrated prototype build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The concept model of LDZ-DDR-002 showed what LoadZone does: a cast dome over potted electronics on a flat base, bonded to the road, and an optional e-paper sign on a pole. Checking it part by part, and with build123d (overlaps, contacts and clearances), found that it could not be built as drawn: the dome had no joint to the base and no way to be potted, the parts inside floated, the cells sat 1.2 mm from the dome wall, the casting method was a phrase rather than a process, and the sign was held to its pole by solid rings that cannot be made or fitted.

The changes keep what LoadZone does: the same puck outside (150 mm across, 31 mm high, the same dome and crown), the same cells, radio, magnetometer, antenna, potting and epoxy bed, the same slot-centre placement, and the same sign face, display and pole mounting height. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now runs 92 constructability checks (`python cad/src/model.py --check`): nothing overlaps, every part touches the part that holds it, and clearances for potting, tabs and leads are met. All 92 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The dome sat on a flat 150 x 6 mm base disc with nothing to locate or seal it, and the cavity was "fully potted" with no way in: potting poured into the open dome before the base went on would trap air under the base, and a closed cavity has no fill path. | The base becomes a printed ASA tray: the same 150 x 6 mm disc plus a tapered locating ring (141.4 mm across at the disc, 135.0 mm at its top, 2.5 mm tall) that fits the dome's cavity with 0.3 mm all round, an 8 mm fill hole and four 4 mm vents through the disc. The dome rim sits flat on the disc, a bead of polyurethane sealant closes the outside seam, and the puck is potted upside down through the fill hole until resin shows at every vent. | Potting from the road side lets air rise to the vents, which are at the highest point when the puck is upside down. The fill and vent holes end up under the epoxy bed, so nothing shows on the finished puck. The ring keeps the dome centred while the sealant cures. |
| P2 | The cells, capacitor, radio board and antenna floated in the cavity (1 to 3 mm above the base) with nothing to hold them while the potting was poured. | Two saddle-shaped cradles per cell (11 x 5 mm, 4 mm tall), four 3 mm board standoffs with pilot holes for M2 screws, and an antenna rib (2 x 50 mm, 8 mm tall) printed on the tray. The capacitor and the antenna stand on the tray. | Every part is held in its place by the tray, so the electronics can be wired, programmed and tested on the bench before the dome goes on. The board keeps its 3 mm gap so potting flows under it; a vent under the board lets the air out. |
| P3 | The cells' end corners were 1.2 mm from the sloping dome wall, with no room for their solder tabs and leads. | Both cells moved 3 mm toward the centre (centres 37 and 20 mm from the axis, 2.5 mm apart) and the pulse capacitor 3 mm with them. | 2.5 mm from the dome wall, enough for the tabs and for potting to flow round them; the cells stay on the side away from the antenna. |
| P4 | The antenna strip stood 1.9 mm from the dome wall with no support. | Antenna moved 2 mm inward (48 mm from the axis) and stuck to the inner face of the rib. | 3.8 mm from the wall; no metal above it and 9.5 mm from the board, as before. |
| P5 | The dome was to be cast in "a printed silicone mould", which names no process: a dome with an inner cavity needs a core as well as an outer mould. | A one-off tooling set: a printed mould master (plate, box wall and the dome's outside shape in one print), a silicone mould cast in it, and a printed core plug whose flange sits on the silicone block, whose skirt centres it, and whose cone forms the cavity. Four 4 mm overflow holes let spare resin and air out. New BOM line 13, one-off tooling, USD 35. | The dome's sides are drafted by about 46 degrees, so it releases from a one-piece open mould and a solid core. The flange sets the 4 mm crown and a flat rim face, which is the face that sits on the tray. |
| P6 | Once potted, the puck's electronics can never be reached again, but the concept had no step for programming or testing them. | Programming pads (SWD and UART) on the radio board; programming and a bench test are a hold point before the dome goes on (build plan step 3). The radio board is a piece of prototyping board carrying the bought module (BOM line 3), since a carrier circuit board is TRL 4 work. | The puck is sealed for life, as the concept intends; later firmware changes can only go over the air (Table 3, A1). |
| P7 | The sign was held by two solid 5 mm rings round the pole with solid arms that only touched the back of the sign: a closed ring cannot be fitted to a pole and the arms had no fixing. | Two brackets cut from 50 x 40 x 3 mm aluminium U-channel, 60 mm long, each bolted to the back of the sign face by two M6 button-head bolts, with a 12 mm stainless worm-drive band clamp that passes through a slot in each flange, across in front of the pole and round its back. The two flange ends bear on the pole; any pole from 60 to 90 mm seats on both. The sign stands 33 mm off the pole (was 30), set by the channel depth, and the brackets sit 100 mm from the top and bottom edges (was 120) to clear the display housing. BOM line 10 is now this bracket, USD 7 each (was USD 5). | A band clamp is how signs are fixed to street poles; the channel gives a flat face for the sign and two bearing edges for the pole from one stock section. |
| P8 | The display housing was a solid block on the face of the sign with no fixing and no way for its cable to reach the host FieldNode. | A bought polycarbonate enclosure with a clear lid (about 200 x 140 x 24 mm), held by four M4 pan-head screws from behind the sign with sealing washers and nuts inside, and an M20 cable gland through its back wall and a 20.5 mm hole in the sign face, so the cable runs down behind the sign. | Nothing passes through the clear lid; the panel tapes to the inside of the lid and the driver board sits on the back wall. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Unchanged at 451 g without the epoxy bed (LDZ-CAL-001 [G2]): the tray features take the place of potting of about the same density. | Follows the model. |
| Cost | Two-puck kit USD 116.00 (was USD 114.00): line 12 adds sealant, M2 screws and mould release (USD 8.00, was USD 6.00). Value-engineering target USD 120, so USD 4.00 under it. Sign option USD 101.00 (was USD 97.00). One-off casting tooling USD 35.00, not part of the per-kit cost. `budget_usd` unchanged. | Parts added for construction. |
| Drawings | LDZ-DWG-001 Rev P3; making sketches LDZ-DWG-101 to 107 added. | Follows the model. |
| Documents | LDZ-CAL-001 v0.3 (cost), LDZ-REQ-001 v0.5 (R13 against the value-engineering target), LDZ-PRC-001 v0.5 (components table, cost). No requirement changed status. | Follows the model. |
| Loads and link | Unchanged: the dome, crown, base diameter and bed are the same, and the antenna is still at the dome edge with no metal above it. | |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The potted puck is sealed for life: its cells cannot be replaced and its firmware can only change over the air. | (a) accept, as the fully potted concept implies, and plan over-the-air updates for TRL 4; (b) add a sealed service port, which weakens R8 and R15. | (a). |
| A2 | The epoxy bed now bonds to a printed ASA tray. Epoxy keys to sanded ASA, but less well than to cast polyurethane, adding a second bond to the one already at risk under R6. | (a) printed ASA, sanded with 80 grit, checked in the TRL 4 pull-off test; (b) cast the tray in polyurethane in a second simple mould. | (a) for the first prototype; (b) if the pull-off test shows the tray side failing first. |
| A3 | The M6 bracket bolts and M4 housing screws show as button heads on the printed face of the sign. | (a) button heads, as modelled; (b) studs bonded to the back of the panel so the face stays clean. | (a) for the prototype. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan LDZ-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); open items are in the design decisions register LDZ-DEC-001.
- Requirement status is unchanged: none not met, 3 at risk (R1, R5, R6), 1 not verifiable at TRL 3 (R14), 7 met on paper, 4 met by design (LDZ-CAL-001 v0.3). R13 is now reported against the value-engineering target: USD 4.00 under it.
- The appearance model `cad/src/product_model.py` and the photoreal renders (`media/render-*.png`), with `media/card.png` and `media/social-preview.png`, still show the concept's ring clamps on the sign; they need updating on Amish's Mac, where Blender is. The puck's outside is unchanged.
- The display enclosure, the e-paper driver board and the band clamps are chosen at TRL 4; their sizes must be checked then and the holes moved to suit (LDZ-DEC-001, items to confirm).
