"""LoadZone parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl, and prints the main envelopes and volumes.

Massing-plus detail: correct interfaces (road bond pad, base, dome, potting, cells, radio
board, magnetometer, antenna; sign face, display housing and band clamps on a pole) and main
dimensions; not fabrication detail.

Puck axes: origin at the center of the puck on the road surface, Z up, X along the curb,
Y across the street. Sign axes: origin on the pole axis at the bottom edge of the sign face,
Z up, the sign face toward +X. Units mm.
"""
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Puck (LDZ-PRC-001 v0.4, R7): surface-bonded cast polyurethane dome over potted electronics
    "pad_r": 85.0, "pad_t": 3.0,            # two-part road-marker epoxy bed (LDZ-DDR-002)
    "base_r": 75.0, "base_t": 6.0,          # flat base disc (150 mm diameter)
    "dome_h": 22.0, "dome_top_r": 52.0,     # frustum dome above the base
    "wall": 4.0,                            # cast dome wall; the cavity is fully potted
    "crown_fillet": 6.0,                    # rounded top edge (R7)
    # Contents
    "cell_d": 14.5, "cell_l": 50.5,         # AA-size Li-SOCl2 bobbin cell (ER14505 class)
    "cell_x": (-40.0, -23.0),               # two cells lying along Y on the -X side
    "cap": (10.0, 10.0, 12.0), "cap_xy": (-8.0, -15.0),     # pulse capacitor envelope
    "board": (36.0, 56.0, 1.6), "board_x": 20.0,            # carrier board
    "module": (13.0, 16.0, 3.0), "module_y": -12.0,         # STM32WL-class LoRaWAN module
    "mag": (22.0, 18.0, 3.0), "mag_y": 14.0,                # magnetometer breakout
    "ant": (1.0, 50.0, 8.0), "ant_x": 50.0,                 # flexible PCB antenna at the dome edge
    # Placement in the bay (DDR-001, D3)
    "slot_l": 7000.0, "puck_from_curb": 1300.0,
    # Sign option on an existing pole (DDR-001, D6)
    "pole_r": 38.0,
    "sign_w": 450.0, "sign_h": 600.0, "sign_t": 3.0, "sign_standoff": 30.0,
    "disp_housing": (24.0, 200.0, 140.0), "disp_z": 200.0,  # 7.5 in e-paper housing, center height on the face
    "clamp_w": 25.0, "clamp_t": 5.0, "clamp_inset": 120.0,
    "sign_z0": 2100.0,                      # bottom edge of the sign face above the sidewalk
}


def derived(p=PARAMS):
    """Derived dimensions used by the calculations and the drawing."""
    zb = p["pad_t"] + p["base_t"]
    return {
        "z_base_top": zb,
        "height": zb + p["dome_h"],                     # total height above the road
        "diameter": 2 * p["base_r"],
        "pad_d": 2 * p["pad_r"],
        "crown_d": 2 * p["dome_top_r"],
        "cavity_h": p["dome_h"] - p["wall"],
    }


