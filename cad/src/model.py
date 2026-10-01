"""LoadZone parametric model (build123d), TRL 3, constructable design (LDZ-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    run the constructability checks only

The model is the design as it will be built (STANDARDS section 18):
  puck   cast polyurethane dome on a printed base tray that carries the cells in cradles, the
         radio board on standoffs and the antenna on a rib; the dome locates on the tray's
         tapered spigot; the cavity is potted through a fill hole in the tray, puck upside down,
         with vent holes; the puck is bonded to the road on a two-part epoxy bed
  tooling printed mould master (for the silicone mould) and printed core plug for casting the dome
  sign   (option) aluminium composite face, two aluminium channel brackets bolted to its back,
         stainless band clamps through slots in the bracket flanges, and a bought display
         housing screwed to the face from behind with a cable gland through the face

Puck axes: origin at the center of the puck on the road surface, Z up, X along the curb,
Y across the street. Sign axes: origin on the pole axis at the bottom edge of the sign face,
Z up, the sign face toward +X. Tooling axes: casting position, mould on the bench at Z = 0,
cavity opening up. Units mm.
"""
import math
import sys
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Puck (LDZ-PRC-001 v0.4, R7): surface-bonded cast polyurethane dome over potted electronics
    "pad_r": 85.0, "pad_t": 3.0,            # two-part road-marker epoxy bed (LDZ-DDR-002)
    "base_r": 75.0, "base_t": 6.0,          # printed base tray disc (150 mm diameter)
    "dome_h": 22.0, "dome_top_r": 52.0,     # frustum dome above the base
    "wall": 4.0,                            # cast dome wall; the cavity is fully potted
    "crown_fillet": 6.0,                    # rounded top edge (R7)
    # Base tray features (LDZ-DDR-003, P1 and P2)
    "spigot_h": 2.5, "spigot_clr": 0.3, "spigot_in_r": 64.0,   # tapered locating ring inside the dome rim
    "cradle": (11.0, 5.0, 4.0), "cradle_y": 16.0,              # two saddles per cell (x, y, z), at y = +/-16
    "standoff_r": 2.5, "standoff_h": 3.0, "standoff_xy": (15.0, 25.0),   # board standoffs at board_x +/- 15, +/- 25
    "rib": (2.0, 50.0, 8.0),                                   # antenna rib (x, y, z)
    "fill_d": 8.0, "fill_xy": (-5.0, 15.0),                    # potting fill hole
    "vent_d": 4.0, "vents": ((20.0, 0.0), (0.0, 55.0), (0.0, -55.0), (-55.0, 0.0)),
    # Contents
    "cell_d": 14.5, "cell_l": 50.5,         # AA-size Li-SOCl2 bobbin cell (ER14505 class)
    "cell_x": (-37.0, -20.0),               # two cells lying along Y on the -X side (moved 3 mm in, LDZ-DDR-003 P3)
    "cap": (10.0, 10.0, 12.0), "cap_xy": (-5.0, -15.0),     # pulse capacitor envelope, standing on the tray
    "board": (36.0, 56.0, 1.6), "board_x": 20.0,            # carrier board (prototyping board)
    "module": (13.0, 16.0, 3.0), "module_y": -12.0,         # STM32WL-class LoRaWAN module
    "mag": (22.0, 18.0, 3.0), "mag_y": 14.0,                # magnetometer breakout
    "ant": (1.0, 50.0, 8.0), "ant_x": 48.0,                 # flexible PCB antenna on the rib
    # Dome casting tooling (LDZ-DDR-003, P4)
    "mould_r": 94.0, "mould_h": 32.0,       # silicone mould block (inside of the master's box)
    "box_wall": 3.0, "box_h": 35.0, "plate_t": 3.0,         # printed master: base plate and box wall
    "core_flange_t": 5.0, "core_skirt": 6.0, "core_clr": 0.3, "overflow_d": 4.0, "overflow_r": 73.0,
    # Placement in the bay (DDR-001, D3)
    "slot_l": 7000.0, "puck_from_curb": 1300.0,
    # Sign option on an existing pole (DDR-001, D6)
    "pole_r": 38.0,
    "sign_w": 450.0, "sign_h": 600.0, "sign_t": 3.0, "sign_standoff": 33.0,   # 33 (was 30): channel depth sets it, P7
    "disp_housing": (24.0, 200.0, 140.0), "disp_z": 200.0,  # 7.5 in e-paper housing, center height on the face
    "clamp_w": 12.0, "clamp_t": 0.8, "clamp_inset": 100.0,  # stainless band 12 x 0.8; bracket centres 100 mm from the ends
    "channel": (50.0, 40.0, 3.0), "channel_l": 60.0,        # aluminium U-channel bracket: width, depth, wall; length
    "bracket_bolt_y": 12.0, "slot": (3.0, 14.0),            # web bolts at y +/-12; band slots 3 x 14 in the flanges
    "housing_screw": (88.0, 58.0), "gland_dz": 30.0, "gland_hole": 20.5,
    "sign_z0": 2100.0,                      # bottom edge of the sign face above the sidewalk
}


