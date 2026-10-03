"""LoadZone concept media (TRL 3), built from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. X runs along the curb (traffic approaches from +X and drives toward -X,
right-hand traffic), Y runs across the street (road at Y < 0, sidewalk at Y > 0, curb face at
Y = 0), Z is up with the road surface at Z = 0 and the sidewalk top at Z = 150.

The core product is the bay sensor puck (BOM 1 to 7), one per vehicle slot. The optional sign
(BOM 8 to 11) hangs on an existing street pole and runs from a host FieldNode. The street, the
pole, the parked van and the second puck under it are grey context.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
import os
os.chdir(ROOT)

from build123d import Box, Cylinder, Pos, Rot
import concept
from concept import Part, render_all, cutaway_parts

sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as MP, build_parts, build_sign  # noqa: E402

# ---------------- key dimensions (mm), from cad/src/model.py ----------------
PUCK_R = MP["base_r"]
SLOT = MP["slot_l"]
CURB_H = 150.0

PX, PY = 0.0, -MP["puck_from_curb"]   # free-slot puck, centered in the slot 1.3 m from the curb face
POLE_X, POLE_Y = 1500.0, 450.0
POLE_R = MP["pole_r"]


# ---------------- bay sensor puck (parametric model) ----------------
def puck(px, py, k=1.0):
    """Puck parts from model.py placed at (px, py) on the road; k scales the puck (k > 1 only for the exploded view)."""
    m = build_parts()
    def place(shape):
        if k != 1.0:
            shape = shape.scale(k)
        return Pos(px, py, 0) * shape
    return dict(pad=place(m["pad"]), base=place(m["base"] + m["potting"]), dome=place(m["dome"]),
                cells=place(m["cells"] + m["cap"]), board=place(m["board"]), mag=place(m["mag"]), ant=place(m["ant"]))


P = puck(PX, PY)

# ---------------- sign option on an existing pole (parametric model) ----------------
SIGN_Z0, SIGN_H, SIGN_W = MP["sign_z0"], MP["sign_h"], MP["sign_w"]
_sg = build_sign()
_at = Pos(POLE_X, POLE_Y, SIGN_Z0)
sign_panel = _at * _sg["sign_face"]
epaper = _at * _sg["display"]
clamps = _at * _sg["clamps"]
# Host FieldNode (enclosure, 6 W panel as hood, clamps), on the back of the pole above the sign
FN_Z = 2950.0
fn_box = Pos(POLE_X - POLE_R - 50, POLE_Y, FN_Z) * Box(90, 150, 200)
fn_panel = Pos(POLE_X - POLE_R - 90, POLE_Y, FN_Z + 200) * Rot(0, -40, 0) * Box(200, 290, 17)
fn_post = Pos(POLE_X - POLE_R - 40, POLE_Y, FN_Z + 130) * Box(20, 20, 70)
fn_clamp = Pos(POLE_X, POLE_Y, FN_Z) * (Cylinder(POLE_R + 5, 25) - Cylinder(POLE_R, 27))
fieldnode = fn_box + fn_panel + fn_post + fn_clamp
pole = Pos(POLE_X, POLE_Y, CURB_H + 1700) * Cylinder(POLE_R, 3400)

KIT = "#0F766E"
parts = [
    Part("Puck dome, cast polyurethane", P["dome"], "#EAB308", 1),
    Part("Magnetometer, 3-axis (LIS2MDL class)", P["mag"], "#7C3AED", 2),
    Part("Controller and LoRa radio (FieldNode core)", P["board"], KIT, 3),
    Part("Internal antenna, flexible PCB", P["ant"], "#111827", 4),
    Part("Primary cells, 2 x AA Li-SOCl2, with pulse capacitor", P["cells"], "#C2410C", 5),
    Part("Puck base and potting", P["base"], "#6B7280", 6),
    Part("Road-marker epoxy bed", P["pad"], "#1F2937", 7),
    Part("Sign face with legend (option)", sign_panel, "#1D4ED8", 8),
    Part("E-paper display in window housing (option)", epaper, "#E5E7EB", 9),
    Part("Sign pole brackets and band clamps (option)", clamps, "#94A3B8", 10),
    Part("Host FieldNode (option, costed in FieldNode)", fieldnode, "#16A34A", 11),
    Part("Existing street pole (not supplied)", pole, "#9CA3AF", None),
]

# ---------------- street context (hero only) ----------------
X0, X1 = -8600.0, 4200.0
road = Pos((X0 + X1) / 2, -2000, -100) * Box(X1 - X0, 4000, 200)
side = Pos((X0 + X1) / 2, 1200, (CURB_H - 200) / 2) * Box(X1 - X0, 2400, CURB_H + 200)
# bay edge line 2.6 m from the curb, and slot ends every 7 m (slot B centered on the free puck)
bay_lines = Pos((X0 + X1) / 2, -2600, 1) * Box(X1 - X0 - 600, 120, 2)
for x in (-SLOT / 2, SLOT / 2):
    if X0 < x < X1:
        bay_lines = bay_lines + Pos(x, -1300, 1) * Box(120, 2600, 2)
# parked van in the occupied slot, over a second (hidden) puck
VX = -SLOT + 1500.0
van_body = Pos(VX, -1300, 400 + 1150) * Box(5400, 2000, 2300)
van_cab = Pos(VX + 2700 + 350, -1300, 400 + 700) * Box(700, 1950, 1400)
wheels = None
for wx in (VX - 1700, VX + 1900):
    for wy in (-1300 - 870, -1300 + 870):
        w = Pos(wx, wy, 350) * Rot(90, 0, 0) * Cylinder(350, 220)
        wheels = w if wheels is None else wheels + w
p2 = puck(VX, -1300)
puck_hidden = p2["dome"] + p2["base"] + p2["pad"]

slot_free = Pos(0, -1300, 0.6) * Box(SLOT - 200, 2400, 1.2)
slot_used = Pos((X0 + 100 - SLOT / 2) / 2, -1300, 0.6) * Box(-SLOT / 2 - X0 - 300, 2400, 1.2)
context = [
    Part("Road and sidewalk", road + side, "#D1D5DB", None),
    Part("Free slot shown on the sign", slot_free, "#99F6E4", None),
    Part("Occupied slot", slot_used, "#FED7AA", None),
    Part("Bay markings", bay_lines, "#F9FAFB", None),
    Part("Parked delivery van", van_body + van_cab + wheels, "#E5E7EB", None),
    Part("Second puck under the van", puck_hidden, "#EAB308", None),
]


def media():
    key = ["One puck per 7 m vehicle slot; puck 150 mm dia, 31 mm high",
           "Report in 18 s typical and worst at SF9, US915 (LDZ-CAL-001)",
           "Cell life 7.7 years at SF9 on 2 x AA Li-SOCl2 (derated 40 %)",
           "Gateway within 300 m of the bay; 340 m reach from under a van",
           "Two-puck kit about $116 (target $120); sign option $101 plus a FieldNode"]
    render_all(parts, project="LoadZone", title="Loading bay occupancy sensor concept", dwg_no="LDZ-DWG-010",
               key_figures=key, date="2026-10-02", cut=False, context=context,
               flow={"title": "bay event flow, % of occupancy changes (estimates)", "unit": "%",
                     "stages": [("Bay state changes", 100), ("Puck detects", 97),
                                ("LoRaWAN uplink", 96), ("Server bay state", 96),
                                ("Sign and data feed", 96)],
                     "losses": [(0, "Missed detections", 3),
                                (1, "Uplink lost; heartbeat corrects", 1)]})

    md = ROOT / "media"
    # Exploded view: pole left out; puck drawn at 4x scale, sign option drawn lower and beside it,
    # so every numbered part reads at one scale.
    K = 4.0
    ex_puck = {1: (0, 0, 470), 2: (260, 0, 330), 3: (60, -40, 230), 4: (420, 60, 160), 5: (-260, -40, 150),
               6: (0, 0, 0), 7: (0, 0, -170)}
    dz = -(SIGN_Z0 - 900)
    ex_sign = {8: (-POLE_X + 1300, -POLE_Y + PY + 150, dz), 9: (-POLE_X + 1550, -POLE_Y + PY + 150, dz),
               10: (-POLE_X + 1080, -POLE_Y + PY + 150, dz),
               11: (-POLE_X + 2500, -POLE_Y + PY - 300, -(FN_Z - 700))}
    PK = puck(PX, PY, K)
    key_of = {1: "dome", 2: "mag", 3: "board", 4: "ant", 5: "cells", 6: "base", 7: "pad"}
    ex_parts = []
    for p in parts:
        if p.bom is None:
            continue
        if p.bom <= 7:
            ex_parts.append(Part(p.name, PK[key_of[p.bom]], p.color, p.bom, ex_puck[p.bom]))
        else:
            ex_parts.append(Part(p.name, p.shape, p.color, p.bom, ex_sign[p.bom]))
    concept._render(ex_parts, md / "exploded.png", offsets=True, labels=True, elev=22, azim=-58,
                    title="LoadZone: exploded view (puck left at 4x scale, sign option right)",
                    note="Callout numbers match bom/bom.csv. Sign option shown lowered; it mounts at 2.1 m on an existing pole.")

    # Cutaway of the puck only, with a slab of road for context.
    road_cut = Part("Road surface", Pos(PX, PY, -30) * Box(260, 260, 60), "#D1D5DB", None)
    puck_parts = [p for p in parts if p.bom is not None and p.bom <= 7] + [road_cut]
    concept._render(cutaway_parts(puck_parts, keep="+Y"), md / "cutaway.png", azim=-90, elev=22,
                    title="LoadZone: puck cutaway",
                    note="Potting (grey) fills the dome around the cells (orange), radio board (teal) and antenna; the magnetometer is behind the cut.")
    for d in md.glob("_views*"):
        import shutil
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    media()
