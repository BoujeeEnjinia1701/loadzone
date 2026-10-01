# Review note: LoadZone

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (LDZ-PRB-001 v0.2): problem in numbers, users and context, prior work with sources, constraints, out of scope; co-design checklist kept and made specific.
- `docs/03-requirements.md` (LDZ-REQ-001 v0.2): 15 measurable requirements (R1 to R15) with targets, status against the concept and planned verification.
- `docs/02-concept.md` (LDZ-PRC-001 v0.2): how it works, components, first-order numbers, design choices, relationship to other lab projects, safety, open questions.
- `cad/src/concept_media.py`: massing model of the bay sensor puck (BOM 1 to 7) and the sign option on an existing pole (BOM 8 to 11), in a two-slot street bay with a parked van and a 1.75 m person.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `model.glb` with `viewer.html`, `exploded.png` (puck drawn at 4x scale, callouts match the BOM), `cutaway.png` (puck section) and `flow.png` (bay event flow, estimates).
- `bom/bom.csv` and `bom/bom-notes.md`: 12 lines with indicative prices, numbered to match the exploded view.
- `README.md`: hero, links line, and the required sections expanded with cited figures.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged. The pitch and problem still match the numbers found.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Puck size | 150 mm diameter, 31 mm high | R7 met |
| Report latency | about 20 s | R2 met |
| Cell life | about 7 years on 2 x AA Li-SOCl2 | R3 met |
| Airtime | about 9 s/day at SF7, about 31 s/day at SF9 | R5 partly met |
| Sign power | about 0.4 Wh/day | R12 met |
| Sign legibility | about 10 m by day, unlit at night | R11 not met |
| Two-slot kit cost | about $110 | R13 met |
| With sign option | about $207 plus a FieldNode (about $126) | R13 not met |

**Requirements not met:** R6 (traffic loads) with a printed housing, R11 (sign legible at 25 m and at night), and R13 if the sign option is included. R5 is met only at SF8 or faster unless heartbeats drop to every 2 h. R1 (detection accuracy), R4 (link from under a vehicle), R8, R14 and R15 are unverified.

### Proposed, awaiting Amish

1. **Installation:** surface-bonded puck for pilots (recommended), or a cored in-ground puck (better protected, needs road works).
2. **Sensing:** magnetometer only (recommended for TRL 3), or magnetometer plus a small upward radar if field data show R1 is missed.
3. **Granularity:** one puck per vehicle slot of about 7 m (recommended), or one per bay (cheaper, cannot say how many slots are free).
4. **Power:** two AA-size Li-SOCl2 primary cells (recommended), or one C-size cell (more margin, taller puck), or rechargeable with a road-level solar cell (not recommended; shaded by vehicles).
5. **Housing:** cast polyurethane dome over potted electronics (recommended), a commercial raised pavement marker shell, or a cast aluminium base.
6. **Sign option and budget:** keep the sign as a separate option outside the $120 budget (recommended); or raise `budget_usd` to about $210 to include sign parts (FieldNode excluded) or about $340 including a FieldNode; or drop the sign in favor of a data feed only. The budget in `project.yaml` is unchanged.
7. **Sign data path:** LoRaWAN class C downlink (recommended, simplest with TwinKit), or the sign listening to pucks directly by LoRa point to point (works offline).
8. **Data format:** publish a feed that maps onto the Curb Data Specification (recommended), or implement the specification directly.
9. **First trial partner:** a city curb team, a business district or a carrier; and the LoRaWAN band.

### Safety concerns

- Road installation: permit, trained crew and traffic management are mandatory; the precis and README say so.
- Primary lithium thionyl chloride cells: no recharging, fusing, and disposal as hazardous waste.
- Adhesives and polyurethane resins (isocyanates) need ventilation and protective equipment.
- A loose puck can be thrown by a tire: bond checks after install, and placement away from bike lanes and crosswalks.
- Sign option is work at height near possible overhead lines.

### Recommended next step

Review this note and the media. If approved, run `/advance-trl3` to check by calculation the power budget, airtime, link budget from under a vehicle, the housing load case and sign legibility, then produce the parametric puck model with STEP export and a drawing sheet. A short field log of magnetometer readings under parked vans would reduce the R1 risk most, but that is TRL 4 work and has not been started.