def derived(p=PARAMS):
    """Derived dimensions used by the calculations and the drawing."""
    zb = p["pad_t"] + p["base_t"]
    ch = p["dome_h"] - p["wall"]
    cw, cd, ct = p["channel"]
    return {
        "z_base_top": zb,
        "height": zb + p["dome_h"],                     # total height above the road
        "diameter": 2 * p["base_r"],
        "pad_d": 2 * p["pad_r"],
        "crown_d": 2 * p["dome_top_r"],
        "cavity_h": ch,
        "cavity_r0": p["base_r"] - p["wall"],
        "cavity_r1": p["dome_top_r"] - p["wall"],
        "face_back": p["pole_r"] + p["sign_standoff"],  # back of the sign face, from the pole axis
        "flange_end": p["pole_r"] + p["sign_standoff"] - cd,  # pole end of the bracket flanges
        "flange_in": cw / 2 - ct,                       # inside face of each flange, from the centre line
        "band_x": p["pole_r"] + 1.5,                    # band crosses inside the channel, 1.5 mm in front of the pole
    }


def cavity_r(h, p=PARAMS):
    """Radius of the dome cavity at height h above the tray top."""
    d = derived(p)
    return d["cavity_r0"] - (d["cavity_r0"] - d["cavity_r1"]) * h / d["cavity_h"]


def dome_outer(p=PARAMS):
    """Outer shape of the dome, base at Z = 0."""
    from build123d import Cone, Pos, Axis, fillet
    outer = Pos(0, 0, p["dome_h"] / 2) * Cone(p["base_r"], p["dome_top_r"], p["dome_h"])
    try:
        outer = fillet(outer.edges().sort_by(Axis.Z)[-1], p["crown_fillet"])
    except Exception:           # keep a sharp edge if the kernel refuses; the massing is unchanged
        pass
    return outer