def build_parts(p=PARAMS):
    """Return {name: shape} for the puck, centered on the origin with the road at Z = 0."""
    from build123d import Box, Cylinder, Cone, Pos, Rot, Axis, fillet
    d = derived(p)
    zb = d["z_base_top"]
    pad = Pos(0, 0, p["pad_t"] / 2) * Cylinder(p["pad_r"], p["pad_t"])
    base = Pos(0, 0, p["pad_t"] + p["base_t"] / 2) * Cylinder(p["base_r"], p["base_t"])
    outer = Pos(0, 0, zb + p["dome_h"] / 2) * Cone(p["base_r"], p["dome_top_r"], p["dome_h"])
    try:
        top_edge = outer.edges().sort_by(Axis.Z)[-1]
        outer = fillet(top_edge, p["crown_fillet"])
    except Exception:           # keep a sharp edge if the kernel refuses; the massing is unchanged
        pass
    ch = d["cavity_h"]
    cavity = Pos(0, 0, zb + ch / 2) * Cone(p["base_r"] - p["wall"], p["dome_top_r"] - p["wall"], ch)
    dome = outer - cavity

    cells = None
    for x in p["cell_x"]:
        c = Pos(x, 0, zb + 1 + p["cell_d"] / 2) * Rot(90, 0, 0) * Cylinder(p["cell_d"] / 2, p["cell_l"])
        cells = c if cells is None else cells + c
    cap = Pos(p["cap_xy"][0], p["cap_xy"][1], zb + 1 + p["cap"][2] / 2) * Box(*p["cap"])
    bx = p["board_x"]
    board = Pos(bx, 0, zb + 3 + p["board"][2] / 2) * Box(*p["board"])
    zt = zb + 3 + p["board"][2]
    module = Pos(bx, p["module_y"], zt + p["module"][2] / 2) * Box(*p["module"])
    mag = Pos(bx, p["mag_y"], zt + p["mag"][2] / 2) * Box(*p["mag"])
    ant = Pos(p["ant_x"], 0, zb + 1 + p["ant"][2] / 2) * Box(*p["ant"])
    potting = cavity - cells - cap - board - module - mag - ant
    return {"pad": pad, "base": base, "dome": dome, "potting": potting, "cells": cells, "cap": cap,
            "board": board + module, "mag": mag, "ant": ant}


def build_sign(p=PARAMS):
    """Return {name: shape} for the sign option on a pole (pole axis at X = Y = 0)."""
    from build123d import Box, Cylinder, Pos
    face_x = p["pole_r"] + p["sign_standoff"]
    z0 = 0.0
    face = Pos(face_x + p["sign_t"] / 2, 0, z0 + p["sign_h"] / 2) * Box(p["sign_t"], p["sign_w"], p["sign_h"])
    hx, hy, hz = p["disp_housing"]
    disp = Pos(face_x + p["sign_t"] + hx / 2, 0, z0 + p["disp_z"]) * Box(hx, hy, hz)
    clamps = None
    for zc in (z0 + p["clamp_inset"], z0 + p["sign_h"] - p["clamp_inset"]):
        ring = Pos(0, 0, zc) * (Cylinder(p["pole_r"] + p["clamp_t"], p["clamp_w"]) - Cylinder(p["pole_r"], p["clamp_w"] + 2))
        arm = Pos((p["pole_r"] + face_x) / 2, 0, zc) * Box(face_x - p["pole_r"] + 4, 40, p["clamp_w"])
        c = ring + arm
        clamps = c if clamps is None else clamps + c
    pole = Pos(0, 0, p["sign_h"] / 2) * Cylinder(p["pole_r"], p["sign_h"] + 400)
    return {"sign_face": face, "display": disp, "clamps": clamps, "pole_ref": pole}


def assemblies(parts=None, sign=None):
    """Assemblies for export. Children are copied so the source parts keep no parent."""
    import copy
    from build123d import Compound
    parts = parts or build_parts()
    sign = sign or build_sign()
    cp = lambda s: copy.copy(s)
    return {
        "loadzone-puck": Compound(children=[cp(v) for v in parts.values()]),
        "loadzone-dome": Compound(children=[cp(parts["dome"])]),
        "loadzone-sign-option": Compound(children=[cp(sign[k]) for k in ("sign_face", "display", "clamps")]),
    }


def volumes(parts=None):
    """Part volumes in cm3 (used by the calculation note for mass)."""
    parts = parts or build_parts()
    return {k: v.volume / 1000.0 for k, v in parts.items()}


if __name__ == "__main__":
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    for name, shape in assemblies(parts).items():
        export_step(shape, str(out / "step" / f"{name}.step"))
        export_stl(shape, str(out / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm")
    d = derived()
    print(f"puck height {d['height']:.1f} mm, base diameter {d['diameter']:.0f} mm, pad diameter {d['pad_d']:.0f} mm")
    print("volumes (cm3): " + ", ".join(f"{k} {v:.1f}" for k, v in volumes(parts).items()))
