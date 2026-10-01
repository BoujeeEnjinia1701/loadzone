"""LoadZone prototype build plan pictures (LDZ-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything. A single picture can be drawn with, for example,
"joints:3" or "steps:5" (one per process keeps memory low). Every picture is drawn from
cad/src/model.py (build_parts, build_tooling, build_sign), so the pictures and the model agree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/LDZ-DWG-101 to 107        making sketches for the made and drilled components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/tray-layout.png     base tray feature positions (matplotlib)
    docs/05-build-plan/sign-holes.png      sign face drilling layout (matplotlib)
    docs/05-build-plan/wiring.png          block-level wiring (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import os  # noqa: E402
os.chdir(ROOT)
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, derived, build_parts, build_tooling, build_sign, cavity_r  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
REPO = "github.com/BoujeeEnjinia1701/loadzone"

COL = {"dome": "#EAB308", "base": "#6B7280", "cells": "#C2410C", "board": "#0F766E", "mag": "#7C3AED",
       "ant": "#111827", "potting": "#7DD3FC", "pad": "#1F2937", "slab": "#9CA3AF", "master": "#60A5FA",
       "mould": "#F472B6", "core": "#34D399", "face": "#1D4ED8", "bracket": "#0E7490", "band": "#9CA3AF",
       "housing": "#E5E7EB", "bolt": "#111827", "gland": "#374151", "pole": "#9CA3AF"}

_C = _T = _S = None

# Leader anchors: a queue of 3D points (or None) consumed in part order by the next picture,
# so a leader can be pinned to a chosen spot on a part instead of the kit's default point.
_ANCHORS = []
_default_anchor = bv._anchor


def _anchor(v):
    import numpy as np
    t = _ANCHORS.pop(0) if _ANCHORS else None
    if t is None:
        return _default_anchor(v)
    return v[np.argmin(np.linalg.norm(v - np.asarray(t, float), axis=1))]


bv._anchor = _anchor


def pin(*pts):
    _ANCHORS[:] = list(pts)


def C():
    global _C
    if _C is None:
        _C = build_parts(P)
    return _C


def T():
    global _T
    if _T is None:
        _T = build_tooling(P)
    return _T


def S():
    global _S
    if _S is None:
        _S = build_sign(P)
    return _S


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def fuse(*shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def box_win(shape, x0, x1, y0, y1, z0, z1):
    import build123d as b
    return shape & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))


def half(shape, keep="+Y"):
    """Keep one half of a shape, cut through the puck axis."""
    big = 1000
    if keep == "+Y":
        return box_win(shape, -big, big, 0, big, -big, big)
    return box_win(shape, -big, big, -big, 0, -big, big)


def slab():
    import build123d as b
    return b.Pos(0, 0, -25) * b.Box(300, 300, 50)


# ----------------------------------------------------------------- overview
def overview():
    import build123d as b
    c, s = C(), S()
    # puck stack in front of and to the left of the sign, at true scale
    at = (560, 330, -120)
    mv = lambda sh, dz: b.Pos(at[0], at[1], at[2] + 2 * dz) * sh.scale(2)  # noqa: E731
    parts = [
        part("Dome, cast polyurethane", mv(c["dome"], 330), COL["dome"]),
        part("Base tray, printed", mv(c["base"], 0), COL["base"]),
        part("Cells and pulse capacitor", mv(c["cells"] + c["cap"], 120), COL["cells"]),
        part("Radio board and magnetometer", mv(c["board"] + c["mag"], 175), COL["board"]),
        part("Antenna", mv(c["ant"], 230), COL["ant"]),
        part("Potting, poured last", mv(c["potting"], 270), COL["potting"]),
        part("Epoxy bed (applied at bonding)", mv(c["pad"], -90), COL["pad"]),
        part("Sign brackets (2) and bolts", s["brackets"] + s["bracket_bolts"], COL["bracket"], (-170, 0, 0)),
        part("Sign face (option)", s["sign_face"], COL["face"]),
        part("Display housing, screws and gland", s["display"] + s["housing_screws"] + s["gland"], "#D1D5DB", (150, 0, 0)),
        part("Band clamps (2)", s["bands"] + s["band_housings"], COL["band"], (-380, 0, 0)),
    ]
    return bv.overview(parts, OUT / "overview.png", "LoadZone prototype: every component, pulled apart",
                       subtitle="Numbered in build order; 8 to 11 are the sign option. Puck drawn at twice "
                                "the sign's scale; the dome casting tooling is in section 3",
                       elev=16, azim=-72, size=(11, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    c, t, s = C(), T(), S()
    base = dict(project="LoadZone", date=DATE)
    out = []
    pole = part("Existing pole (not supplied)", s["pole_ref"], COL["pole"])
    H = P["mould_h"]
    R = P["mould_r"]

    def want(n):
        return only is None or n in only

    if want(101):
        out.append(bv.component_sheet(
            Part("Mould master", t["master"], COL["master"]), [],
            dwg_no="LDZ-DWG-101", title="LoadZone dome mould master: making sketch",
            material="PETG, 3D printed in one piece, 0.2 mm layers", inset_view=(30, -60),
            notes=["One print: a 194 mm round plate 3 mm thick, a box wall 3 mm thick",
                   "  and 35 mm tall round its edge (188 mm inside), and the dome",
                   "  shape standing on the plate in the middle, crown up.",
                   "Dome shape: 150 mm across at the plate, 104 mm across the crown,",
                   "  22 mm tall, 6 mm radius round the crown edge.",
                   "Print with the plate on the bed; 4 walls; 20 % infill is enough.",
                   "Sand the dome shape smooth (to 400 grit) and seal it with primer:",
                   "  the silicone copies every layer line onto the dome.",
                   "Seal the joint between plate and wall with a bead of hot glue.",
                   "Use: spray mould release, pour silicone to 10 mm over the crown",
                   "  (32 mm deep), let it cure, then pull the block out (step 1).",
                   "Check: the plate sits flat; no gap at the foot of the dome."],
            **base))

    if want(102):
        core_print = b.Rot(180, 0, 0) * b.Pos(0, 0, -(H + P["core_flange_t"])) * t["core"]
        out.append(bv.component_sheet(
            Part("Core plug", t["core"], COL["core"]), [part("Silicone mould", t["mould"], COL["mould"])],
            dwg_no="LDZ-DWG-102", title="LoadZone dome core plug: making sketch",
            material="PETG, 3D printed, 0.2 mm layers", view_shape=core_print, inset_view=(35, -60),
            notes=["Drawn as printed: flange on the bed, core pointing up.",
                   "Flange 194.6 mm across, 5 mm thick, with a skirt 6 mm deep and",
                   "  3 mm thick round its edge (188.6 mm inside): the skirt slides",
                   "  over the silicone block and centres the core in the cavity.",
                   "Core: a cone 142 mm across at the flange, 96 mm across at the tip,",
                   "  18 mm long. It forms the inside of the dome.",
                   "Four 4 mm overflow holes on a 146 mm circle, at 45 degrees to",
                   "  each other: spare resin and air come out here.",
                   "Sand the core smooth and spray mould release before each cast.",
                   "Fit: flange flat on the top of the silicone block; the gap between",
                   "  the core and the cavity is the 4 mm dome wall at the crown.",
                   "Check: on a trial fit with no resin the flange sits flat all round."],
            **base))

    if want(103):
        dome_up = b.Pos(0, 0, -D["z_base_top"]) * c["dome"]
        out.append(bv.component_sheet(
            Part("Dome", c["dome"], COL["dome"]), [part("Base tray", c["base"], COL["base"]), part("Epoxy bed", c["pad"], COL["pad"])],
            dwg_no="LDZ-DWG-103", title="LoadZone puck dome (make 2): casting sketch",
            material="Rigid cast polyurethane, Shore D about 80, yellow, UV stabilised", view_shape=dome_up, inset_view=(25, -60),
            notes=["Outside: 150 mm across at the rim, 104 mm across the crown, 22 mm",
                   "  tall, 6 mm radius round the crown edge.",
                   "Inside: a cone 142 mm across at the rim and 96 mm at the top,",
                   "  18 mm deep, so the crown is 4 mm thick and the rim face is a",
                   "  flat ring 4 mm wide.",
                   "Cast in the silicone mould with the core plug (step 2): mix about",
                   "  95 g of resin with yellow pigment, pour it into the cavity, press",
                   "  the core plug down until its flange sits on the block.",
                   "Demould after the maker's time; post-cure as the data sheet says.",
                   "Trim the flash at the rim with a knife; keep the rim face flat.",
                   "Fit: the rim sits flat on the base tray, over its locating ring.",
                   "Check: 22 mm tall outside and 18 mm deep inside (so the crown",
                   "  is 4 mm), no bubbles in the crown, rim flat on a glass plate."],
            **base))

    if want(104):
        tray_up = b.Pos(0, 0, -P["pad_t"]) * c["base"]
        out.append(bv.component_sheet(
            Part("Base tray", c["base"], COL["base"]),
            [part("Cells", c["cells"] + c["cap"], COL["cells"]), part("Board", c["board"] + c["mag"], COL["board"]),
             part("Antenna", c["ant"], COL["ant"])],
            dwg_no="LDZ-DWG-104", title="LoadZone base tray (make 2): making sketch",
            material="ASA, 3D printed, 100 % infill in the disc", view_shape=tray_up, inset_view=(40, -60),
            notes=["Disc 150 mm across, 6 mm thick; road side flat. The tray layout",
                   "  picture gives every position from the centre.",
                   "Locating ring: tapered, 141.4 mm across at the disc, 135.0 mm at",
                   "  its top, 2.5 mm tall, 128 mm inside. It fits the dome's cavity",
                   "  with 0.3 mm all round.",
                   "Cell cradles: two per cell, 11 x 5 mm, 4 mm tall, saddle-shaped,",
                   "  centred 37 and 20 mm left of centre, 16 mm each side.",
                   "Board standoffs: four, 5 mm across, 3 mm tall, 1.6 mm pilot hole",
                   "  for M2 screws, at 5 and 35 mm right, 25 mm each side.",
                   "Antenna rib: 2 x 50 mm, 8 mm tall; its inner face 48.5 mm right.",
                   "Holes through the disc: fill 8 mm; four 4 mm vents (layout).",
                   "Print disc down in an enclosed printer. Sand the road side with",
                   "  80 grit so the epoxy bed keys to it.",
                   "Check: the dome drops over the ring and sits flat on the disc."],
            **base))

    if want(105):
        z0 = P["clamp_inset"]
        br = box_win(s["brackets"], -200, 200, -200, 200, z0 - 40, z0 + 40)
        br_flat = b.Pos(-D["face_back"], 0, -z0) * br
        out.append(bv.component_sheet(
            Part("Sign bracket", br, COL["bracket"]),
            [part("Sign face", box_win(s["sign_face"], -300, 300, -110, 110, z0 - 70, z0 + 70), COL["face"]),
             part("Pole", box_win(s["pole_ref"], -300, 300, -300, 300, z0 - 90, z0 + 90), COL["pole"]),
             part("Band", box_win(s["bands"] + s["band_housings"], -300, 300, -300, 300, z0 - 40, z0 + 40), COL["band"])],
            dwg_no="LDZ-DWG-105", title="LoadZone sign bracket (make 2): making sketch",
            material="Aluminium U-channel 50 x 40 x 3 mm, 6063 class", view_shape=br_flat, inset_view=(35, -125),
            notes=["Cut two 60 mm lengths of 50 x 40 x 3 mm channel; square and",
                   "  deburr the ends, and break the sharp edges of the flange ends.",
                   "Web (the 50 mm face that goes on the sign): two 6.5 mm holes,",
                   "  12 mm each side of centre, half way along (30 mm).",
                   "Flanges: one band slot in each, 3 mm wide and 14 mm long along",
                   "  the channel, centred half way along and 8.5 mm from the",
                   "  flange end. Chain drill 3 mm and file square.",
                   "Fit: the web sits flat on the back of the sign face on two M6",
                   "  button-head bolts from the front, nyloc nuts inside the channel.",
                   "The two flange ends bear on the pole; the band runs in through",
                   "  one slot, across in front of the pole, out of the other slot",
                   "  and round the back of the pole. Poles 60 to 90 mm seat.",
                   "Check: both slots line up; the bolts clear the band."],
            **base))

    if want(106):
        # laid flat: the printed front faces up, so the top view shows the holes as drilled
        face_flat = b.Plane(origin=(D["face_back"], 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0)).to_local_coords(s["sign_face"])
        out.append(bv.component_sheet(
            Part("Sign face", s["sign_face"], COL["face"]),
            [part("Brackets", s["brackets"], COL["bracket"]), part("Display housing", s["display"], COL["housing"]), pole],
            dwg_no="LDZ-DWG-106", title="LoadZone sign face (option): drilling sketch",
            material="Aluminium composite panel 450 x 600 x 3 mm, printed legend", view_shape=face_flat, inset_view=(20, -50),
            notes=["Drawn laid flat, printed side up. Bought from a sign maker with",
                   "  the legend printed; drill it here.",
                   "Heights from the bottom edge, sideways from the centre line.",
                   "Bracket bolts: four 6.5 mm holes, 12 mm each side of centre,",
                   "  100 and 500 mm up.",
                   "Display housing screws: four 4.5 mm holes, 88 mm each side of",
                   "  centre, 142 and 258 mm up.",
                   "Cable gland: one 20.5 mm hole on the centre line, 230 mm up",
                   "  (step drill).",
                   "Back the panel with scrap wood; drill from the printed side so",
                   "  the face does not lift. Deburr and peel the film.",
                   "The sign face drilling layout picture repeats these positions.",
                   "Check: hold a bracket and the housing to the panel and look",
                   "  through each hole."],
            **base))

    if want(107):
        hx, hy, hz = P["disp_housing"]
        hs = b.Plane(origin=(D["face_back"] + P["sign_t"], 0, P["disp_z"]), x_dir=(0, -1, 0), z_dir=(-1, 0, 0)).to_local_coords(s["display"])
        out.append(bv.component_sheet(
            Part("Display housing", s["display"], "#9CA3AF"),
            [part("Sign face", s["sign_face"], COL["face"]), part("Gland", s["gland"], COL["gland"])],
            dwg_no="LDZ-DWG-107", title="LoadZone display housing (option): drilling sketch",
            material="Bought polycarbonate enclosure, clear lid, about 200 x 140 x 24 mm", view_shape=hs, inset_view=(20, -50),
            notes=["Drawn laid flat, back wall up (the side you drill). Bought, clear lid,",
                   "  about 200 x 140 x 24 mm, IP65.",
                   "In the back wall, measured from its centre:",
                   "  four 4.5 mm holes, 88 mm each side and 58 mm above and below;",
                   "  one 20.5 mm hole for the M20 gland, 30 mm above centre.",
                   "Drill slowly from the outside with wood behind; deburr.",
                   "Inside: the e-paper panel tapes to the inside of the clear lid;",
                   "  the driver board sits on the back wall on its standoffs.",
                   "Fit: back wall flat on the front of the sign face; four M4",
                   "  pan-head screws from behind the sign, sealing washer and nut",
                   "  inside the housing; the gland body passes through the sign",
                   "  face and its nut tightens from behind.",
                   "Check: the lid gasket closes with no wire across it."],
            **base))
    return out


# ----------------------------------------------------------------- joints
def joints(only=None):
    import build123d as b
    out = []

    def want(n):
        return only is None or n in only

    if want(1):
        t = T()
        win = lambda sh: box_win(sh, 30, 110, -2, 3, 0, 45)  # noqa: E731
        out.append(bv.joint([
            part("Silicone mould", win(t["mould"]), COL["mould"]),
            part("Core plug (flange, skirt and core)", win(t["core"]), COL["core"]),
            part("Dome as cast", win(t["cast"]), COL["dome"])],
            OUT / "joint-01.png", "Joint 1: core plug in the silicone mould, cut open",
            subtitle="The flange sits on the block and the skirt centres it; the gap left is the dome wall",
            elev=8, azim=-90, size=(8, 6)))
    if want(2):
        c = C()
        win = lambda sh: box_win(sh, 53, 80, -2, 3, 0, 26)  # noqa: E731
        out.append(bv.joint([
            part("Dome wall; its rim sits flat on the tray", win(c["dome"]), COL["dome"]),
            part("Base tray and its locating ring", win(c["base"]), COL["base"]),
            part("Potting", win(c["potting"]), COL["potting"], alpha=0.85)],
            OUT / "joint-02.png", "Joint 2: dome rim on the base tray, cut open",
            subtitle="The tapered ring locates the dome with 0.3 mm all round; a sealant bead closes the outside seam",
            elev=8, azim=-90, size=(8, 6)))
    if want(3):
        c = C()
        pin((-60, -40, 9), None, None, None, None, None)
        out.append(bv.joint([
            part("Base tray: cradles, standoffs, rib", c["base"], COL["base"]),
            part("Cells (2) in their cradles", c["cells"], COL["cells"]),
            part("Pulse capacitor", c["cap"], "#EA580C"),
            part("Radio board on its standoffs", c["board"], COL["board"]),
            part("Magnetometer breakout", c["mag"], COL["mag"]),
            part("Antenna on the rib", c["ant"], COL["ant"])],
            OUT / "joint-03.png", "Joint 3: parts on the base tray, before the dome goes on",
            subtitle="Every part rests on the tray: cells on saddles, board on four standoffs, antenna stuck to the rib",
            elev=35, azim=-60, size=(8, 6)))
    if want(4):
        c = C()
        parts = [part("Dome", c["dome"], COL["dome"]), part("Base tray", c["base"], COL["base"]),
                 part("Potting fills every gap", c["potting"], COL["potting"], alpha=0.9),
                 part("Cells", c["cells"], COL["cells"]), part("Radio board", c["board"], COL["board"]),
                 part("Antenna", c["ant"], COL["ant"])]
        pin(None, (-70, 0, 3), (25, 0, 24), None, None, None)
        out.append(bv.joint(parts, OUT / "joint-04.png", "Joint 4: the potted puck, cut through a vent",
                            subtitle="Poured upside down through the fill hole; air leaves by the vents; cured flush with the road side",
                            cut="+Y", elev=12, azim=-90, size=(8, 6)))
    if want(5):
        c = C()
        win = lambda sh: box_win(sh, 53, 100, -2, 3, -20, 30)  # noqa: E731
        pin(None, None, (60, 0, 5), None, None)
        out.append(bv.joint([
            part("Test slab (asphalt or concrete paver)", win(slab()), COL["slab"]),
            part("Epoxy bed, 3 mm, 10 mm wider than the puck", win(c["pad"]), COL["pad"]),
            part("Base tray, road side sanded", win(c["base"]), COL["base"]),
            part("Dome", win(c["dome"]), COL["dome"]),
            part("Potting", win(c["potting"]), COL["potting"])],
            OUT / "joint-05.png", "Joint 5: puck on its epoxy bed, cut open at the edge",
            subtitle="The bed runs 10 mm beyond the rim all round; smooth the squeeze-out into a sloped edge before it cures",
            elev=8, azim=-90, size=(8, 6)))
    if want(6):
        s = S()
        zc = P["clamp_inset"]
        win = lambda sh: box_win(sh, -60, 80, -45, 45, zc - 6, zc + 4)  # noqa: E731
        pin((-20, -20, zc + 4), (50, 24, zc + 4), None, (-50, -5, zc + 4), (72.5, -40, zc + 4))
        out.append(bv.joint([
            part("Pole (existing)", win(s["pole_ref"]), COL["pole"]),
            part("Bracket", win(s["brackets"]), COL["bracket"]),
            part("Band through both flange slots", win(s["bands"]), "#475569"),
            part("Worm-drive housing behind the pole", win(s["band_housings"]), "#334155"),
            part("Sign face", win(s["sign_face"]), COL["face"])],
            OUT / "joint-06.png", "Joint 6: bracket and band on the pole, seen from above",
            subtitle="Cut level with the lower band. Both flange ends of the bracket bear on the pole; tightening the band pulls the pole onto them",
            elev=88, azim=-90, size=(8, 6)))
    if want(7):
        s = S()
        zc = P["clamp_inset"]
        win = lambda sh: box_win(sh, 20, 90, -40, 40, zc - 40, zc + 40)  # noqa: E731
        fb = D["face_back"]
        pin((fb, 38, zc - 36), (fb - 20, -25, zc + 30), (fb - 6, 12, zc))
        out.append(bv.joint([
            part("Sign face", win(s["sign_face"]), COL["face"]),
            part("Bracket web and flanges", win(s["brackets"]), COL["bracket"]),
            part("M6 button-head bolts, nyloc nuts inside", win(s["bracket_bolts"]), COL["bolt"])],
            OUT / "joint-07.png", "Joint 7: bracket on the back of the sign face",
            subtitle="Seen from behind and above. Two bolts from the front; the web lies flat on the panel; nuts inside the channel",
            elev=30, azim=180, size=(8, 6)))
    if want(8):
        s = S()
        zc = P["disp_z"]
        fb = D["face_back"]
        zs = zc + P["housing_screw"][1]          # the upper screws' axis
        win = lambda sh: box_win(sh, fb - 30, fb + 40, -110, 0, zc + 15, zs)  # noqa: E731
        st = P["sign_t"]
        pin((fb + st / 2, -104, zs), (fb + st + 20, -60, zs), (fb - 1, -88, zs), (fb - 8, 0, zc + 30))
        out.append(bv.joint([
            part("Sign face", win(s["sign_face"]), COL["face"]),
            part("Display housing (clear lid at the front)", win(s["display"]), "#CBD5E1"),
            part("M4 screw from behind, nut inside", win(s["housing_screws"]), COL["bolt"]),
            part("M20 gland through the face", win(s["gland"]), COL["gland"])],
            OUT / "joint-08.png", "Joint 8: display housing on the sign face, cut through a screw and the gland",
            subtitle="Seen from the front, above and right. The housing back lies flat on the face; the gland takes the cable out behind",
            elev=40, azim=60, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    import build123d as b
    out = []

    def want(n):
        return only is None or n in only

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    if want(1):
        t = T()
        H = P["mould_h"]
        block_up = b.Pos(0, 0, H) * b.Rot(180, 0, 0) * b.Pos(0, 0, -H) * t["mould"]   # as poured: crown up
        st(1, [part("Mould master", t["master"], COL["master"])],
           [part("Silicone, poured to 10 mm over the crown", half(block_up, "+Y"), COL["mould"], (0, 0, 90))],
           "make the silicone mould",
           "Release agent on the master; pour slowly into one corner; cure; pull the block out and turn it over. Shown cut",
           elev=22, azim=-60, label_done=True)
    if want(2):
        t = T()
        st(2, [part("Silicone mould, cavity up, resin poured in", half(t["mould"], "+Y"), COL["mould"])],
           [part("Core plug", half(t["core"], "+Y"), COL["core"], (0, 0, 70))],
           "cast the dome",
           "Shown cut. Pour about 95 g of mixed resin into the cavity; press the core plug down until its flange sits on the block",
           elev=25, azim=-60, label_done=True)
    if want(3):
        c = C()
        st(3, [part("Base tray", c["base"], COL["base"])],
           [part("Cells and capacitor", c["cells"] + c["cap"], COL["cells"], (0, 0, 45)),
            part("Radio board and magnetometer", c["board"] + c["mag"], COL["board"], (0, 0, 60)),
            part("Antenna", c["ant"], COL["ant"], (0, 0, 75))],
           "electronics onto the base tray",
           "Cells into the cradles, board on four M2 screws, antenna onto the rib; then wire, program and test (hold point)",
           elev=35, azim=-60, label_done=True)
    if want(4):
        c = C()
        inside = fuse(c["cells"], c["cap"], c["board"], c["mag"], c["ant"])
        st(4, [part("Base tray with electronics", c["base"] + inside, COL["base"])],
           [part("Dome", c["dome"], COL["dome"], (0, 0, 60))],
           "dome onto the base tray",
           "Lower the dome over the locating ring; tape it down; run a bead of sealant round the outside seam",
           elev=25, azim=-60, label_done=True)
    if want(5):
        c = C()
        flip = lambda sh: b.Rot(180, 0, 0) * sh  # noqa: E731
        done = [part("Dome (crown down, in a padded ring)", half(flip(c["dome"])), COL["dome"]),
                part("Base tray (now on top)", half(flip(c["base"])), COL["base"]),
                part("Cells, board and antenna", half(flip(fuse(c["cells"], c["cap"], c["board"], c["mag"], c["ant"]))), COL["cells"])]
        st(5, done, [part("Potting, poured through the fill hole", half(flip(c["potting"])), COL["potting"], (0, 0, 80))],
           "pot the puck, upside down",
           "Shown cut. Pour slowly through the 8 mm fill hole until resin shows at every vent; top up; cure; scrape flush",
           elev=15, azim=-80, label_done=True)
    if want(6):
        c = C()
        puck = fuse(c["dome"], c["base"])
        st(6, [part("Test slab, cleaned and dry", slab(), COL["slab"])],
           [part("Epoxy bed, spread first", c["pad"], COL["pad"], (0, 0, 0)),
            part("Puck", puck, COL["dome"], (0, 0, 110))],
           "bond the puck to a test slab",
           "Spread the mixed epoxy 3 mm thick and 170 mm across; press the puck in with a twist; tool the squeeze-out",
           elev=22, azim=-60, label_done=True)
    if want(7):
        s = S()
        hi = lambda sh: box_win(sh, -500, 500, -500, 500, P["sign_h"] / 2, 2000)  # noqa: E731
        lo = lambda sh: box_win(sh, -500, 500, -500, 500, -500, P["sign_h"] / 2)  # noqa: E731
        st(7, [part("Sign face, printed side away from you", s["sign_face"], COL["face"])],
           [part("Upper bracket, two M6 bolts and nyloc nuts", hi(s["brackets"] + s["bracket_bolts"]), COL["bracket"], (-90, 0, 0)),
            part("Lower bracket, two M6 bolts and nyloc nuts", lo(s["brackets"] + s["bracket_bolts"]), COL["bracket"], (-90, 0, 0))],
           "brackets onto the back of the sign",
           "Seen from behind, with the sign face down on a soft cloth. Bolts from the printed side; nyloc nuts inside the channel",
           elev=20, azim=-150, label_done=True)
    if want(8):
        s = S()
        st(8, [part("Sign face with brackets", s["sign_face"] + s["brackets"] + s["bracket_bolts"], COL["face"])],
           [part("Display housing, panel and driver inside", s["display"], "#818CF8", (150, 0, 0)),
            part("M20 gland, in the housing", s["gland"], COL["gland"], (150, 0, 0)),
            part("M4 screws, from behind", s["housing_screws"], COL["bolt"], (-110, 0, 0))],
           "display housing onto the sign face",
           "Seen from the left. Housing back flat on the face; gland body through the face; four M4 screws from behind, nuts inside",
           elev=15, azim=-75, label_done=True)
    if want(9):
        s = S()
        sign = s["sign_face"] + s["brackets"] + s["bracket_bolts"] + s["display"] + s["gland"] + s["housing_screws"]
        hi = lambda sh: box_win(sh, -500, 500, -500, 500, P["sign_h"] / 2, 2000)  # noqa: E731
        lo = lambda sh: box_win(sh, -500, 500, -500, 500, -500, P["sign_h"] / 2)  # noqa: E731
        bands = s["bands"] + s["band_housings"]
        st(9, [part("Sign with brackets and display", sign, COL["face"])],
           [part("Upper band clamp", hi(bands), "#475569", (-120, 0, 0)),
            part("Lower band clamp", lo(bands), "#475569", (-120, 0, 0))],
           "sign onto the pole stub",
           "Seen from behind. Flange ends against the pole; each band through both slots and round the pole; tighten",
           context=[part("Pole stub", b.Pos(0, 0, 300) * b.Cylinder(P["pole_r"], 900), COL["pole"])],
           elev=20, azim=-150, label_done=True)
    return out


# ----------------------------------------------------------------- layouts (matplotlib)
INK, MUT, AC = "#111827", "#4B5563", "#0F766E"


def _foot(fig):
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, REPO, fontsize=7, color=AC, ha="right", family="monospace")


def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle, Wedge
    OUT.mkdir(parents=True, exist_ok=True)
    res = []
    # ---- base tray, seen from above (the side the parts go on)
    fig = plt.figure(figsize=(11, 8.2), dpi=150)
    ax = fig.add_axes([0.03, 0.07, 0.62, 0.82]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Circle((0, 0), P["base_r"], fc="#F3F4F6", ec=INK, lw=1.2))
    sh = P["spigot_h"]
    r0 = cavity_r(0) - P["spigot_clr"]
    ax.add_patch(Wedge((0, 0), r0, 0, 360, width=r0 - P["spigot_in_r"], fc="#D1D5DB", ec=MUT, lw=0.8))
    ax.axhline(0, color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3))); ax.axvline(0, color=MUT, lw=0.5, ls=(0, (8, 3, 2, 3)))
    cx, cy, cz = P["cradle"]
    for x in P["cell_x"]:
        ax.add_patch(Rectangle((x - P["cell_d"] / 2, -P["cell_l"] / 2), P["cell_d"], P["cell_l"], fc="none", ec=COL["cells"], lw=0.8, ls="--"))
        for s_ in (-1, 1):
            ax.add_patch(Rectangle((x - cx / 2, s_ * P["cradle_y"] - cy / 2), cx, cy, fc="#9CA3AF", ec=INK, lw=0.8))
    bx = P["board_x"]
    ax.add_patch(Rectangle((bx - P["board"][0] / 2, -P["board"][1] / 2), P["board"][0], P["board"][1], fc="none", ec=COL["board"], lw=0.8, ls="--"))
    sx, sy = P["standoff_xy"]
    for i in (-1, 1):
        for j in (-1, 1):
            ax.add_patch(Circle((bx + i * sx, j * sy), P["standoff_r"], fc="#9CA3AF", ec=INK, lw=0.8))
    rx, ry, rz = P["rib"]
    xr = P["ant_x"] + P["ant"][0] / 2
    ax.add_patch(Rectangle((xr, -ry / 2), rx, ry, fc="#9CA3AF", ec=INK, lw=0.8))
    ax.add_patch(Rectangle((P["cap_xy"][0] - 5, P["cap_xy"][1] - 5), 10, 10, fc="none", ec="#EA580C", lw=0.8, ls="--"))
    fx, fy = P["fill_xy"]
    ax.add_patch(Circle((fx, fy), P["fill_d"] / 2, fc="white", ec=INK, lw=1.2))
    for vx, vy in P["vents"]:
        ax.add_patch(Circle((vx, vy), P["vent_d"] / 2, fc="white", ec=INK, lw=1.2))
    lab = dict(fontsize=7.2, color=INK, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
    ax.annotate("fill hole 8\n(-5, +15)", (fx, fy), (-8, 40), ha="center", arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5), **lab)
    ax.annotate("vent 4 (+20, 0)\nunder the board", (20, 0), (20, -40), ha="center", arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5), **lab)
    ax.annotate("vent 4 (0, +55)", (0, 55), (30, 64), ha="left", arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5), **lab)
    ax.annotate("vent 4 (0, -55)", (0, -55), (30, -64), ha="left", arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5), **lab)
    ax.annotate("vent 4\n(-55, 0)", (-55, 0), (-98, -18), ha="center", arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5), **lab)
    ax.annotate("antenna rib\ninner face +48.5", (xr + 1, 20), (88, 35), ha="left", arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5), **lab)
    ax.annotate("standoffs at +5 and +35,\n25 each side", (bx + sx, sy), (88, 8), ha="left", arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5), **lab)
    ax.annotate("cradles at -37 and -20,\n16 each side", (P["cell_x"][0], -P["cradle_y"]), (-88, -50), ha="center",
                arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5), **lab)
    ax.annotate("locating ring", (-48, 50), (-88, 66), ha="center", arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5), **lab)
    ax.annotate("capacitor (-5, -15)", (P["cap_xy"][0], P["cap_xy"][1] - 5), (-20, -42), ha="center", arrowprops=dict(arrowstyle="-", color=MUT, lw=0.5), **lab)
    ax.text(0, -84, "positions in mm from the centre: + to the right (toward the antenna) and + up the page", ha="center", fontsize=7.6, color=MUT)
    ax.set_xlim(-115, 128); ax.set_ylim(-90, 82)
    fig.text(0.03, 0.965, "Base tray: where every feature goes", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.93, "Seen from above, the side the parts sit on. Grey: printed features. Dashed: the parts that sit on them. Circles: holes through the disc.",
             fontsize=8.2, color=MUT, va="top")
    key = ["Disc 150 across, 6 thick", "Locating ring 141.4 to 135.0 across,", "  2.5 tall, 128 inside",
           "Cradles 11 x 5, 4 tall, saddle", "  shaped, two per cell", "Standoffs 5 across, 3 tall,",
           "  1.6 pilot for M2 screws", "Antenna rib 2 x 50, 8 tall", "Fill hole 8; four vents 4",
           "", "Cells run up the page,", "  14.5 across and 50.5 long, 2.5 apart", "Board 36 x 56, its long side",
           "  up the page"]
    fig.text(0.70, 0.84, "Sizes (mm)", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, t_ in enumerate(key):
        fig.text(0.70, 0.81 - i * 0.026, t_, fontsize=8, color=INK, va="top")
    _foot(fig)
    fig.savefig(OUT / "tray-layout.png", facecolor="white"); plt.close(fig); res.append(OUT / "tray-layout.png")

    # ---- sign face, seen from the front
    fig = plt.figure(figsize=(9.5, 11), dpi=150)
    ax = fig.add_axes([0.08, 0.07, 0.6, 0.84]); ax.set_aspect("equal"); ax.set_axis_off()
    W, Hs = P["sign_w"], P["sign_h"]
    ax.add_patch(Rectangle((-W / 2, 0), W, Hs, fc="#EFF6FF", ec=INK, lw=1.2))
    hx, hy, hz = P["disp_housing"]
    zc = P["disp_z"]
    ax.add_patch(Rectangle((-hy / 2, zc - hz / 2), hy, hz, fc="none", ec=MUT, lw=0.8, ls="--"))
    ax.text(0, zc + hz / 2 - 5, "display housing outline", ha="center", va="top", fontsize=7, color=MUT, bbox=dict(boxstyle="square,pad=0.15", fc="#EFF6FF", ec="none"))
    for z in (P["clamp_inset"], Hs - P["clamp_inset"]):
        ax.add_patch(Rectangle((-25, z - 30), 50, 60, fc="none", ec=COL["bracket"], lw=0.8, ls="--"))
    holes = []
    for z in (P["clamp_inset"], Hs - P["clamp_inset"]):
        holes += [(s_ * P["bracket_bolt_y"], z, 6.5) for s_ in (-1, 1)]
    hy_s, hz_s = P["housing_screw"]
    holes += [(sy_ * hy_s, zc + sz_ * hz_s, 4.5) for sy_ in (-1, 1) for sz_ in (-1, 1)]
    holes += [(0, zc + P["gland_dz"], P["gland_hole"])]
    for x, z, d in holes:
        ax.add_patch(Circle((x, z), d / 2, fc="white", ec=INK, lw=1))
        ax.plot([x - d / 2 - 3, x + d / 2 + 3], [z, z], color=MUT, lw=0.4); ax.plot([x, x], [z - d / 2 - 3, z + d / 2 + 3], color=MUT, lw=0.4)
    ax.plot([0, 0], [-6, Hs + 6], color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
    xs = sorted({abs(h[0]) for h in holes if h[0] > 0})
    for i, x in enumerate(xs):
        ax.plot([x, x], [0, -12], color=AC, lw=0.4, ls=":")
        ax.text(x, -15, f"{x:g}", ha="center", va="top", fontsize=7.5, color=AC)
    ax.text(0, -38, "sideways from the centre line, mm (same each side)", ha="center", fontsize=8, color=MUT)
    zs = sorted({h[1] for h in holes})
    for i, z in enumerate(zs):
        ax.plot([-W / 2 - 14, -W / 2], [z, z], color=AC, lw=0.4, ls=":")
        ax.text(-W / 2 - 16, z, f"{z:g}", ha="right", va="center", fontsize=7.5, color=AC)
    ax.text(-W / 2 - 62, Hs / 2, "up from the bottom edge, mm", rotation=90, ha="center", va="center", fontsize=8, color=MUT)
    ax.set_xlim(-W / 2 - 75, W / 2 + 10); ax.set_ylim(-45, Hs + 10)
    fig.text(0.04, 0.975, "Sign face: drilling layout", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.95, "Seen from the front (the printed side). Dashed: the brackets behind and the housing in front.", fontsize=8.5, color=MUT, va="top")
    key = ["Panel 450 x 600 x 3", "Bracket bolts 6.5, at 12,", "  100 and 500 up", "Housing screws 4.5, at 88,",
           "  142 and 258 up", "Gland 20.5 on the centre", "  line, 230 up"]
    fig.text(0.72, 0.86, "Holes (mm)", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, t_ in enumerate(key):
        fig.text(0.72, 0.83 - i * 0.024, t_, fontsize=8, color=INK, va="top")
    _foot(fig)
    fig.savefig(OUT / "sign-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "sign-holes.png")
    return res


def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.0), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 70); ax.set_axis_off()
    ax.text(2, 68, "LoadZone puck: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 64.6, "Bought modules on a 36 x 56 mm piece of prototyping board; no circuit board is laid out. Stranded copper, "
            "soldered joints, heat shrink on every joint (no screw terminals: the puck is potted).", fontsize=8.3, color=MUT, va="top")
    _foot(fig)

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.3, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.2, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, RF = "#B91C1C", "#1D4ED8", "#6B7280", "#374151"
    ax.add_patch(FancyBboxPatch((30, 10), 60, 44, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(31.5, 52.8, "The radio board (prototyping board), with the pulse capacitor beside it on the tray", fontsize=8, color=MUT, va="top")
    blk(3, 38, 18, 12, "Cell 1", "AA Li-SOCl2, 3.6 V,\nsolder tabs", "#C2410C")
    blk(3, 18, 18, 12, "Cell 2", "AA Li-SOCl2, 3.6 V,\nsolder tabs", "#C2410C")
    blk(34, 30, 16, 14, "Diodes and fuse", "one Schottky diode\nper cell; 0.5 A fuse\nafter the join", "#7C3AED")
    blk(34, 13, 16, 12, "Pulse capacitor", "85 °C hybrid,\non the tray", "#EA580C")
    blk(58, 30, 15, 14, "Radio module", "STM32WL class,\nwith 2 MB flash", "#0F766E")
    blk(76, 30, 12, 14, "Magnetometer", "LIS2MDL class\nbreakout, I2C", "#7C3AED")
    blk(58, 13, 15, 10, "Programming pads", "SWD and UART,\nused before potting", "#374151")
    blk(98, 30, 18, 14, "Antenna", "flexible PCB,\non the tray rib", RF)
    wire([(21, 44), (34, 39)], RED); lab(22, 46.5, "cell 1 +, 0.5 mm²", RED)
    wire([(21, 24), (34, 34)], RED); lab(22, 21.5, "cell 2 +, 0.5 mm²", RED)
    wire([(50, 37), (58, 37)], RED); lab(54, 39.5, "3.4 V rail", RED, "center")
    wire([(54, 37), (54, 25), (50, 19)], RED); lab(54.6, 30.5, "0.5 mm²", RED)
    wire([(73, 41), (76, 41)], BLU, 1.4); lab(74.5, 46, "I2C,\n0.25 mm²", BLU, "center")
    wire([(65.5, 30), (65.5, 23)], GRY, 1.4); lab(66.2, 26.5, "pads", GRY)
    wire([(71, 30), (71, 27.5), (107, 27.5), (107, 30)], RF, 1.2); lab(92, 25.6, "u.FL lead", RF, "center")
    wire([(12, 38), (12, 30)], GRY, 1.4); lab(12.6, 34, "negatives joined, then to board\nground, 0.5 mm²", GRY)
    ax.text(3, 7.2, "Safety: Li-SOCl2 cells are never charged. Each cell feeds the rail only through its own diode, so one cell can never charge the other.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(3, 4.4, "Red: power. Blue: signal. Grey: return and programming. All circuits are extra-low voltage (3.67 V at most).",
            fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        name, _, sel = w.partition(":")
        if sel:
            r = fns[name](only={int(k) for k in sel.split(",")})
        else:
            r = fns[name]()
        print(w, "->", r)