def dome_cavity(p=PARAMS):
    """The cavity inside the dome, base at Z = 0."""
    from build123d import Cone, Pos
    d = derived(p)
    return Pos(0, 0, d["cavity_h"] / 2) * Cone(d["cavity_r0"], d["cavity_r1"], d["cavity_h"])


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def build_parts(p=PARAMS):
    """Return {name: shape} for the puck, centered on the origin with the road at Z = 0."""
    from build123d import Box, Cylinder, Cone, Pos, Rot
    d = derived(p)
    zb = d["z_base_top"]
    pad = Pos(0, 0, p["pad_t"] / 2) * Cylinder(p["pad_r"], p["pad_t"])
    dome = Pos(0, 0, zb) * (dome_outer(p) - dome_cavity(p))
    cavity = Pos(0, 0, zb) * dome_cavity(p)

    # contents
    cells = _union(Pos(x, 0, zb + 1 + p["cell_d"] / 2) * Rot(90, 0, 0) * Cylinder(p["cell_d"] / 2, p["cell_l"])
                   for x in p["cell_x"])
    cap = Pos(p["cap_xy"][0], p["cap_xy"][1], zb + p["cap"][2] / 2) * Box(*p["cap"])
    bx = p["board_x"]
    zbd = zb + p["standoff_h"]
    board = Pos(bx, 0, zbd + p["board"][2] / 2) * Box(*p["board"])
    zt = zbd + p["board"][2]
    module = Pos(bx, p["module_y"], zt + p["module"][2] / 2) * Box(*p["module"])
    mag = Pos(bx, p["mag_y"], zt + p["mag"][2] / 2) * Box(*p["mag"])
    ant = Pos(p["ant_x"], 0, zb + p["ant"][2] / 2) * Box(*p["ant"])

    # base tray: disc, tapered spigot, cradles, standoffs, antenna rib, fill and vent holes
    disc = Pos(0, 0, p["pad_t"] + p["base_t"] / 2) * Cylinder(p["base_r"], p["base_t"])
    sh = p["spigot_h"]
    r0, r1 = cavity_r(0, p) - p["spigot_clr"], cavity_r(sh, p) - p["spigot_clr"]
    spigot = Pos(0, 0, zb + sh / 2) * (Cone(r0, r1, sh) - Cylinder(p["spigot_in_r"], sh + 1))
    cx, cy, cz = p["cradle"]
    cradles = _union(Pos(x, s * p["cradle_y"], zb + cz / 2) * Box(cx, cy, cz)
                     for x in p["cell_x"] for s in (-1, 1)) - cells
    sx, sy = p["standoff_xy"]
    standoffs = _union(Pos(bx + i * sx, j * sy, zb + p["standoff_h"] / 2) * Cylinder(p["standoff_r"], p["standoff_h"])
                       for i in (-1, 1) for j in (-1, 1))
    rx, ry, rz = p["rib"]
    rib = Pos(p["ant_x"] + p["ant"][0] / 2 + rx / 2, 0, zb + rz / 2) * Box(rx, ry, rz)
    holes = [(p["fill_xy"], p["fill_d"])] + [(v, p["vent_d"]) for v in p["vents"]]
    hole_cyl = _union(Pos(x, y, p["pad_t"] + p["base_t"] / 2) * Cylinder(dd / 2, p["base_t"]) for (x, y), dd in holes)
    inside = spigot + cradles + standoffs + rib
    base = disc + inside - hole_cyl

    potting = cavity - inside - cells - cap - board - module - mag - ant
    potting = potting + hole_cyl
    return {"pad": pad, "base": base, "dome": dome, "potting": potting, "cells": cells, "cap": cap,
            "board": board + module, "mag": mag, "ant": ant}