Suggestion (not in the repo): CurbCount and LoadZone could share one server and data feed through CityTwin.

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so every item that carried a recommendation is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (LDZ-DDR-001 v0.1, status proposed): eight items adopted as recommended for TRL 3, open for Amish's review (D1 to D8); O1 left open; six new items raised (O2 to O7).
- `docs/04-calcs/01-sizing.md` (LDZ-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: airtime, energy and cell life, pulse supply, latency, link from road level, detection, loads and bond, size and mass, sign power, legibility and downlinks, and cost, with a status for every requirement. The script imports the model, reads the BOM and `project.yaml`, prints every quoted number with a tag and writes `docs/04-calcs/results.csv`.
- `cad/src/model.py`: parametric build123d puck (pad, base, filleted dome, potting, two cells, pulse capacitor, carrier with module, magnetometer, antenna) and sign option (face, display housing, band clamps). Exports `cad/step/` and `cad/stl/` for `loadzone-puck`, `loadzone-dome` and `loadzone-sign-option`.
- `cad/src/sheets.py` and `cad/drawings/LDZ-DWG-001.svg`, `.pdf`, `.png`: general arrangement of the puck at Rev P1, 1:2, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". LDZ-DWG-001 was free because the concept blueprint is LDZ-DWG-010.
- `bom/bom.csv` (12 lines, all priced with a supplier or supplier type; item 11 now carries FieldNode's $126.00 for reference) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now builds the puck and sign from the model; all of `media/` was re-rendered and every image checked. The cutaway caption was corrected because the potting now hides the magnetometer. No `media/_views*` folders remain.
- LDZ-PRB-001, LDZ-PRC-001 and LDZ-REQ-001 revised to v0.3; `README.md` (TRL badge and line, links, key figures, components) and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

### Requirement status (LDZ-CAL-001, Table 2)

2 not met, 3 at risk, 1 not verifiable at TRL 3, 5 met on paper, 4 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R4 Link from road level | **Not met** | -6.0 dB at 1 km out of sight at SF9 with a van over; about 350 m with a 10 dB fade margin |
| R11 Sign legibility | **Not met** (night) | About 28 m by day at full contrast (TRL 2 said 10 m); unlit at night; a 0.5 W light needs 2.5 times FieldNode's 100 mW allowance |
| R1 Detection | At risk | Line-dipole model: van 10.0 µT, weak-steel truck 3.85 µT, next lane 0.46 µT against 3 µT; calibration assumed |
| R5 Airtime | At risk | 25.5 s/day at SF9 (TRL 2 said 31 s); 51.0 s at SF10 |
| R6 Traffic | At risk | Crown 7.4 MPa, factor 5.4 on PU, 2.0 on potting; bond shear 1.51 MPa against about 1.0 MPa assumed |
| R14 Install time | Not verifiable at TRL 3 | Needs an install trial |
| R2, R3, R7, R12, R13 | Met on paper | 38.6 s worst latency at SF9; 7.7 years; 31 mm high; 0.42 Wh/day sign; $114.00 |
| R8, R9, R10, R15 | Met by design | CDS event types checked against the specification |

Other corrections to TRL 2 figures: puck mass 451 g (was 0.35 kg) because the cavity is fully potted; kit cost $114.00 (was about $110) with the diodes and 85 °C capacitor.

### Decisions recorded (LDZ-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: D1 surface-bonded puck; D2 magnetometer only; D3 one puck per 7 m slot; D4 two AA-size Li-SOCl2 cells; D5 cast polyurethane dome over fully potted electronics; D6 sign outside the $120 budget, which now covers the two-puck kit only (R13 redefined; `budget_usd` unchanged); D7 LoRaWAN class C downlink to the sign; D8 a feed that maps onto the Curb Data Specification. No reworded pitch or problem was recommended, so `project.yaml` and `README.md` keep the existing wording.

### Still awaiting Amish

1. **O1, first trial partner and LoRaWAN band.** No preference stated. Proposed, awaiting Amish.
2. **O2, R4.** Recommendation: restate R4 as a gateway within 300 m of the bay. Not applied.
3. **O3, R6 bond.** Recommendation: two-part road-marker epoxy, and restate R6 with the finding that parked wheels straddle the puck. Not applied.
4. **O4, R11.** Recommendation: a daylight-only legibility target. Not applied.
5. **O5, sign network.** About 200 downlinks a day against The Things Network's 10: the sign needs TwinKit or another private network server.
6. **O6, engineering proposals:** a Schottky diode per cell, an 85 °C hybrid pulse capacitor, the fully potted cavity and a 6 mm crown radius. In the model and BOM, awaiting confirmation.
7. **O7, payload.** Pack the payload into 11 bytes if the band is US915.

### Cross-repo consistency

- FieldNode (TRL 3): LoadZone uses its radio currents, SF9 sensitivity and $126.00 core cost, and its adopted choices (LoRaWAN, STM32WL-class module, TwinKit first). The sign's 17.7 mW fits both the published 115 mW allowance and the 100 mW FieldNode proposes. No conflict.
- TwinKit (TRL 3): its airtime figures use a 20-byte reading; LoadZone's 12-byte uplink is shorter. TwinKit's review does not mention class C downlinks; the sign's 200 downlinks a day use 0.38 % of the RX2 sub-band allowance, but TwinKit's network stack must support class C. Noted here; TwinKit not edited.
- CalRig: could check magnetometer offset and noise before installation; no interface assumed. CellGuard, MotionCore and ThermaCart are not used.

### Safety concerns

- Road installation: permit, trained crew and traffic management; a loose puck can be thrown by a tire, and the calculated bond margin under braking is below 1 on the upper bound, so bond checks after install matter.
- Primary Li-SOCl2 cells in a hot road: parallel cells only through a diode each, fused, never recharged; the pulse capacitor must be rated for 85 °C; spent cells are hazardous waste.
- Polyurethane resins (isocyanates) and road adhesives: ventilation and protective equipment.
- Sign option: work at height near possible overhead lines; pole owner's consent for wind load.

### Gaps and notes

- Citations: none were flagged as unchecked at TRL 2. The Things Network fair-use figures (30 s uplink, 10 downlinks a day) and the Curb Data Specification event types were checked by WebFetch on 2026-09-25. The MUTCD legibility index (section 2A.13) and 3GPP TR 38.901 are cited by section, not fetched.
- Assumptions only tests can settle: the 10 µT vehicle signal, the 10 dB road-level and 10 to 20 dB vehicle losses, adhesive-to-asphalt strength, and material strengths.
- The UMi path-loss model is used below its 1.5 m height floor; the road-level loss term covers this.
- The kit's cutaway cuts at the mean Y of the parts; the puck (at Y = -1.3 m) is passed alone with a slab of road, as at TRL 2, and the section shows the cells, board and antenna. The magnetometer falls behind the cut and appears only in the exploded view. The concept blueprint's orthographic views are small because the street context sets the scale; the GA sheet shows the puck at 1:2.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) and empty `electronics/` and `firmware/` placeholders are present, untouched and not extended. No test, build or firmware material was created.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on D1 to D8 and O1 to O7. For the record only, TRL 4 would need: a bench build of one puck; a lab test report (TST, `environment: lab`) covering magnetometer readings under parked vehicles, sleep current and charge per uplink, a crush test of the cast and potted puck, a pull-off and shear test of the bond on asphalt at 20 and 50 °C, and immersion sealing; and build log entries. None of this has been started.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (LDZ-DDR-002 v0.1). Nothing past TRL 3 was done.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| D1 to D8 | As recommended in LDZ-DDR-001 | "Adopted as recommended for TRL 3, open for his review" | Decided; LDZ-DDR-001 v0.2 |
| D6 budget | Sign outside the budget; budget covers the two-puck kit | `budget_usd` $120 | $120 (unchanged; scope already redefined in R13); kit $114.00 |
| O2 R4 | Gateway within 300 m of the bay | 1 km target; -6.0 dB margin; not met | 300 m target; 353 m range at SF9 with 10 dB fade margin; met on paper |
| O3 R6 | Two-part road-marker epoxy; R6 restated around maneuvering wheels | Bitumen pad or epoxy; parked-wheel finding not in R6 | Epoxy bed (BOM line 7, $4.00 unchanged); R6 restated; bond factor 0.66 unchanged, still at risk |
| O4 R11 | Daylight-only legibility | 25 m by day and night; not met | 25 m by day; about 28 m; met on paper |
| O5 Sign network | Private network server (TwinKit) or a permissive city network | Proposed | Decided constraint in precis and problem statement |
| O6 Engineering proposals | Diode per cell, 85 °C pulse capacitor, full potting, 6 mm crown radius | Awaiting confirmation | Confirmed; no geometry or cost change |
| O7 Payload | 11 bytes if the band is US915 | Proposed | Decided firmware rule; [A2] 370.7 ms at SF10; firmware itself on hold (TRL 4) |

Also updated to match FieldNode's published figure (FND-DDR-002): the sign's 17.7 mW is now checked against 100 mW only (was 115 mW and 100 mW).

Files changed: LDZ-PRB-001 v0.4, LDZ-PRC-001 v0.4, LDZ-REQ-001 v0.4, LDZ-CAL-001 v0.2 (`docs/04-calcs/sizing.py` and `results.csv` re-run), LDZ-DDR-001 v0.2, new LDZ-DDR-002 v0.1; `bom/bom.csv` and `bom/bom-notes.md`; `cad/src/model.py` (comment only; STEP and STL re-exported); `cad/src/sheets.py` and LDZ-DWG-001 at Rev P2 (material note and two notes; geometry unchanged); `cad/src/concept_media.py` (blueprint key figure and exploded-view label; all of `media/` re-rendered and checked); `README.md` (key figures, components, "What sparked the idea"); `project.yaml` (evidence list); all PDFs in `docs/pdf/` rebuilt. Pitch and problem unchanged; no rewording was recommended.

### Requirement status (LDZ-CAL-001 v0.2)

None not met (was 2), 3 at risk, 1 not verifiable at TRL 3, 7 met on paper (was 5), 4 met by design.

| ID | Status | Key number |
| --- | --- | --- |
| R1 Detection | At risk | Weak-steel truck 3.85 µT against a 3 µT threshold; calibration assumed |
| R5 Airtime | At risk | 25.5 s/day at SF9; 51.0 s at SF10 |
| R6 Traffic | At risk | Epoxy bond shear 1.51 MPa against about 1.0 MPa assumed (factor 0.66) |
| R14 Install time | Not verifiable at TRL 3 | Needs an install trial |
| R2, R3, R4, R7, R11, R12, R13 | Met on paper | 38.6 s worst; 7.7 years; 353 m against 300 m; 31 mm; about 28 m by day; 17.7 mW against 100 mW; $114.00 |
| R8, R9, R10, R15 | Met by design | Unchanged |

### Still awaiting Amish

1. **O1, first trial partner and LoRaWAN band.** No recommendation was made. Proposed, awaiting Amish. The US915 payload rule (O7) applies only if that band is chosen.

### Cross-repo actions (other repos not edited)

- **TwinKit:** its network stack must support LoRaWAN class C downlinks, about 200 a day for each LoadZone sign (O5). TwinKit's review does not yet mention class C.
- **FieldNode:** none required. LoadZone now uses FieldNode's published 100 mW allowance and $126.00 core cost, and a 12-byte (or 11-byte in US915) payload, shorter than FieldNode's 20-byte reading.

### README and inspiration

"What sparked the idea" now traces the design to San Francisco's SFpark pilot and the SFMTA Parking Sensor Data Guide (2013), which records in-ground magnetometer sensors whose batteries, meant to last about five years, began failing about a year early; the earlier text about a September 2026 review of research areas was removed. No other file attributed the idea to a review.

### TRL 4

TRL 4 remains on hold by Amish's instruction. The bond pull-off and shear test on asphalt, a field link survey, a magnetometer log under parked vehicles and the payload firmware are decided or recommended but not started.

## Session 2026-09-26: sources strengthened

Sources in the README were checked against the standard of 2026-09-26 ("Fix the weaker sources"); every kept link was fetched and confirmed.

| Where | Old source | New source |
| --- | --- | --- |
| Region table, European Union | gdpr-info.eu (unofficial reproduction of GDPR Article 25) | Regulation (EU) 2016/679, Article 25, on EUR-Lex |
| Region table, India | None (uncited claim about few formal loading bays) | DPIIT, Guidelines for Preparing City Logistics Plan (row rewritten to what the guidelines say about loading lots and per-bay use data) |
| Region table, Mexico and Brazil | None (uncited) | Row replaced by Brazil: CET São Paulo page listing 1,749 on-street truck loading bays |
| What sparked the idea | SFMTA Parking Sensor Data Guide (kept) | Same source; wording corrected to note that noise-filtering software had cut the expected battery life to about three years before the early failures |

No budget change in this session.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session adds an appearance model for photoreal renders; the render images themselves are produced later by the portfolio orchestrator.

### What was added

- `cad/src/product_model.py`: `product_parts()` (33 parts: 5 shell, 12 internal, 10 accessory, 6 context), `TITLE` and `RENDER_VIEWS` (hero, exploded and detail). It imports `PARAMS`, `derived()` and `build_parts()` from `cad/src/model.py`, so every main dimension and interface is unchanged.
- Puck: the model.py dome with a softened foot, a mold parting line, 24 radial anti-skid grooves on the flank, and a recessed crown badge ("LOADZONE BAY SENSOR") with a teal accent ring; the base disc with softened edges; the epoxy bed with a rounded squeeze-out bead; clear amber potting; cells with end caps; the pulse capacitor; the radio carrier board with a shielded module, flash, regulator, diodes and u.FL connector; the magnetometer breakout with its IC and header; the flexible antenna with a copper trace pattern.
- Sign option: rounded, painted sign face with a raised "LOADING ZONE" legend, border and teal band; a filleted display housing with a polycarbonate window over the e-paper panel showing "2 FREE BAYS" and an arrow; a cable gland; band clamps with ears, clamp bolts and face bolts.
- Context (neutral colours): an asphalt road patch with a white bay edge line and slot end line, a kerb stone, sidewalk paving and a short section of the existing street pole.
- README: hero image now points to `media/render-hero.png`, with a link to `media/render-exploded.png`.

### Where the appearance model differs from model.py

1. **Render layout.** In the hero view the kerb is drawn 400 mm from the puck (installed 1.3 m) and the sign's lower edge 250 mm above the sidewalk (installed 2.1 m), so the puck and sign read in one frame; the view note says so. Proposed, awaiting Amish. Recommendation: accept for the hero render, and keep the true layout in the concept hero and the drawing.
2. **Dome surface detail.** The anti-skid grooves (about 1.1 mm deep), parting line (0.45 mm) and crown badge recess (1.0 mm) are cut into the 4 mm cast wall. Proposed, awaiting Amish. Recommendation: accept as appearance only, and check the local wall and the wheel-load path when the mold is designed.
3. **Potting colour.** The potting is shown as a clear amber polyurethane so the internals read in the exploded render; the BOM does not set a colour. Proposed, awaiting Amish. Recommendation: treat clear potting as a render convention unless a clear grade suits the budget.
4. **Sign artwork.** The legend, "FREE BAYS" label, teal band and e-paper image are placeholder artwork. Proposed, awaiting Amish. Recommendation: set the final legend to the local traffic sign rules of the first trial city (O1).
5. **Host FieldNode.** The host FieldNode (BOM 11) above the sign is left out of the renders to keep the frame compact; only the cable gland hints at its supply. Proposed, awaiting Amish. Recommendation: accept, and mention the FieldNode in the render caption.
6. **Minor.** The flexible antenna is drawn 0.6 mm thick (1.0 mm envelope in model.py), the display housing is filleted with a window pocket, and the clamps gain bolt ears. The exploded view shows the puck only, because the 600 mm sign would dwarf the 150 mm puck.

### Status

This is an appearance model only: no tolerances, PCB layouts or fabrication detail were added. `trl` stays 3, and TRL 4 remains on hold. No budget change in this session.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: design for construction and prototype build plan (kit 1.7.0)

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Constructability review of every part, with build123d checks in `cad/src/model.py` (`python cad/src/model.py --check`): 92 checks, all pass. The model now also builds the dome casting tooling (`build_tooling`) and a sign mount that can be made and fitted.
- `docs/decisions/0003-design-for-construction.md` (LDZ-DDR-003 v0.1, Draft): every change, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `docs/05-build-plan.md` (LDZ-BLD-001 v0.1): the illustrated prototype build plan, with 7 making sketches (`cad/drawings/LDZ-DWG-101` to `107`), 8 joint close-ups, 9 step pictures, a tray layout, a sign face drilling layout and a wiring diagram (`docs/05-build-plan/`), all drawn by `cad/src/build_plan_media.py`.
- `docs/06-design-decisions.md` (LDZ-DEC-001 v0.1): 10 open decisions, 7 items to confirm when parts are bought, a value-engineering section and the decisions made.
- `bom/bom.csv`: lines 1, 3, 6, 9, 10 and 12 re-specified, line 13 (one-off casting tooling) added; `bom/bom-notes.md` updated.
- Calculations re-run on the constructable design: LDZ-CAL-001 v0.3 (`docs/04-calcs/sizing.py` now reports cost against the value-engineering target); LDZ-REQ-001 v0.5 and LDZ-PRC-001 v0.5 updated to match.
- STEP and STL regenerated (puck, dome, base tray, sign option, dome tooling); general arrangement LDZ-DWG-001 Rev P3; concept media regenerated (`python cad/src/concept_media.py`).
- `project.yaml`: `design_state: constructable`; build plan, register, DDR-003 and the picture script added to `trl_evidence`. `budget_usd` unchanged at 120.
- `README.md`: value-engineering wording in the header, "Prototype build plan" and "Design decisions" links, and a "Building the prototype" section before "Safety".

### Design changes made for construction (LDZ-DDR-003)

1. Base: a printed tray with a tapered locating ring for the dome, an 8 mm fill hole and four 4 mm vents; the seam is sealed and the puck is potted upside down.
2. Inside the puck: cradles for the cells, four board standoffs and an antenna rib printed on the tray; the capacitor and antenna stand on the tray.
3. Cells moved 3 mm and the capacitor with them toward the centre (2.5 mm from the dome wall, was 1.2 mm).
4. Antenna moved 2 mm inward onto the rib (3.8 mm from the dome wall, was 1.9 mm).
5. Dome casting: printed mould master, silicone mould and printed core plug with flange, skirt and overflow holes (BOM line 13).
6. Programming pads on the radio board and a programming and bench-test hold point before the dome goes on; the board is prototyping board.
7. Sign mount: two aluminium channel brackets bolted to the sign, with stainless band clamps through slots in their flanges, in place of solid rings; sign 33 mm off the pole (was 30); brackets 100 mm from the sign's ends (was 120).
8. Display housing: a bought enclosure with a clear lid, screwed from behind the sign, with an M20 gland through the sign face.

### Key results

- Mass unchanged at 451 g without the bed; height 31 mm; loads, link, energy and detection figures unchanged.
- Value-engineering target: USD 120. Estimated cost of the constructable design: USD 116 for the two-puck kit (USD 4 under the target). Sign option USD 101 (was 97) plus a USD 126 FieldNode; one-off tooling USD 35.
- Requirement status unchanged: none not met, 3 at risk (R1, R5, R6), 1 not verifiable at TRL 3 (R14), 7 met on paper, 4 met by design.

### Proposed, awaiting Amish

All are in `docs/06-design-decisions.md`. New this session: acceptance of LDZ-DDR-003 (item 1), a sealed-for-life puck with over-the-air updates (item 3), the base tray material for the epoxy bond (item 4) and fixings showing on the sign face (item 5).

### Safety concerns

- Potting over live Li-SOCl2 cells: use a low-exotherm grade and check its peak temperature (build plan stop S4).
- Polyurethane casting and potting involve isocyanates: ventilation and a suitable respirator (stop S3).

### Stale media (made on Amish's Mac; not regenerated here)

- `cad/src/product_model.py` still draws the concept's ring clamps (it reads the clamp band width and thickness, now 12 and 0.8 mm), and its puck internals use the old cell and antenna positions. The photoreal renders that show the sign (`media/render-hero.png` and any other `media/render-*.png` with the sign) and `media/card.png` and `media/social-preview.png` are stale for the sign mount; the puck's outside is unchanged.

### Recommended next step

Amish's review of LDZ-DDR-003 and the open decisions in LDZ-DEC-001, then the product model and renders updated on the Mac. TRL 4 (building to this plan) remains on hold.
