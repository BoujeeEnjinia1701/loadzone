"""LoadZone sizing calculations, LDZ-CAL-001 v0.1 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md (tags in brackets, for example
[B2]) and writes docs/04-calcs/results.csv. The script imports PARAMS, derived() and the part
volumes from cad/src/model.py, so the geometry here is the geometry in the STEP files and in
drawing LDZ-DWG-001. It also reads bom/bom.csv and budget_usd in project.yaml.
First-principles paper estimates; nothing here is measured.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P, derived, build_parts, volumes  # noqa: E402

D = derived(P)
rows = []


def out(tag, text):
    print(f"[{tag}] {text}")


def res(rid, value, target, status):
    rows.append((rid, value, target, status))


# =============================================================== assumptions
# Traffic and reporting (LDZ-REQ-001 v0.3)
CHANGES = 100            # state changes per puck per day (50 vehicles a slot)
HEARTBEAT_H = 1.0        # heartbeat interval, h
DEBOUNCE = 15.0          # s a new state must hold before it is reported
SAMPLE_S = 1.0           # magnetometer sampling period, s
BACKEND_S = 2.0          # gateway to network server to LoadZone service, s (assumed)
LATENCY_REQ = 60.0       # s (R2)
# Radio (same core and figures as FND-CAL-001)
PAYLOAD, OVERHEAD = 12, 13
BW, CR, NPRE = 125e3, 1, 8
TTN_S = 30.0             # s uplink per node per day (TTN fair use, checked 2026-09-25)
TTN_DL = 10              # downlinks per node per day (TTN fair use, checked 2026-09-25)
EU_DC = 0.01             # EU868 g1 sub-band duty cycle (default channels)
I_TX, I_RX, I_MCU = 45e-3, 4.6e-3, 8e-3     # A: SX1262 at +14 dBm, receive, controller awake
T_RX, N_RX, T_AWAKE = 0.10, 2, 0.5          # s per RX window, windows per uplink, awake per uplink
I_SLEEP = 6e-6           # A: module stop mode, magnetometer idle, leakage
T_SAMPLE, I_SAMPLE = 0.010, 2e-3            # s awake and A per magnetometer reading
V_SYS = 3.3
TX_DBM, LOSS_NODE = 14.0, 0.5
ANT_PUCK = -2.0          # dBi, small flexible antenna inside a potted dome (assumed)
ANT_GW, LOSS_GW = 2.0, 2.0
NF = 6.0
SNR_LIM = {7: -7.5, 8: -10.0, 9: -12.5, 10: -15.0, 11: -17.5, 12: -20.0}
F_GHZ = 0.868
H_GW = 10.0              # m, gateway on a pole or low roof in a street canyon (3GPP UMi)
GROUND_LOSS = 10.0       # dB, antenna about 25 mm above the road (estimate)
VEH_LOSS = (10.0, 20.0)  # dB, vehicle parked over the puck, typical and worst (estimate, TRL 2)
FADE = 10.0              # dB
D_REQ = 1.0              # km (R4)
# Cells (DDR-001, D4)
CELL_AH, N_CELLS = 2.6, 2
DERATE = 0.40            # cold, pulse loads, self-discharge, end-of-life voltage
LIFE_REQ = 5.0           # years (R3)
V_OCV = 3.67             # V, fresh Li-SOCl2 open circuit (typical)
V_DIODE = 0.25           # V, Schottky drop per cell branch (proposed)
V_MOD_MAX = 3.6          # V, recommended maximum supply of STM32WL-class modules (typical)
DROOP = 0.3              # V allowed on the pulse capacitor during one uplink
# Detection model (R1): vehicle as a line of vertical induced dipoles; all values are assumptions
B_REF = 10.0             # uT, |dB| under the middle of a parked van (assumed calibration)
THRESH = 3.0             # uT, detection threshold (10 x the magnetometer's 0.3 uT RMS noise)
VEH = {                  # name: (length m, effective dipole height m, moment relative to a van)
    "van": (5.4, 0.8, 1.0), "car": (4.5, 0.6, 0.5), "small car": (3.6, 0.55, 0.4),
    "box truck (high chassis)": (7.0, 1.4, 3.0), "box truck (weak steel)": (7.0, 1.4, 1.5)}
LANE_OFFSET = 2.95       # m, puck to the center of the next traffic lane
# Loads (R6)
AXLE_T = 10.0            # t, single axle; wheel load is half
DYN = 1.3                # dynamic factor for slow maneuvering over the puck
MU = 0.7                 # tire to puck friction for braking or scrubbing
SIG_PU = 40.0            # MPa, rigid cast polyurethane compressive strength (typical range 30 to 80)
SIG_POT = 15.0           # MPa, semi-rigid potting compound compressive strength (assumed)
TAU_BOND = {"20 C": 1.0, "50 C": 0.2}       # MPa, adhesive to asphalt surface shear (assumed)
BAY_W, VAN_W, VAN_TRACK, TIRE_W = 2.6, 2.0, 1.75, 0.225   # m
CAR_W, CAR_TRACK, CAR_TIRE = 1.8, 1.55, 0.20
# Mass
RHO = {"dome": 1.15, "potting": 1.10, "base": 1.07, "pad": 1.10}   # g/cm3 (cast PU, PU potting, ASA, adhesive)
M_CELL, M_ELEC = 19.0, 12.0                  # g per cell; board, module, magnetometer, antenna, capacitor
# Sign option (DDR-001, D6, D7)
SIGN_CHANGES = 2 * CHANGES                  # bay free-count changes per day for two slots
P_RX = I_RX * V_SYS                          # W, class C receiver on continuously
P_SLEEP_SIGN = 30e-6 * V_SYS                 # W, controller and panel driver idle
E_REDRAW = 0.0264 * 5 + I_MCU * V_SYS * 5    # J: panel 26.4 mW for 5 s plus controller awake 5 s (typical 7.5 in panel)
ETA_RAIL = 0.90
ALLOW = {"115 mW (published)": 0.115, "100 mW (proposed in FieldNode)": 0.100}
PANEL_H_MM = 97.9                            # active area height of a 7.5 in 800 x 480 panel
DIGIT_FRAC = 0.80
LI_M_PER_MM = 30 * 0.3048 / 25.4            # MUTCD legibility index 30 ft per inch
LEGIBLE_REQ = 25.0
LIGHT_W, LIGHT_H = 0.5, 12.0                 # W and h/day for a small front light (option)
DL_PAYLOAD = 3

# =============================================================== A. Airtime (R5) and energy per uplink
def toa(sf, pl=PAYLOAD + OVERHEAD, bw=BW):
    """LoRa time on air, s (Semtech AN1200.13), explicit header, CRC on, CR 4/5."""
    de = 1 if (sf >= 11 and bw == 125e3) else 0
    ts = 2 ** sf / bw
    n = 8 + max(math.ceil((8 * pl - 4 * sf + 28 + 16) / (4 * (sf - 2 * de))) * (CR + 4), 0)
    return (NPRE + 4.25) * ts + n * ts


ups = CHANGES + 24 / HEARTBEAT_H
air = {}
for sf in range(7, 13):
    t = toa(sf)
    per_day = t * ups
    hb_room = (TTN_S - CHANGES * t) / t
    max_changes = TTN_S / t
    air[sf] = (t, per_day)
    hb_txt = f"heartbeat every {24 / hb_room:.1f} h fits" if hb_room >= 1 else "does not fit even with no heartbeats"
    out("A1", f"SF{sf}: {t * 1000:.1f} ms per {PAYLOAD}-byte uplink; {per_day:.1f} s/day at {ups:.0f} uplinks; "
              f"within {TTN_S:.0f} s: {hb_txt}; at most {max_changes:.0f} uplinks a day")
res("R5", f"{air[7][1]:.1f} s/day at SF7, {air[8][1]:.1f} at SF8, {air[9][1]:.1f} at SF9, {air[10][1]:.1f} at SF10, "
          f"{air[12][1]:.1f} at SF12 ({ups:.0f} uplinks)", "30 s/day or less", "At risk (met at SF7 to SF9; not met at SF10 to SF12)")

# =============================================================== B. Energy and cell life (R3)
q_up = {sf: I_TX * air[sf][0] + I_RX * T_RX * N_RX + I_MCU * T_AWAKE for sf in air}   # A s
q_sleep = I_SLEEP * 86400
q_samp = (I_SAMPLE * T_SAMPLE / SAMPLE_S) * 86400
usable = CELL_AH * N_CELLS * (1 - DERATE)
out("B1", f"sleep {q_sleep / 3.6:.3f} mAh/day; sampling {I_SAMPLE * T_SAMPLE / SAMPLE_S * 1e6:.0f} uA avg = {q_samp / 3.6:.3f} mAh/day")
life = {}
for sf in (7, 9, 10, 12):
    day = (q_sleep + q_samp + q_up[sf] * ups) / 3.6       # mAh/day
    yr = day * 365 / 1000                                  # Ah/yr
    life[sf] = usable / yr
    out("B2", f"SF{sf}: {q_up[sf] * 1000:.1f} mA s per uplink, uplinks {q_up[sf] * ups / 3.6:.3f} mAh/day; "
              f"total {day:.2f} mAh/day = {yr:.3f} Ah/yr; life {life[sf]:.1f} years on {usable:.2f} Ah usable")
out("B3", f"usable capacity {CELL_AH * N_CELLS:.1f} Ah nameplate x {1 - DERATE:.2f} = {usable:.2f} Ah; "
          f"share of the SF9 budget: sampling {q_samp / (q_sleep + q_samp + q_up[9] * ups):.0%}, "
          f"uplinks {q_up[9] * ups / (q_sleep + q_samp + q_up[9] * ups):.0%}")
res("R3", f"{life[9]:.1f} years at SF9 ({life[7]:.1f} at SF7, {life[12]:.1f} at SF12) with 40 % derating",
    "5 years or more at 100 changes a day plus hourly heartbeats", "Met on paper" if life[9] >= LIFE_REQ else "Not met")

for sf in (9, 12):
    c = I_TX * air[sf][0] / DROOP
    out("B4", f"pulse capacitor, SF{sf}: {I_TX * air[sf][0] * 1000:.1f} mC per uplink; {c * 1000:.0f} mF if the capacitor alone "
              f"supplies it with {DROOP} V droop")
out("B5", f"supply: fresh cells {V_OCV} V open circuit against {V_MOD_MAX} V module maximum; with a {V_DIODE} V Schottky per cell "
          f"branch {V_OCV - V_DIODE:.2f} V, which also stops one cell charging the other")

# =============================================================== C. Latency (R2)
for sf in (9, 10, 11, 12):
    off = air[sf][0] * (1 / EU_DC - 1)
    worst = DEBOUNCE + SAMPLE_S + off + air[sf][0] + BACKEND_S
    typ = DEBOUNCE + SAMPLE_S / 2 + air[sf][0] + BACKEND_S
    out("C1", f"SF{sf}: typical {typ:.1f} s; worst {worst:.1f} s including a {off:.1f} s EU868 duty-cycle wait after the previous uplink")
    if sf == 9:
        lat9 = (typ, worst)
    if sf == 10:
        lat10 = worst
res("R2", f"typical {lat9[0]:.1f} s; worst {lat9[1]:.1f} s at SF9, {lat10:.1f} s at SF10; over 60 s at SF11 and SF12",
    "60 s or less", "Met on paper (SF10 or faster)")

# =============================================================== D. Link (R4), 3GPP TR 38.901 UMi street canyon
def umi(d_km, h_ut=1.5, h_bs=H_GW, fc=F_GHZ):
    d3 = math.hypot(d_km * 1000, h_bs - h_ut)
    dbp = 4 * (h_bs - 1) * (h_ut - 1) * fc * 1e9 / 3e8
    if d_km * 1000 <= dbp:
        los = 32.4 + 21 * math.log10(d3) + 20 * math.log10(fc)
    else:
        los = 32.4 + 40 * math.log10(d3) + 20 * math.log10(fc) - 9.5 * math.log10(dbp ** 2 + (h_bs - h_ut) ** 2)
    nlos = max(los, 35.3 * math.log10(d3) + 22.4 + 21.3 * math.log10(fc) - 0.3 * (h_ut - 1.5))
    return los, nlos


eirp = TX_DBM - LOSS_NODE + ANT_PUCK
los1, nlos1 = umi(D_REQ)
out("D1", f"EIRP {eirp:.1f} dBm; UMi path loss at {D_REQ:.0f} km, gateway {H_GW:.0f} m: LOS {los1:.1f} dB, NLOS {nlos1:.1f} dB; "
          f"road-level loss {GROUND_LOSS:.0f} dB, vehicle {VEH_LOSS[0]:.0f} to {VEH_LOSS[1]:.0f} dB")
for sf in (9, 12):
    sens = -174 + 10 * math.log10(BW) + NF + SNR_LIM[sf]
    budget = eirp + ANT_GW - LOSS_GW - sens
    extra = GROUND_LOSS + VEH_LOSS[0]
    m_n = budget - nlos1 - extra
    m_l = budget - los1 - extra
    rng = []
    for fade in (0.0, FADE):
        lo, hi = 0.01, 20.0
        for _ in range(60):
            mid = (lo + hi) / 2
            (lo, hi) = (mid, hi) if umi(mid)[1] + extra + fade < budget else (lo, mid)
        rng.append(lo * 1000)
    out("D2", f"SF{sf}: sensitivity {sens:.1f} dBm, budget {budget:.1f} dB; margin at {D_REQ:.0f} km with a van over "
              f"(typical): NLOS {m_n:.1f} dB, LOS {m_l:.1f} dB; worst vehicle {m_n - (VEH_LOSS[1] - VEH_LOSS[0]):.1f} dB NLOS; "
              f"NLOS range {rng[0]:.0f} m (no fade margin), {rng[1]:.0f} m ({FADE:.0f} dB fade margin)")
    if sf == 9:
        link9 = (budget, m_n, m_l, rng)
res("R4", f"SF9 margin at 1 km with a van over: {link9[1]:.1f} dB NLOS, {link9[2]:.1f} dB LOS; NLOS range {link9[3][1]:.0f} m with 10 dB fade margin",
    "1 km in a street canyon with a van parked over the puck", "Not met")

# =============================================================== E. Detection (R1), line-dipole model
MU0_4PI = 1.0   # absorbed into the calibration


def field(vlen, h, moment, dx=0.0, dy=0.0, n=81):
    """|dB| at the puck from a vehicle of length vlen (m) whose center is dx along and dy across, dipoles at height h."""
    xs = np.linspace(-vlen / 2, vlen / 2, n) + dx
    m = moment / n
    B = np.zeros(3)
    for x in xs:
        r = np.array([-x, -dy, -h])            # from dipole to puck
        rn = np.linalg.norm(r); rh = r / rn
        mv = np.array([0, 0, m])
        B += (3 * np.dot(mv, rh) * rh - mv) / rn ** 3
    return np.linalg.norm(B)


k_cal = B_REF / field(*VEH["van"][:2], VEH["van"][2])
cases = [("van, centered", "van", 0, 0),
         ("car, centered", "car", 0, 0),
         ("car at the slot end", "car", P["slot_l"] / 2000 - 4.5 / 2, 0),
         ("small car at the slot end", "small car", P["slot_l"] / 2000 - 3.6 / 2, 0),
         ("box truck (high chassis), centered", "box truck (high chassis)", 0, 0),
         ("box truck (weak steel), centered", "box truck (weak steel)", 0, 0),
         ("van passing in the next lane", "van", 0, LANE_OFFSET),
         ("van in the next slot, 0.5 m past the line", "van", P["slot_l"] / 2000 + 0.5 + 5.4 / 2, 0)]
det = {}
for name, v, dx, dy in cases:
    L, h, mo = VEH[v]
    b = k_cal * field(L, h, mo, dx, dy)
    det[name] = b
    should = "next" not in name
    ok = (b >= THRESH) == should
    out("E1", f"{name}: {b:.2f} uT ({b / THRESH:.2f} x threshold) -> {'correct' if ok else 'WRONG'}")
missed = [k for k, b in det.items() if "next" not in k and b < THRESH]
out("E2", f"calibration {B_REF} uT under a van; threshold {THRESH} uT; would be missed: {', '.join(missed) or 'none'}")
res("R1", f"Model: van {det['van, centered']:.1f} uT, high-chassis truck {det['box truck (high chassis), centered']:.1f} uT, "
          f"small car at slot end {det['small car at the slot end']:.1f} uT, next lane {det['van passing in the next lane']:.2f} uT "
          f"against a {THRESH:.0f} uT threshold", "97 % of slot states correct over a day",
    "At risk (not verifiable at TRL 3)")

# =============================================================== F. Loads (R6) and wheel paths
W = AXLE_T * 1000 * 9.81 / 2
flat_r = P["dome_top_r"] - P["crown_fillet"]
a_crown = math.pi * flat_r ** 2
a_base = math.pi * P["base_r"] ** 2
a_pad = math.pi * P["pad_r"] ** 2
s_crown, s_base = W / a_crown, W / a_base
out("F1", f"wheel load {W / 1000:.1f} kN static, {W * DYN / 1000:.1f} kN with x{DYN} dynamic; crown flat {2 * flat_r:.0f} mm: "
          f"{s_crown:.2f} MPa static, {s_crown * DYN:.2f} MPa dynamic; base {s_base:.2f} MPa")
out("F2", f"factor on rigid PU ({SIG_PU:.0f} MPa): {SIG_PU / s_crown:.1f} static, {SIG_PU / (s_crown * DYN):.1f} dynamic; "
          f"on potting ({SIG_POT:.0f} MPa): {SIG_POT / s_crown:.1f} static, {SIG_POT / (s_crown * DYN):.1f} dynamic")
tau = MU * W / a_pad
out("F3", f"bond shear with mu {MU}: {MU * W / 1000:.1f} kN over the {2 * P['pad_r']:.0f} mm pad = {tau:.2f} MPa; "
          + "; ".join(f"factor {v / tau:.2f} at {k}" for k, v in TAU_BOND.items()))
lat_van = (BAY_W - VAN_W) / 2
inner_van = VAN_TRACK / 2 - TIRE_W / 2 - lat_van
lat_car = (BAY_W - CAR_W) / 2
inner_car = CAR_TRACK / 2 - CAR_TIRE / 2 - lat_car
out("F4", f"parked within the bay lines, the nearest tire edge stays {inner_van * 1000:.0f} mm (van) and {inner_car * 1000:.0f} mm (car) "
          f"from the puck axis, against a {P['base_r']:.0f} mm puck radius: parked wheels straddle the puck; only maneuvering wheels cross it")
res("R6", f"crown {s_crown:.1f} MPa static, factor {SIG_PU / s_crown:.1f} on PU and {SIG_POT / s_crown:.1f} on potting; "
          f"bond shear {tau:.2f} MPa, factor {TAU_BOND['20 C'] / tau:.2f} at 20 C, {TAU_BOND['50 C'] / tau:.2f} at 50 C",
    "50 kN static wheel load and repeated drive-overs without cracking or debonding", "At risk (debond under braking)")

# =============================================================== G. Size, mass (R7)
vol = volumes(build_parts())
mass = sum(vol[k] * RHO[k] for k in ("dome", "potting", "base")) + N_CELLS * M_CELL + M_ELEC
out("G1", f"height {D['height']:.1f} mm, base {D['diameter']:.0f} mm, pad {D['pad_d']:.0f} mm, crown {D['crown_d']:.0f} mm, "
          f"crown fillet {P['crown_fillet']:.0f} mm")
out("G2", "volumes cm3: " + ", ".join(f"{k} {v:.1f}" for k, v in vol.items())
          + f"; puck mass {mass:.0f} g without the pad; pad {vol['pad'] * RHO['pad']:.0f} g")
res("R7", f"{D['height']:.0f} mm high, {D['diameter']:.0f} mm diameter, {P['crown_fillet']:.0f} mm crown radius, yellow dome",
    "35 mm or less, rounded edges, high visibility", "Met on paper")

# =============================================================== H. Sign option (R11, R12)
e_day = (P_RX + P_SLEEP_SIGN) * 86400 + E_REDRAW * SIGN_CHANGES      # J delivered
wh = e_day / 3600
drawn = wh / ETA_RAIL
avg_mw = drawn / 24 * 1000
out("H1", f"class C receive {P_RX * 1000:.1f} mW = {P_RX * 24:.3f} Wh/day; {SIGN_CHANGES} redraws x {E_REDRAW:.2f} J = "
          f"{E_REDRAW * SIGN_CHANGES / 3600:.3f} Wh/day; total {wh:.3f} Wh delivered, {drawn:.3f} Wh drawn = {avg_mw:.1f} mW average")
for k, a in ALLOW.items():
    out("H2", f"against the FieldNode allowance of {k}: {avg_mw / (a * 1000):.0%} used; {a * 24:.2f} Wh/day available")
light = LIGHT_W * LIGHT_H
out("H3", f"a {LIGHT_W} W front light for {LIGHT_H:.0f} h adds {light:.1f} Wh/day, {light / (0.100 * 24):.1f} x the 100 mW allowance")
digit = PANEL_H_MM * DIGIT_FRAC
dist = digit * LI_M_PER_MM
out("H4", f"digit {digit:.0f} mm on a {PANEL_H_MM} mm panel; legibility index {LI_M_PER_MM:.2f} m per mm -> {dist:.1f} m by day at full contrast; "
          f"digit needed for {LEGIBLE_REQ:.0f} m: {LEGIBLE_REQ / LI_M_PER_MM:.0f} mm")
t_dl = toa(9, DL_PAYLOAD + OVERHEAD)
out("H5", f"downlinks: {SIGN_CHANGES}/day against TTN's {TTN_DL}/day; on a private gateway {SIGN_CHANGES} x {t_dl * 1000:.0f} ms "
          f"= {SIGN_CHANGES * t_dl:.0f} s/day at SF9 in RX2, {SIGN_CHANGES * t_dl / 86400 / 0.10:.2%} of the 10 % sub-band allowance")
res("R11", f"about {dist:.0f} m by day at full contrast ({digit:.0f} mm digits); unlit at night", "25 m by day and night", "Not met (night)")
res("R12", f"{drawn:.2f} Wh/day drawn ({avg_mw:.1f} mW) against 2.40 to 2.76 Wh/day", "Within the host FieldNode allowance",
    "Met on paper (private network only: 200 downlinks/day)")

# =============================================================== I. Cost (R13)
bom = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
budget = None
for line in (ROOT / "project.yaml").read_text().splitlines():
    if line.startswith("budget_usd:"):
        budget = float(line.split(":")[1].split("#")[0])
def ln(r):
    return int(r["item"].split()[0])
def cost(r):
    return float(r["qty"]) * float(r["unit_cost_usd"])
core = sum(cost(r) for r in bom if ln(r) <= 7 or ln(r) == 12)
sign = sum(cost(r) for r in bom if 8 <= ln(r) <= 10)
fn = sum(cost(r) for r in bom if ln(r) == 11)
per_puck = sum(float(r["unit_cost_usd"]) for r in bom if ln(r) <= 7)
out("I1", f"two-puck kit ${core:.2f} against budget_usd ${budget:.0f} (margin ${budget - core:.2f}); per puck ${per_puck:.2f}; "
          f"sign option ${sign:.2f}; host FieldNode ${fn:.2f}; bay with sign ${core + sign + fn:.2f}")
res("R13", f"${core:.2f} for two pucks; sign option ${sign:.2f} plus FieldNode ${fn:.2f}, outside the budget (D6)",
    f"Two-puck kit ${budget:.0f} or less", "Met on paper" if core <= budget else "Not met")

# =============================================================== J. Design-review items
res("R8", "Cells -55 to +85 C, magnetometer and module -40 to +85 C class; pulse capacitor must be an 85 C hybrid type; fully potted",
    "IP68; -25 to +70 C road surface; salt, oil, fuel", "Met by design (sealing not verifiable at TRL 3)")
res("R9", "Magnetometer only; 12-byte payload of state, timer, confidence, voltage, temperature", "No images, audio or identifiers", "Met by design")
res("R10", "park_start, park_end, scheduled_report, comms_lost and comms_restored map onto CDS Events; occupancy and dwell onto Metrics",
    "Open API mapping onto CDS Events and Metrics", "Met by design")
res("R14", "Bonded pad, no road cutting; time depends on the adhesive", "15 min per puck, two-person crew", "Not verifiable at TRL 3")
res("R15", "No external fasteners; bonded; removal flagged by a field and orientation step", "No screws; removal reported", "Met by design")

order = {f"R{i}": i for i in range(1, 16)}
rows.sort(key=lambda r: order[r[0]])
with (ROOT / "docs/04-calcs/results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "value", "target", "status"])
    w.writerows(rows)
counts = {}
for r in rows:
    key = r[3].split(" (")[0]
    counts[key] = counts.get(key, 0) + 1
out("K", "status counts: " + ", ".join(f"{k} {v}" for k, v in counts.items()) + f"; {len(rows)} requirements; wrote docs/04-calcs/results.csv")