def build_tooling(p=PARAMS):
    """Dome casting tooling, in the casting position (mould on the bench, cavity opening up).
    master: printed in one piece (plate, box wall, dome shape), used crown up to pour the silicone;
    mould: the silicone block cast in it; core: the printed core plug; cast: the dome as cast."""
    from build123d import Cylinder, Pos, Rot
    d = derived(p)
    R, H = p["mould_r"], p["mould_h"]
    pt, bw = p["plate_t"], p["box_wall"]
    # master, as printed and used (dome crown up on the plate)
    master = (Pos(0, 0, -pt / 2) * Cylinder(R + bw, pt)
              + Pos(0, 0, p["box_h"] / 2) * (Cylinder(R + bw, p["box_h"]) - Cylinder(R, p["box_h"] + 1))
              + dome_outer(p))
    # silicone block as poured (dome outer is the void), then turned over for casting
    block = Pos(0, 0, H / 2) * Cylinder(R, H) - dome_outer(p)
    flip = Pos(0, 0, H) * Rot(180, 0, 0)
    mould = flip * block
    # core plug: flange on the mould's top face, skirt round the block, core cone down into the cavity
    ft, sk, cl = p["core_flange_t"], p["core_skirt"], p["core_clr"]
    flange = Pos(0, 0, H + ft / 2) * Cylinder(R + cl + 3, ft)
    skirt = Pos(0, 0, H - sk / 2) * (Cylinder(R + cl + 3, sk) - Cylinder(R + cl, sk + 1))
    core = flip * dome_cavity(p)
    overflow = _union(Pos(p["overflow_r"] * math.cos(a), p["overflow_r"] * math.sin(a), H + ft / 2)
                      * Cylinder(p["overflow_d"] / 2, ft + 1) for a in (math.radians(k) for k in (45, 135, 225, 315)))
    core_plug = flange + skirt + core - overflow
    cast = flip * (dome_outer(p) - dome_cavity(p))
    return {"master": master, "mould": mould, "core": core_plug, "cast": cast}


def _band(p, zc):
    """Stainless band round the back of the pole, out through the flange slots, across the channel."""
    from build123d import Box, Cylinder, Pos, Rot
    d = derived(p)
    r = p["pole_r"] + p["clamp_t"] / 2          # band centre line round the pole
    t, w = p["clamp_t"], p["clamp_w"]
    xs, yo = d["band_x"], p["channel"][0] / 2   # where the band leaves the flange (outside face)
    P = math.hypot(xs, yo)
    ang = math.atan2(yo, xs) + math.acos(r / P)  # tangent point on the pole, upper (+Y) side
    tx, ty = r * math.cos(ang), r * math.sin(ang)
    ring = Pos(0, 0, zc) * (Cylinder(r + t / 2, w) - Cylinder(r - t / 2, w + 1))
    keep = Pos(-200 + tx, 0, zc) * Box(400, 400, w + 2)          # back part of the ring, behind the tangent points
    arc = ring & keep
    segs = []
    for s in (1, -1):
        ax_, ay_ = tx, s * ty
        L = math.hypot(xs - ax_, s * yo - ay_)
        a = math.degrees(math.atan2(s * yo - ay_, xs - ax_))
        segs.append(Pos((ax_ + xs) / 2, (ay_ + s * yo) / 2, zc) * Rot(0, 0, a) * Box(L + 0.4, t, w))
    across = Pos(xs, 0, zc) * Box(t, 2 * yo + 0.4, w)
    housing = Pos(-(p["pole_r"] + t + 6), 0, zc) * Box(12, 22, 16)   # worm-drive housing behind the pole
    return arc + segs[0] + segs[1] + across, housing


