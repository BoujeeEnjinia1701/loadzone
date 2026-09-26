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
