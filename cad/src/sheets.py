"""LoadZone general arrangement drawing LDZ-DWG-001 (Rev P4).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/LDZ-DWG-001.svg, .pdf and .png from the parametric model.
LDZ-DWG-001 is free because the concept blueprint is LDZ-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, derived, build_parts, assemblies  # noqa: E402

D = derived(P)
asm = assemblies(build_parts())["loadzone-puck"]
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

s = Sheet(project="LoadZone", title="General arrangement, bay sensor puck", dwg_no="LDZ-DWG-001",
          rev="P4", author="Amish Chadha", date="2026-10-02", concept=True,
          material="Dome rigid cast PU, yellow; PU potting; printed ASA base tray; two-part road-marker epoxy bed. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from LDZ-CAL-001 v0.1", "2026-09-25", "AC"),
                     ("P2", "Epoxy bed; notes per LDZ-DDR-002", "2026-09-25", "AC"),
                     ("P3", "Base tray, cradles, fill and vents (LDZ-DDR-003)", "2026-10-01", "AC"),
                     ("P4", "Figures per LDZ-CAL-001 v0.4 (US915); decisions of 2026-10-02 carried in", "2026-10-02", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 84, label="Isometric view", sublabel="Not to scale")
s.add_notes("Key dimensions and interfaces (mm)", [
    f"Height {D['height']:.0f} above road: pad {P['pad_t']:.0f}, base {P['base_t']:.0f}, dome {P['dome_h']:.0f}",
    f"Base dia {D['diameter']:.0f}; pad dia {D['pad_d']:.0f}; crown dia {D['crown_d']:.0f}",
    f"Dome wall {P['wall']:.0f}; crown radius {P['crown_fillet']:.0f}; cavity fully potted",
    f"Cells 2 x AA Li-SOCl2 ({P['cell_d']} x {P['cell_l']}) in tray cradles",
    "Base tray: spigot locates dome; board on 3 mm standoffs",
    f"Pot through {P['fill_d']:.0f} mm fill hole, puck inverted; {len(P['vents'])} vents {P['vent_d']:.0f} mm",
    "Antenna on the tray rib at +X; no metal above it",
    f"Placement: slot center, {P['puck_from_curb'] / 1000:.1f} m from curb face,",
    f"  one puck per {P['slot_l'] / 1000:.0f} m slot, clear of bike lanes",
    "Bond: two-part road-marker epoxy bed",
    "Crown 7.4 MPa at a 49 kN wheel (LDZ-CAL-001 F)",
    "Mass about 0.45 kg without pad",
    "Road work only under permit and traffic control",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=128, width=140)
s.save(ROOT / "cad/drawings/LDZ-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/LDZ-DWG-001.svg, .pdf, .png")