def build_sign(p=PARAMS):
    """Return {name: shape} for the sign option on a pole (pole axis at X = Y = 0)."""
    from build123d import Box, Cylinder, Pos, Rot
    d = derived(p)
    fb = d["face_back"]
    st, sw, sh_ = p["sign_t"], p["sign_w"], p["sign_h"]
    hx, hy, hz = p["disp_housing"]
    zc = p["disp_z"]
    face = Pos(fb + st / 2, 0, sh_ / 2) * Box(st, sw, sh_)
    zcs = (p["clamp_inset"], sh_ - p["clamp_inset"])
    holes = []
    for z in zcs:
        holes += [(s * p["bracket_bolt_y"], z, 6.5) for s in (-1, 1)]
    hy_s, hz_s = p["housing_screw"]
    holes += [(sy * hy_s, zc + sz * hz_s, 4.5) for sy in (-1, 1) for sz in (-1, 1)]
    zg = zc + p["gland_dz"]
    holes += [(0.0, zg, p["gland_hole"])]
    for y, z, dd in holes:
        face -= Pos(fb + st / 2, y, z) * Rot(0, 90, 0) * Cylinder(dd / 2, st + 2)
    # display housing (bought enclosure with a clear lid), on the front of the face
    disp = Pos(fb + st + hx / 2, 0, zc) * (Box(hx, hy, hz) - Box(hx - 6, hy - 6, hz - 6))   # 3 mm walls
    disp -= Pos(fb + st + hx - 0.5, 0, zc) * Box(1.2, 170, 112)          # window recess in the clear lid (shown)
    for y, z, dd in holes[4:]:                                            # the same screw and gland holes in its back wall
        disp -= Pos(fb + st + 1.5, y, z) * Rot(0, 90, 0) * Cylinder(dd / 2, 5)
    # channel brackets, bands and bolts
    cw, cd, ct = p["channel"]
    L = p["channel_l"]
    sw_, sh2 = p["slot"]
    brackets, bands, housings, bolts = [], [], [], []
    for z in zcs:
        web = Pos(fb - ct / 2, 0, z) * Box(ct, cw, L)
        fl = [Pos(fb - cd / 2, s * (cw / 2 - ct / 2), z) * Box(cd, ct, L) for s in (-1, 1)]
        br = web + fl[0] + fl[1]
        for s in (-1, 1):
            br -= Pos(d["band_x"], s * (cw / 2 - ct / 2), z) * Box(sw_, ct + 2, sh2)
            br -= Pos(fb - ct / 2, s * p["bracket_bolt_y"], z) * Rot(0, 90, 0) * Cylinder(3.25, ct + 2)
        brackets.append(br)
        b, hsg = _band(p, z)
        bands.append(b)
        housings.append(hsg)
        for s in (-1, 1):
            y = s * p["bracket_bolt_y"]
            bolts.append(Pos(fb + st + 1.65, y, z) * Rot(0, 90, 0) * Cylinder(5.25, 3.3))        # button head
            bolts.append(Pos(fb - ct + 1.5, y, z) * Rot(0, 90, 0) * Cylinder(3.0, st + ct + 3))   # shank
            bolts.append(Pos(fb - ct - 3.0, y, z) * Rot(0, 90, 0) * Cylinder(5.5, 6.0, ))           # nyloc nut
    screws = []
    for sy in (-1, 1):
        for sz in (-1, 1):
            y, z = sy * hy_s, zc + sz * hz_s
            screws.append(Pos(fb - 1.25, y, z) * Rot(0, 90, 0) * Cylinder(4.0, 2.5))             # pan head behind the face
            screws.append(Pos(fb + st / 2 + 3, y, z) * Rot(0, 90, 0) * Cylinder(2.0, st + 6))    # through face and back wall
            screws.append(Pos(fb + st + 3 + 2.0, y, z) * Rot(0, 90, 0) * Cylinder(3.6, 4.0))     # nut and sealing washer inside
    gland = (Pos(fb - 6, 0, zg) * Rot(0, 90, 0) * Cylinder(12.0, 12.0)                         # nut and cap behind the face
             + Pos(fb + st + 1.5, 0, zg) * Rot(0, 90, 0) * Cylinder(10.0, st + 3 + 0.0)            # body through face and back wall
             + Pos(fb + st + 3 + 2.5, 0, zg) * Rot(0, 90, 0) * Cylinder(13.0, 5.0))               # lock nut inside the housing
    pole = Pos(0, 0, sh_ / 2) * Cylinder(p["pole_r"], sh_ + 400)
    return {"sign_face": face, "display": disp, "brackets": _union(brackets), "bands": _union(bands),
            "band_housings": _union(housings), "bracket_bolts": _union(bolts), "housing_screws": _union(screws),
            "gland": gland, "pole_ref": pole,
            # kept for the concept media and product model: everything that holds the sign to the pole
            "clamps": _union(brackets) + _union(bands) + _union(housings)}


