"""LoadZone product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders. The bay sensor puck gets a filleted cast dome with a
mold parting line, radial anti-skid grooves and a recessed crown badge, a dark base disc, the
epoxy bed with a squeezed-out bead, and dressed internals (cells, pulse capacitor, radio carrier
with shielded module, magnetometer breakout, flexible antenna, clear potting). The sign option gets
a painted face with a raised legend, a display housing with a polycarbonate window over the
e-paper panel, aluminium channel brackets with stainless worm-drive band clamps, button-head bolts and a cable gland.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS and derived() in model.py.
Axes as model.py: origin at the center of the puck on the road surface, Z up, X along the curb
(traffic approaches from +X), Y across the street (curb at +Y). Units mm.

Render layout (not the installed layout): the kerb is drawn 500 mm from the puck (installed
1.3 m, PARAMS["puck_from_curb"]) and the sign is drawn with its lower edge 300 mm above the
sidewalk (installed 2.1 m, PARAMS["sign_z0"]), so the puck and the sign read in one frame.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from math import atan2, degrees
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build123d import (Align, Axis, Box, Cone, Cylinder, Plane, Pos, RectangleRounded, Rot,
                       RegularPolygon, Text, extrude, fillet)
from model import PARAMS, derived, build_parts, build_sign

TITLE = "LoadZone: loading bay occupancy sensor puck and driver sign"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 28, "az": -40,
     "note": "Product render from the road side, front right and above (about 28 deg elevation); sensor puck bonded "
             "in the bay beside the white bay line, e-paper sign on the street pole behind the kerb. Kerb and "
             "sign are drawn closer and lower than installed"},
    {"name": "exploded", "groups": ["shell", "internal"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): cast dome, clear potting, "
             "magnetometer, radio board and antenna, cells and pulse capacitor, base disc and road epoxy bed"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 22, "az": -40,
     "note": "Detail of the puck alone from the front right and slightly above (about 22 deg elevation), "
             "without context: mold line, anti-skid grooves and crown badge"},
]

# Render layout (see the module docstring)
KERB_Y = 400.0            # kerb face, drawn closer than the installed 1.3 m
KERB_T = 150.0            # kerb width across Y
CURB_H = 150.0            # sidewalk top above the road
POLE_X, POLE_Y = 120.0, KERB_Y + KERB_T + 150.0
SIGN_DRAWN_Z0 = CURB_H + 250.0   # lower edge of the sign face as drawn (installed 2.1 m above the sidewalk)
ROAD_X = (-480.0, 620.0)
ROAD_Y0 = -400.0
SIDE_Y1 = POLE_Y + 200.0
SLAB_T = 60.0             # context slab thickness below the road surface

# Colours (restrained product palette; kit accent)
C_DOME = "#E3B21B"        # high-visibility yellow, cast polyurethane
C_BASE = "#3D434B"
C_EPOXY = "#26282C"
C_BADGE = "#2B2F36"
C_ACCENT = "#0F766E"
C_POTTING = "#D9B26A"
C_PCB = "#1A1D21"
C_PCB_MAG = "#1E3A8A"
C_SHIELD = "#B8BEC6"
C_CHIP = "#111827"
C_CELL = "#7A1F1F"
C_METAL = "#C3C8CE"
C_ALU = "#AEB4BC"        # aluminium channel brackets (brushed)
C_CAP = "#1F2937"
C_FLEX = "#B45309"
C_COPPER = "#D08A3C"
C_SIGN = "#F2F3F1"
C_LEGEND = "#1B1E23"
C_HOUSING = "#3A3F47"
C_EPAPER = "#E4E2DB"
C_POLY = "#DCEBF5"
C_ASPHALT = "#62666C"
C_KERB = "#B9BBB7"
C_PAVING = "#D3D2CD"
C_LINE = "#F4F4F2"
C_POLE = "#A9AFB5"

FONT = str(HERE.parents[1] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf")


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _top_edges(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom_edges(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _rad(e):
    """Edge radius, or 0 for an edge that is not a circle."""
    try:
        return e.radius
    except Exception:
        return 0.0


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _text(txt, size, plane, h=0.5):
    """Raised text on `plane` (x_dir reads left to right, z_dir out of the surface)."""
    try:
        t = Text(txt, font_size=size, font_path=FONT, align=(Align.CENTER, Align.CENTER))
    except Exception:
        t = Text(txt, font_size=size, align=(Align.CENTER, Align.CENTER))
    return extrude(plane * t, amount=h)


def _plate(w, h, r, plane, t):
    """Rounded rectangle w x h on `plane`, extruded by t along its normal."""
    r = max(min(r, min(w, h) / 2 - 0.01), 0.01)
    return extrude(plane * RectangleRounded(w, h, r), amount=t)


# ------------------------------------------------------------------ puck
def _puck(P, D, m, add):
    zb = D["z_base_top"]
    H = D["height"]
    R, Rt, dh = P["base_r"], P["dome_top_r"], P["dome_h"]

    # road-marker epoxy bed (BOM 7): the disc of model.py with a squeezed-out bead at its edge
    pad = m["pad"]
    pad = _fillet_try(pad, [e for e in _top_edges(pad) if _rad(e) > R + 1], [1.4, 1.0, 0.6])
    add("Road-marker epoxy bed", pad, C_EPOXY, "rubber", 7, "shell", (0, 0, -40))

    # base disc (BOM 6): model.py disc with softened outer edges
    base = m["base"]
    base = _fillet_try(base, [e for e in base.edges() if _rad(e) > R - 0.5], [1.0, 0.6, 0.3])
    add("Puck base disc (ASA)", base, C_BASE, "plastic", 6, "shell", (0, 0, 0))

    # cast dome (BOM 1): model.py dome, softened foot, parting line, anti-skid grooves, crown badge recess
    dome = m["dome"]
    foot = [e for e in _bottom_edges(dome) if _rad(e) > R - 0.5]
    dome = _fillet_try(dome, foot, [1.2, 0.8, 0.4])
    slope = (R - Rt) / dh                                   # radius lost per mm of height
    zg = zb + 2.5
    rg = R - slope * 2.5
    dome -= Pos(0, 0, zg) * (Cylinder(R + 3, 0.6) - Cylinder(rg - 0.45, 0.8))   # mold parting line
    theta = degrees(atan2(dh, R - Rt))                      # flank angle from horizontal
    grooves = []
    for k in range(24):
        a = 360.0 * k / 24 + 7.5
        zc = zb + 11.0
        rc = R - slope * 11.0
        g = Rot(0, 0, a) * Pos(rc, 0, zc) * Rot(0, theta, 0) * Box(16.0, 2.2, 2.2)
        grooves.append(g)
    dome -= _union(grooves)
    dome -= Pos(0, 0, H - 0.4) * Cylinder(34.0, 1.2)        # crown badge recess, 0.8 deep below the top
    dome -= Pos(0, 0, H - 0.3) * (Cylinder(39.0, 1.0) - Cylinder(37.6, 1.2))   # accent ring groove
    add("Puck dome, cast polyurethane", dome, C_DOME, "plastic", 1, "shell", (0, 0, 150))

    ring = Pos(0, 0, H - 0.4) * (Cylinder(38.9, 0.8) - Cylinder(37.7, 1.0))
    add("Crown accent ring inlay", ring, C_ACCENT, "painted", 1, "shell", (0, 0, 150))
    zt = H - 1.0
    badge = _text("LOADZONE", 8.5, Plane(origin=(0, 3.0, zt), x_dir=(1, 0, 0), z_dir=(0, 0, 1)), h=0.6)
    badge += _text("BAY SENSOR", 4.2, Plane(origin=(0, -7.5, zt), x_dir=(1, 0, 0), z_dir=(0, 0, 1)), h=0.6)
    add("Crown badge lettering", badge, C_BADGE, "painted", 1, "shell", (0, 0, 150))

    # clear semi-rigid potting (BOM 6) filling the dome around the parts
    add("Potting, semi-rigid polyurethane (clear)", m["potting"], C_POTTING, "clear", 6, "internal", (0, 0, 100))

    # cells (BOM 5): two AA-size Li-SOCl2 cells lying along Y, with end caps; pulse capacitor
    cr, cl = P["cell_d"] / 2, P["cell_l"]
    zc = zb + 1 + cr
    endc = 0.8
    wraps, caps = [], []
    for x in P["cell_x"]:
        w = Pos(x, 0, zc) * Rot(90, 0, 0) * Cylinder(cr, cl - 2 * endc)
        wraps.append(_fillet_try(w, w.edges(), [0.6, 0.3]))
        for sy in (-1, 1):
            caps.append(Pos(x, sy * (cl / 2 - endc / 2), zc) * Rot(90, 0, 0) * Cylinder(cr - 0.8, endc))
    caps.append(Pos(P["cell_x"][0], cl / 2 - 0.2, zc) * Rot(90, 0, 0) * Cylinder(2.2, 0.4))   # + terminal button
    add("Li-SOCl2 cell wraps", _union(wraps), C_CELL, "painted", 5, "internal", (0, 0, 32))
    add("Cell end caps", _union(caps), C_METAL, "metal", 5, "internal", (0, 0, 32))
    cap = m["cap"]
    cap = _fillet_try(cap, cap.edges().filter_by(Axis.Z), [2.0, 1.0])
    cap = _fillet_try(cap, _top_edges(cap), [1.0, 0.5])
    add("Hybrid pulse capacitor", cap, C_CAP, "plastic", 5, "internal", (0, -10, 32))

    # carrier board and LoRaWAN module (BOM 3)
    bx = P["board_x"]
    bl, bw, bt = P["board"]
    zb0 = zb + P["standoff_h"]
    pcb = Pos(bx, 0, zb0) * extrude(RectangleRounded(bl, bw, 2.0), amount=bt)
    for (hx, hy) in ((bx - bl / 2 + 3, -bw / 2 + 3), (bx + bl / 2 - 3, -bw / 2 + 3),
                     (bx - bl / 2 + 3, bw / 2 - 3), (bx + bl / 2 - 3, bw / 2 - 3)):
        pcb -= Pos(hx, hy, zb0 + bt / 2) * Cylinder(1.1, bt + 1)
    add("Radio carrier board", pcb, C_PCB, "plastic", 3, "internal", (0, 0, 52))
    zt = zb0 + bt
    mx, my, mz = P["module"]
    mod = Pos(bx, P["module_y"], zt + mz / 2) * Box(mx, my, mz)
    mod = _fillet_try(mod, _top_edges(mod), [0.5, 0.3])
    add("LoRaWAN module shield can", mod, C_SHIELD, "metal", 3, "internal", (0, 0, 52))
    parts3 = Pos(bx - 8, P["module_y"] - 2, zt + 0.6) * Box(5.0, 5.0, 1.2)        # SPI flash
    parts3 += Pos(bx + 12.5, P["module_y"] - 4, zt + 0.6) * Box(3.0, 6.0, 1.2)     # regulator
    parts3 += Pos(bx - 12, -24.0, zt + 0.6) * Box(6.0, 3.0, 1.2)                   # diode pair
    add("Carrier board components", parts3, C_CHIP, "plastic", 3, "internal", (0, 0, 52))
    ufl = Pos(bx + 5.5, P["module_y"] + 9.5, zt + 0.6) * Cylinder(1.3, 1.2)
    add("u.FL antenna connector", ufl, C_METAL, "metal", 3, "internal", (0, 0, 52))

    # magnetometer breakout (BOM 2)
    gx, gy, gz = P["mag"]
    mag = Pos(bx, P["mag_y"], zt) * extrude(RectangleRounded(gx, gy, 1.5), amount=1.6)
    for sx in (-1, 1):
        mag -= Pos(bx + sx * (gx / 2 - 2.5), P["mag_y"] + gy / 2 - 2.5, zt + 0.8) * Cylinder(1.0, 3.0)
    add("Magnetometer breakout", mag, C_PCB_MAG, "plastic", 2, "internal", (0, 0, 70))
    chip = Pos(bx, P["mag_y"] - 1.0, zt + 1.6 + 0.4) * Box(2.0, 2.0, 0.8)
    chip += Pos(bx - 5, P["mag_y"] - 6.5, zt + 1.6 + 0.9) * Box(10.0, 2.4, 1.8)   # header strip
    add("Magnetometer IC and header", chip, C_CHIP, "plastic", 2, "internal", (0, 0, 70))

    # flexible PCB antenna (BOM 4) at the dome edge, with its trace pattern
    ax_, ay, az = P["ant"]
    z0 = zb
    ant = Pos(P["ant_x"], 0, z0 + az / 2) * Box(ax_ * 0.6, ay, az)
    ant = Pos(-0.2, 0, 0) * ant
    add("Flexible PCB antenna", ant, C_FLEX, "plastic", 4, "internal", (34, 0, 44))
    trace = Pos(P["ant_x"] + 0.2, 0, z0 + az / 2) * Box(0.3, ay - 6, 1.2)
    for yy in (-18.0, -6.0, 6.0, 18.0):
        trace += Pos(P["ant_x"] + 0.2, yy, z0 + az / 2) * Box(0.3, 1.2, az - 2.5)
    add("Antenna copper trace", trace, C_COPPER, "metal", 4, "internal", (34, 0, 44))


# ------------------------------------------------------------------ sign option
def _sign(P, add):
    face_x = P["pole_r"] + P["sign_standoff"]
    st, sw, sh = P["sign_t"], P["sign_w"], P["sign_h"]
    at = Pos(POLE_X, POLE_Y, SIGN_DRAWN_Z0)
    E = (130, 0, 0)

    # sign face (BOM 8): rounded aluminium composite panel, painted, raised legend
    face = Pos(face_x, 0, sh / 2) * extrude(Plane.YZ * RectangleRounded(sw, sh, 18.0), amount=st)
    add("Sign face, aluminium composite", at * face, C_SIGN, "painted", 8, "accessory", E)
    fx = face_x + st
    tp = lambda y, z: Plane(origin=(fx, y, z), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    border = _plate(sw - 24, sh - 24, 12.0, tp(0, sh / 2), 0.5) - _plate(sw - 36, sh - 36, 7.0, tp(0, sh / 2), 2.0)
    legend = _text("LOADING", 64, tp(0, 505), 0.6)
    legend += _text("ZONE", 64, tp(0, 425), 0.6)
    legend += _text("FREE BAYS", 22, tp(0, 322), 0.6)
    add("Sign legend and border", at * (border + legend), C_LEGEND, "painted", 8, "accessory", E)
    band = _plate(sw - 36, 26, 4.0, tp(0, 42), 0.5)
    add("Sign accent band", at * band, C_ACCENT, "painted", 8, "accessory", E)

    # e-paper display housing (BOM 9): filleted housing, polycarbonate window, e-paper panel and cable gland
    hx, hy, hz = P["disp_housing"]
    zc = P["disp_z"]
    hs = Pos(fx + hx / 2, 0, zc) * Box(hx, hy, hz)
    hs = _fillet_try(hs, hs.edges().filter_by(Axis.X), [8.0, 5.0, 3.0])
    hs = _fillet_try(hs, hs.faces().sort_by(Axis.X)[-1].edges(), [3.0, 2.0, 1.0])
    win_w, win_h = 172.0, 106.0
    hs -= extrude(Plane(origin=(fx + hx - 1.2, 0, zc), x_dir=(0, -1, 0), z_dir=(1, 0, 0))
                  * RectangleRounded(win_w + 6, win_h + 6, 5.0), amount=3.0)
    hs -= extrude(Plane(origin=(fx + hx - 6.0, 0, zc), x_dir=(0, -1, 0), z_dir=(1, 0, 0))
                  * RectangleRounded(win_w, win_h, 3.0), amount=8.0)
    add("Display housing", at * hs, C_HOUSING, "plastic", 9, "accessory", (E[0] + 60, 0, 0))
    wpl = Plane(origin=(fx + hx - 1.2, 0, zc), x_dir=(0, -1, 0), z_dir=(1, 0, 0))
    win = extrude(wpl * RectangleRounded(win_w + 5.6, win_h + 5.6, 4.8), amount=1.0)
    add("Polycarbonate display window", at * win, C_POLY, "clear", 9, "accessory", (E[0] + 110, 0, 0))
    epl = Plane(origin=(fx + hx - 6.0, 0, zc), x_dir=(0, -1, 0), z_dir=(1, 0, 0))
    panel = extrude(epl * RectangleRounded(win_w - 0.4, win_h - 0.4, 2.8), amount=1.2)
    add("E-paper panel, 7.5 in", at * panel, C_EPAPER, "paper", 9, "accessory", (E[0] + 85, 0, 0))
    gpl = lambda y, z: Plane(origin=(fx + hx - 4.8, y, z), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    ink = _text("2", 64, gpl(-36, zc + 2), 0.3)
    ink += _text("FREE", 24, gpl(26, zc + 14), 0.3)
    ink += _text("BAYS", 24, gpl(26, zc - 14), 0.3)
    arrow = extrude(gpl(12, zc - 38) * RegularPolygon(7.0, 3, rotation=180), amount=0.3)
    arrow += extrude(gpl(28, zc - 38) * RectangleRounded(24, 4, 1.0), amount=0.3)
    add("E-paper image (bay count)", at * (ink + arrow), C_LEGEND, "paper", 9, "accessory", (E[0] + 85, 0, 0))
    gland = Pos(fx + hx / 2, hy / 2 - 30, zc - hz / 2 - 5) * Cylinder(6.0, 10.0)
    gland += Pos(fx + hx / 2, hy / 2 - 30, zc - hz / 2 - 11) * Cylinder(3.2, 6.0)
    gland = _fillet_try(gland, _bottom_edges(gland), [1.0, 0.5])
    add("Cable gland", at * gland, C_CHIP, "rubber", 9, "accessory", (E[0] + 60, 0, 0))

    # pole brackets (BOM 10): aluminium channel bolted to the back of the face, worm-drive band clamp
    # round the pole through the flange slots; shapes come straight from model.build_sign
    sg = build_sign(P)
    br = sg["brackets"]
    br = _fillet_try(br, br.edges().filter_by(Axis.Z), [1.0, 0.5])
    add("Aluminium channel brackets", at * br, C_ALU, "metal", 10, "accessory", (-60, 0, 0))
    add("Stainless band clamps", at * (sg["bands"] + sg["band_housings"]), C_METAL, "metal", 10, "accessory", (-60, 0, 0))
    add("Button-head bolts and nyloc nuts", at * sg["bracket_bolts"], C_METAL, "metal", 10, "accessory", (-60, 0, 0))


# ------------------------------------------------------------------ context
def _context(P, add):
    x0, x1 = ROAD_X
    L = x1 - x0
    xc = (x0 + x1) / 2
    road = Pos(xc, (ROAD_Y0 + KERB_Y) / 2, -SLAB_T / 2) * Box(L, KERB_Y - ROAD_Y0, SLAB_T)
    add("Road surface (asphalt)", road, C_ASPHALT, "rubber", None, "context", (0, 0, 0))
    kerb = Pos(xc, KERB_Y + KERB_T / 2, (CURB_H - SLAB_T) / 2) * Box(L, KERB_T, CURB_H + SLAB_T)
    kerb = _fillet_try(kerb, [e for e in kerb.edges().filter_by(Axis.X)
                              if abs(e.center().Y - KERB_Y) < 1 and e.center().Z > CURB_H - 1], [18.0, 10.0])
    for xj in (x0 + L * 0.36, x0 + L * 0.8):
        kerb -= Pos(xj, KERB_Y + KERB_T / 2, CURB_H / 2) * Box(4.0, KERB_T + 40, CURB_H + 2 * SLAB_T)
    add("Kerb stone", kerb, C_KERB, "rubber", None, "context", (0, 0, 0))
    side_y0 = KERB_Y + KERB_T
    side = Pos(xc, (side_y0 + SIDE_Y1) / 2, (CURB_H - 10 - SLAB_T) / 2) * Box(L, SIDE_Y1 - side_y0, CURB_H - 10 + SLAB_T)
    for xj in (x0 + L * 0.2, x0 + L * 0.6):
        side -= Pos(xj, (side_y0 + SIDE_Y1) / 2, CURB_H - 10) * Box(4.0, SIDE_Y1 - side_y0 + 2, 4.0)
        add("Sidewalk paving", side, C_PAVING, "rubber", None, "context", (0, 0, 0))
    line = Pos(xc, -310.0, 0.75) * Box(L - 2, 100.0, 1.5)             # bay edge line (road side)
    line += Pos(x1 - 130, (-360.0 + KERB_Y) / 2, 0.75) * Box(100.0, KERB_Y + 360 - 2, 1.5)   # slot end line
    add("Bay marking, thermoplastic", line, C_LINE, "painted", None, "context", (0, 0, 0))
    ptop = SIGN_DRAWN_Z0 + P["sign_h"] + 140
    pole = Pos(POLE_X, POLE_Y, (CURB_H - 10 + ptop) / 2) * Cylinder(P["pole_r"], ptop - CURB_H + 10)
    pole += Pos(POLE_X, POLE_Y, ptop + 4) * Cylinder(P["pole_r"] + 2, 8)
    pole = _fillet_try(pole, _top_edges(pole), [4.0, 2.0])
    add("Street pole section (existing, not supplied)", pole, C_POLE, "metal", None, "context", (0, 0, 0))


def product_parts(P=PARAMS):
    D = derived(P)
    m = build_parts(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    _puck(P, D, m, add)
    _sign(P, add)
    _context(P, add)
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:45s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