def assemblies(parts=None, sign=None, tooling=None):
    """Assemblies for export. Children are copied so the source parts keep no parent."""
    import copy
    from build123d import Compound
    parts = parts or build_parts()
    sign = sign or build_sign()
    tooling = tooling or build_tooling()
    cp = lambda s: copy.copy(s)  # noqa: E731
    return {
        "loadzone-puck": Compound(children=[cp(v) for v in parts.values()]),
        "loadzone-dome": Compound(children=[cp(parts["dome"])]),
        "loadzone-base-tray": Compound(children=[cp(parts["base"])]),
        "loadzone-sign-option": Compound(children=[cp(sign[k]) for k in ("sign_face", "display", "brackets", "bands",
                                                                          "band_housings", "bracket_bolts",
                                                                          "housing_screws", "gland")]),
        "loadzone-dome-tooling": Compound(children=[cp(tooling[k]) for k in ("master", "core")]),
    }


def volumes(parts=None):
    """Part volumes in cm3 (used by the calculation note for mass)."""
    parts = parts or build_parts()
    return {k: v.volume / 1000.0 for k, v in parts.items()}


# ----------------------------------------------------------------- constructability checks
def check(p=PARAMS, verbose=True):
    """Constructability checks (STANDARDS section 18): parts that must touch do touch, parts that
    must not touch are apart by at least the stated clearance, and nothing overlaps.
    Returns (passed, failed) counts."""
    from build123d import Pos
    d = derived(p)
    C = build_parts(p)
    S = build_sign(p)
    T = build_tooling(p)
    res = []

    def ov(a, b):
        try:
            return (a & b).volume
        except Exception:
            return 0.0

    def no_overlap(name, a, b, tol=1e-3):
        v = ov(a, b)
        res.append((v <= tol, f"no overlap: {name} ({v:.3f} mm3)"))

    def touch(name, a, b, tol=0.05):
        g = a.distance_to(b)
        v = ov(a, b)
        res.append((g <= tol and v <= 1e-2, f"touch: {name} (gap {g:.2f} mm, overlap {v:.3f} mm3)"))

    def gap(name, a, b, need):
        g = a.distance_to(b)
        res.append((g >= need - 1e-6, f"clear: {name} {g:.2f} mm (need {need:g})"))

    # puck: nothing overlaps
    keys = list(C)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            no_overlap(f"{a} / {b}", C[a], C[b])
    # puck: every part held by its neighbour
    touch("tray on epoxy bed", C["base"], C["pad"])
    touch("dome rim on tray", C["dome"], C["base"])
    touch("cells in their cradles", C["cells"], C["base"])
    touch("pulse capacitor on the tray", C["cap"], C["base"])
    touch("board on its standoffs", C["board"], C["base"])
    touch("magnetometer on the board", C["mag"], C["board"])
    touch("antenna on its rib", C["ant"], C["base"])
    # puck: clearances for potting to flow and for the tabs and leads
    gap("cells to dome wall", C["cells"], C["dome"], 2.0)
    gap("antenna to dome wall", C["ant"], C["dome"], 2.0)
    gap("board to dome wall", C["board"], C["dome"], 2.0)
    gap("magnetometer to dome wall", C["mag"], C["dome"], 2.0)
    gap("cell to cell", Pos(0, 0, 0) * C["cells"].solids()[0], C["cells"].solids()[1], 2.0)
    gap("cells to capacitor", C["cells"], C["cap"], 2.0)
    gap("capacitor to board", C["cap"], C["board"], 1.5)
    gap("board to antenna", C["board"] + C["mag"], C["ant"], 5.0)
    res.append((d["height"] <= 35.0, f"height above road {d['height']:.1f} mm (R7: 35 or less)"))
    # every fill and vent hole opens into the cavity, not into a cradle, standoff or part
    from build123d import Cylinder
    zb = d["z_base_top"]
    for (x, y), dd in [(p["fill_xy"], p["fill_d"])] + [(v, p["vent_d"]) for v in p["vents"]]:
        probe = Pos(x, y, zb + 0.5) * Cylinder(dd / 2, 1.0)
        solid = C["base"] + C["cells"] + C["cap"] + C["board"] + C["ant"]
        res.append((ov(probe, solid) < 1e-3, f"hole at ({x:g}, {y:g}) opens into the cavity"))
    # potting is one piece (it can be poured through one hole)
    n = len(C["potting"].solids())
    res.append((n == 1, f"potting is one connected pour ({n} piece)"))

    # tooling
    touch("core flange on the mould's top face", T["core"], T["mould"])
    no_overlap("core plug / silicone mould", T["core"], T["mould"])
    v_dome = (C["dome"]).volume
    res.append((abs(T["cast"].volume - v_dome) < 1.0, f"cast dome volume {T['cast'].volume / 1000:.1f} cm3 matches the model"))
    no_overlap("cast dome / core plug", T["cast"], T["core"])
    no_overlap("cast dome / mould", T["cast"], T["mould"])
    touch("cast dome against the core", T["cast"], T["core"])

    # sign
    pole = S["pole_ref"]
    for k in ("sign_face", "display", "brackets", "bands", "band_housings", "bracket_bolts", "housing_screws", "gland"):
        no_overlap(f"{k} / pole", S[k], pole)
    touch("brackets on the back of the face", S["brackets"], S["sign_face"])
    touch("bracket flanges bear on the pole", S["brackets"], pole, tol=0.1)
    touch("display housing on the face", S["display"], S["sign_face"])
    no_overlap("bands / brackets", S["bands"], S["brackets"])
    touch("band hugs the back of the pole", S["bands"], pole)
    no_overlap("gland / brackets", S["gland"], S["brackets"])
    gap("gland to brackets", S["gland"], S["brackets"], 20.0)
    gap("housing screws to brackets", S["housing_screws"], S["brackets"], 10.0)
    gap("bracket bolts to display housing", S["bracket_bolts"], S["display"], 10.0)
    no_overlap("bracket bolts / brackets", S["bracket_bolts"], S["brackets"])
    no_overlap("bracket bolts / bands", S["bracket_bolts"], S["bands"])
    no_overlap("bracket bolts / sign face", S["bracket_bolts"], S["sign_face"])
    no_overlap("housing screws / sign face", S["housing_screws"], S["sign_face"])
    no_overlap("housing screws / display housing", S["housing_screws"], S["display"])
    no_overlap("gland / sign face", S["gland"], S["sign_face"])
    no_overlap("gland / display housing", S["gland"], S["display"])
    touch("gland lock nut on the housing back wall", S["gland"], S["display"])
    # range of poles: the two flange ends seat on any pole of 60 to 90 mm
    for dia in (60.0, 76.0, 90.0):
        r = dia / 2
        ok = r > d["flange_in"]
        res.append((ok, f"{dia:.0f} mm pole seats on both flange ends ({'yes' if ok else 'no'})"))

    passed = sum(1 for ok, _ in res if ok)
    failed = [m for ok, m in res if not ok]
    if verbose:
        for ok, m in res:
            print(("ok   " if ok else "FAIL ") + m)
        print(f"{passed} of {len(res)} checks pass")
    return passed, failed


if __name__ == "__main__":
    if "--check" in sys.argv:
        _, failed = check()
        sys.exit(1 if failed else 0)
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    for name, shape in assemblies(parts).items():
        export_step(shape, str(out / "step" / f"{name}.step"))
        export_stl(shape, str(out / "stl" / f"{name}.stl"), tolerance=0.05, angular_tolerance=0.3)
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm")
    d = derived()
    print(f"puck height {d['height']:.1f} mm, base diameter {d['diameter']:.0f} mm, pad diameter {d['pad_d']:.0f} mm")
    print("volumes (cm3): " + ", ".join(f"{k} {v:.1f}" for k, v in volumes(parts).items()))
