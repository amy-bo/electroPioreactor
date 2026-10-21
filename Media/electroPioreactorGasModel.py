#!/usr/bin/env python3
"""
electroPioreactorGasModel.py

Independent first-principles re-derivation of the electroPioreactor CO2/gas
spreadsheet (Media/electroPioreactorGasModel.xlsx), together with a verification
harness that compares this twin against the workbook FILE - never against a
snapshot of it.

The contract
------------
* The physics is computed HERE, independently. The explicitly listed diagnostic
  outputs are derived from the input parameters and physical/chemical constants,
  never read back as computed answers. This is broad parity coverage, not a claim
  that every formula cell is independently re-derived. The definition guard also
  detects changes to any scalar input, formula or defined-name target.
* The comparison target is the workbook itself. `cached(sheet, ref)` opens
  electroPioreactorGasModel.xlsx (path resolved relative to this script, so it
  works from any working directory), unzips it in memory and returns the value
  Excel cached for that cell. There are no hard-coded expected numbers anywhere
  in the harness, so a stale twin and a moved-on workbook can no longer agree
  with each other by construction - which is exactly how an earlier version of
  this file managed to report "92/92 match" against its own stale copy.
* The inputs are ASSERTED, not assumed. The declarations below correspond to
  Summary D2:D10 plus the two headspace selectors D111:D112, and are checked against the workbook before anything is
  compared. On any drift the harness names the offending pairs and exits
  non-zero WITHOUT comparing outputs: a twin evaluated at different inputs from
  the workbook produces meaningless agreement (and meaningless disagreement).
* A workbook shipped without formula caches - Excel recomputes on load and some
  save paths drop them - is reported per cell as "no cached value", counted
  separately from a mismatch, and still exits non-zero. It is never silently
  scored as a match. The wave-4 revision drops the cache on every changed cell,
  so a freshly-written workbook reports a large "no cached value" block until it
  has been opened and saved in Excel once. That is expected.

Standard library only; keep gas_model_verification.py and the verification JSON
beside the workbook. After intentional input/formula changes, recalculate in Excel,
rebase both companions, explicitly record the new definition and rerun the checks.
Run with:
    python3 electroPioreactorGasModel.py
Exit status is 0 only when the inputs match the workbook AND every output agrees
with the workbook's cached value within 0.5%.

iterM additions: pulse volume V = V0 + Q*t fitted from CO2 flows (Mass Transfer D401-D411,
all duty -> interval conversions on the full-flow-equivalent time), carryover limit from CO2
flows column M, CO2 uptake ratio, bicarbonate capacity (DIC_cap) in the CO2 pool, dry-gas
basis P_dry for gas partial pressures, O2 salting-out, and the PCET credit withdrawn above the
buffer limit. The conditional-format changes have no twin counterpart.

iterF additions (final-gate fixes R5-M1, R5-m1..m9): the calibration gate and solenoid floor accept a
Calibrations-tab flow / Min pulse (cal_flow, cal_pulse_floor; both None here, the tab is empty) with the
pulse_floor_default fallback; Summary D128 tests both pH band edges and reports overrides; the lag-phase
cathodic O2 loss and H2 are evaluated at a typed reference lag DO (DO_lag_ref, Electrochemistry D129-D134)
and feed every lag source; the flammability remedy interval is the exact sawtooth result (Biology D89-D92);
Summary kLa rows are in 1/h; ec_DO_design follows the DO target; the CO2 sparge basis is the dry-gas pressure.

The model mirrors the workbook's sheet structure (Summary -> Geometry ->
Electrochemistry -> Chemistry -> Biology -> Mass Transfer -> CO2 flows) but the
arithmetic is re-implemented cleanly from the documented formula logic. Because
the wave-4 revision makes the faradaic efficiencies CALCULATED, the evaluation
order below no longer follows tab order: Geometry -> Electrochemistry (areas)
-> Biology (Henry, DO target) -> Electrochemistry (cathodic split) -> Chemistry
(chloride -> anodic split) -> Electrochemistry (gas rates) -> Biology (gas
budget) -> Chemistry (conductivity, activity) -> Electrochemistry (cell
voltage) -> Mass Transfer -> Chemistry (pH solve). Every step is still a pure
function of the inputs; nothing is circular.
"""

import builtins
import math
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from decimal import Decimal, ROUND_HALF_UP
from gas_model_verification import verify_definition

# ============================================================================
# SUMMARY TAB - user inputs (the only free variables in the model)
#   These mirror Summary D2:D10 (+ D111:D112) and are verified against the workbook at
#   startup (see check_inputs() at the bottom). Change them only together with
#   the workbook: the harness refuses to compare a twin run at other inputs.
# ============================================================================
Reactor_sel    = "ed04"            # D2
electrode_sel  = "MMO tube"        # D3
organism_sel   = "Xanthobacter tagetidis"  # D4
media_sel      = "AMYBO03"         # D5
led_intensity  = 3.0               # D6  (%)
stir_rpm_set   = 1000.0            # D7  (rpm)
temp_C         = 30.0              # D8  (degC)
media_volume   = 0.0               # D9  (mL; blank in workbook -> 0.0 -> use recommended max)
P_atm_set      = 0.0               # D10 (Pa; blank in workbook -> 0.0 -> default 101325)
NaHCO3_add_gL  = 0.0               # D133 (g/L NaHCO3 added on top of the recipe; blank -> 0.0)
N2_sweep_set   = 0.0               # D98 (mL/min continuous N2 headspace sweep; blank -> 0.0, owner decision T7)
# Headspace-model owner decisions (Summary D111:D112, typed text; anything else -> #N/A)
vent_model_sel = "Open vent"       # D111 ("Outflow only" | "Open vent" | "Air exchange")
O2_phase_sel   = "Growth"          # D112 ("Growth" | "Lag") phase the O2 sizing is done on

NA = float("nan")                  # spreadsheet #N/A sentinel for unmeasured data


def _nan_in(args):
    return any(isinstance(v, float) and math.isnan(v)
               for a in args for v in (a if isinstance(a, (list, tuple)) else (a,)))


def max(*args, **kw):
    """Excel MAX/MIN propagate an error (#N/A); Python's silently skip a NaN depending on argument order."""
    return float("nan") if _nan_in(args) else builtins.max(*args, **kw)


def min(*args, **kw):
    return float("nan") if _nan_in(args) else builtins.min(*args, **kw)


def isnum(x):
    """Mirror Excel ISNUMBER: True for a real (non-NaN) float."""
    return isinstance(x, (int, float)) and not (isinstance(x, float) and math.isnan(x))


def xltext(value, fmt):
    """Excel TEXT() for the handful of formats the workbook's verdict strings use.

    Excel rounds half away from zero; Python's round() is half-to-even, so the
    decimal module is used rather than f-string formatting.
    """
    if fmt.endswith("%"):
        return xltext(value * 100, fmt[:-1]) + "%"
    places = len(fmt.split(".")[1]) if "." in fmt else 0
    q = Decimal(1).scaleb(-places) if places else Decimal(1)
    return f"{Decimal(repr(float(value))).quantize(q, rounding=ROUND_HALF_UP):.{places}f}"


# ============================================================================
# GEOMETRY TAB
# ============================================================================
# Reactor -> type lookup (Geometry A59:B80)
REACTOR_TYPE = {
    "imp01": "AEP0.1.1", "imp02": "AEP0.1.1", "imp03": "AEP0.1.1",
    "imp04": "AEP0.1.1", "imp05": "AEP0.1.1", "imp06": "AEP0.1.1",
    "ed01": "AEP0.1.1", "ed02": "AEP0.1.1", "ed03": "AEP0.1.1",
    "ed04": "MEP0.3", "ed05": "MEP0.3",
    "ed06": "AEP0.2", "ed07": "AEP0.2", "ed08": "AEP0.2",
    "imp07": "AEP0.2", "imp08": "AEP0.2", "imp09": "AEP0.2",
    "imp10": "AEP0.2", "imp11": "AEP0.2", "imp12": "AEP0.2",
    "nm01": "AEP0.2a", "nm02": "AEP0.2",
}
# Reactor-type -> geometry lookup (Geometry A84:I87)
#   cols: [vial mL, usable depth mm, max working mL, total vial mL, vial OD mm, stir bar L mm, stir bar dia mm]
TYPE_GEOM = {
    "AEP0.1.1": dict(vial=20, depth=55, vmax=16, vtot=20, od=27.48, stir_L=12, stir_dia=3),
    "MEP0.3":   dict(vial=20, depth=55, vmax=16, vtot=20, od=27.48, stir_L=12, stir_dia=3),
    "AEP0.2":   dict(vial=40, depth=95, vmax=30, vtot=42, od=27.48, stir_L=15, stir_dia=6),
    "AEP0.2a":  dict(vial=40, depth=95, vmax=30, vtot=42, od=27.48, stir_L=15, stir_dia=6),
}

rx_ver       = REACTOR_TYPE[Reactor_sel]          # D51
g            = TYPE_GEOM[rx_ver]
vial_OD      = g["od"]                             # D18 (mm)
vial_wall    = 1.1                                 # D19 (mm)
vial_ID      = vial_OD - 2 * vial_wall             # D20 (mm)
A_x          = math.pi / 4 * vial_ID ** 2          # D21 (mm^2)
D_int        = g["depth"]                          # D22 (mm)
V_max        = g["vmax"]                           # D23 (mL)
V_vial_total = g["vtot"]                           # D24 (mL)
h_datum      = V_max * 1000 / A_x                  # D25 (mm)
rod_d        = 6.0                                 # D26 (mm)
rod_n        = 2                                   # D27
elec_clear   = 22.0                                # D28 (mm)
elec_ins     = D_int - elec_clear                  # D29 (mm)
spg_OD       = 3.175                               # D30 (mm)
spg_ID       = 1.5875                              # D31 (mm)
spg_tip_h    = elec_clear                          # D32 (mm)
eff_OD       = 3.175                               # D33 (mm)
eff_ID       = 1.5875                              # D34 (mm)
elec_sub_L   = max(0.0, h_datum - elec_clear)      # D35 (mm) bare datum - displacement bookkeeping only
elec_disp    = rod_n * (math.pi / 4 * rod_d ** 2) * elec_sub_L / 1000          # D36 (mL)
spg_disp     = (math.pi / 4 * spg_OD ** 2) * max(0.0, h_datum - spg_tip_h) / 1000  # D37 (mL)
eff_sub_L    = (eff_OD + eff_ID) / 2               # D38 (mm)
eff_disp     = (math.pi / 4 * (eff_OD ** 2 - eff_ID ** 2)) * eff_sub_L / 1000  # D39 (mL)
disp_tot     = elec_disp + spg_disp + eff_disp     # D40 (mL)
V_charge     = media_volume if media_volume > 0 else round(V_max - disp_tot)   # D41 (mL)
h_actual     = (V_charge + disp_tot) * 1000 / A_x  # D42 (mm)
sparge_depth = max(0.0, h_actual - spg_tip_h)      # D43 (mm)
interface_A  = A_x - (rod_n * (math.pi / 4 * rod_d ** 2)
                      + (math.pi / 4 * spg_OD ** 2)
                      + (math.pi / 4 * eff_OD ** 2))                            # D44 (mm^2)
xtube_OD     = eff_OD                               # D45 (mm)
xtube_n      = 3                                    # D46
xtube_pro    = 5.0                                  # D47 (mm)
spg_len      = D_int - spg_tip_h                    # D50 (mm)
V_inserts    = (rod_n * (math.pi / 4 * rod_d ** 2) * elec_ins
                + (math.pi / 4 * spg_OD ** 2) * spg_len
                + (math.pi / 4 * (eff_OD ** 2 - eff_ID ** 2)) * (D_int - h_actual)
                + xtube_n * (math.pi / 4 * xtube_OD ** 2) * xtube_pro) / 1000   # D48 (mL)
cal_hs, cal_hs_fill = None, None                   # Calibrations D76/D77 (no vial-geometry runs yet)
if cal_hs is not None and cal_hs_fill is not None:  # D49: measured headspace, shifted to V_charge
    headspace_V = cal_hs - (V_charge - cal_hs_fill)
else:
    headspace_V = V_vial_total - V_charge - V_inserts  # D49 (mL)
stir_bar_L   = g["stir_L"]                          # D52 (mm)
media_vol_warn = "MEDIA > MAX WORKING VOLUME" if V_charge > V_max else "OK"     # D54
depth_warn     = "LIQUID OVER USABLE DEPTH" if h_actual > D_int else "OK"       # D55
if abs(A_x * D_int / 1000 - V_vial_total) <= 3:                                # D90
    geom_check = "OK"
elif cal_hs is not None and cal_hs_fill is not None:
    geom_check = "HEADSPACE MEASURED - bore depth still inconsistent (measure body volume)"
else:
    geom_check = "VIAL GEOMETRY INCONSISTENT - measure true fill volume & bore depth"
# --- electrode geometry for the ohmic drop (wave-4, Geometry rows 91-93) ---
elec_gap       = 14.0                               # D92 (mm) DATA GAP - centre-to-centre, measure with calipers
elec_sub_L_act = max(0.0, h_actual - elec_clear)    # D93 (mm) submerged length at the ACHIEVED level
# NOTE: D93 replaces D35 as the wetted-area basis. The bare datum h_datum ignores
# the insert displacement that actually raises the liquid, so it overstated the
# submerged length by ~6.5% and understated every current density by the same
# factor. D35 survives only for the displacement bookkeeping that produced it.


# ============================================================================
# ELECTROCHEMISTRY TAB - part A: current, electrode geometry, current density
#   (T_K, P_atm, R_gas come from Biology / Mass Transfer, defined below.)
# ============================================================================
# Electrode lookup (Electrochemistry A35:N38): sparger, sinter porosity, z_e_ORR
ELECTRODE = {
    "Pt/Ti rod": dict(sparger="Tube",     por="n/a", z_e_ORR=2),
    "MMO rod":   dict(sparger="Tube",     por="n/a", z_e_ORR=2),
    "MMO tube":  dict(sparger="Sintered", por=0,     z_e_ORR=2),
}
gerrit_slope = 1.03          # D11 (mA/%)
gerrit_int   = 2.6           # D12 (mA)
gerrit_min   = 3.0           # D13 (%)
gerrit_max   = 25.0          # D14 (%)
F_const      = 96485.33212   # D15 (C/mol)
z_e_H2       = 2             # D16
z_e_O2       = 4             # D17
intensity    = led_intensity # D10 (%)
# The plugin accepts lower powers and clamps high ones, but neither operation
# validates extrapolation of the empirical current fit. Refuse an unsupported run.
if not gerrit_min <= intensity <= min(gerrit_max, 10.0):
    raise SystemExit("Unsupported electrolysis power: model requires 3–10%; no extrapolated schedule was calculated.")
I_app        = (gerrit_slope * intensity + gerrit_int) / 1000   # D19 (A)
I_valid      = "OK" if (gerrit_min <= intensity <= gerrit_max) else "OUT"  # D20
e            = ELECTRODE[electrode_sel]
sparger_e    = e["sparger"]                                     # D31
por_grade_e  = e["por"] if isnum(e["por"]) else 0               # D32
z_e_ORR      = e["z_e_ORR"]                                     # D27

# --- current density, shape-aware wetted area & limits (Electrochemistry rows 40-76) ---
# NOTE ON THE CALIBRATIONS LAYER: in the workbook every parameter below that has a
# bench calibration (gerrit_slope/int, etaF/etaF_OER, kLa, DO bands, knallgas ratio,
# vial geometry, sinter grade, strain j) is read as IFERROR(<Calibrations aggregate>,
# <default>). With an empty Calibrations tab the aggregates error and the model uses
# these defaults, so this twin mirrors the empty-calibration (default) state exactly.
# In wave-4 the etaF/etaF_OER defaults are no longer the constant 1: they are the
# CALCULATED cells D88 / D104 below.
ELECTRODE_GEOM = {  # anode/cathode shape+dia (mm); plating limits (mA/cm2); material
    "Pt/Ti rod":    dict(a_shape="rod",  a_d=6.0, c_shape="rod", c_d=6.0, jc=100, jm=500, mat="Pt/Ti"),
    "MMO rod":      dict(a_shape="rod",  a_d=6.0, c_shape="rod", c_d=6.0, jc=50,  jm=500, mat="MMO"),
    "MMO tube":     dict(a_shape="tube", a_d=6.0, c_shape="rod", c_d=6.0, jc=10,  jm=60,  mat="MMO"),
    "Graphite rod": dict(a_shape="rod",  a_d=6.0, c_shape="rod", c_d=6.0, jc=35,  jm=50,  mat="Graphite"),
}
eg = ELECTRODE_GEOM[electrode_sel]
anode_dia   = eg["a_d"]                                         # D42 (mm)
cathode_dia = eg["c_d"]                                         # D44 (mm)
L_sub       = elec_sub_L_act                                    # D45 (mm) <- Geometry D93


def _wetted(shape, d):                         # cm^2: lateral + end face for a rod, none for a tube
    return (math.pi * d * L_sub + (math.pi / 4 * d ** 2 if shape == "rod" else 0)) / 100


A_anode_wet = _wetted(eg["a_shape"], anode_dia)                 # D46 (cm^2)
A_cath_wet  = _wetted(eg["c_shape"], cathode_dia)               # D47 (cm^2)
j_anode     = I_app * 1000 / A_anode_wet                        # D48 (mA/cm^2)
j_cathode   = I_app * 1000 / A_cath_wet                         # D49 (mA/cm^2)
anode_j_cont, anode_j_max = eg["jc"], eg["jm"]                  # D50, D51
cath_j_cont,  cath_j_max  = 80, 250                             # D52, D53 (SS HER norm)
STRAIN_J = {  # per-organism (optimum, tolerated-ceiling) mA/cm^2; calibration-overridable
    "Cupriavidus necator": (2, 4), "Xanthobacter autotrophicus": (2, 4),
    "Xanthobacter flavus": (2, 4), "Xanthobacter tagetidis": (2, 4),
    "Cupriavidus metallidurans": (2, 4), "UdG (mixed)": (2.14, 4.29),
}
j_opt_strain, j_ceiling_strain = STRAIN_J.get(organism_sel, (1, 2))   # D56, D57 (fallback 1/2)
power_max   = 10.0                                              # D73 (%) AEP-Plugin electrolysis_power clamp
I_max_mA    = gerrit_slope * power_max + gerrit_int             # D74 (mA) current at max power
j_anode_max = I_max_mA / A_anode_wet                            # D75 (mA/cm^2)


# ============================================================================
# BIOLOGY TAB - part A: temperature, pressure, Henry solubilities, DO bands
#   (the gas budget needs the electrolysis rates and is finished further down.)
# ============================================================================
T_C        = temp_C                                   # D17 (degC)
T_K        = T_C + 273.15                             # D18 (K)
P_atm      = P_atm_set if P_atm_set > 0 else 101325.0  # D19 (Pa)
Pa_per_atm = 101325.0                                 # D20
T_ref      = 298.15                                   # D23 (K)
R_gas_mt   = 8.314462618                              # Mass Transfer D101 (J/mol/K)

bio_H2  = 6.0                                         # D10
bio_O2  = 2.0                                         # D11
bio_CO2 = 1.0                                         # D12

# Media ionic composition (g/L) and molar masses
MW = dict(KH2PO4=136.086, Na2HPO4=141.96, NaH2PO4_2H2O=156.01, NaHCO3=84.007,
          K2SO4=174.26, CaSO4_2H2O=172.17, MgSO4_7H2O=246.48, NH42SO4=132.14,
          CaCl2=110.98)
mc = dict(Na2HPO4=2.895, NaH2PO4_2H2O=3.06, K2SO4=0.17, CaSO4_2H2O=0.097,
          MgSO4_7H2O=0.8, NH42SO4=0.943)              # MC02 g/L
udg = dict(KH2PO4=2.3, Na2HPO4=2.9, NaHCO3=1.05, MgSO4_7H2O=0.5,
           NH42SO4=0.47, CaCl2=0.01)                  # UdG g/L
amy = dict(Na2HPO4=4.26, NaH2PO4_2H2O=4.68, K2SO4=0.17, CaSO4_2H2O=0.097,
           MgSO4_7H2O=0.8, NH42SO4=0.943, NaHCO3=3.36)  # AMYBO03 C6:C12 g/L (Teo Reid MRes, Table 2)
amy_mM = {k: v / MW[k] * 1000 for k, v in amy.items()}  # AMYBO03 E6:E12 (mM)
# stocks (AMYBO03 rows 21-31): final uM = stock mM x dose mL/L
amy_dose_Fe, amy_dose_TM = 0.68, 0.05                  # AMYBO03 B15, B16 (mL/L)
amy_Fe   = 15 / 278.01 * 1000 * amy_dose_Fe           # G21 FeSO4 (uM)
amy_H2SO4 = 200 * amy_dose_Fe + 200 * amy_dose_TM     # G22 + G31 (uM)
amy_TM = [c / mw * 1000 * amy_dose_TM for c, mw in
          ((2.4, 287.54), (2.4, 169.02), (0.48, 249.68), (1.5, 262.85), (0.0402, 281.1))]  # G26:G30 Zn Mn Cu Ni Co sulfates (uM)
amy_Mo = 1.8 / 241.95 * 1000 * amy_dose_TM            # G25 Na2MoO4 (uM)

def _by_media(mc02_val, udg_val, amy_val=NA):
    if media_sel == "MC02":
        return mc02_val
    if media_sel == "UdG phosphate":
        return udg_val
    if media_sel == "AMYBO03":
        return amy_val
    return NA


# --- ionic strength (Chemistry D183:D185), hoisted: the O2 salting-out factor below needs it ---
I_mc02 = 0.5 * (2 * mc["Na2HPO4"] / MW["Na2HPO4"]
                + mc["NaH2PO4_2H2O"] / MW["NaH2PO4_2H2O"]
                + 2 * mc["K2SO4"] / MW["K2SO4"]
                + 2 * mc["NH42SO4"] / MW["NH42SO4"]
                + 4 * mc["MgSO4_7H2O"] / MW["MgSO4_7H2O"]
                + 4 * mc["CaSO4_2H2O"] / MW["CaSO4_2H2O"]
                + mc["NaH2PO4_2H2O"] / MW["NaH2PO4_2H2O"]
                + 4 * mc["Na2HPO4"] / MW["Na2HPO4"]
                + 4 * (mc["K2SO4"] / MW["K2SO4"] + mc["MgSO4_7H2O"] / MW["MgSO4_7H2O"]
                       + mc["CaSO4_2H2O"] / MW["CaSO4_2H2O"]
                       + mc["NH42SO4"] / MW["NH42SO4"]))                       # D183 (mol/L)
I_udg = 0.5 * ((udg["NaHCO3"] / MW["NaHCO3"] + 2 * udg["Na2HPO4"] / MW["Na2HPO4"])
               + udg["KH2PO4"] / MW["KH2PO4"]
               + 2 * udg["NH42SO4"] / MW["NH42SO4"]
               + 4 * udg["MgSO4_7H2O"] / MW["MgSO4_7H2O"]
               + 4 * udg["CaCl2"] / MW["CaCl2"]
               + udg["KH2PO4"] / MW["KH2PO4"]
               + 4 * udg["Na2HPO4"] / MW["Na2HPO4"]
               + 4 * (udg["MgSO4_7H2O"] / MW["MgSO4_7H2O"]
                      + udg["NH42SO4"] / MW["NH42SO4"])
               + udg["NaHCO3"] / MW["NaHCO3"]
               + 2 * udg["CaCl2"] / MW["CaCl2"])                               # D184 (mol/L)
_a = amy_mM
I_amy = (3 * _a["Na2HPO4"] + _a["NaH2PO4_2H2O"] + 3 * _a["K2SO4"] + 4 * (_a["CaSO4_2H2O"] + _a["MgSO4_7H2O"])
         + 3 * _a["NH42SO4"] + _a["NaHCO3"]) / 1000 \
        + (4 * (amy_Fe + sum(amy_TM)) + 3 * amy_Mo + 3 * amy_H2SO4) / 1e6   # AMYBO03 D59 (mol/L)
M_NaHCO3 = 84.007                                     # Chemistry D307 (g/mol) IUPAC
alk_add_M = NaHCO3_add_gL / M_NaHCO3                  # Chemistry D318 (mol/L) added Na+ (strong cation)
I_ionic = _by_media(I_mc02, I_udg, I_amy) + alk_add_M  # D185 (mol/L) recipe + added Na+ and HCO3- (z = 1)

# --- Henry solubilities (van 't Hoff) ---
H_O2ref  = 1.2e-5                                     # D21 (mol/m3/Pa)
H_O2T    = 1500.0                                     # D22 (K)
I_ionic_b = I_ionic                                    # Biology D121 (mol/L) <- Chemistry D185
ks_O2     = 0.14                                       # Biology D122 (L/mol per unit ionic strength) Setschenow coefficient, Weisenberger & Schumpe 1996 summed over the UdG recipe
f_salt_O2 = 10 ** (-ks_O2 * I_ionic_b)                 # Biology D123 (-) O2 salting-out factor
H_O2_T   = H_O2ref * math.exp(H_O2T * (1 / T_K - 1 / T_ref)) * f_salt_O2   # D24 (mol/m3/Pa) van 't Hoff x salting-out
O2_ceil_atm = 0.30                                    # D25 (atm)
O2_ceil_Pa  = O2_ceil_atm * Pa_per_atm                # D26 (Pa)
O2_ceil_C   = H_O2_T * O2_ceil_Pa                     # D27 (mol/m3)
O2_ceil_uM  = O2_ceil_C * 1000                        # D28 (uM)

H_CO2ref = 3.3e-4                                     # D29
H_CO2T   = 2400.0                                     # D30
H_CO2_T  = H_CO2ref * math.exp(H_CO2T * (1 / T_K - 1 / T_ref))  # D31
pw_A, pw_B, pw_C = 610.94, 17.625, 243.04             # D203:D205 Magnus coefficients (Pa, -, degC)
p_sat_w   = pw_A * math.exp(pw_B * (T_K - 273.15) / ((T_K - 273.15) + pw_C))   # D206 (Pa) saturated water vapour at reactor T
P_dry     = P_atm - p_sat_w                           # D418 (Pa) dry-gas pressure: the basis of every gas partial pressure in a Henry term
p_CO2_sparge = P_dry                                  # D32 (Pa) <- MT D418 (dry-gas basis, R5-m9)
CO2_diss = H_CO2_T * p_CO2_sparge                     # D33 (mol/m3)
Km_CO2   = 50.0                                       # D34 (uM)
CO2_carbon_margin = CO2_diss * 1000 / Km_CO2          # D35 (x)
Ka1_carb = 4.45e-7                                    # D36 (mol/L)
pH_CO2_unbuf = -math.log10(math.sqrt(Ka1_carb * (CO2_diss / 1000)))  # D37

H_H2ref  = 7.8e-6                                     # D38
H_H2T    = 500.0                                      # D39
H_H2_T   = H_H2ref * math.exp(H_H2T * (1 / T_K - 1 / T_ref))    # D40
C_H2_sat = H_H2_T * P_atm                             # D41 (mol/m3)

# --- organism DO thresholds (HOB lookup A52:F57); '?' -> unmeasured (#N/A) ---
HOB_DO = {  # organism: (min, opt, impair, toxic) - '?' means data gap
    "Cupriavidus necator":       ("?", 2.6, 3.0, 11.5),
    "Xanthobacter autotrophicus": ("?", "?", "?", 11.5),
    "Xanthobacter flavus":       ("?", "?", "?", "?"),
    "Xanthobacter tagetidis":    ("?", "?", "?", "?"),
    "Cupriavidus metallidurans": ("?", "?", "?", "?"),
    "UdG (mixed)":               ("?", "?", "?", "?"),
}


def _do(v):
    return v if isinstance(v, (int, float)) else NA


_row = HOB_DO[organism_sel]
DO_min    = _do(_row[0])                              # D45 (mg/L)
DO_opt    = _do(_row[1])                              # D46
DO_impair = _do(_row[2])                              # D47
DO_toxic  = _do(_row[3])                              # D48

# --- target dissolved-O2 fraction (wave-4: ONE definition, Biology rows 59-61) ---
# Replaces the unsourced 0.5 that Mass Transfer used to carry locally. The
# fallback is C. necator's own band, the only measured one in the table.
DO_frac_fallback = 0.226086956521739                  # D61 (-)  = 2.6 / 11.5 (DO_opt/DO_toxic)
DO_frac_target   = (DO_opt / DO_toxic if (isnum(DO_opt) and isnum(DO_toxic))
                    else DO_frac_fallback)            # D60 (-)


# ============================================================================
# ELECTROCHEMISTRY TAB - part B: the CALCULATED cathodic faradaic split
#   (Electrochemistry rows 78-89). etaF is no longer assumed to be 1: some of
#   the cathode current reduces dissolved O2 instead of making H2, at the O2
#   mass-transport limit for the design DO. Evaluated at the DESIGN DO rather
#   than the modelled steady DO, which would make the sheet circular.
# ============================================================================
ec_O2_ceil   = O2_ceil_C                               # D80 (mol/m3) <- Biology D27
ec_V_L       = V_charge / 1000                         # D82 (L)      <- Biology D6 / 1000
km_O2_default = 4.0e-3                                 # D165 (cm/s) Eisenberg-Tobias-Wilke, 6 mm rod in axial swirl
km_exp       = 0.644                                   # D84 (-) k_m ~ D^(1-0.356); documents the km_Cl scaling
n_e_fcn      = 1                                       # Calibrations D192 one-electron ferricyanide couple
km_T_tol     = 1                                       # Calibrations D193 (degC) a k_m run counts within this of temp_C
KM_CAL = []   # Calibrations rows 168-175: (reactor, electrode, rpm, T_C, I_lim_mA, A_cm2, C_mM, D_fcn_m2s, include); tab empty


def km_ferricyanide(I_lim_mA, A_cm2, C_mM):
    """Calibrations column J (cm/s): k_m = I_lim/(n F A C), the limiting-current definition."""
    return (I_lim_mA / 1000) / (n_e_fcn * F_const * (A_cm2 / 10000) * C_mM) * 100


def km_O2_from_ferricyanide(km_fcn, D_fcn, D_O2_T):
    """Calibrations column K (cm/s): the same D^km_exp scaling the model applies to every species."""
    return km_fcn * (D_O2_T / D_fcn) ** km_exp


def _same(a, b):
    """Excel criteria compare text without regard to case."""
    return str(a).strip().lower() == str(b).strip().lower()


def cal_km_O2_of(rows, D_O2_T):
    """Calibrations D176: mean O2-scaled k_m over included runs for this reactor and electrode at the
    Summary rpm and T. Rows missing an input give "" in columns K/L, which AVERAGEIFS skips."""
    ks = [km_O2_from_ferricyanide(km_ferricyanide(I, A, C), Df, D_O2_T)
          for rx, el, rpm, T, I, A, C, Df, inc in rows
          if _same(rx, Reactor_sel) and _same(el, electrode_sel) and _same(inc, "y")
          and rpm == stir_rpm_set and abs(T - temp_C) <= km_T_tol
          and all(isnum(v) and v != 0 for v in (I, A, C, Df))]
    return sum(ks) / len(ks) if ks else NA


NO_CAL_TXT = "no included runs — model uses its default"   # Calibrations value-in-use text when nothing is included
HB_a, HB_b, HB_c = -4.41, 773.8, 506.4                # D171-D173 Han & Bartels (1996)
cal_km_O2    = cal_km_O2_of(KM_CAL, 10 ** (HB_a + HB_b / T_K - (HB_c / T_K) ** 2) / 10000)   # Calibrations D176 (cm/s) <- Mass Transfer D32 D_O2; NA = no included run
km_O2        = cal_km_O2 if isnum(cal_km_O2) else km_O2_default   # D83 (cm/s) measured if included, else the estimate
M_O2 = 31.998                                          # MT D231 (g/mol) IUPAC 2 x 15.999
DO_target     = (DO_opt / M_O2 if isnum(DO_opt)
                 else DO_frac_target * O2_ceil_C)       # MT D179 (mol/m3) organism optimum (mg/L -> mol/m3) when measured, else the fraction rule
ec_DO_design = DO_target                               # D85 (mol/m3) <- MT D179 (the DO target)
f_HOOH        = 0.15                                   # D91 (-) peroxide selectivity on stainless (Le Bozec 2001)
n_ORR_eff     = z_e_ORR * f_HOOH + z_e_O2 * (1 - f_HOOH)   # Electrochemistry D141 (e-/O2) selectivity-weighted: 2 e- to H2O2, 4 e- to H2O
i_ORR_design = n_ORR_eff * F_const * (km_O2 / 100) * ec_DO_design * (A_cath_wet / 10000)   # D86 (A)
i_ORR_ceiling = n_ORR_eff * F_const * (km_O2 / 100) * ec_O2_ceil * (A_cath_wet / 10000)    # D87 (A)
etaF_calc     = max(0.0, 1 - i_ORR_design / I_app)     # D88 (-)
etaF_calc_min = max(0.0, 1 - i_ORR_ceiling / I_app)    # D89 (-) worst case at the ceiling DO
cal_etaF     = NA                                      # empty calibration; assert against Calibrations D26
etaF          = cal_etaF if isnum(cal_etaF) else etaF_calc                              # D18 = IFERROR(cal_etaF, etaF_calc)


# ============================================================================
# CHEMISTRY TAB - part A: media composition and the chloride pool
#   Hoisted above the Electrochemistry gas rates because the ANODIC faradaic
#   efficiency is now 1 - (chlorine share) - (metal-dissolution share), and the
#   chlorine share comes from the chloride mass-transport limit on this tab.
#   None of it depends on pH, so there is no circularity.
# ============================================================================
TKc   = T_K                                           # D4 (K)
Iappc = I_app                                         # D6 (A)
Fcc   = F_const                                       # D7 (C/mol)
VLc   = V_charge / 1000                               # D8 (L)
R_gas_chem = 8.314462618                                    # D9 (J/mol/K)


def vant_hoff(K25, dH_kJ):
    """K(T) = K25 * exp(-dH/R * (1/T - 1/298.15)), dH in kJ/mol."""
    return K25 * math.exp(-dH_kJ * 1000 / R_gas_chem * (1 / TKc - 1 / 298.15))


Ka1c   = vant_hoff(4.45e-7, 9.15)                     # D13 carbonate Ka1 (thermodynamic)
Ka2c   = vant_hoff(4.69e-11, 14.9)                    # D14 carbonate Ka2
Ka1p   = vant_hoff(7.1e-3, -8.0)                      # D15 phosphate Ka1
Ka2p   = vant_hoff(6.31e-8, 3.6)                      # D16 phosphate Ka2
Ka3p   = vant_hoff(4.2e-13, 16.0)                     # D17 phosphate Ka3
Ka_NH4 = vant_hoff(5.6e-10, 52.2)                     # D18 ammonium Ka
Kw_w   = vant_hoff(1e-14, 55.8)                       # D19 water Kw
Ka_HOCl = vant_hoff(2.8840315031266057e-8, 13.8)      # D20 hypochlorous Ka
pKa_HOCl = -math.log10(Ka_HOCl)                       # D21


PT_mc02  = mc["Na2HPO4"] / MW["Na2HPO4"] + mc["NaH2PO4_2H2O"] / MW["NaH2PO4_2H2O"]  # D35
# BUGFIX (review 2026-06-26): the divalent strong cations Mg2+ and Ca2+ were
# missing from the cation sum while their SO4(2-) was subtracted in the anion
# bracket, so each wrongly contributed -2 to SID (~7.6 mM too low -> MC02 pH
# ~0.34 too acidic). Mg/Ca are strong, pH-independent ions and belong in SID
# (NH4+ is correctly excluded - it is handled dynamically via the pH_NT term).
# The UdG SID below already had them and is unaffected.
SID_mc02 = ((2 * mc["Na2HPO4"] / MW["Na2HPO4"] + mc["NaH2PO4_2H2O"] / MW["NaH2PO4_2H2O"]
             + 2 * mc["K2SO4"] / MW["K2SO4"]
             + 2 * mc["MgSO4_7H2O"] / MW["MgSO4_7H2O"] + 2 * mc["CaSO4_2H2O"] / MW["CaSO4_2H2O"])
            - 2 * (mc["NH42SO4"] / MW["NH42SO4"] + mc["MgSO4_7H2O"] / MW["MgSO4_7H2O"]
                   + mc["K2SO4"] / MW["K2SO4"] + mc["CaSO4_2H2O"] / MW["CaSO4_2H2O"]))  # D36
NT_mc02  = 2 * mc["NH42SO4"] / MW["NH42SO4"]                                            # D37
Cl_mc02  = 0.0                                                                          # D38

PT_udg  = udg["KH2PO4"] / MW["KH2PO4"] + udg["Na2HPO4"] / MW["Na2HPO4"]                 # D39
SID_udg = ((udg["NaHCO3"] / MW["NaHCO3"] + 2 * udg["Na2HPO4"] / MW["Na2HPO4"]
            + udg["KH2PO4"] / MW["KH2PO4"] + 2 * udg["MgSO4_7H2O"] / MW["MgSO4_7H2O"]
            + 2 * udg["CaCl2"] / MW["CaCl2"])
           - (2 * (udg["NH42SO4"] / MW["NH42SO4"] + udg["MgSO4_7H2O"] / MW["MgSO4_7H2O"])
              + 2 * udg["CaCl2"] / MW["CaCl2"]))                                        # D40
NT_udg  = 2 * udg["NH42SO4"] / MW["NH42SO4"]                                            # D41
Cl_udg  = 2 * udg["CaCl2"] / MW["CaCl2"]                                                # D42

# AMYBO03 (AMYBO03 D54:D57): SID as MC02 - strong cations less all sulfate; sulfuric acid in the
# stocks removes two equivalents per mole; trace metal sulfates and molybdate cancel.
PT_amy  = (_a["Na2HPO4"] + _a["NaH2PO4_2H2O"]) / 1000                                    # D54
SID_amy = ((2 * _a["Na2HPO4"] + _a["NaH2PO4_2H2O"] + _a["NaHCO3"] + 2 * _a["K2SO4"]
            + 2 * _a["CaSO4_2H2O"] + 2 * _a["MgSO4_7H2O"]) / 1000
           - 2 * (_a["K2SO4"] + _a["CaSO4_2H2O"] + _a["MgSO4_7H2O"] + _a["NH42SO4"]) / 1000
           - 2 * amy_H2SO4 / 1e6)                                                       # D55
NT_amy  = 2 * _a["NH42SO4"] / 1000                                                      # D56
Cl_amy  = 0.0                                                                           # D57



pH_SID = _by_media(SID_mc02, SID_udg, SID_amy) + alk_add_M     # D44 recipe SID + added alkalinity
pH_PT  = _by_media(PT_mc02, PT_udg, PT_amy)                   # D45
pH_NT  = _by_media(NT_mc02, NT_udg, NT_amy)                   # D46
pH_Cl  = _by_media(Cl_mc02, Cl_udg, Cl_amy)                   # D47

# --- chlorine current: the binding limit of efficiency vs chloride arrival ---
FE_CER   = 0.5                                         # D128 max CER efficiency (high-Cl plateau)
D_O2_cl  = 10 ** (HB_a + HB_b / T_K - (HB_c / T_K) ** 2) / 10000   # = Mass Transfer D32 via Electrochemistry D81 (Chemistry D274)
D_Cl     = 2.032e-9                                    # D277 (m2/s) CRC Vanysek, 25 C
km_Cl    = km_O2 * (D_Cl / D_O2_cl) ** km_exp          # D129 (cm/s) scaled from km_O2 by D^0.644
A_anode  = A_anode_wet                                 # D130 (cm2) <- Electrochemistry D46
I_Cl_FE  = Iappc * FE_CER                              # D131 (A) efficiency-limited
n_e_Cl   = 2                                           # D148 electrons per produced HOCl (moved above D132: R1-03)
k_Cl_turn = km_Cl * A_anode / 1000 / VLc              # D271 (1/s) transport-limited chloride turnover, km.A/V
tau_NH2Cl_default = 1                                  # Chemistry D314 (h) weak central estimate
M_Cl2_mg  = 70906                                       # Chemistry D223 (mg/mol)
TAU_CAL = []  # Calibrations rows 181-188: (reactor, medium, plateau mg/L as Cl2, k_Cl_turn 1/s, Cl pool mol/L, P_Cl_max mol/L/s, include); tab empty


def tau_from_dpd(C_Cl2_mgL, k_turn, Cl_pool, P_max):
    """Calibrations column I (h): invert the steady state B = min(C k tau/(1+k tau), P tau) for tau.
    Both branches increase with tau, so tau = max of the two inverses; NA when B reaches the pool."""
    B = C_Cl2_mgL / M_Cl2_mg
    if B >= Cl_pool:
        return NA
    return max(B / (k_turn * (Cl_pool - B)), B / P_max) / 3600


cal_tau_NH2Cl = (lambda ts: sum(ts) / len(ts) if ts else NA)(
    [t for t in (tau_from_dpd(C, k, pool, P) for rx, med, C, k, pool, P, inc in TAU_CAL
                 if _same(rx, Reactor_sel) and _same(med, media_sel) and _same(inc, "y")) if isnum(t)])   # Calibrations D189 (h)
tau_NH2Cl = cal_tau_NH2Cl if isnum(cal_tau_NH2Cl) else tau_NH2Cl_default   # D142 (h) monochloramine residence
P_Cl_max = I_Cl_FE / (n_e_Cl * Fcc * VLc)              # Chemistry D315 (mol/L/s) efficiency-limited production, tau-independent
Cl_bound = min(pH_Cl * k_Cl_turn * tau_NH2Cl * 3600 / (1 + k_Cl_turn * tau_NH2Cl * 3600),
               I_Cl_FE / (n_e_Cl * Fcc * VLc) * tau_NH2Cl * 3600, pH_NT)
Cl_free_frac = max(0.0, 1 - Cl_bound / pH_Cl) if pH_Cl > 0 else 1.0  # D278 free share of the recycled chloride pool
I_Cl_mt  = n_e_Cl * Fcc * km_Cl * (pH_Cl * Cl_free_frac / 1000) * A_anode   # D132 (A) transport limit on FREE chloride
I_Cl     = min(I_Cl_FE, I_Cl_mt)                       # D133 (A) binding limit (mt-limited at trace Cl-)
# WAVE-4: n_e_Cl is now the constant 2 on every route (2Cl- -> Cl2 -> HOCl, and
# the direct Cl- + H2O -> HOCl route, are both 2 e- per HOCl). The n = 1 in the
# mass-transport limit above is a FLUX count of arriving chloride, not a
# stoichiometry, so the old 1-or-2 regime switch conflated two different things.


# ============================================================================
# ELECTROCHEMISTRY TAB - part C: the CALCULATED anodic split, then gas rates
#   (Electrochemistry rows 100-104, then 21-29)
# ============================================================================
ec_I_Cl     = I_Cl                                     # D101 (A)  <- Chemistry D133
ec_corr_I   = NA                                       # D102 (-)  <- Chemistry D158 (DATA GAP)
f_HOR_anode = NA                                       # D145 (-)  fraction of anodic charge lost to H2 oxidation. DATA GAP (empty cell) - measure
f_Cl_anode  = ec_I_Cl / I_app                          # D103 (-)
etaF_OER_calc = max(0.0, 1 - f_Cl_anode
                    - (ec_corr_I if isnum(ec_corr_I) else 0.0)
                    - (f_HOR_anode if isnum(f_HOR_anode) else 0.0))   # D104 (-)
etaF_OER    = etaF_OER_calc                            # D26 = IFERROR(cal_etaF_OER, etaF_OER_calc)

ec_C_H2_sat = C_H2_sat                                 # D146 (mol/m3) <- Biology D41
i_HOR_lim   = z_e_H2 * F_const * (km_O2 / 100) * ec_C_H2_sat * (A_anode_wet / 10000)   # D147 (A) H2 mass-transport limit at the anode (km_O2 stand-in)
f_HOR_lim   = i_HOR_lim / I_app                        # D148 (-) upper bound on f_HOR_anode
r_H2_HOR    = (f_HOR_anode * I_app / (z_e_H2 * F_const) * 3600
               if isnum(f_HOR_anode) else 0.0)         # D149 (mol/h) H2 re-oxidised at the anode (0 while the gap is empty)
rH2_gen    = I_app * etaF / (z_e_H2 * F_const) * 3600          # D21 (mol/h)
rO2_gen    = I_app * etaF_OER / (z_e_O2 * F_const) * 3600      # D22 (mol/h)
O2_cathode_ORR = I_app * (1 - etaF) / (n_ORR_eff * F_const) * 3600  # D28 (mol/h)
O2_net_gen = rO2_gen - O2_cathode_ORR                          # D29 (mol/h)
# R5-m2: the lag-phase cathodic O2 loss at the lag DO, through a typed reference (Electrochemistry D128-D134)
DO_lag_ref = 0.174849986629                                     # D129 (mol/m3) INPUT: last lag cycle-mean DO (a link would be circular)
DO_lag_tol = 0.05                                      # D130 (-) tolerance before DO_lag_ref must be re-entered
O2_ORR_lag = min(I_app / (n_ORR_eff * F_const) * 3600,
                 (O2_cathode_ORR if isnum(cal_etaF) else i_ORR_design / (n_ORR_eff * F_const) * 3600) * DO_lag_ref / ec_DO_design)   # D131 (mol/h) O2 reduced at the cathode during lag
O2_net_lag = rO2_gen - O2_ORR_lag                      # D132 (mol/h) net O2 to the liquid during lag
rH2_lag    = max(0.0, I_app - O2_ORR_lag / 3600 * n_ORR_eff * F_const) / (z_e_H2 * F_const) * 3600   # D133 (mol/h) H2 evolved during lag
O2_net_lag_mt = O2_net_lag                             # MT D394 <- Electrochemistry D132
rH2_lag_mt    = rH2_lag                                # MT D395 <- Electrochemistry D133
V_H2_gen   = rH2_gen / 60 * R_gas_mt * T_K / P_atm * 1e6       # D23 (mL/min)
V_O2_gen   = rO2_gen / 60 * R_gas_mt * T_K / P_atm * 1e6       # D24 (mL/min)
V_gas_total = V_H2_gen + V_O2_gen                              # D25 (mL/min)


# ============================================================================
# ELECTROCHEMISTRY TAB - part D: hydrogen peroxide (rows 90-99)
#   The 2-electron branch of the same cathodic O2 reduction that sets etaF.
#   A source term the model previously did not have at all.
# ============================================================================
M_H2O2        = 34.0147                                # D92 (g/mol)
r_H2O2        = f_HOOH * I_app * (1 - etaF) / (n_ORR_eff * F_const) * M_H2O2 * 1000 * 3600 / ec_V_L  # D93 (mg/L/h)
k_cat_cells   = 4.1e-3                                 # D94 (1/s) whole-culture catalase clearance, ~1e8 cells/mL
H2O2_ss       = r_H2O2 / (k_cat_cells * 3600)          # D95 (mg/L) growing culture
H2O2_thresh   = 0.17                                   # D97 (mg/L) 5 uM sustained slows growth (Li & Imlay 2018)
# (D96 H2O2_lag_1h, D98 t_H2O2_thresh and D99 H2O2_flag need the lag-phase DO from
#  Mass Transfer D135, so they are evaluated further down, after the schedule.)


# ============================================================================
# BIOLOGY TAB - part B: gas requirement ratios & consumption (rows 13-16, 42-44)
# ============================================================================
H2_HOR_b  = r_H2_HOR                                   # Biology D96 (mol/h) <- Electrochemistry D149
H2_cons  = max(0.0, rH2_gen - H2_HOR_b)               # D13 (mol/h) H2 reaching the culture, net of anodic re-oxidation
O2_cons  = H2_cons * bio_O2 / bio_H2                  # D14 (mol/h)
CO2_cons = H2_cons * bio_CO2 / bio_H2                 # D15 (mol/h)
O2_excess = max(0.0, O2_net_gen - O2_cons)            # D16 (mol/h) floored: pole at the knallgas cap
t_H2_sat = C_H2_sat * (V_charge / 1e6) / rH2_gen * 60          # D42 (min)
H2_turnover = rH2_gen / (V_charge / 1e6) / C_H2_sat   # D43 (1/h)
H2_safety = "EXPLOSIVE" if H2_turnover > 1 else "watch"        # D44


# ============================================================================
# CHEMISTRY TAB - part B: solution conductivity (Kohlrausch sum, rows 165-180)
#   Feeds the ohmic term of the cell-voltage budget.
# ============================================================================
lam_Na, lam_K, lam_NH4 = 50.08, 73.48, 73.5           # D166, D167, D168 (S.cm2/mol)
lam_Mg, lam_Ca         = 106.0, 118.94                # D169, D170 (per mol, i.e. z^2-weighted already)
lam_H2PO4, lam_HPO4    = 36.0, 114.0                  # D171, D172
lam_SO4, lam_HCO3, lam_Cl = 160.0, 44.5, 76.31        # D173, D174, D175
kappa0_mc02 = ((2 * mc["Na2HPO4"] / MW["Na2HPO4"] * lam_Na
                + mc["NaH2PO4_2H2O"] / MW["NaH2PO4_2H2O"] * lam_Na
                + 2 * mc["K2SO4"] / MW["K2SO4"] * lam_K
                + 2 * mc["NH42SO4"] / MW["NH42SO4"] * lam_NH4
                + mc["MgSO4_7H2O"] / MW["MgSO4_7H2O"] * lam_Mg
                + mc["CaSO4_2H2O"] / MW["CaSO4_2H2O"] * lam_Ca
                + mc["Na2HPO4"] / MW["Na2HPO4"] * lam_HPO4
                + mc["NaH2PO4_2H2O"] / MW["NaH2PO4_2H2O"] * lam_H2PO4
                + (mc["K2SO4"] / MW["K2SO4"] + mc["MgSO4_7H2O"] / MW["MgSO4_7H2O"]
                   + mc["CaSO4_2H2O"] / MW["CaSO4_2H2O"]
                   + mc["NH42SO4"] / MW["NH42SO4"]) * lam_SO4) / 10)          # D176 (S/m)
kappa0_udg = (((udg["NaHCO3"] / MW["NaHCO3"] + 2 * udg["Na2HPO4"] / MW["Na2HPO4"]) * lam_Na
               + udg["KH2PO4"] / MW["KH2PO4"] * lam_K
               + 2 * udg["NH42SO4"] / MW["NH42SO4"] * lam_NH4
               + udg["MgSO4_7H2O"] / MW["MgSO4_7H2O"] * lam_Mg
               + udg["CaCl2"] / MW["CaCl2"] * lam_Ca
               + udg["Na2HPO4"] / MW["Na2HPO4"] * lam_HPO4
               + udg["KH2PO4"] / MW["KH2PO4"] * lam_H2PO4
               + (udg["MgSO4_7H2O"] / MW["MgSO4_7H2O"]
                  + udg["NH42SO4"] / MW["NH42SO4"]) * lam_SO4
               + udg["NaHCO3"] / MW["NaHCO3"] * lam_HCO3
               + 2 * udg["CaCl2"] / MW["CaCl2"] * lam_Cl) / 10)               # D177 (S/m)
kappa0_amy = (((2 * _a["Na2HPO4"] + _a["NaH2PO4_2H2O"] + _a["NaHCO3"]) * lam_Na
               + 2 * _a["K2SO4"] * lam_K + 2 * _a["NH42SO4"] * lam_NH4
               + _a["MgSO4_7H2O"] * lam_Mg + _a["CaSO4_2H2O"] * lam_Ca
               + _a["Na2HPO4"] * lam_HPO4 + _a["NaH2PO4_2H2O"] * lam_H2PO4
               + _a["NaHCO3"] * lam_HCO3
               + (_a["K2SO4"] + _a["CaSO4_2H2O"] + _a["MgSO4_7H2O"] + _a["NH42SO4"]) * lam_SO4) / 1000
              + (amy_Fe + amy_H2SO4 + sum(amy_TM)) / 1e6 * lam_SO4) / 10                # AMYBO03 D58 (S/m), trace sulfates included
kappa_fI  = 0.78                                      # D178 (-) Lambda/Lambda0 at I ~ 0.1 M
kappa_TC  = 0.02                                      # D179 (1/K) +2 %/K, ISO 7888
kappa_med = ((_by_media(kappa0_mc02, kappa0_udg, kappa0_amy) + alk_add_M * (lam_Na + lam_HCO3) / 10)
             * kappa_fI * (1 + kappa_TC * (TKc - 298.15)))  # D180, added NaHCO3 in the Kohlrausch sum

# --- ionic strength & Davies activity coefficients (rows 182-197) ---
A_DH    = 1.82e6 * (78.54 * (298.15 / TKc) ** 1.368) ** -1.5 * TKc ** -1.5     # D186 (-)
_davies = math.sqrt(I_ionic) / (1 + math.sqrt(I_ionic)) - 0.3 * I_ionic
gam1 = 10 ** (-A_DH * 1 * _davies)                    # D187
gam2 = 10 ** (-A_DH * 4 * _davies)                    # D188
gam3 = 10 ** (-A_DH * 9 * _davies)                    # D189
# Thermodynamic constants -> the concentration scale the charge balance solves on.
Ka1c_c   = Ka1c / gam1 ** 2                           # D190  CO2(aq) -> H+ + HCO3-
Ka2c_c   = Ka2c / gam2                                # D191  HCO3- -> H+ + CO3(2-)
Ka1p_c   = Ka1p / gam1 ** 2                           # D192  H3PO4 -> H+ + H2PO4-
Ka2p_c   = Ka2p / gam2                                # D193  H2PO4- -> H+ + HPO4(2-)
Ka3p_c   = Ka3p * gam2 / (gam1 * gam3)                # D194  HPO4(2-) -> H+ + PO4(3-)
Kw_c     = Kw_w / gam1 ** 2                           # D195
KaHOCl_c = Ka_HOCl / gam1 ** 2                        # D196
KaN_c    = Ka_NH4                                     # D197  charges cancel exactly

# --- R2-m3: bicarbonate storage in the CO2 pool (Chemistry D290-D296) ---
pH_ref_DIC  = 6.35994620453                                    # D291 (pH) reference pH for the DIC capacity (input; re-enter if pH moves by >0.1)
h_ref_DIC   = 10 ** -pH_ref_DIC                       # D292 (mol/L)
r_HCO3_ref  = Ka1c_c / h_ref_DIC                      # D293 (-) [HCO3-]/[CO2(aq)] at the reference pH
HCO3_ref    = (pH_SID + pH_NT * h_ref_DIC / (h_ref_DIC + KaN_c) + h_ref_DIC
               - (pH_PT * Ka1p_c * h_ref_DIC ** 2 + 2 * pH_PT * Ka1p_c * Ka2p_c * h_ref_DIC
                  + 3 * pH_PT * Ka1p_c * Ka2p_c * Ka3p_c)
               / (h_ref_DIC ** 3 + Ka1p_c * h_ref_DIC ** 2 + Ka1p_c * Ka2p_c * h_ref_DIC + Ka1p_c * Ka2p_c * Ka3p_c)
               - Kw_c / h_ref_DIC) / (1 + 2 * Ka2c_c / h_ref_DIC)   # D294 (mol/L) bicarbonate from the charge balance at the reference pH
beta_nonC   = math.log(10) * (pH_PT * Ka1p_c * h_ref_DIC / (Ka1p_c + h_ref_DIC) ** 2
                              + pH_PT * Ka2p_c * h_ref_DIC / (Ka2p_c + h_ref_DIC) ** 2
                              + pH_NT * KaN_c * h_ref_DIC / (KaN_c + h_ref_DIC) ** 2
                              + h_ref_DIC + Kw_c / h_ref_DIC)       # D295 (mol/L/pH) non-carbonate buffer capacity
DIC_cap     = 1 + r_HCO3_ref * beta_nonC / (beta_nonC + math.log(10) * HCO3_ref)   # D296 (-) total-DIC / CO2(aq) capacity of the liquid


# ============================================================================
# ELECTROCHEMISTRY TAB - part E: cell-voltage budget (rows 105-122)
#   Reversible voltage + both Tafel overpotentials + the phosphate-buffer
#   (PCET) credit + the ohmic drop, against the 5 V LED drive rail.
# ============================================================================
E0_OER      = 1.229                                    # Chemistry D201 (V vs SHE)
ec_E_rev    = E0_OER                                   # D106 (V) E_OER - E_HER, pH-independent
b_anode     = 0.12                                     # D107 (V/decade) OER on Pt
j0_anode    = 1e-10                                    # D108 (A/cm2) OER on Pt - spans 1e-9..1e-11
b_cath      = 0.14                                     # D109 (V/decade) HER on stainless
j0_cath     = 1.5e-6                                   # D110 (A/cm2) HER on stainless, buffered pH 7.5
eta_anode   = b_anode * math.log10(j_anode / 1000 / j0_anode)     # D111 (V)
eta_cath    = b_cath * math.log10(j_cathode / 1000 / j0_cath)     # D112 (V)
pcet_credit = -0.15                                    # D113 (V) neutral-pH OER via the buffer base
ec_kappa    = kappa_med                                # D114 (S/m) <- Chemistry D180
ec_gap      = elec_gap                                 # D115 (mm)  <- Geometry D92
k_geom      = 1.0                                      # D116 (-) unbounded-electrolyte correction (R1-06: was 2, a double count; Gerrit-validated range now consistent)
R_cell      = k_geom * math.acosh(ec_gap / anode_dia) / (math.pi * ec_kappa * (L_sub / 1000))  # D117 (ohm)
V_IR        = I_app * R_cell                           # D118 (V)


# ============================================================================
# CO2 FLOWS TAB - calibration aggregation for the active reactor
#   latest_date, flowrate_cal, min_sparge_cal, has_cal come from SUMPRODUCTs
#   over rows keyed on Reactor with column J (nominal flowrate) > 0.
#   For ed04 the only J>0 row is the header calibration row (date 46190,
#   J=3.33 ml/s, I=0.25 s). Re-derived from that calibration record.
# ============================================================================
# (Reactor, date, min_sparge I, nominal_flow J) records where J is populated:
CO2_CAL = [
    ("ed04", 46190, 0.25, 3.33),
]
CO2_FIT = [  # (Reactor, volume mL = CO2 flows E, time s = CO2 flows F, excluded = CO2 flows N); rows with F blank/0 omitted
    ("ed04", 50.0, 15.0, 0),  # CO2 flows row 5
    ("ed04", 12.0, 4.0, 0),  # CO2 flows row 7
    ("ed04", 14.0, 4.0, 0),  # CO2 flows row 8
    ("ed04", 14.0, 4.0, 0),  # CO2 flows row 9
    ("ed04", 6.0, 2.0, 0),  # CO2 flows row 11
    ("ed04", 9.0, 2.0, 0),  # CO2 flows row 12
    ("ed04", 6.0, 2.0, 0),  # CO2 flows row 13
    ("ed04", 8.0, 2.0, 0),  # CO2 flows row 14
    ("ed04", 6.0, 2.0, 0),  # CO2 flows row 15
    ("ed04", 10.0, 2.0, 0),  # CO2 flows row 16
    ("ed04", 4.0, 1.0, 0),  # CO2 flows row 18
    ("ed04", 4.0, 1.0, 0),  # CO2 flows row 19
    ("ed04", 3.0, 1.0, 0),  # CO2 flows row 20
    ("ed04", 4.0, 1.0, 0),  # CO2 flows row 21
    ("ed04", 4.0, 1.0, 0),  # CO2 flows row 22
    ("ed04", 4.0, 1.0, 0),  # CO2 flows row 23
    ("ed04", 2.0, 0.5, 0),  # CO2 flows row 25
    ("ed04", 2.0, 0.5, 0),  # CO2 flows row 26
    ("ed04", 2.0, 0.5, 0),  # CO2 flows row 27
    ("ed04", 2.0, 0.5, 0),  # CO2 flows row 28
    ("ed04", 2.0, 0.5, 0),  # CO2 flows row 29
    ("ed04", 1.0, 0.25, 0),  # CO2 flows row 30
    ("ed04", 1.0, 0.25, 0),  # CO2 flows row 31
    ("ed04", 1.0, 0.25, 0),  # CO2 flows row 32
    ("ed04", 1.0, 0.25, 0),  # CO2 flows row 33
    ("ed04", 1.0, 0.25, 0),  # CO2 flows row 34
    ("ed04", 0.4, 0.2, 1),  # CO2 flows row 36 (red outlier, column N = 1)
    ("ed04", 0.8, 0.2, 0),  # CO2 flows row 37
    ("ed04", 1.0, 0.2, 0),  # CO2 flows row 38
    ("ed04", 0.8, 0.2, 0),  # CO2 flows row 39
    ("ed04", 0.4, 0.1, 0),  # CO2 flows row 41
    ("ed04", 0.4, 0.1, 0),  # CO2 flows row 42
    ("ed04", 0.6, 0.1, 0),  # CO2 flows row 43
    ("ed04", 0.6, 0.1, 0),  # CO2 flows row 44
    ("ed04", 0.6, 0.1, 0),  # CO2 flows row 45
    ("ed04", 0.2, 0.1, 1),  # CO2 flows row 46 (red outlier, column N = 1)
]
CO2_CARRY = []                                         # (Reactor, max flow without carryover mL/s) = CO2 flows column M; none entered (data gap)
_cal_rows = [r for r in CO2_CAL if r[0] == Reactor_sel and r[3] > 0]
# Calibrations tab, CO2-flow section (R5-M1): flow (cal_flow, column F) and Min pulse (cal_pulse_floor,
# column J) are "most recent included run for the active reactor". The tab is empty in the shipped
# workbook, so both are None here; the precedence below is the workbook's.
cal_flow        = None                                 # Calibrations cal_flow (mL/s) - no included run
cal_pulse_floor = None                                 # Calibrations D61 cal_pulse_floor (s) - no included run
pulse_floor_default = 0.25                             # MT D396 (s) solenoid floor when no minimum pulse is recorded
has_cal      = len(_cal_rows) + (1 if isnum(cal_flow) else 0)   # MT D119
latest_date  = max((r[1] for r in _cal_rows), default=0)  # MT D116
_latest = [r for r in _cal_rows if r[1] == latest_date]
_n_latest = max(1, len(_latest))
flowrate_cal   = (cal_flow if isnum(cal_flow)
                  else sum(r[3] for r in _latest) / _n_latest if _latest else 0.0)  # MT D117 (ml/s)
min_sparge_cal = (cal_pulse_floor if isnum(cal_pulse_floor)
                  else sum(r[2] for r in _latest) / _n_latest if _cal_rows
                  else pulse_floor_default)            # MT D118 (s)
cal_source_txt = " (flow from the Calibrations tab)" if isnum(cal_flow) else " (flow from CO2 flows)"


# ============================================================================
# MASS TRANSFER TAB
#   WAVE-4: the water properties are now functions of the reactor temperature
#   rather than constants frozen at 30 degC (rows 166-175).
# ============================================================================
stir_len  = stir_bar_L                                # D5 (mm)  (from Geometry)
sigma_0, sigma_k = 0.07589, -0.000157                 # D167, D168 IAPWS R1-76(2014) linear fit
rho_0,   rho_k   = 1003.33, -0.2556                   # D169, D170 IAPWS-95 linear fit
D_CO2_ref = 1.92e-9                                   # D174 (m2/s) CO2 in water at 25 degC
Ea_D_CO2  = 19000.0                                   # D175 (J/mol) Arrhenius / Stokes-Einstein equivalent
sigma     = sigma_0 + sigma_k * (T_K - 273.15)        # D29 (N/m)
rho_L     = rho_0 + rho_k * (T_K - 273.15)            # D30 (kg/m3)
g_const   = 9.80665                                   # D31 (m/s2)
D_O2      = 10 ** (HB_a + HB_b / T_K - (HB_c / T_K) ** 2) / 10000   # D32 (m2/s)
M_CO2     = 44.0095                                   # D103 (g/mol)
R_gas     = R_gas_mt                                  # D101 (J/mol/K)

POR_UM = [205, 130, 70, 28, 13, 1.3]                  # grades 0..5 (D33:D38)
por_pore = POR_UM[por_grade_e] / 1e6                  # D39 (m)
spg_name_1, spg_name_2 = "Tube", "Sintered"           # D27, D28
tube_d_m = spg_ID / 1000                              # D40 (m)
if sparger_e == spg_name_1:
    d_orifice = tube_d_m
elif sparger_e == spg_name_2:
    d_orifice = por_pore
else:
    d_orifice = NA                                    # D41 (m)

d_bubble    = (6 * d_orifice * sigma / (rho_L * g_const)) ** (1 / 3)  # D42 (m)
d_bubble_mm = d_bubble * 1000                          # D43 (mm)
mend_a = 2.14                                          # D44
mend_b = 0.505                                         # D45
u_rise = math.sqrt(mend_a * sigma / (rho_L * d_bubble) + mend_b * g_const * d_bubble)  # D46

# --- CO2 dosing & schedule (folded from old Dosing sheet) ---
Reactor   = Reactor_sel                                # D115
Q_CO2     = flowrate_cal * 60 if has_cal > 0 else NA   # D102 (mL/min)
nCO2_rate = P_atm * (Q_CO2 / 1e6 / 60) / (R_gas * T_K) # D104 (mol/s)
pulse_floor = min_sparge_cal                           # D99 (s)
flush_factor = 1.0                                     # D106

# --- R2-M3: delivered pulse volume V = V0 + Q*t, least squares over this reactor's CO2 flows points (MT D401-D411) ---
_fit = [(v, t) for (r, v, t, ex) in CO2_FIT if r == Reactor_sel and t > 0 and ex != 1]
fit_n   = len(_fit)                                    # D401 (points used)
fit_St  = sum(t for v, t in _fit)                      # D402 (s)
fit_SV  = sum(v for v, t in _fit)                      # D403 (mL)
fit_Stt = sum(t * t for v, t in _fit)                  # D404 (s2)
fit_StV = sum(t * v for v, t in _fit)                  # D405 (mL.s)
fit_n_min = 3                                          # D406 (minimum points for the fit; fewer -> no-intercept fallback)
_fit_ok = fit_n >= fit_n_min and fit_n * fit_Stt - fit_St ** 2 > 0
Q_CO2_fit = (cal_flow if isnum(cal_flow)
             else (fit_n * fit_StV - fit_St * fit_SV) / (fit_n * fit_Stt - fit_St ** 2)
             if _fit_ok else Q_CO2 / 60)               # D407 (mL/s) slope; a Calibrations flow takes precedence; fallback = nominal flow
pulse_V0  = (0.0 if isnum(cal_flow)
             else (fit_SV - Q_CO2_fit * fit_St) / fit_n if _fit_ok else 0.0)   # D408 (mL) valve-opening intercept (0 with a Calibrations flow)
kLa_meas  = 0.0                                        # D97 (1/h)

# --- surface stripping path (kL_surf) ---
stir_rpm   = stir_rpm_set                              # D67 (1/min)
tip_speed  = math.pi * (stir_len / 1000) * stir_rpm / 60   # D68 (m/s)
s_renew    = tip_speed / (vial_ID / 1000)              # D69 (1/s)
kL_surf    = 2 * math.sqrt(D_O2 * s_renew / math.pi)   # D70 (m/s)
a_surf     = interface_A / V_charge                    # D71 (1/m)
kLa_surf   = kL_surf * a_surf                          # D72 (1/s)
kLa_surf_used = kLa_meas / 3600 if kLa_meas > 0 else kLa_surf  # D98 (1/s)
surf_strip = kLa_surf_used * (V_charge / 1e6) * O2_ceil_C * 3600  # D73 (mol/h)

# --- target / margin inputs ---
target_DO_frac = DO_frac_target                        # D84 <- Biology D60 (one definition)
carbon_margin_min = 2.0                                # D85

# --- duty floors & the two interval caps -------------------------------------
duty_carbon = carbon_margin_min * CO2_cons / (nCO2_rate * 3600)        # D86
# Worst-case O2 source the safety guards size on: net O2 generation with the
# surface-strip credit WITHHELD (kL_surf is a ~375%-uncertain best-case proxy
# and must never gate a safety guard).
O2_src_guard = O2_net_gen                              # D132 (mol/h)
duty_O2vent = O2_src_guard / (target_DO_frac * (O2_ceil_Pa / P_atm)) / (nCO2_rate * 3600)  # D87
duty_opt    = max(duty_carbon, duty_O2vent)            # D88
spg_int_max = (target_DO_frac * O2_ceil_C * (V_charge / 1e6)
               / O2_src_guard * 60)                                   # D89 (min) lag-accumulation cap
spg_dur_opt = max(pulse_floor, (flush_factor * headspace_V - pulse_V0) / Q_CO2_fit)  # D90 (s)
spg_dur_eq_opt = (pulse_V0 + Q_CO2_fit * spg_dur_opt) / (Q_CO2 / 60)   # D409 (s) full-flow-equivalent time of the optimal pulse (delivered volume / nominal flow)
spg_int_carbon = spg_dur_eq_opt / (60 * duty_carbon)   # D112 (min) - carbon-limited

# --- WAVE-4: headspace O2 balance and the DO-LIMITED interval (rows 177-188) --
# The SURFACE-HELD / SPARGE-NEEDED branch is gone. Dissolved O2 can never fall
# below equilibrium with the headspace, so the schedule's job is to dilute
# oxygen OUT of the headspace with CO2. kL_surf now moves the answer
# continuously instead of switching which formula runs.
CO2_rate_full = nCO2_rate * 3600                       # D178 (mol/h) sparge line at 100% duty

# --- iterH: ONE headspace balance (MT rows 300-382) shared by the O2 block, the
# CO2 pool and the lag flammability block. The headspace is a well-mixed volume
# at 1 atm fed by CO2 pulses, gas evolved from the liquid and (one vent model
# only) exchanged air; drained by the vent and the fixation sink.
headspace_V_m3 = headspace_V / 1e6                      # MT D140 (m3)
Q_vent         = 0.5                                    # MT D142 (mL/min) restricted vent bleed / TOTAL air ingress - KEY UNCERTAIN PARAMETER, measure. INPUT
n_hs_gas       = P_dry * headspace_V_m3 / (R_gas * T_K) # MT D150 (mol) headspace gas inventory
vent_model     = vent_model_sel                         # MT D301 <- Summary D111
vent_name_1, vent_name_2 = "Outflow only", "Air exchange"   # MT D302, D303
vent_name_3    = "Open vent"                            # MT D384 third vent option
Q_backdraw     = 0.015                                  # MT D385 (mL/min) open-vent back-draw air - MEASURE (schedule-dependent). INPUT
Q_vent_used    = (0.0 if vent_model == vent_name_1
                  else Q_backdraw if vent_model == vent_name_3
                  else Q_vent if vent_model == vent_name_2
                  else NA)                              # MT D386 (mL/min) air ingress for the selected vent model
H2_HOR_mt      = r_H2_HOR                               # MT D387 (mol/h) <- Electrochemistry D149
O2_sizing_phase = O2_phase_sel                          # MT D304 <- Summary D112
phase_name_1, phase_name_2 = "Growth", "Lag"            # MT D305, D306
y_O2_air       = 0.2095                                 # MT D307 (-) dry-air O2 mole fraction
F_vent_ex      = P_atm * (Q_vent_used / 1e6 / 60) / (R_gas * T_K) * 3600   # MT D308 (mol/h) air exchanged through the vent (NaN for an invalid selector)
F_N2           = P_atm * (N2_sweep_set / 1e6 / 60) / (R_gas * T_K) * 3600  # MT D424 (mol/h) N2 sweep, same reference as F_vent_ex
F_dil          = F_vent_ex + F_N2                       # MT D425 (mol/h) non-pulse inflow; only the air part carries O2 and CO2
O2_src_g       = O2_excess                              # MT D309 (mol/h)
O2_src_l       = O2_net_lag_mt                          # MT D310 (mol/h) lag: net of the cathodic loss at DO_lag_ref
H2_src_g       = max(0.0, rH2_gen - H2_HOR_mt - H2_cons)   # MT D313 (mol/h) (MT D311 rH2_gen, D312 H2_cons imported)
H2_src_l       = max(0.0, rH2_lag_mt - H2_HOR_mt)       # MT D314 (mol/h) lag: lag-DO H2 net of anodic H2 oxidation
H2_src_l_b     = H2_src_l                               # Biology D113 <- MT D314
O2_src_l_b     = O2_src_l                               # Biology D115 <- MT D310
CO2_fix_g      = CO2_cons                               # MT D315 (mol/h)
CO2_fix_l      = 0.0                                    # MT D316 (mol/h)
def _by_phase(g_val, l_val):
    """IF(O2_sizing_phase=phase_name_1, g, IF(O2_sizing_phase=phase_name_2, l, NA()))."""
    return g_val if O2_sizing_phase == phase_name_1 else l_val if O2_sizing_phase == phase_name_2 else NA
O2_src_sched   = _by_phase(O2_src_g, O2_src_l)          # MT D317 (mol/h)
H2_src_sched   = _by_phase(H2_src_g, H2_src_l)          # MT D318 (mol/h)
CO2_fix_sched  = _by_phase(CO2_fix_g, CO2_fix_l)        # MT D319 (mol/h)
flush_vol_opt  = nCO2_rate * spg_dur_eq_opt / n_hs_gas     # MT D320 (-) headspace volumes per optimal pulse
flush_ret_opt  = math.exp(-flush_vol_opt)               # MT D321 (-)
saw_factor     = flush_vol_opt * (1 + flush_ret_opt) / (2 * (1 - flush_ret_opt))   # MT D322 (-) time-mean / flux-mean headspace O2
DO_surf_excess = O2_src_sched / (kLa_surf_used * 3600 * (V_charge / 1e6))  # D180 (mol/m3) sizing phase
DO_surf_excess_lag = O2_src_l / (kLa_surf_used * 3600 * (V_charge / 1e6))  # D181 (mol/m3)
hs_O2_allow   = DO_target - DO_surf_excess             # D182 (mol/m3)
y_O2_star     = (hs_O2_allow / (H_O2_T * P_dry)) if hs_O2_allow > 0 else NA   # D183 (-)
duty_DO       = (max(0.0, ((O2_src_sched + y_O2_air * F_vent_ex) * saw_factor / y_O2_star
                            - F_dil - O2_src_sched - H2_src_sched + CO2_fix_sched) / CO2_rate_full)
                 if isnum(y_O2_star) else NA)          # D184 (-) flux mean at y*/saw_factor -> cycle mean at target
spg_int_DO    = ((spg_dur_eq_opt / (60 * duty_DO) if duty_DO > 0 else spg_int_carbon)
                 if isnum(duty_DO) else NA)            # D185 (min); duty 0 -> carbon-limited interval
kLa_surf_req  = O2_src_sched / (DO_target * 3600 * (V_charge / 1e6))          # D186 (1/s)

pulse_res   = 0.05                                     # MT D241 (s) solenoid timing resolution
def _mround(x, m):
    """Excel MROUND (half away from zero)."""
    return float((Decimal(repr(x)) / Decimal(repr(m))).quantize(Decimal(1), rounding=ROUND_HALF_UP)) * m
spg_dur_run = max(pulse_floor, _mround(spg_dur_opt, pulse_res))   # MT D242 (s) pulse duration as actually run
# --- schedule mode resolution: Summary 'Your setting' override > Manual cells > Optimal ---
sched_mode   = "Optimal"                               # D81
spg_dur_man  = 1.0                                     # D82 (s)
spg_int_man  = 1.0                                     # D83 (min)
user_spg_dur = None                                    # Summary G13 (blank -> recommended)
user_spg_int = None                                    # Summary G15 (blank -> recommended)
spg_dur = (user_spg_dur if (isnum(user_spg_dur) and user_spg_dur > 0)
           else (spg_dur_man if sched_mode == "Manual" else spg_dur_run))   # D121
pH_band_hi = 7.5                                        # Chemistry D237 (pH) HOB band upper edge
pCO2_air       = 40.0                                   # MT D139 (Pa) atmospheric pCO2 ~400 ppm INPUT

# --- pH-ceiling interval (Chemistry D320-D324, MT D428-D539): the longest interval whose cycle-mean
#     dissolved CO2 still holds the probe pH at the band ceiling. Binds only when something other than CO2
#     dilutes the headspace (an N2 sweep, D98). The CO2-pool constants do not depend on the interval, so
#     they are evaluated here, ahead of the schedule; they equal MT D193-D195/D380 (checked in the tests).
pH_hi_c  = pH_band_hi + math.log10(gam1)                 # Chemistry D321 (pH, concentration scale)
h_hi     = 10 ** -pH_hi_c                                # Chemistry D322 (mol/L)
resid_noC_hi = (pH_SID + pH_NT * h_hi / (h_hi + KaN_c) + h_hi
                - (pH_PT * Ka1p_c * h_hi ** 2 + 2 * pH_PT * Ka1p_c * Ka2p_c * h_hi + 3 * pH_PT * Ka1p_c * Ka2p_c * Ka3p_c)
                / (h_hi ** 3 + Ka1p_c * h_hi ** 2 + Ka1p_c * Ka2p_c * h_hi + Ka1p_c * Ka2p_c * Ka3p_c)
                - Kw_c / h_hi)                           # Chemistry D323 (mol/L) charge balance without the carbonate terms
CO2_pH_hi = max(0.0, resid_noC_hi) / (Ka1c_c / h_hi + 2 * Ka1c_c * Ka2c_c / h_hi ** 2)   # Chemistry D324 (mol/L)
_flush_ret_e = math.exp(-(P_atm * ((pulse_V0 + Q_CO2_fit * spg_dur) / 1e6) / (R_gas * T_K)) / n_hs_gas)   # = MT D324
_F_gap_e  = F_dil + max(0.0, O2_src_sched + H2_src_sched - CO2_fix_sched)   # = MT D371
_V_L_CO2_e = V_charge / 1e6 * DIC_cap                    # = MT D416
_Vg_e     = headspace_V_m3 / (H_CO2_T * R_gas * T_K)     # = MT D192
_Csat_e, _Cair_e = H_CO2_T * P_dry, H_CO2_T * pCO2_air   # = MT D145, D146
_pool_a_e = _V_L_CO2_e / (_V_L_CO2_e + _Vg_e)
_pool_b_e = _Csat_e * (1 - _pool_a_e) * (1 - _flush_ret_e)
_pool_ret_e = _pool_a_e + (1 - _pool_a_e) * _flush_ret_e
_k_eff_e  = _F_gap_e / 3600 / n_hs_gas * _Vg_e / (_V_L_CO2_e + _Vg_e)   # = MT D195


def co2_mean_at(t_min):
    """MT grid columns B-I: cycle-mean dissolved CO2 (mol/m3) at a trial interval, as D198-D200/D162."""
    t_off = max(0.0, t_min * 60 - spg_dur)
    x = _k_eff_e * t_off
    e = math.exp(-x)
    phi = (1 - e) / x if x > 0 else 1.0
    psi = (x - 1 + e) / x ** 2 if x > 0 else 0.5
    D_raw = (_Cair_e / _Csat_e * F_vent_ex - CO2_fix_sched) * (t_off / 3600) / (_V_L_CO2_e + _Vg_e)
    C_start = (D_raw * phi + _pool_b_e * e) / (1 - _pool_ret_e * e)
    return min(_Csat_e, max(_Cair_e, (_pool_ret_e * C_start + _pool_b_e) * phi + D_raw * psi))


grid_t_min, grid_ratio, grid_n = 0.25, 1.09, 100        # MT D430, D431 and the 100 grid rows 440-539
pH_grid_t = [grid_t_min * grid_ratio ** i for i in range(grid_n)]
pH_grid_C = [co2_mean_at(t) for t in pH_grid_t]
CO2_pH_hi_mt = CO2_pH_hi * 1000                          # MT D429 (mol/m3)
pH_grid_start = []                                       # MT column H, CO2 at the pulse start
for _t in pH_grid_t:
    _toff = max(0.0, _t * 60 - spg_dur); _x = _k_eff_e * _toff; _e = math.exp(-_x)
    _phi = (1 - _e) / _x if _x > 0 else 1.0
    _Dr = (_Cair_e / _Csat_e * F_vent_ex - CO2_fix_sched) * (_toff / 3600) / (_V_L_CO2_e + _Vg_e)
    pH_grid_start.append((_Dr * _phi + _pool_b_e * _e) / (1 - _pool_ret_e * _e))
_cross = [math.exp(math.log(pH_grid_t[i]) + (math.log(pH_grid_t[i + 1]) - math.log(pH_grid_t[i]))
                   * (pH_grid_C[i] - CO2_pH_hi_mt) / (pH_grid_C[i] - pH_grid_C[i + 1]))
          for i in range(grid_n - 1) if pH_grid_C[i] >= CO2_pH_hi_mt > pH_grid_C[i + 1]]   # MT column J
ph_unreach = CO2_pH_hi_mt > 0 and pH_grid_C[0] < CO2_pH_hi_mt   # MT D434
if CO2_pH_hi_mt <= 0:
    spg_int_pH = "no pH bound"                           # the ceiling is out of reach even without CO2
elif ph_unreach:
    spg_int_pH = "pH above the band ceiling at any interval \u2013 reduce the N\u2082 sweep or the added alkalinity"
else:
    spg_int_pH = max(_cross) if _cross else "no pH bound"   # MT D432 (min) on the pulse in use, ln-interpolated
_dur_eq_e = (pulse_V0 + Q_CO2_fit * spg_dur) / (Q_CO2 / 60)   # = MT D410 spg_dur_eq
spg_int_pH_opt = (spg_int_pH * spg_dur_eq_opt / _dur_eq_e if isnum(spg_int_pH)
                  else "no pH bound")                    # MT D433: on the optimal-pulse basis of D91, so D420 runs spg_int_pH
_pH_cap = spg_int_pH_opt if isnum(spg_int_pH_opt) else spg_int_carbon

sel_invalid = math.isnan(F_vent_ex + O2_src_sched)     # an unlisted vent/phase selector -> #N/A in MT D91/D94/D134
spg_int_opt = (NA if sel_invalid or ph_unreach else
               min(spg_int_carbon, spg_int_DO, _pH_cap) if isnum(spg_int_DO)
               else min(spg_int_carbon, spg_int_max, _pH_cap))         # D91 (min)
spg_int_opt_s = spg_int_opt * 60                       # D92 (s)
duty_actual = spg_dur_eq_opt / (spg_int_opt * 60)      # D93 (-) full-flow-equivalent duty
if sel_invalid:
    opt_binding = "INVALID SELECTOR (Summary D111/D112)"
elif ph_unreach:
    opt_binding = "pH CEILING UNREACHABLE \u2013 reduce the N\u2082 sweep or the added alkalinity"
elif isnum(spg_int_pH_opt) and spg_int_pH_opt < min(spg_int_carbon, spg_int_DO if isnum(spg_int_DO) else spg_int_max):
    opt_binding = "pH CEILING (keeping pH at or under the band ceiling sets the interval)"
elif not isnum(spg_int_DO):
    opt_binding = "O2-INFEASIBLE \u2013 the legacy O2 flush guard (D89) sets the interval (see D134)"
elif spg_int_DO < spg_int_carbon:
    opt_binding = "O2-DILUTION (headspace O2 sets the interval)"
else:
    opt_binding = "CARBON (CO2 supply sets the interval)"   # D94
if sel_invalid:
    spg_int_regime = "INVALID SELECTOR (Summary D111/D112) \u2013 no schedule until both are listed values"
elif not isnum(spg_int_DO):
    spg_int_regime = ("DO TARGET UNREACHABLE — the surface cannot carry the O2 flux at this kLa; "
                      "no interval fixes it (raise kL_surf, lower the current, or accept a higher DO)")
elif kLa_meas > 0:
    spg_int_regime = "MEASURED kLa — DO-limited interval is " + xltext(spg_int_DO, "0.0") + " min"
else:
    spg_int_regime = ("ESTIMATED kLa — DO-limited interval is " + xltext(spg_int_DO, "0.0")
                      + " min; confirm by measuring kL_surf")   # D134

interval_res = 0.01                                   # MT D419 (min), plugin accepts decimal minutes
spg_int_run = math.floor(((pulse_V0 + Q_CO2_fit * spg_dur) / (Q_CO2 / 60)) / (60 * duty_actual) / interval_res + 1e-12) * interval_res if isnum(duty_actual) else NA
if spg_int_run * 60 <= spg_dur:
    spg_int_run = NA                                  # D420: no positive executable gap
spg_int = (user_spg_int if (isnum(user_spg_int) and user_spg_int > 0)
           else (spg_int_man if sched_mode == "Manual" else spg_int_run))   # D122
if spg_int * 60 <= spg_dur:
    spg_int = NA  # same rejected overlap as Excel, including manual and overrides
od_ok = "OK" if (spg_int * 60 - spg_dur >= 5) else "TIGHT"    # D95 (uses schedule in use)
duty    = spg_dur / (spg_int * 60)                     # D105

spg_dur_eq = (pulse_V0 + Q_CO2_fit * spg_dur) / (Q_CO2 / 60)   # D410 (s) full-flow-equivalent time of the pulse in use
V_pulse    = pulse_V0 + Q_CO2_fit * spg_dur            # D411 (mL) delivered volume per pulse
CO2_pulse  = P_atm * (V_pulse / 1e6) / (R_gas * T_K)   # D123 (mol)
pulses_h   = 60 / spg_int                               # D124 (/h)
pulses_d   = pulses_h * 24                              # D125 (/d)
CO2_supply = CO2_pulse * pulses_h                       # D100 (mol/h)
CO2_sd_ratio = CO2_supply / CO2_cons if CO2_cons > 0 else NA  # D126

# --- iterH headspace balance, schedule in use (MT rows 323-374) ---
t_on_CO2       = spg_dur                                # MT D151 (s) pulse duration
t_off_CO2      = max(0.0, spg_int * 60 - spg_dur)       # MT D152 (s) gap, GUARD floored at 0
flush_vol      = CO2_pulse / n_hs_gas                   # MT D323 (-) headspace volumes per pulse
flush_ret      = math.exp(-flush_vol)                   # MT D324 (-) well-mixed flush retains e^-V
t_gap_h        = t_off_CO2 / 3600                       # MT D325 (h)
tau_L_h        = 1 / (kLa_surf_used * 3600)             # MT D326 (h) liquid O2 response time
def _phi(x):
    """Phi(x) = (1-e^-x)/x, limit 1."""
    return (1 - math.exp(-x)) / x if x > 0 else 1.0
def _psi(x):
    """Psi(x) = (x-1+e^-x)/x^2, limit 1/2."""
    return (x - 1 + math.exp(-x)) / x ** 2 if x > 0 else 0.5
def _hs_phase(O2_src, H2_src, CO2_fix, DO_exc):
    """One phase of the display block (growth rows 327-342, lag rows 349-363)."""
    S_O2   = O2_src + y_O2_air * F_vent_ex                          # D327/D349 (mol/h)
    F_net  = CO2_supply + O2_src + H2_src - CO2_fix                 # D328/D350 (mol/h)
    y_mf   = S_O2 / (F_dil + F_net) if F_dil + F_net > 0 else NA          # D329/D351 (-)
    yH2_mf = H2_src / (F_dil + F_net) if F_dil + F_net > 0 else NA        # D330/D352 (-)
    F_gap  = F_dil + max(0.0, O2_src + H2_src - CO2_fix)            # D331/D353 (mol/h) air + N2 + net evolved gas
    x      = F_gap * t_gap_h / n_hs_gas                             # D332/D354 (-)
    phi, psi = _phi(x), _psi(x)                                     # D333-334/D355-356
    dy     = S_O2 * t_gap_h / n_hs_gas                              # D335/D357 (-)
    y_end  = dy * phi / (1 - flush_ret * math.exp(-x))              # D336/D358 (-)
    y_post = y_end * flush_ret                                      # D337/D359 (-)
    y_avg  = y_post * phi + dy * psi                                # D338/D360 (-)
    DO_mf  = DO_exc + H_O2_T * P_dry * y_mf                         # D340/D361 (mol/m3)
    DO_avg = DO_exc + H_O2_T * P_dry * y_avg                        # D341/D362 (mol/m3)
    DO_pk  = DO_exc + H_O2_T * P_dry * max(y_avg, y_end - (S_O2 - F_gap * y_end) / n_hs_gas * tau_L_h)  # D342/D363
    return dict(S_O2=S_O2, F_net=F_net, y_mf=y_mf, yH2_mf=yH2_mf, F_gap=F_gap, x=x, phi=phi, psi=psi,
                dy=dy, y_end=y_end, y_post=y_post, y_avg=y_avg, DO_mf=DO_mf, DO_avg=DO_avg, DO_peak=DO_pk)
def _feas(m):
    return ("reachable – kLa margin " + xltext(m, "0.00") + "×" if m >= 1 else
            "UNREACHABLE at this surface kLa – margin " + xltext(m, "0.00")
            + "× (raise kL_surf, lower the current, or accept a higher DO)")
def _peak_chk(pk, pk_mgL):
    return ("peak " + xltext(pk_mgL, "0.0") + " mg/L under the " + xltext(O2_ceil_C * M_O2, "0.0") + " mg/L ceiling"
            if pk <= O2_ceil_C else
            "PEAK " + xltext(pk_mgL, "0.0") + " mg/L OVER THE " + xltext(O2_ceil_C * M_O2, "0.0") + " mg/L INHIBITION CEILING")
DO_surf_excess_g = O2_src_g / (kLa_surf_used * 3600 * (V_charge / 1e6))   # MT D339 (mol/m3)
hs_g = _hs_phase(O2_src_g, H2_src_g, CO2_fix_g, DO_surf_excess_g)   # MT D327-D342
y_O2_mf_g, y_H2_mf_g, F_gap_g = hs_g["y_mf"], hs_g["yH2_mf"], hs_g["F_gap"]   # MT D329, D330, D331
x_hs_g, y_O2_end_g, y_O2_avg_g = hs_g["x"], hs_g["y_end"], hs_g["y_avg"]      # MT D332, D336, D338
DO_mf_g, DO_avg_g, DO_peak_g = hs_g["DO_mf"], hs_g["DO_avg"], hs_g["DO_peak"]  # MT D340, D341, D342 (mol/m3)
DO_avg_g_mgL   = DO_avg_g * M_O2                        # MT D343 (mg/L)
DO_peak_g_mgL  = DO_peak_g * M_O2                       # MT D344 (mg/L)
kLa_surf_req_g = O2_src_g / (DO_target * 3600 * (V_charge / 1e6))   # MT D345 (1/s)
kLa_margin_g   = kLa_surf_used / kLa_surf_req_g if kLa_surf_req_g > 0 else "no positive source"         # MT D346 (x)
DO_feas_g      = _feas(kLa_margin_g) if kLa_surf_req_g > 0 else "No positive biological O2 surplus; check air ingress and operating DO"                    # MT D347
DO_peak_chk_g  = _peak_chk(DO_peak_g, DO_peak_g_mgL)    # MT D348
hs_l = _hs_phase(O2_src_l, H2_src_l, CO2_fix_l, DO_surf_excess_lag)  # MT D349-D363
y_O2_mf_l, y_H2_mf_l, F_gap_l = hs_l["y_mf"], hs_l["yH2_mf"], hs_l["F_gap"]   # MT D351, D352, D353
x_hs_l, y_O2_end_l, y_O2_avg_l = hs_l["x"], hs_l["y_end"], hs_l["y_avg"]      # MT D354, D358, D360
DO_mf_l, DO_avg_l, DO_peak_l = hs_l["DO_mf"], hs_l["DO_avg"], hs_l["DO_peak"]  # MT D361, D362, D363 (mol/m3)
DO_avg_l_mgL   = DO_avg_l * M_O2                        # MT D364 (mg/L)
DO_peak_l_mgL  = DO_peak_l * M_O2                       # MT D365 (mg/L)
kLa_surf_req_l = O2_src_l / (DO_target * 3600 * (V_charge / 1e6))   # MT D366 (1/s)
kLa_margin_l   = kLa_surf_used / kLa_surf_req_l         # MT D367 (x)
DO_feas_l      = _feas(kLa_margin_l)                    # MT D368
DO_peak_chk_l  = _peak_chk(DO_peak_l, DO_peak_l_mgL)    # MT D369
y_H2_end_l     = H2_src_l * t_gap_h / n_hs_gas * hs_l["phi"] / (1 - flush_ret * math.exp(-x_hs_l))   # MT D388 (-) lag H2 fraction just before the next pulse
y_H2_end_b     = y_H2_end_l                             # Biology D114 <- MT D388
F_gap_sched    = _by_phase(F_gap_g, F_gap_l)            # MT D371 (mol/h)
DO_avg_sched   = _by_phase(DO_avg_g, DO_avg_l)          # MT D372 (mol/m3)
DO_peak_sched  = _by_phase(DO_peak_g, DO_peak_l)        # MT D373 (mol/m3)
if isnum(DO_opt) and isnum(DO_impair):
    DO_peak_band = (("peak " + xltext(DO_peak_sched * M_O2, "0.0") + " mg/L under impairment")
                    if DO_peak_sched * M_O2 < DO_impair
                    else ("PEAK " + xltext(DO_peak_sched * M_O2, "0.0") + " mg/L OVER IMPAIRMENT"))
    DO_peak_band += (("; mean " + xltext(DO_avg_sched * M_O2, "0.0") + " mg/L at/under optimum")
                     if DO_avg_sched * M_O2 <= DO_opt
                     else ("; MEAN " + xltext(DO_avg_sched * M_O2, "0.0") + " mg/L ABOVE OPTIMUM"))
elif DO_peak_sched <= O2_ceil_C:
    DO_peak_band = ("organism band unknown – peak " + xltext(DO_peak_sched * M_O2, "0.0")
                    + " mg/L is under the inhibition ceiling")
else:
    DO_peak_band = ("organism band unknown – PEAK " + xltext(DO_peak_sched * M_O2, "0.0")
                    + " mg/L OVER THE INHIBITION CEILING")   # MT D374

# --- Biology rows 75-88: lag-phase headspace flammability (replaces the H2_turnover proxy at D44) ---
CO2_supply_b    = CO2_supply                            # Biology D76 (mol/h) <- MT D100
CO2_rate_full_b = CO2_rate_full                         # Biology D77 (mol/h) <- MT D178
spg_dur_b       = spg_dur_eq_opt                        # Biology D78 (s)     <- MT D409
R_gas_b         = R_gas                                 # Biology D79 (J/mol/K) <- MT D101
F_vent_ex_b     = F_vent_ex                             # Biology D111 (mol/h) <- MT D308
F_dil_b         = F_dil                                 # Biology D125 (mol/h) <- MT D425 (air + N2)
y_O2_air_b      = y_O2_air                              # Biology D112 (-)     <- MT D307
H2_LFL     = 0.04                                       # Biology D80 (-) H2 lower flammability limit
O2_LOC_H2  = 0.052                                      # Biology D81 (-) limiting O2 conc., CO2 diluent
LOC_margin = 0.6                                        # Biology D82 (-) NFPA 69 design margin
n_flamm_src = H2_src_l_b + O2_src_l_b                      # Biology D83 (mol/h) gas into headspace, lag
y_H2_hs_lag = H2_src_l_b / (n_flamm_src + CO2_supply_b + F_dil_b)        # Biology D84 (-) = MT D352
y_O2_hs_lag = ((O2_src_l_b + y_O2_air_b * F_vent_ex_b)
               / (n_flamm_src + CO2_supply_b + F_dil_b))               # Biology D85 (-) = MT D351
duty_H2safe = max(0.0, min(H2_src_l_b / H2_LFL - n_flamm_src - F_dil_b,
                           (O2_src_l_b + y_O2_air_b * F_vent_ex_b) / (O2_LOC_H2 * LOC_margin)
                           - n_flamm_src - F_dil_b)) / CO2_rate_full_b   # Biology D86 (-)
spg_int_H2safe = (spg_dur_b / (60 * duty_H2safe)) if duty_H2safe > 0 else NA   # Biology D87 (min)
N2_sweep_H2safe = (max(0.0, H2_src_l_b / H2_LFL - n_flamm_src - F_vent_ex_b) / 3600 * R_gas_b * T_K / P_atm
                   * 1000000 * 60)                      # Biology D88 (mL/min)
# R5-m3: exact sawtooth remedy interval (Biology D89-D92, imports D115-D119)
spg_dur_opt_b   = spg_dur                           # Biology D89 (s) <- MT D90
O2_src_l_b      = O2_src_l                              # Biology D115 (mol/h) <- MT D310
F_gap_l_b       = F_gap_l                               # Biology D116 (mol/h) <- MT D353
n_hs_gas_b      = n_hs_gas                              # Biology D117 (mol) <- MT D150
flush_ret_opt_b = flush_ret                         # Biology D118 (-) <- MT D321
y_O2_end_b      = y_O2_end_l                            # Biology D119 (-) <- MT D358
def _t_gap(src, lim):
    """Longest gap keeping the pre-pulse fraction of a species (source src mol/h) under lim: 'none needed' if it cannot reach lim."""
    if src > lim * F_gap_l_b:
        q = lim * F_gap_l_b / src
        return n_hs_gas_b / F_gap_l_b * math.log((1 - q * flush_ret_opt_b) / (1 - q)) * 60
    return "none needed"
t_gap_H2_LFL = _t_gap(H2_src_l_b, H2_LFL)                                              # Biology D90 (min)
t_gap_O2_LOC = _t_gap(O2_src_l_b + y_O2_air_b * F_vent_ex_b, O2_LOC_H2 * LOC_margin)   # Biology D91 (min)
spg_int_H2safe_saw = ("any interval" if isinstance(t_gap_H2_LFL, str) or isinstance(t_gap_O2_LOC, str)
                      else max(t_gap_H2_LFL, t_gap_O2_LOC) + spg_dur_opt_b / 60)       # Biology D92 (min)
remedy_res = 0.1                                       # Biology D120 (min or mL/min) remedy display resolution
remedy_interval = max(0, math.ceil(spg_int_H2safe_saw / remedy_res) * remedy_res - remedy_res) if isnum(spg_int_H2safe_saw) else NA
interval_remedy = ("sparge every ≤" + xltext(remedy_interval, "0.0") + " min or "
                   if remedy_interval * 60 > spg_dur else "interval remedy unavailable; ")
if y_H2_end_b >= H2_LFL and y_O2_end_b >= O2_LOC_H2 * LOC_margin:
    H2_safety = ("POTENTIAL FLAMMABILITY (lag screen): H\u2082 " + xltext(y_H2_hs_lag, "0%")
                 + " mean, " + xltext(y_H2_end_b, "0%") + " before each pulse; O\u2082 " + xltext(y_O2_hs_lag, "0%")
                 + " mean, " + xltext(y_O2_end_b, "0%") + " before each pulse \u2013 until uptake starts, "
                 + interval_remedy + "sweep \u2265" + xltext(math.floor(N2_sweep_H2safe / remedy_res) * remedy_res + remedy_res, "0.0")
                 + " mL/min N\u2082; vent to a hood; no ignition sources")
else:
    H2_safety = ("Below nominal H\u2082/O\u2082 screening thresholds (lag; not safety certification): H\u2082 "
                 + xltext(y_H2_end_b, "0%") + ", O\u2082 " + xltext(y_O2_end_b, "0%") + " before each pulse ("
                 + xltext(y_H2_hs_lag, "0%") + " / " + xltext(y_O2_hs_lag, "0%") + " mean)")   # Biology D44

# --- steady dissolved O2 = headspace floor + the excess that drives the surface flux ---
y_O2_actual = _by_phase(y_O2_mf_g, y_O2_mf_l)          # D187 (-) mean-field headspace O2, sizing phase
DO_hs_floor = (H_O2_T * y_O2_actual * P_dry) if isnum(y_O2_actual) else NA      # D188 (mol/m3)
DO_ss = DO_avg_sched * M_O2                            # D108 (mg/L) cycle-mean (sawtooth) DO, sizing phase
# DO if the interval relaxed to the carbon-limited one: the same headspace balance at duty_carbon
_F_carb = F_dil + CO2_rate_full * duty_carbon + O2_src_sched + H2_src_sched - CO2_fix_sched
DO_at_carbon = (DO_surf_excess + H_O2_T * P_dry * min(1.0, saw_factor * (O2_src_sched + y_O2_air * F_vent_ex) / _F_carb)
                if _F_carb > 0 else DO_surf_excess + H_O2_T * P_dry)   # MT D232 (mol/m3) saw-corrected, guarded, capped at saturation
DO_ss_sawtooth = DO_avg_sched                          # D133 (mol/m3, sizing-phase cycle mean)
DO_ss_sawtooth_lag = DO_avg_l                          # D135 (mol/m3, LAG cycle mean, H2 as diluent)
# N2 sweep that lets the carbon-limited duty hold the DO target: the duty_DO inversion solved for the
# inert inflow instead of the CO2 supply (MT D426, mL/min; #N/A when the target is unreachable).
N2_for_DO = ((max(0.0, (O2_src_sched + y_O2_air * F_vent_ex) * saw_factor / y_O2_star - F_vent_ex - O2_src_sched
                  - H2_src_sched + CO2_fix_sched - CO2_rate_full * duty_carbon) / 3600 * R_gas * T_K / P_atm * 1e6 * 60)
             if isnum(y_O2_star) else NA)


# --- Electrochemistry D96/D98/D99 + rows 150-152: lag-phase peroxide, first-order anodic loss (R1-09) ---
ec_DO_lag     = DO_ss_sawtooth_lag                     # Electrochemistry D150 (mol/m3) <- MT D135
k_H2O2_anode  = (km_O2 / 100) * (A_anode_wet / 10000) / (ec_V_L / 1000)   # D151 (1/s) peroxide re-oxidised at the anode
def _pct_signed(x):
    """TEXT(x,"+0%;-0%")."""
    return ("+" if x >= 0 else "-") + xltext(abs(x), "0%")
DO_lag_ref_chk = (("RE-ENTER DO_lag_ref (D129): the lag DO is now " + xltext(ec_DO_lag, "0.000") + " mol/m\u00b3 ("
                   + _pct_signed(DO_lag_ref / ec_DO_lag - 1) + " off)")
                  if abs(DO_lag_ref / ec_DO_lag - 1) > DO_lag_tol else
                  "OK \u2013 DO_lag_ref within " + xltext(DO_lag_tol, "0%") + " of the lag DO ("
                  + xltext(ec_DO_lag, "0.000") + " mol/m\u00b3)")   # Electrochemistry D134 (display only)
r_H2O2_lag    = f_HOOH * O2_ORR_lag * M_H2O2 * 1000 / ec_V_L      # D152 (mg/L/h) source scaled by the lag-phase DO
H2O2_lag_1h   = r_H2O2_lag / (k_H2O2_anode * 3600) * (1 - math.exp(-k_H2O2_anode * 3600))   # D96 (mg/L) 1 h with no catalase pool, anodic loss included
_arg = 1 - H2O2_thresh * k_H2O2_anode * 3600 / r_H2O2_lag if r_H2O2_lag > 0 else NA
t_H2O2_thresh = (-math.log(_arg) / k_H2O2_anode / 60) if (isnum(_arg) and _arg > 0) else NA   # D98 (min)
if H2O2_ss > H2O2_thresh:
    H2O2_flag = ("PEROXIDE ABOVE THE GROWTH-INHIBITION THRESHOLD even with a full catalase pool ("
                 + xltext(H2O2_ss, "0.00") + " mg/L)")
elif H2O2_lag_1h > H2O2_thresh:
    H2O2_flag = ("watch — steady growth is clear (" + xltext(H2O2_ss, "0.000")
                 + " mg/L) but LAG PHASE is not: peroxide passes the threshold in "
                 + xltext(t_H2O2_thresh, "0") + " min before biomass can scavenge it")
else:
    H2O2_flag = "OK — peroxide stays below the growth-inhibition threshold in both phases"  # D99

# --- bubble-path stripping (sub-mm bubble -> excluded) ---
u_sg     = (Q_CO2 / 1e6 / 60) / (A_x / 1e6)            # D47 (m/s)
holdup   = u_sg / u_rise                                # D48
a_int    = 6 * holdup / d_bubble                        # D49 (1/m)
t_contact = d_bubble / u_rise                            # D50 (s)
kL       = 2 * math.sqrt(D_O2 / (math.pi * t_contact))  # D51 (m/s)
kLa_sparge = kL * a_int                                 # D52 (1/s)
kLa_avg  = kLa_sparge * duty                            # D53 (1/s)
strip_sparge = 0.0 if d_bubble < 0.001 else kLa_sparge * (V_charge / 1e6) * O2_ceil_C * 3600  # D54
strip_avg = strip_sparge * duty                         # D55 (mol/h)
strip_ratio = (strip_avg / O2_excess) if O2_excess > 0 else NA  # D56
kLa_req = (O2_excess / 3600 / ((V_charge / 1e6) * O2_ceil_C)) if O2_excess > 0 else NA  # D57
u_g_max = 0.05                                          # D58 (m/s)
carry_flag_usg = (("RISK – " + xltext(u_sg * 1000, "0.0") + " mm/s superficial gas velocity over the " + xltext(u_g_max * 1000, "0") + " mm/s rule of thumb")
                  if u_sg > u_g_max else
                  ("OK – " + xltext(u_sg * 1000, "0.0") + " mm/s against the " + xltext(u_g_max * 1000, "0") + " mm/s rule of thumb"))   # D414 (secondary line)
_carry = [m for (r, m) in CO2_CARRY if r == Reactor_sel and m > 0]
carry_n     = len(_carry)                              # D412
Q_carry_max = min(_carry) if carry_n > 0 else "not measured"   # D413 (mL/s) lowest recorded no-carryover flow, conservative
if carry_n == 0:
    carry_flag = "not measured – record the max flow without carryover for " + Reactor_sel + " in CO2 flows column M"
elif Q_CO2 / 60 > Q_carry_max:
    carry_flag = ("RISK – pulse flow " + xltext(Q_CO2 / 60, "0.00") + " mL/s exceeds the measured "
                  + xltext(Q_carry_max, "0.00") + " mL/s no-carryover limit")
else:
    carry_flag = ("OK – pulse flow " + xltext(Q_CO2 / 60, "0.00") + " mL/s within the measured "
                  + xltext(Q_carry_max, "0.00") + " mL/s no-carryover limit")   # D59

rho_CO2  = P_atm * (M_CO2 / 1000) / (R_gas * T_K)       # D60 (kg/m3)
n_pores_active = 1                                      # D61
v_orifice = (Q_CO2 / 1e6 / 60) / (n_pores_active * (math.pi / 4 * d_orifice ** 2))  # D62 (m/s)
We_orifice = rho_CO2 * v_orifice ** 2 * d_orifice / sigma  # D63
if d_bubble < 0.001:
    bubble_regime = "Sinter OOR - add fine-bubble model"
else:
    bubble_regime = "Static" if We_orifice < 2 else "Dynamic"   # D64

# --- O2 time-to-ceiling family ---
t_O2_ceiling = O2_ceil_C * (V_charge / 1e6) / O2_excess * 60 if O2_excess > 0 else "never (source <= 0)"   # D65 (min)
t_O2_ceiling_strip = (O2_ceil_C * (V_charge / 1e6) / (O2_excess - strip_avg) * 60
                      if (O2_excess - strip_avg) > 0 else "never (strip \u2265 source)")  # D66
# (MT D75 y_O2_vent and D76 DO_vent_eq cleared in iterR4)
hs_flush_time = headspace_V * spg_int / V_pulse         # D77 (min) headspace volumes per interval / delivered volume
surf_ratio = (surf_strip / O2_excess) if O2_excess > 0 else NA   # D74
O2_removal_ratio = ((strip_avg + surf_strip) / O2_excess) if O2_excess > 0 else NA  # D78
t_O2_ceiling_lag = O2_ceil_C * (V_charge / 1e6) / O2_net_gen * 60   # D79 (min)
t_O2_ceiling_rem = (O2_ceil_C * (V_charge / 1e6) / (O2_net_gen - strip_avg - surf_strip) * 60
                    if (O2_net_gen - strip_avg - surf_strip) > 0 else "never (removal \u2265 source)")  # D80

kinetic_caveat = "see note ->"                          # D96

# (MT D109 DO_ss_vs_opt cleared in iterR4)
if isnum(DO_min):
    DO_ss_vs_min = "above minimum" if DO_ss >= DO_min else "BELOW MINIMUM"
else:
    DO_ss_vs_min = "minimum DO unknown - measure"        # D110
tip_warn = "TIP SPEED > 1.5 m/s" if tip_speed > 1.5 else "OK"  # D111
sched_regime = ("Carbon supply alone holds the DO target – the interval may relax to "
                + xltext(min(spg_int_carbon, _pH_cap), "0") + " min"
                if DO_at_carbon <= DO_target
                else "Do NOT relax: at the carbon-limited interval (" + xltext(spg_int_carbon, "0")
                + " min) the cycle-mean DO would be \u2248" + xltext(DO_at_carbon * M_O2, "0")
                + " mg/L, "
                + ("above the " + xltext(O2_ceil_C * M_O2, "0.0") + " mg/L inhibition ceiling"
                   if DO_at_carbon > O2_ceil_C
                   else "against a " + xltext(DO_target * M_O2, "0.0") + " mg/L target")
                + " (peaks higher)")   # D113
cal_warning = (f"calibrated: {Reactor}" + cal_source_txt if has_cal > 0
               else f"NO CALIBRATION for {Reactor} \u2013 record a CO\u2082 flow in the Calibrations tab (CO\u2082 flow section, Include = y) or add a row in CO2 flows with nominal flowrate + minimum sparge")  # MT D120

O2_accum = O2_excess / 60 * spg_int                     # D127 (mol)
O2_strip_pulse = strip_sparge / 3600 * spg_dur          # D128 (mol)
sched_bal = (O2_strip_pulse / O2_accum) if O2_accum > 0 else NA  # D129
dur_ok = "OK" if spg_dur >= pulse_floor else "LOW"      # D130
kL_surf_crit = kLa_surf_req / a_surf                    # D131 (m/s)


# ============================================================================
# MASS TRANSFER TAB - schedule -> dissolved CO2
#   The superseded two-compartment closed form (rows 153-161) is cleared in the
#   workbook and gone from here. Rows 190-200 hold ONE pooled inventory (liquid
#   + headspace at Henry equilibrium). iterH: between pulses the pool drains
#   only through the gas that must leave to hold 1 atm (exchanged air plus net
#   evolved gas, F_gap) and the fixation sink; a pulse is a well-mixed flush
#   that keeps e^-V of the old headspace. Gap evolution uses Phi/Psi (rows
#   375-380) so k_vent = 0 (outflow-only, growth) is exact, not 0/0.
#   CO2aqc (Chemistry D5) reads the pooled cycle average.
# ============================================================================
D_CO2          = D_CO2_ref * math.exp(-Ea_D_CO2 / R_gas * (1 / T_K - 1 / 298.15))  # MT D138 (m2/s)
V_L_m3         = V_charge / 1e6                         # MT D141 (m3)   (D140, D142 defined with the headspace balance)
V_L_CO2        = V_L_m3 * DIC_cap                       # MT D416 (m3) liquid volume with its bicarbonate storage (DIC_cap = D415 <- Chemistry D296)
k_vent         = F_gap_sched / 3600 / n_hs_gas          # MT D143 (1/s) headspace turnover between pulses
tau_hs         = 1 / k_vent / 60 if k_vent > 0 else "none between pulses"   # MT D144 (min) headspace residence time
hs_H_CO2       = H_CO2_T                                # MT D191 (mol/m3/Pa) <- Biology D31
C_sat_CO2      = hs_H_CO2 * P_dry                       # MT D145 (mol/m3) pure-CO2 sparge saturation
C_air_CO2      = H_CO2_T * pCO2_air                     # MT D146 (mol/m3) air-equilibrium
sqrtD_CO2      = math.sqrt(D_CO2 / D_O2)                # MT D147 penetration-theory diffusivity scaling
kLa_CO2_off    = kLa_surf_used * sqrtD_CO2                   # MT D148 (1/s) surface-path between pulses
tau_surf_floor = 1 / kLa_CO2_off / 60                   # MT D149 (min) surface-relaxation time
# (MT D150 n_hs_gas, D151 t_on_CO2, D152 t_off_CO2 are defined with the headspace balance above)
# --- OPERATIVE: mass-conserving pooled limit cycle (MT rows 190-200) ---
Vg_CO2         = headspace_V_m3 / (hs_H_CO2 * R_gas * T_K)   # MT D192 (m3) headspace as liquid-equivalent volume
pool_a         = V_L_CO2 / (V_L_CO2 + Vg_CO2)             # MT D193 (-) liquid share of a pooled inventory
pool_b         = C_sat_CO2 * (1 - pool_a) * (1 - flush_ret)   # MT D194 (mol/m3) CO2 the pulse leaves behind (well-mixed flush)
k_eff_CO2      = k_vent * Vg_CO2 / (V_L_CO2 + Vg_CO2)    # MT D195 (1/s) pool decay through the vent
pool_beta_ratio = (kLa_CO2_off * V_L_m3 / Vg_CO2) / k_vent if k_vent > 0 else "no turnover between pulses"   # MT D196 (x) quasi-equilibrium validity
pool_e         = math.exp(-k_eff_CO2 * t_off_CO2)       # MT D197 (-)
pool_D_raw     = ((C_air_CO2 / C_sat_CO2 * F_vent_ex - CO2_fix_sched) * t_gap_h
                  / (V_L_CO2 + Vg_CO2))                 # MT D375 (mol/m3) gap change, slow-vent limit
pool_x         = k_eff_CO2 * t_off_CO2                  # MT D376 (-)
pool_phi       = _phi(pool_x)                           # MT D377 (-)
pool_psi       = _psi(pool_x)                           # MT D378 (-)
pool_D_gap     = pool_D_raw * pool_phi                  # MT D379 (mol/m3)
pool_ret       = pool_a + (1 - pool_a) * flush_ret      # MT D380 (-) pool share retained through a pulse
C_cycle_start  = (pool_D_gap + pool_b * pool_e) / (1 - pool_ret * pool_e)   # MT D198 (mol/m3) fixed point of the cycle
C_cycle_peak   = pool_ret * C_cycle_start + pool_b      # MT D199 (mol/m3)
pool_start_chk = ("WATCH \u2013 the carbon pool empties within the cycle (pulse-start CO\u2082 below air "
                  "equilibrium): fixation outruns supply at this interval"
                  if C_cycle_start < C_air_CO2 else "OK")   # MT D435
hs_sag         = (pool_a * (C_cycle_peak - C_cycle_start) * (V_L_CO2 + Vg_CO2)
                  + max(0.0, CO2_fix_sched - O2_src_sched - H2_src_sched) * t_gap_h) / n_hs_gas   # MT D389 (-) fractional headspace pressure sag per cycle
CO2_uptake_ratio = ((C_cycle_peak - C_cycle_start) * V_L_CO2 * pulses_h / CO2_cons
                    if CO2_cons > 0 else NA)            # MT D417 (x) CO2 absorbed per pulse / fixation demand (informative, not pass/fail)
hs_sag_max     = 0.05                                   # MT D390 (-) tolerated sag for a sealed cap. INPUT
if F_N2 > 0 and F_N2 * t_gap_h >= hs_sag * n_hs_gas:
    hs_sag_chk = "OK \u2013 the N\u2082 sweep supplies the per-cycle make-up gas; vent outflow unverified"
elif F_vent_ex > 0:
    hs_sag_chk = "UNVERIFIED pressure closure: air ingress is assumed; measure vent make-up flow"
elif hs_sag - F_N2 * t_gap_h / n_hs_gas > hs_sag_max:
    hs_sag_chk = ("HEADSPACE SAGS " + xltext(hs_sag - F_N2 * t_gap_h / n_hs_gas, "0%") + " below 1 atm each cycle \u2013 a real cap will draw "
                  "air back: use Open vent or Air exchange")
else:
    hs_sag_chk = "OK \u2013 sag " + xltext(max(0.0, hs_sag - F_N2 * t_gap_h / n_hs_gas), "0%") + " per cycle, within the assumed sag tolerance; cap performance unverified"   # MT D391
C_cycle_start_b = C_cycle_start                         # Biology D97 (mol/m3) <- MT D198
CO2_margin_trough = C_cycle_start_b * 1000 / Km_CO2     # Biology D98 (x) carbon margin at the cycle trough (R2-m4)
CO2_cyc_avg_new = C_cycle_peak * pool_phi + pool_D_raw * pool_psi   # MT D200 (mol/m3) cycle mean
_F_out = F_dil + CO2_supply + O2_src_sched + H2_src_sched - CO2_fix_sched
y_CO2_mf       = ((CO2_supply - CO2_fix_sched + pCO2_air / P_dry * F_vent_ex) / _F_out
                  if _F_out > 0 else NA)                # MT D381 (-) mean-field headspace CO2 (cross-check)
C_CO2_mf       = y_CO2_mf * C_sat_CO2                   # MT D382 (mol/m3)
CO2aqc         = min(C_sat_CO2, max(C_air_CO2, CO2_cyc_avg_new)) / 1000   # MT D162 = Chemistry D5 (mol/L)
vent_floor_chk = ("no vent turnover between pulses (OK)" if isinstance(tau_hs, str)
                  else "vent turnover slower than the surface (OK)" if tau_hs >= tau_surf_floor
                  else "WARNING: the vent turns the headspace over faster than the surface relaxes the liquid")  # MT D163
sched_valid    = "OK" if (spg_int * 60 >= spg_dur) else "INVALID: interval < pulse"  # MT D164


# ============================================================================
# CHEMISTRY pH SOLVE (deferred) - ACTIVITY-CORRECTED buffered charge balance
#   Runs here because it consumes the schedule-dependent CO2aqc above. WAVE-4:
#   every equilibrium constant in the residual is now on the CONCENTRATION
#   scale (rows 190-197), because the balance is written in concentrations. The
#   root is therefore a concentration-scale pH; pH_meas (D220) converts it to
#   the activity scale a glass electrode reads, and EVERY downstream pH
#   comparison uses pH_meas rather than pH_op.
# ============================================================================
# pH solve grid (A50:A100 trial pH 4.0..9.0 step 0.1); root by linear interp.
def charge_residual(pH):
    h = 10 ** (-pH)
    return (pH_SID
            + pH_NT * h / (h + KaN_c)
            + h
            - (pH_PT * Ka1p_c * h ** 2 + 2 * pH_PT * Ka1p_c * Ka2p_c * h
               + 3 * pH_PT * Ka1p_c * Ka2p_c * Ka3p_c)
              / (h ** 3 + Ka1p_c * h ** 2 + Ka1p_c * Ka2p_c * h + Ka1p_c * Ka2p_c * Ka3p_c)
            - Ka1c_c * CO2aqc / h
            - 2 * Ka1c_c * Ka2c_c * CO2aqc / h ** 2
            - Kw_c / h)


_pH_grid = [round(4.0 + 0.1 * i, 10) for i in range(51)]  # 4.0 .. 9.0
_resid = [charge_residual(p) for p in _pH_grid]
_interp_sum = 0.0
n_cross = 0
for i in range(len(_pH_grid) - 1):
    b, bn = _resid[i], _resid[i + 1]
    if b >= 0 and bn < 0:                              # sign change (root bracket)
        n_cross += 1                                   # D105
        _interp_sum += _pH_grid[i] + 0.1 * b / (b - bn)
pH_op = _interp_sum if n_cross == 1 else NA            # D103 (concentration-scale operating pH)
pH_meas = pH_op - math.log10(gam1)                     # D220 (what a probe reads)

pH_fHOCl = 1 / (1 + KaHOCl_c / 10 ** -pH_op)           # D104 concentration scale at pH_op
# --- naive FE=1 cells (NOT operative; kept for contrast) ---
bleach_rate   = Iappc / (2 * Fcc) * 52460 * 3600 / VLc # D107 (mg/L/h, FE=1 ceiling)
bleach_t1ppm  = 1 / bleach_rate * 60                   # D108 (min)
HOCl_max = pH_Cl * pH_fHOCl * 52460                    # D125 (naive FE=1 ceiling, superseded)
# --- graded kinetic free-chlorine penalty model (operative; Chemistry rows 128-149) ---
P_HOCl   = I_Cl / (n_e_Cl * Fcc * VLc)                 # D134 (mol/L/s) volumetric free-Cl production
NH3_N    = pH_NT * 14007                               # D135 (mg/L) ammonium as N
k1_NH2Cl = 4.2e6                                       # D136 (M^-1 s^-1) HOCl+NH3 rate constant
pKa_NH4  = -math.log10(Ka_NH4)                         # D137 (from the van 't Hoff-corrected Ka_NH4)
NH3_free = pH_NT / (1 + 10 ** (pKa_NH4 - pH_op))       # D138 (M) reactive free ammonia
HOCl_ss  = P_HOCl / (k1_NH2Cl * NH3_free)              # D139 (M) steady bulk free HOCl (already the undissociated acid)
HOCl_ss_mgL = HOCl_ss * 52460                          # D140 (mg/L)
f_local  = 10                                          # D141 anode boundary-layer enrichment (numerically inert: chloramine dominates ~1e4x)
# BUGFIX (review 2026-06-26) chloride mass balance: chlorine (free + combined)
# can never exceed the medium chloride pool. The old cap was on ammonium
# capacity (5.06*NH3_N, never binds) and let NH2Cl reach 17 mg/L from only
# ~9.45 mg/L of chloride - physically impossible. Cap by the chloride pool.
# (In a closed batch this pool also DEPLETES; a steady value at the cap presumes
#  chloride is regenerated as HOCl is reduced back to Cl- - stated, not proven.)
Cl_pool_mgL = pH_Cl * 52460                            # D149 (mg/L as HOCl-equiv) chloride-pool ceiling
cl_per_N = 5.06                                        # (mg Cl2 per mg NH3-N) NH2Cl stoichiometric cap; x M_HOCl/M_Cl2 puts it on the HOCl-equivalent basis
M_HOCl_mg = 52460                                       # Chemistry D222 (mg/mol)
def _nh2cl(tau_h):
    """Chloride pool partly turned over to chlorine in tau: pool * k*tau/(1+k*tau), capped by the ammonium stoichiometry."""
    kt = k_Cl_turn * tau_h * 3600
    return min(pH_Cl * kt / (1 + kt), I_Cl_FE / (n_e_Cl * Fcc * VLc) * tau_h * 3600, pH_NT) * M_HOCl_mg
NH2Cl_mgL = _nh2cl(tau_NH2Cl)                          # D143 (mg/L) combined chlorine, pool-capped (R1-02: pool depletes as it turns over)
R_chloramine = 25                                      # D144 monochloramine potency divisor
# BUGFIX (review 2026-06-26) double pH-discount removed: HOCl_ss is ALREADY the
# undissociated hypochlorous acid, so the old extra *pH_fHOCl multiplier on the
# free term discounted dissociation twice. Dropped.
C_eff    = f_local * HOCl_ss_mgL + NH2Cl_mgL / R_chloramine  # D145 (mg/L) OPERATIVE
Cl_onset = 0.1                                         # D146 (mg/L) sub-lethal onset
Cl_kill  = 2                                           # D147 (mg/L) kill
# --- C_eff uncertainty band from the two unmeasured knobs (tau, R), pool-capped ---
tau_NH2Cl_lo = 1 / 60                                  # D150 (h) 1 min
tau_NH2Cl_hi = 5                                       # D151 (h)
R_chloramine_lo = 18                                   # D152 most-potent end of defensible band
R_chloramine_hi = 70                                   # D153 least-potent end
NH2Cl_lo = _nh2cl(tau_NH2Cl_lo)                        # D154
NH2Cl_hi = _nh2cl(tau_NH2Cl_hi)                        # D155
C_eff_lo = f_local * HOCl_ss_mgL + NH2Cl_lo / R_chloramine_hi  # D156 least chlorine, least potent
C_eff_hi = f_local * HOCl_ss_mgL + NH2Cl_hi / R_chloramine_lo  # D157 most chlorine, most potent
# --- electrode-corrosion / dissolved-metal pathway (DATA GAP: the UNMODELLED prime suspect for Exp-2) ---
corr_I_frac   = NA                                     # D158 fraction of anodic charge -> metal dissolution. DATA GAP - measure
metal_MW      = 63.55                                  # D159 (g/mol) Cu, representative leached transition metal
metal_z       = 2                                      # D160 electrons per dissolved metal ion
metal_leach_rate = (corr_I_frac * Iappc / (metal_z * Fcc) * metal_MW * 1000 * 3600 / VLc
                    if isnum(corr_I_frac) else NA)     # D161 (mg/L/h) #N/A until corr_I_frac measured
metal_tox_thresh = 0.5                                 # D162 (mg/L) order-of-magnitude bactericidal Cu/Ni for gram-negatives
metal_flag = ("DATA GAP - measure dissolved Cu/Ni/Fe in spent medium; the green anode implicates "
              "electrode corrosion / metal leaching as the unmodelled prime suspect for the Exp-2 death"
              if not isnum(corr_I_frac)
              else f"metal leach {metal_leach_rate:.2f} mg/L/h vs ~{metal_tox_thresh} mg/L bactericidal threshold")  # D163
C_eff_Cl2 = C_eff * M_Cl2_mg / M_HOCl_mg                # Chemistry D226 (mg/L as Cl2)
C_eff_lo_Cl2 = C_eff_lo * M_Cl2_mg / M_HOCl_mg          # Chemistry D259 (mg/L as Cl2)
C_eff_hi_Cl2 = C_eff_hi * M_Cl2_mg / M_HOCl_mg          # Chemistry D260 (mg/L as Cl2)
if C_eff_Cl2 < Cl_onset:                               # D109
    bleach_flag = ("negligible free chlorine (" + xltext(C_eff_Cl2, "0.00") + " mg/L as Cl₂ < onset); "
                   "does NOT account for the Exp-2 death - see metal_flag")
elif C_eff_Cl2 < Cl_kill:
    bleach_flag = ("sub-lethal " + xltext(C_eff_Cl2, "0.00") + " mg/L as Cl₂ (band "
                   + xltext(C_eff_lo_Cl2, "0.00") + "-" + xltext(C_eff_hi_Cl2, "0.00")
                   + "); chloride-pool-bounded, cannot reach the kill threshold in this medium; "
                   "does NOT explain the death - see metal_flag")
else:
    bleach_flag = "SEVERE free chlorine: " + xltext(C_eff_Cl2, "0.0") + " mg/L as Cl₂ - biofilm/electrode damage (Baek 2021)"
if pH_meas < 6.5:
    pH_band_flag = "pH BELOW HOB optimum (<6.5) — reduce the CO₂ dose or lengthen the interval"
elif pH_meas > 7.5:
    pH_band_flag = "pH above optimum (>7.5)"
else:
    pH_band_flag = "pH in HOB band 6.5–7.5"       # D110

# --- buffer capacity at the electrode surface (Chemistry rows 213-219) ---
D_HPO4     = 7.59e-10                                  # D214 (m2/s) CRC tabulated
km_O2_c    = km_O2                                     # D272 (cm/s) <- Electrochemistry D83
km_exp_c   = km_exp                                    # D273 (-)    <- Electrochemistry D84
D_O2_c     = D_O2                                      # D274 (m2/s) <- Electrochemistry D81
delta_diff = D_O2_c / (km_O2_c / 100) * 1e6            # D215 (um) DERIVED display: film thickness implied by km_O2 (was a typed 40)
D_HCO3     = 1.185e-9                                  # D251 (m2/s) CRC
HCO3_op    = Ka1c_c * CO2aqc / 10 ** -pH_op            # D252 (mol/L) concentration scale
HPO4_op    = pH_PT / (1 + 10 ** (-math.log10(Ka2p_c) - pH_op))   # D253 (mol/L)
km_HPO4    = km_O2_c * (D_HPO4 / D_O2_c) ** km_exp_c   # D275 (cm/s) k_m scaled by the same D^0.644 law as km_Cl
km_HCO3    = km_O2_c * (D_HCO3 / D_O2_c) ** km_exp_c   # D276 (cm/s)
j_buffer_lim = Fcc * ((km_HPO4 / 100) * HPO4_op + (km_HCO3 / 100) * HCO3_op) * 1000 / 10   # D216 (mA/cm2) phosphate + bicarbonate acceptors
j_anode_c    = j_anode                                 # D217 <- Electrochemistry D48
j_buffer_ratio = j_anode_c / j_buffer_lim              # D218 (-)
if j_buffer_ratio > 1:
    buffer_flag = ("BUFFER EXCEEDED — anode surface acidifies (local pH ~1 unit below bulk); "
                   "the pH solved above is the bulk value only")
elif j_buffer_ratio > 0.5:
    buffer_flag = ("watch — running at " + xltext(j_buffer_ratio, "0%")
                   + " of the phosphate buffer limit; expect a 0.4–1.0 unit excursion "
                     "at each electrode surface")
else:
    buffer_flag = "OK — buffer holds the electrode surfaces at the bulk pH"   # D219

# --- R1-14: the PCET credit is withdrawn once the anode current passes the buffer limit (Electrochemistry D161-D163) ---
I_at_gerrit_max = (gerrit_slope * gerrit_max + gerrit_int) / 1000        # Electrochemistry D142 (A)
ec_jbuf_ratio    = j_buffer_ratio                      # Electrochemistry D161 <- Chemistry D218
pcet_credit_op   = 0.0 if ec_jbuf_ratio > 1 else pcet_credit                  # D162 (V) credit at the operating point
pcet_credit_gmax = 0.0 if ec_jbuf_ratio * I_at_gerrit_max / I_app > 1 else pcet_credit   # D163 (V) credit at the top of the Gerrit band (j scales with I)

V_cell_est  = ec_E_rev + eta_anode + eta_cath + pcet_credit_op + V_IR   # D119 (V)
V_rail      = 5.0                                      # D120 (V) Pioreactor LED channel supply
V_headroom  = V_rail - V_cell_est                      # D121 (V)
if V_headroom < 0:
    V_flag = "OVER RAIL — the drive cannot deliver this current; the linear current law will not hold"
elif V_headroom < 1:
    V_flag = ("watch — within 1 V of the rail (" + xltext(V_cell_est, "0.00") + " V of "
              + xltext(V_rail, "0") + " V); expect the current law to bend")
else:
    V_flag = ("OK — " + xltext(V_cell_est, "0.00") + " V estimated against a "
              + xltext(V_rail, "0") + " V rail")       # D122
# --- R1-06: the same budget at the top of the Gerrit-validated band ---
V_at_gerrit_max = (ec_E_rev + b_anode * math.log10(I_at_gerrit_max / A_anode_wet / j0_anode)
                   + b_cath * math.log10(I_at_gerrit_max / A_cath_wet / j0_cath)
                   + pcet_credit_gmax + I_at_gerrit_max * R_cell)             # D143 (V)
if V_at_gerrit_max > V_rail:
    V_gerrit_flag = ("INCONSISTENT — the budget needs " + xltext(V_at_gerrit_max, "0.00") + " V at "
                     + xltext(gerrit_max, "0") + " %, above the " + xltext(V_rail, "0")
                     + " V rail, where Gerrit's Law is validated linear: R_cell (k_geom) or j₀ is too high")
else:
    V_gerrit_flag = ("OK — " + xltext(V_at_gerrit_max, "0.00") + " V at " + xltext(gerrit_max, "0")
                     + " %, under the " + xltext(V_rail, "0") + " V rail across the validated band")   # D144

# --- electrode potentials at the operating pH (Chemistry rows 199-211) ---
nernst_slope = R_gas * TKc / Fcc * math.log(10)        # D200 (V/pH)
E0_HER  = 0.0                                          # D202 (V vs SHE) SHE convention
E0_Cl2  = 1.358                                        # D203
E0_ORR2 = 0.695                                        # D204 the parasitic cathode branch
E0_Cu   = 0.3419                                       # D205
E_OER   = E0_OER - nernst_slope * pH_meas              # D206
E_HER   = E0_HER - nernst_slope * pH_meas              # D207
E_Cl2   = E0_Cl2 + nernst_slope * (-math.log10(max(gam1 * pH_Cl * Cl_free_frac, 1e-12))) if pH_Cl > 0 else NA  # D208
E_anode_op = E_OER + eta_anode + pcet_credit_op           # Chemistry D256 (V vs SHE) E_OER + eta_anode_c (Echem D111) + pcet_credit_c (Chemistry D255 <- Echem D162)
E0_HOCl = 1.482                                        # Chemistry D257 (V) CRC
E_HOCl_Cl = E0_HOCl + nernst_slope / 2 * (math.log10(max(HOCl_ss * f_local, 1e-12))
                                            - pH_meas - math.log10(max(gam1 * pH_Cl * Cl_free_frac, 1e-12))) if pH_Cl > 0 else NA   # Chemistry D258 (V vs SHE)
E_Cl_margin = E_HOCl_Cl - E_anode_op                   # D209 (V) HOCl/Cl- couple minus operating anode potential
E_ORR2  = E0_ORR2 - nernst_slope * pH_meas             # D210
E_Cu_margin = E_anode_op - E0_Cu                       # D211 (V) operating anode above Cu2+/Cu



# ============================================================================
# SUMMARY TAB - results & checks (the headline deliverables)
# ============================================================================
def iferror(fn, fallback):
    try:
        v = fn()
        if isinstance(v, float) and math.isnan(v):
            return fallback
        return v
    except Exception:
        return fallback


def round_half_up(x):
    """Excel ROUND(x, 0): half away from zero (Python round() is banker's)."""
    return int(Decimal(repr(x)).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def round_sig_or_int(x):
    """Excel: IF(NOT(ISNUMBER(x)),x, IF(x>0.5, ROUND(x,0), ROUND(x, 1-(1+INT(LOG10(ABS(x))))))) ."""
    if not isnum(x):
        return x
    if x > 0.5:
        return round(x)
    digits = 1 - (1 + int(math.log10(abs(x))))
    return round(x, digits)


CAL_FIRST = "calibrate this reactor first (CO\u2082 flow section of the Calibrations tab, or a CO2 flows row)"   # R5-M1 wording
S_D13 = iferror(lambda: spg_dur_opt,   # D13: ='Mass Transfer'!D90 (spg_dur_opt)
                CAL_FIRST)
S_D14 = spg_dur if isnum(S_D13) else S_D13         # actual resolved pulse
S_D15 = iferror(lambda: spg_int_opt, CAL_FIRST)
S_D16 = spg_int if isnum(S_D15) else S_D15         # actual resolved interval
S_D19 = geom_check                                      # D19 vial geometry
S_D20 = cal_warning                                     # D20 reactor calibrated
S_D21 = DO_peak_band                                    # D21 peak DO vs organism band (MT D374)
S_D22 = DO_ss_vs_min                                    # D22 O2 above minimum
S_D23 = sched_regime                                    # D23 interval relaxable
S_D24 = H2_safety                                       # D24 H2 headspace safe
S_D25 = bubble_regime                                   # D25 bubble model valid
S_D26 = iferror(lambda: f"×{CO2_sd_ratio:.1f}" + (" OK" if CO2_sd_ratio >= 1 else " SHORTFALL (CO2 < demand)")
                + f" delivered; ×{CO2_uptake_ratio:.1f} absorbed per pulse (row 135)",
                "calibrate this reactor first")         # D26 CO2 supply : demand (this schedule)
S_D27 = iferror(lambda: dur_ok, CAL_FIRST)  # D27 pulse >= floor
S_D28 = iferror(lambda: od_ok, CAL_FIRST)   # D28 dosing window
S_D29 = carry_flag                                      # D29 carryover risk
S_D30 = tip_warn                                        # D30 tip-speed shear
S_D31 = media_vol_warn                                  # D31 media volume fits
S_D32 = depth_warn                                      # D32 liquid level OK
S_D33 = I_valid                                         # D33 LED current-law range
S_D34 = ("inputs present" if (isnum(DO_min) and isnum(DO_opt) and isnum(DO_impair) and isnum(DO_toxic))
         else "DATA GAP - organism DO thresholds unmeasured; results unreliable")  # D34
S_D35 = pH_meas                                         # D35 endpoint pH (activity scale) = Chemistry D220
S_D36 = C_eff_Cl2                                       # D36 effective biocidal chlorine, as Cl2 = Chemistry D226
S_D38 = DO_ss                                           # D38 steady-state DO
S_D39 = spg_int_carbon                                  # D39 interval if O2 handled
S_D40 = tip_speed                                       # D40 stir-bar tip speed
S_D41 = CO2_margin_trough                                # D41 carbon margin at the cycle trough (Biology D98)
# --- wave-4 block (Summary rows 81-90): hand these to an electrochemist ---
S_D95 = (((pulse_V0 + Q_CO2_fit * S_D14) / (Q_CO2 / 60)) / (60 * S_D16) / duty_actual if (isnum(S_D14) and isnum(S_D16)) else
         CAL_FIRST)   # D95 as-run / optimised duty
S_D82 = etaF_calc                                       # D82 cathodic faradaic efficiency (calculated)
S_D83 = V_cell_est                                      # D83 estimated cell voltage
S_D84 = V_flag                                          # D84 cell-voltage verdict
S_D85 = H2O2_flag                                       # D85 peroxide verdict
S_D86 = buffer_flag                                     # D86 electrode-surface pH verdict
S_D87 = E_Cl_margin                                     # D87 chlorine headroom above O2 evolution
S_D88 = E_Cu_margin                                     # D88 copper dissolution headroom
S_D89 = pH_meas                                         # D89 measured (activity-scale) pH
S_D90 = kLa_surf_req * 3600                             # D90 surface kLa required for the DO target (1/h, R5-m6)
S_A15 = "CO\u2082 sparge interval (" + vent_model_sel + ", sized on " + O2_phase_sel + ")"   # A15 label (formula)
S_F121 = ("Same on the lag source. Currently " + xltext(kLa_margin_l, "0.00") + "\u00d7: "
          + ("the target cannot be held during lag at the kLa in use, whatever the schedule \u2014 an owner decision (target the ceiling with a margin during lag?)."
             if kLa_margin_l < 1 else "the target can be held during lag at the kLa in use."))   # F121 (formula)
S_D129 = hs_sag                                         # D129 headspace sag per cycle
S_D130 = hs_sag_chk                                     # D130 sealed-cap plausibility
S_D135 = CO2_uptake_ratio                               # D135 CO2 absorbed per pulse / demand (x) <- MT D417
S_D136 = carry_flag_usg                                 # D136 superficial-velocity carryover rule of thumb <- MT D414
# --- iterH block (Summary rows 110-128): headspace model selectors and both-phase DO ---
pH_band_lo = 6.5                                        # Chemistry D236 (pH) HOB band lower edge
# --- alkalinity needed for a target pH (Chemistry rows 302-308; first order:
# CO2aqc and the activity coefficients held at the schedule in use) ---
alk_pH_target   = pH_band_lo                           # D303 (pH, probe scale) <- D236
alk_pH_target_c = alk_pH_target + math.log10(gam1)     # D304 (pH, concentration scale)
alk_resid_t     = charge_residual(alk_pH_target_c)     # D305 (mol/L)
alk_needed      = max(0.0, -alk_resid_t)               # D306 (mol/L) strong base to add
alk_NaHCO3_gL   = alk_needed * M_NaHCO3                # D308 (g/L)
S_D131 = alk_NaHCO3_gL                                  # D131 NaHCO3 for the target pH (g/L) <- Chemistry D308
S_D132 = alk_needed * 1000                              # D132 extra alkalinity (mM) <- Chemistry D306
S_D111 = vent_model_sel                                 # D111 vent model (input)
S_D112 = O2_phase_sel                                   # D112 O2 sizing phase (input)
S_D113 = Q_vent_used                                    # D113 vent air ingress in use (mL/min) -> MT D386
S_D114 = DO_avg_g_mgL                                   # D114 cycle-mean DO, growth (mg/L)
S_D115 = DO_peak_g_mgL                                  # D115 peak DO, growth (mg/L)
S_D116 = DO_avg_l_mgL                                   # D116 cycle-mean DO, lag (mg/L)
S_D117 = DO_peak_l_mgL                                  # D117 peak DO, lag (mg/L)
S_D118 = DO_peak_chk_g                                  # D118 peak vs ceiling, growth
S_D119 = DO_peak_chk_l                                  # D119 peak vs ceiling, lag
S_D120 = DO_feas_g                                      # D120 target reachable, growth
S_D121 = DO_feas_l                                      # D121 target reachable, lag
S_D122 = kLa_surf_req_g * 3600                          # D122 surface kLa required, growth (1/h)
S_D123 = kLa_surf_req_l * 3600                          # D123 surface kLa required, lag (1/h)
S_D124 = y_O2_mf_g                                      # D124 headspace O2 fraction, growth
S_D125 = y_O2_mf_l                                      # D125 headspace O2 fraction, lag
S_D126 = y_H2_mf_l                                      # D126 headspace H2 fraction, lag
S_D127 = y_CO2_mf                                       # D127 headspace CO2 fraction, sizing phase
DIC_ref_check = "OK" if abs(pH_ref_DIC - pH_op) <= 0.1 else "REFRESH DIC reference pH"
if sel_invalid:
    S_D128 = "#N/A – check the selectors in D111/D112"
elif not isnum(spg_int_DO):
    S_D128 = "DO target unreachable on the sizing phase; schedule is a legacy fallback"
elif DIC_ref_check != "OK" or abs(DO_lag_ref / ec_DO_lag - 1) > DO_lag_tol:
    S_D128 = "watch – refresh the DIC or lag-DO reference before claiming either target"
elif pH_band_lo <= pH_meas <= pH_band_hi and DO_ss <= DO_target * M_O2:
    S_D128 = "yes – both targets met by the evaluated schedule"
else:
    S_D128 = "NO – evaluated schedule misses the pH band or mean DO target"


# ============================================================================
# VERIFICATION HARNESS - reads the workbook itself
#   Minimal read-only .xlsx reader: unzip in memory, walk workbook.xml (sheet
#   name -> r:id), workbook.xml.rels (r:id -> part), sharedStrings.xml and the
#   sheet parts. Returns the value Excel CACHED for a cell, so the twin is
#   compared against the live file rather than a transcribed literal.
# ============================================================================
WORKBOOK_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "electroPioreactorGasModel.xlsx")

_MAIN_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


class NoCachedValue:
    """Sentinel: the cell holds a formula but Excel stored no cached result."""

    def __repr__(self):
        return "<no cached value>"


class CellAbsent:
    """Sentinel: the workbook has no such cell (empty / never written)."""

    def __repr__(self):
        return "<cell absent>"


NO_CACHE = NoCachedValue()
ABSENT = CellAbsent()


class WorkbookReader:
    """Cached-value reader for an .xlsx, standard library only."""

    def __init__(self, path):
        self.path = path
        with zipfile.ZipFile(path) as z:
            self._parts = {n: z.read(n) for n in z.namelist()
                           if (n.startswith("xl/worksheets/") and n.endswith(".xml"))
                           or n in ("xl/workbook.xml", "xl/_rels/workbook.xml.rels",
                                    "xl/sharedStrings.xml")}
        rels = {}
        rel_xml = self._parts.get("xl/_rels/workbook.xml.rels")
        if rel_xml is not None:
            for r in ET.fromstring(rel_xml):
                rels[r.get("Id")] = r.get("Target")
        # Sheet TAB NAME -> part name. Note sheetId is NOT the part number
        # (Chemistry is sheetId=7 but lives in sheet4.xml), so the r:id -> rels
        # indirection is mandatory, not decorative.
        self._sheet_part = {}
        for sh in ET.fromstring(self._parts["xl/workbook.xml"]).iter(_MAIN_NS + "sheet"):
            target = rels.get(sh.get(_REL_NS + "id"), "")
            if target:
                self._sheet_part[sh.get("name")] = (target.lstrip("/") if target.startswith("/") else "xl/" + target)
        sst_xml = self._parts.get("xl/sharedStrings.xml")
        self._shared = []
        if sst_xml is not None:
            for si in ET.fromstring(sst_xml):
                self._shared.append("".join(t.text or "" for t in si.iter(_MAIN_NS + "t")))
        self._cells = {}   # sheet name -> {cell ref: value}

    def sheet_names(self):
        return list(self._sheet_part)

    def _cell_value(self, c):
        t = c.get("t")
        if t == "inlineStr":
            is_el = c.find(_MAIN_NS + "is")
            if is_el is None:
                return ABSENT
            return "".join(x.text or "" for x in is_el.iter(_MAIN_NS + "t"))
        v = c.find(_MAIN_NS + "v")
        if v is None or v.text is None:
            # A formula with no <v> means the cache was dropped; a bare empty
            # cell (style only) means there is nothing there at all.
            return NO_CACHE if c.find(_MAIN_NS + "f") is not None else ABSENT
        raw = v.text
        if t == "s":                       # index into sharedStrings
            try:
                return self._shared[int(raw)]
            except (ValueError, IndexError):
                return raw
        if t == "str":                     # literal string result of a formula
            return raw
        if t == "e":                       # error cell: #N/A, #DIV/0!, ...
            return NA if raw.strip() == "#N/A" else raw
        if t == "b":
            return raw not in ("0", "false", "FALSE")
        try:                               # no t -> numeric
            return float(raw)
        except ValueError:
            return raw

    def _load(self, sheet_name):
        part = self._sheet_part.get(sheet_name)
        if part is None:
            raise KeyError(f"no sheet named {sheet_name!r} in {self.path} "
                           f"(have: {', '.join(self.sheet_names())})")
        cells = {}
        for c in ET.fromstring(self._parts[part]).iter(_MAIN_NS + "c"):
            ref = c.get("r")
            if ref:
                cells[ref] = self._cell_value(c)
        self._cells[sheet_name] = cells
        return cells

    def cached(self, sheet_name, cell_ref):
        """Cached value of one cell: float, str, NA (#N/A), NO_CACHE or ABSENT."""
        cells = self._cells.get(sheet_name)
        if cells is None:
            cells = self._load(sheet_name)
        return cells.get(cell_ref, ABSENT)


_READER = None


def cached(sheet_name, cell_ref):
    """Module-level accessor; opens the workbook once, on first use."""
    global _READER
    if _READER is None:
        _READER = WorkbookReader(WORKBOOK_PATH)
    return _READER.cached(sheet_name, cell_ref)


# Label prefix -> real workbook tab name.
SHEET_OF_PREFIX = {
    "Summary": "Summary",
    "Geometry": "Geometry",
    "Electrochem": "Electrochemistry",
    "Echem": "Electrochemistry",
    "Chemistry": "Chemistry",
    "Biology": "Biology",
    "MassXfer": "Mass Transfer",
    "AMYBO03": "AMYBO03",
    "Calib": "Calibrations",
}

_LABEL_RE = re.compile(r"^(\w+)\s+(\$?[A-Z]{1,3}\$?[0-9]{1,7})\b")


def cell_of(label):
    """('MassXfer D108 DO_ss (mg/L)') -> ('Mass Transfer', 'D108')."""
    m = _LABEL_RE.match(label)
    if not m:
        raise ValueError(f"cannot parse a workbook cell out of label {label!r}")
    prefix, ref = m.group(1), m.group(2).replace("$", "")
    if prefix not in SHEET_OF_PREFIX:
        raise ValueError(f"unknown sheet prefix {prefix!r} in label {label!r}")
    return SHEET_OF_PREFIX[prefix], ref


# ============================================================================
# OUTPUT  - final outputs grouped by sheet. The workbook cell is carried in the
#           label and read live; there is deliberately NO expected value here.
# ============================================================================
# Each entry: (label carrying "<Sheet> <Cell>", computed value)
OUTPUTS = [
    # --- Geometry ---
    ("Geometry D42  Resulting liquid level (mm)",      h_actual),
    ("Geometry D43  Sparge depth (mm)",                sparge_depth),
    ("Geometry D90  geom_check (text)",                geom_check),
    ("Geometry D54  media_vol_warn",                   media_vol_warn),
    ("Geometry D55  depth_warn",                       depth_warn),
    ("Geometry D93  elec_sub_L_act (mm)",              elec_sub_L_act),

    # --- Electrochemistry current density (rows 40-76) ---
    ("Echem D46  anode wetted area (cm2)",             A_anode_wet),
    ("Echem D47  cathode wetted area (cm2)",           A_cath_wet),
    ("Echem D48  anode current density (mA/cm2)",      j_anode),
    ("Echem D49  cathode current density (mA/cm2)",    j_cathode),
    ("Echem D75  max anode current density (mA/cm2)",  j_anode_max),
    ("Electrochem D23  V_H2_gen (mL/min)",             V_H2_gen),
    ("Electrochem D24  V_O2_gen (mL/min)",             V_O2_gen),
    ("Electrochem D25  V_gas_total (mL/min)",          V_gas_total),
    ("Electrochem D20  I_valid",                       I_valid),

    # --- Electrochemistry: calculated faradaic split (wave-4, rows 78-89) ---
    ("Echem D85  ec_DO_design (mol/m3)",               ec_DO_design),
    ("Echem D129 DO_lag_ref (mol/m3)",                 DO_lag_ref),
    ("Echem D130 DO_lag_tol (-)",                      DO_lag_tol),
    ("Echem D131 O2_ORR_lag (mol/h)",                  O2_ORR_lag),
    ("Echem D132 O2_net_lag (mol/h)",                  O2_net_lag),
    ("Echem D133 rH2_lag (mol/h)",                     rH2_lag),
    ("Echem D134 DO_lag_ref_chk",                      DO_lag_ref_chk),
    ("Echem D141 n_ORR_eff (e-/O2)",                  n_ORR_eff),
    ("Echem D86  i_ORR_design (A)",                    i_ORR_design),
    ("Echem D87  i_ORR_ceiling (A)",                   i_ORR_ceiling),
    ("Echem D88  etaF_calc (-)",                       etaF_calc),
    ("Echem D89  etaF_calc_min (-)",                   etaF_calc_min),
    # --- Electrochemistry: hydrogen peroxide (wave-4, rows 90-99) ---
    ("Echem D93  r_H2O2 (mg/L/h)",                     r_H2O2),
    ("Echem D95  H2O2_ss (mg/L)",                      H2O2_ss),
    ("Echem D96  H2O2_lag_1h (mg/L)",                  H2O2_lag_1h),
    ("Echem D98  t_H2O2_thresh (min)",                 t_H2O2_thresh),
    ("Echem D99  H2O2_flag",                           H2O2_flag),
    ("Echem D150 ec_DO_lag (mol/m3)",                  ec_DO_lag),
    ("Echem D151 k_H2O2_anode (1/s)",                  k_H2O2_anode),
    ("Echem D152 r_H2O2_lag (mg/L/h)",                 r_H2O2_lag),
    # --- Electrochemistry: anodic charge budget (wave-4, rows 100-104) ---
    ("Echem D103 f_Cl_anode (-)",                      f_Cl_anode),
    ("Echem D104 etaF_OER_calc (-)",                   etaF_OER_calc),
    # --- Electrochemistry: cell-voltage budget (wave-4, rows 105-122) ---
    ("Echem D111 eta_anode (V)",                       eta_anode),
    ("Echem D112 eta_cath (V)",                        eta_cath),
    ("Echem D117 R_cell (ohm)",                        R_cell),
    ("Echem D118 V_IR (V)",                            V_IR),
    ("Echem D119 V_cell_est (V)",                      V_cell_est),
    ("Echem D121 V_headroom (V)",                      V_headroom),
    ("Echem D122 V_flag",                              V_flag),
    ("Echem D142 I_at_gerrit_max (A)",                 I_at_gerrit_max),
    ("Echem D143 V_at_gerrit_max (V)",                 V_at_gerrit_max),
    ("Echem D144 V_gerrit_flag",                       V_gerrit_flag),
    # --- Electrochemistry: anodic H2 oxidation (R1-08; f_HOR_anode is an empty data gap) ---
    ("Echem D146 ec_C_H2_sat (mol/m3)",                ec_C_H2_sat),
    ("Echem D147 i_HOR_lim (A)",                       i_HOR_lim),
    ("Echem D148 f_HOR_lim (-)",                       f_HOR_lim),
    ("Echem D149 r_H2_HOR (mol/h)",                    r_H2_HOR),

    # --- Summary tab (every cell with a Value/result) ---
    ("Summary D13  CO2 pulse duration (s)",            S_D13),
    ("Summary D14  CO2 pulse duration rounded (s)",    S_D14),
    ("Summary D15  CO2 sparge interval (min)",         S_D15),
    ("Summary D16  CO2 sparge interval rounded (min)", S_D16),
    ("Summary D19  Vial geometry consistent?",         S_D19),
    ("Summary D20  Reactor calibrated?",               S_D20),
    ("Summary D21  O2 at/under optimum?",              S_D21),
    ("Summary D22  O2 above minimum?",                 S_D22),
    ("Summary D23  Interval relaxable?",               S_D23),
    ("Summary D24  H2 headspace safe?",                S_D24),
    ("Summary D25  Bubble model valid?",               S_D25),
    ("Summary D26  CO2 supply : demand",               S_D26),
    ("Summary D27  Pulse >= solenoid floor?",          S_D27),
    ("Summary D28  Dosing window OK?",                 S_D28),
    ("Summary D29  Carryover risk?",                   S_D29),
    ("Summary D30  Tip-speed shear OK?",               S_D30),
    ("Summary D31  Media volume fits vial?",           S_D31),
    ("Summary D32  Liquid level OK?",                  S_D32),
    ("Summary D33  LED current-law in range?",         S_D33),
    ("Summary D34  Organism DO data present?",         S_D34),
    ("Summary D35  Endpoint pH (activity scale)",      S_D35),
    ("Summary D36  C_eff_Cl2 (mg/L)",                  S_D36),
    ("Summary D38  Steady-state DO (mg/L)",            S_D38),
    ("Summary D39  Sparge interval if O2 handled (min)", S_D39),
    ("Summary D40  Stir-bar tip speed (m/s)",          S_D40),
    ("Summary D41  Carbon margin at cycle trough (x)", S_D41),
    ("Summary D95  As-run / optimised duty (x)",       S_D95),
    ("Summary D82  Cathodic faradaic efficiency",      S_D82),
    ("Summary D83  Estimated cell voltage (V)",        S_D83),
    ("Summary D84  Cell-voltage verdict",              S_D84),
    ("Summary D85  Peroxide verdict",                  S_D85),
    ("Summary D86  Electrode-surface pH verdict",      S_D86),
    ("Summary D87  Chlorine headroom (V)",             S_D87),
    ("Summary D88  Copper dissolution headroom (V)",   S_D88),
    ("Summary D89  Measured (activity-scale) pH",      S_D89),
    ("Summary D90  Surface kLa required (1/h)",        S_D90),
    # --- Summary iterH block (rows 111-128) ---
    ("Summary D111 Vent model (input echo)",           S_D111),
    ("Summary D112 O2 sizing phase (input echo)",      S_D112),
    ("Summary D113 Vent air ingress in use (mL/min)",    S_D113),
    ("Summary D114 Cycle-mean DO growth (mg/L)",       S_D114),
    ("Summary D115 Peak DO growth (mg/L)",             S_D115),
    ("Summary D116 Cycle-mean DO lag (mg/L)",          S_D116),
    ("Summary D117 Peak DO lag (mg/L)",                S_D117),
    ("Summary D118 Peak under ceiling? growth",        S_D118),
    ("Summary D119 Peak under ceiling? lag",           S_D119),
    ("Summary D120 DO target reachable? growth",       S_D120),
    ("Summary D121 DO target reachable? lag",          S_D121),
    ("Summary D122 Surface kLa required growth (1/h)", S_D122),
    ("Summary D123 Surface kLa required lag (1/s)",    S_D123),
    ("Summary D124 Headspace O2 fraction growth",      S_D124),
    ("Summary D125 Headspace O2 fraction lag",         S_D125),
    ("Summary D126 Headspace H2 fraction lag",         S_D126),
    ("Summary D127 Headspace CO2 fraction",            S_D127),
    ("Summary D128 DO target and pH band together?",   S_D128),
    ("Summary D129 Headspace sag per cycle (-)",       S_D129),
    ("Summary D130 Sealed-cap plausibility",           S_D130),
    ("Summary A15  CO2 sparge interval label",         S_A15),
    ("Summary F121 Lag target note",                   S_F121),

    # --- Chemistry ---
    ("Chemistry D103  pH_op (concentration scale)",    pH_op),
    ("Chemistry D104  HOCl fraction at op pH",         pH_fHOCl),
    ("Chemistry D108  Time to ~1 ppm HOCl (min)",      bleach_t1ppm),
    ("Chemistry D109  bleach_flag",                    bleach_flag),
    ("Chemistry D110  pH_band_flag",                   pH_band_flag),
    ("Chemistry D125  HOCl_max (mg/L)",                HOCl_max),
    ("Chemistry D133  I_Cl (A)",                       I_Cl),
    ("Chemistry D134  P_HOCl (mol/L/s)",               P_HOCl),
    ("Chemistry D271  k_Cl_turn (1/s)",                k_Cl_turn),
    ("Chemistry D278  Cl_free_frac (-)",               Cl_free_frac),
    ("Chemistry D129  km_Cl (cm/s)",                   km_Cl),
    ("Chemistry D132  I_Cl_mt (A)",                    I_Cl_mt),
    ("Chemistry D154  NH2Cl_lo (mg/L)",                NH2Cl_lo),
    ("Chemistry D155  NH2Cl_hi (mg/L)",                NH2Cl_hi),
    ("Chemistry D139  HOCl_ss (M)",                    HOCl_ss),
    ("Chemistry D143  NH2Cl (mg/L)",                   NH2Cl_mgL),
    ("Chemistry D145  C_eff (mg/L)",                   C_eff),
    ("Chemistry D149  Cl_pool_mgL (mg/L)",             Cl_pool_mgL),
    ("Chemistry D156  C_eff_lo (mg/L)",                C_eff_lo),
    ("Chemistry D157  C_eff_hi (mg/L)",                C_eff_hi),
    ("Chemistry D226  C_eff_Cl2 (mg/L)",               C_eff_Cl2),
    ("Chemistry D161  metal_leach_rate (mg/L/h)",      metal_leach_rate),
    ("Chemistry D163  metal_flag",                     metal_flag),
    # --- Chemistry: conductivity & activity (wave-4, rows 165-197) ---
    ("Chemistry D180  kappa_med (S/m)",                kappa_med),
    ("Chemistry D185  I_ionic (mol/L)",                I_ionic),
    ("Chemistry D186  A_DH (-)",                       A_DH),
    ("Chemistry D187  gam1 (-)",                       gam1),
    ("Chemistry D188  gam2 (-)",                       gam2),
    ("Chemistry D189  gam3 (-)",                       gam3),
    # --- Chemistry: electrode potentials & buffer capacity (wave-4, rows 199-220) ---
    ("Chemistry D207  E_HER (V vs SHE)",               E_HER),
    ("Chemistry D209  E_Cl_margin (V)",                E_Cl_margin),
    ("Chemistry D210  E_ORR2 (V vs SHE)",              E_ORR2),
    ("Chemistry D211  E_Cu_margin (V)",                E_Cu_margin),
    ("Chemistry D215  delta_diff (um)",                delta_diff),
    ("Chemistry D275  km_HPO4 (cm/s)",                 km_HPO4),
    ("Chemistry D276  km_HCO3 (cm/s)",                 km_HCO3),
    ("Chemistry D216  j_buffer_lim (mA/cm2)",          j_buffer_lim),
    ("Chemistry D251  D_HCO3 (m2/s)",                  D_HCO3),
    ("Chemistry D252  HCO3_op (mol/L)",                 HCO3_op),
    ("Chemistry D253  HPO4_op (mol/L)",                 HPO4_op),
    ("Chemistry D254  eta_anode_c (V)",                 eta_anode),
    ("Chemistry D255  pcet_credit_c (V)",               pcet_credit_op),
    ("Chemistry D256  E_anode_op (V vs SHE)",           E_anode_op),
    ("Chemistry D257  E0_HOCl (V)",                     E0_HOCl),
    ("Chemistry D258  E_HOCl_Cl (V vs SHE)",            E_HOCl_Cl),
    ("Chemistry D259  C_eff_lo_Cl2 (mg/L)",             C_eff_lo_Cl2),
    ("Chemistry D260  C_eff_hi_Cl2 (mg/L)",             C_eff_hi_Cl2),
    ("Chemistry D218  j_buffer_ratio (-)",             j_buffer_ratio),
    ("Chemistry D219  buffer_flag",                    buffer_flag),
    ("Chemistry D220  pH_meas (activity scale)",       pH_meas),

    # --- Biology ---
    ("Biology  D28  O2_ceil_uM (uM)",                  O2_ceil_uM),
    ("Biology  D32  P_dry basis for CO2 sparge (Pa)",  p_CO2_sparge),
    ("Biology  D35  CO2_carbon_margin (x)",            CO2_carbon_margin),
    ("Biology  D89  spg_dur_opt_b (s)",                spg_dur_opt_b),
    ("Biology  D90  t_gap_H2_LFL (min)",               t_gap_H2_LFL),
    ("Biology  D91  t_gap_O2_LOC (min)",               t_gap_O2_LOC),
    ("Biology  D92  spg_int_H2safe_saw (min)",         spg_int_H2safe_saw),
    ("Biology  D115 O2_src_l_b (mol/h)",               O2_src_l_b),
    ("Biology  D116 F_gap_l_b (mol/h)",                F_gap_l_b),
    ("Biology  D117 n_hs_gas_b (mol)",                 n_hs_gas_b),
    ("Biology  D118 flush_ret_opt_b (-)",              flush_ret_opt_b),
    ("Biology  D119 y_O2_end_b (-)",                   y_O2_end_b),
    ("Biology  D13  H2_cons (mol/h)",                  H2_cons),
    ("Biology  D96  H2_HOR_b (mol/h)",                 H2_HOR_b),
    ("Biology  D97  C_cycle_start_b (mol/m3)",         C_cycle_start_b),
    ("Biology  D98  CO2_margin_trough (x)",            CO2_margin_trough),
    ("Biology  D37  pH_CO2_unbuf",                     pH_CO2_unbuf),
    ("Biology  D42  t_H2_sat (min)",                   t_H2_sat),
    ("Biology  D43  H2_turnover (1/h)",                H2_turnover),
    ("Biology  D44  H2_safety",                        H2_safety),
    ("Biology  D83  n_flamm_src (mol/h)",              n_flamm_src),
    ("Biology  D84  y_H2_hs_lag (-)",                  y_H2_hs_lag),
    ("Biology  D85  y_O2_hs_lag (-)",                  y_O2_hs_lag),
    ("Biology  D86  duty_H2safe (-)",                  duty_H2safe),
    ("Biology  D87  spg_int_H2safe (min)",             spg_int_H2safe),
    ("Biology  D88  N2_sweep_H2safe (mL/min)",         N2_sweep_H2safe),
    ("Biology  D60  DO_frac_target (-)",               DO_frac_target),
    ("Biology  D113 H2_src_l_b (mol/h)",               H2_src_l_b),
    ("Biology  D114 y_H2_end_b (-)",                   y_H2_end_b),
    ("Biology  D111 F_vent_ex_b (mol/h)",              F_vent_ex_b),
    ("Biology  D112 y_O2_air_b (-)",                   y_O2_air_b),

    # --- Mass Transfer ---
    ("MassXfer D29  sigma (N/m)",                      sigma),
    ("MassXfer D30  rho_L (kg/m3)",                    rho_L),
    ("MassXfer D32  D_O2 (m2/s)",                      D_O2),
    ("MassXfer D53  kLa_avg (1/s)",                    kLa_avg),
    ("MassXfer D55  strip_avg (mol/h)",                strip_avg),
    ("MassXfer D56  strip_ratio (x)",                  strip_ratio),
    ("MassXfer D57  kLa_req (1/s)",                    kLa_req),
    ("MassXfer D59  carry_flag",                       carry_flag),
    ("MassXfer D64  bubble_regime",                    bubble_regime),
    ("MassXfer D65  t_O2_ceiling (min)",               t_O2_ceiling),
    ("MassXfer D66  t_O2_ceiling_strip (min)",         t_O2_ceiling_strip),
    ("MassXfer D74  surf_ratio (x)",                   surf_ratio),
    ("MassXfer D77  hs_flush_time (min)",              hs_flush_time),
    ("MassXfer D78  O2_removal_ratio (x)",             O2_removal_ratio),
    ("MassXfer D79  t_O2_ceiling_lag (min)",           t_O2_ceiling_lag),
    ("MassXfer D80  t_O2_ceiling_rem (min)",           t_O2_ceiling_rem),
    ("MassXfer D92  spg_int_opt_s (s)",                spg_int_opt_s),
    ("MassXfer D93  duty_actual",                      duty_actual),
    ("MassXfer D241 pulse_res (s)",                    pulse_res),
    ("MassXfer D242 spg_dur_run (s)",                  spg_dur_run),
    ("MassXfer D94  opt_binding",                      opt_binding),
    ("MassXfer D95  od_ok",                            od_ok),
    ("MassXfer D98  kLa_surf_used (1/s)",              kLa_surf_used),
    ("MassXfer D108 DO_ss (mg/L)",                     DO_ss),
    ("MassXfer D110 DO_ss_vs_min",                     DO_ss_vs_min),
    ("MassXfer D111 tip_warn",                         tip_warn),
    ("MassXfer D113 sched_regime",                     sched_regime),
    ("MassXfer D231 M_O2 (g/mol)",                     M_O2),
    ("MassXfer D232 DO_at_carbon (mol/m3)",            DO_at_carbon),
    ("MassXfer D124 pulses_h (/h)",                    pulses_h),
    ("MassXfer D125 pulses_d (/d)",                    pulses_d),
    ("MassXfer D126 CO2_sd_ratio (x)",                 CO2_sd_ratio),
    ("MassXfer D127 O2_accum (mol)",                   O2_accum),
    ("MassXfer D128 O2_strip_pulse (mol)",             O2_strip_pulse),
    ("MassXfer D129 sched_bal (x)",                    sched_bal),
    ("MassXfer D130 dur_ok",                           dur_ok),
    ("MassXfer D131 kL_surf_crit (m/s)",               kL_surf_crit),
    ("MassXfer D133 DO_ss_sawtooth (mol/m3)",          DO_ss_sawtooth),
    ("MassXfer D134 spg_int_regime",                   spg_int_regime),
    ("MassXfer D135 DO_ss_sawtooth_lag (mol/m3)",      DO_ss_sawtooth_lag),
    # --- Mass Transfer: headspace O2 balance & DO-limited interval (wave-4) ---
    ("MassXfer D179 DO_target (mol/m3)",               DO_target),
    ("MassXfer D180 DO_surf_excess (mol/m3)",          DO_surf_excess),
    ("MassXfer D181 DO_surf_excess_lag (mol/m3)",      DO_surf_excess_lag),
    ("MassXfer D182 hs_O2_allow (mol/m3)",             hs_O2_allow),
    ("MassXfer D183 y_O2_star (-)",                    y_O2_star),
    ("MassXfer D184 duty_DO (-)",                      duty_DO),
    ("MassXfer D185 spg_int_DO (min)",                 spg_int_DO),
    ("MassXfer D186 kLa_surf_req (1/s)",               kLa_surf_req),
    ("MassXfer D187 y_O2_actual (-)",                  y_O2_actual),
    ("MassXfer D188 DO_hs_floor (mol/m3)",             DO_hs_floor),
    # --- Mass Transfer: mass-conserving CO2 limit cycle (wave-4) ---
    ("MassXfer D138 D_CO2 (m2/s)",                     D_CO2),
    ("MassXfer D162 CO2aqc_ss (mol/L)",                CO2aqc),
    ("MassXfer D163 vent_floor_chk",                   vent_floor_chk),
    ("MassXfer D164 sched_valid",                      sched_valid),
    ("MassXfer D192 Vg_CO2 (m3)",                      Vg_CO2),
    ("MassXfer D193 pool_a (-)",                       pool_a),
    ("MassXfer D194 pool_b (mol/m3)",                  pool_b),
    ("MassXfer D195 k_eff_CO2 (1/s)",                  k_eff_CO2),
    ("MassXfer D196 pool_beta_ratio (x)",              pool_beta_ratio),
    ("MassXfer D197 pool_e (-)",                       pool_e),
    ("MassXfer D198 C_cycle_start (mol/m3)",           C_cycle_start),
    ("MassXfer D199 C_cycle_peak (mol/m3)",            C_cycle_peak),
    ("MassXfer D200 CO2_cyc_avg_new (mol/m3)",         CO2_cyc_avg_new),
    ("MassXfer D143 k_vent (1/s)",                     k_vent),
    ("MassXfer D144 tau_hs (min)",                     tau_hs),
    # --- Mass Transfer: iterH unified headspace balance (rows 300-382) ---
    ("MassXfer D308 F_vent_ex (mol/h)",                F_vent_ex),
    ("MassXfer D424 F_N2 (mol/h)",                     F_N2),
    ("MassXfer D425 F_dil (mol/h)",                    F_dil),
    ("MassXfer D426 N2 sweep for DO at carbon duty (mL/min)", N2_for_DO),
    ("Chemistry D321 pH_hi_c", pH_hi_c),
    ("Chemistry D323 resid_noC_hi (mol/L)", resid_noC_hi),
    ("Chemistry D324 CO2_pH_hi (mol/L)", CO2_pH_hi),
    ("MassXfer D429 CO2_pH_hi_mt (mol/m3)", CO2_pH_hi_mt),
    ("MassXfer D432 spg_int_pH (min)", spg_int_pH),
    ("MassXfer D433 spg_int_pH_opt (min)", spg_int_pH_opt),
    ("MassXfer D434 ph_unreach", ph_unreach),
    ("MassXfer D435 pool_start_chk", pool_start_chk),
    ("MassXfer I440 grid CO2 mean, first row", pH_grid_C[0]),
    ("MassXfer I539 grid CO2 mean, last row", pH_grid_C[-1]),
    ("Summary D101 pH-ceiling interval", spg_int_pH),
    ("Biology  D125 F_dil_b (mol/h)",                  F_dil_b),
    ("Biology  D120 remedy_res",                       remedy_res),
    ("Summary D99 N2 for DO at carbon duty",           N2_for_DO),
    ("Summary D100 N2 for lag H2 below LFL",           N2_sweep_H2safe),
    ("MassXfer D384 vent_name_3",                      vent_name_3),
    ("MassXfer D385 Q_backdraw (mL/min)",              Q_backdraw),
    ("MassXfer D386 Q_vent_used (mL/min)",             Q_vent_used),
    ("MassXfer D387 H2_HOR_mt (mol/h)",                H2_HOR_mt),
    ("MassXfer D388 y_H2_end_l (-)",                   y_H2_end_l),
    ("MassXfer D389 hs_sag (-)",                       hs_sag),
    ("MassXfer D390 hs_sag_max (-)",                   hs_sag_max),
    ("MassXfer D391 hs_sag_chk",                       hs_sag_chk),
    ("MassXfer D314 H2_src_l (mol/h)",                 H2_src_l),
    ("MassXfer D91  spg_int_opt (min)",                spg_int_opt),
    ("MassXfer D134 spg_int_regime",                   spg_int_regime),
    ("MassXfer D313 H2_src_g (mol/h)",                 H2_src_g),
    ("MassXfer D317 O2_src_sched (mol/h)",             O2_src_sched),
    ("MassXfer D318 H2_src_sched (mol/h)",             H2_src_sched),
    ("MassXfer D319 CO2_fix_sched (mol/h)",            CO2_fix_sched),
    ("MassXfer D320 flush_vol_opt (-)",                flush_vol_opt),
    ("MassXfer D322 saw_factor (-)",                   saw_factor),
    ("MassXfer D323 flush_vol (-)",                    flush_vol),
    ("MassXfer D324 flush_ret (-)",                    flush_ret),
    ("MassXfer D325 t_gap_h (h)",                      t_gap_h),
    ("MassXfer D326 tau_L_h (h)",                      tau_L_h),
    ("MassXfer D328 F_hs_net_g (mol/h)",               hs_g["F_net"]),
    ("MassXfer D329 y_O2_mf_g (-)",                    y_O2_mf_g),
    ("MassXfer D330 y_H2_mf_g (-)",                    y_H2_mf_g),
    ("MassXfer D331 F_gap_g (mol/h)",                  F_gap_g),
    ("MassXfer D332 x_hs_g (-)",                       x_hs_g),
    ("MassXfer D335 dy_O2_g (-)",                      hs_g["dy"]),
    ("MassXfer D336 y_O2_end_g (-)",                   y_O2_end_g),
    ("MassXfer D337 y_O2_post_g (-)",                  hs_g["y_post"]),
    ("MassXfer D338 y_O2_avg_g (-)",                   y_O2_avg_g),
    ("MassXfer D339 DO_surf_excess_g (mol/m3)",        DO_surf_excess_g),
    ("MassXfer D340 DO_mf_g (mol/m3)",                 DO_mf_g),
    ("MassXfer D341 DO_avg_g (mol/m3)",                DO_avg_g),
    ("MassXfer D342 DO_peak_g (mol/m3)",               DO_peak_g),
    ("MassXfer D346 kLa_margin_g (x)",                 kLa_margin_g),
    ("MassXfer D347 DO_feas_g",                        DO_feas_g),
    ("MassXfer D348 DO_peak_chk_g",                    DO_peak_chk_g),
    ("MassXfer D350 F_hs_net_l (mol/h)",               hs_l["F_net"]),
    ("MassXfer D351 y_O2_mf_l (-)",                    y_O2_mf_l),
    ("MassXfer D352 y_H2_mf_l (-)",                    y_H2_mf_l),
    ("MassXfer D353 F_gap_l (mol/h)",                  F_gap_l),
    ("MassXfer D354 x_hs_l (-)",                       x_hs_l),
    ("MassXfer D355 phi_hs_l (-)",                     hs_l["phi"]),
    ("MassXfer D356 psi_hs_l (-)",                     hs_l["psi"]),
    ("MassXfer D358 y_O2_end_l (-)",                   y_O2_end_l),
    ("MassXfer D359 y_O2_post_l (-)",                  hs_l["y_post"]),
    ("MassXfer D360 y_O2_avg_l (-)",                   y_O2_avg_l),
    ("MassXfer D361 DO_mf_l (mol/m3)",                 DO_mf_l),
    ("MassXfer D362 DO_avg_l (mol/m3)",                DO_avg_l),
    ("MassXfer D363 DO_peak_l (mol/m3)",               DO_peak_l),
    ("MassXfer D367 kLa_margin_l (x)",                 kLa_margin_l),
    ("MassXfer D368 DO_feas_l",                        DO_feas_l),
    ("MassXfer D369 DO_peak_chk_l",                    DO_peak_chk_l),
    ("MassXfer D371 F_gap_sched (mol/h)",              F_gap_sched),
    ("MassXfer D372 DO_avg_sched (mol/m3)",            DO_avg_sched),
    ("MassXfer D373 DO_peak_sched (mol/m3)",           DO_peak_sched),
    ("MassXfer D374 DO_peak_band",                     DO_peak_band),
    ("MassXfer D375 pool_D_raw (mol/m3)",              pool_D_raw),
    ("MassXfer D376 pool_x (-)",                       pool_x),
    ("MassXfer D379 pool_D_gap (mol/m3)",              pool_D_gap),
    ("MassXfer D380 pool_ret (-)",                     pool_ret),
    ("MassXfer D381 y_CO2_mf (-)",                     y_CO2_mf),
    ("MassXfer D382 C_CO2_mf (mol/m3)",                C_CO2_mf),
    # --- iterM: pulse-volume fit, carryover, CO2 uptake, DIC capacity, dry-gas basis, O2 salting-out, PCET coupling ---
    ("MassXfer D401 fit_n (points)",                    float(fit_n)),
    ("MassXfer D402 fit_St (s)",                        fit_St),
    ("MassXfer D403 fit_SV (mL)",                       fit_SV),
    ("MassXfer D404 fit_Stt (s2)",                      fit_Stt),
    ("MassXfer D405 fit_StV (mL.s)",                    fit_StV),
    ("MassXfer D118 min_sparge_cal (s)",                min_sparge_cal),
    ("MassXfer D119 has_cal (count)",                   has_cal),
    ("MassXfer D120 calibration verdict",               cal_warning),
    ("MassXfer D310 O2_src_l (mol/h)",                  O2_src_l),
    ("MassXfer D394 O2_net_lag_mt (mol/h)",             O2_net_lag_mt),
    ("MassXfer D395 rH2_lag_mt (mol/h)",                rH2_lag_mt),
    ("MassXfer D396 pulse_floor_default (s)",           pulse_floor_default),
    ("MassXfer D407 Q_CO2_fit (mL/s)",                  Q_CO2_fit),
    ("MassXfer D408 pulse_V0 (mL)",                     pulse_V0),
    ("MassXfer D409 spg_dur_eq_opt (s)",                spg_dur_eq_opt),
    ("MassXfer D410 spg_dur_eq (s)",                    spg_dur_eq),
    ("MassXfer D411 V_pulse (mL)",                      V_pulse),
    ("MassXfer D90  spg_dur_opt (s)",                   spg_dur_opt),
    ("MassXfer D112 spg_int_carbon (min)",              spg_int_carbon),
    ("MassXfer D123 CO2_pulse (mol)",                   CO2_pulse),
    ("MassXfer D412 carry_n",                           float(carry_n)),
    ("MassXfer D413 Q_carry_max (mL/s)",                Q_carry_max),
    ("MassXfer D414 carry_flag_usg",                    carry_flag_usg),
    ("MassXfer D415 DIC_cap_mt (-)",                    DIC_cap),
    ("MassXfer D416 V_L_CO2 (m3)",                      V_L_CO2),
    ("MassXfer D417 CO2_uptake_ratio (x)",              CO2_uptake_ratio),
    ("MassXfer D206 p_sat_w (Pa)",                      p_sat_w),
    ("MassXfer D418 P_dry (Pa)",                        P_dry),
    ("MassXfer D145 C_sat_CO2 (mol/m3)",                C_sat_CO2),
    ("Chemistry D292 h_ref_DIC (mol/L)",                h_ref_DIC),
    ("Chemistry D293 r_HCO3_ref (-)",                   r_HCO3_ref),
    ("Chemistry D294 HCO3_ref (mol/L)",                 HCO3_ref),
    ("Chemistry D295 beta_nonC (mol/L/pH)",             beta_nonC),
    ("Chemistry D296 DIC_cap (-)",                      DIC_cap),
    ("Biology  D121 I_ionic_b (mol/L)",                 I_ionic_b),
    ("Biology  D123 f_salt_O2 (-)",                     f_salt_O2),
    ("Biology  D24  H_O2_T (mol/m3/Pa)",                H_O2_T),
    ("Biology  D78  spg_dur_b (s)",                     spg_dur_b),
    ("Echem D161 ec_jbuf_ratio (-)",                    ec_jbuf_ratio),
    ("Echem D162 pcet_credit_op (V)",                   pcet_credit_op),
    ("Echem D163 pcet_credit_gmax (V)",                 pcet_credit_gmax),
    ("Summary D131 NaHCO3 for target pH (g/L)",        S_D131),
    ("Summary D132 Extra alkalinity (mM)",             S_D132),
    ("Chemistry D304 alk_pH_target_c (pH)",            alk_pH_target_c),
    ("Chemistry D305 alk_resid_t (mol/L)",              alk_resid_t),
    ("AMYBO03 D54 PT_AMYBO03 (mol/L)",                 PT_amy),
    ("AMYBO03 D55 SID_AMYBO03 (mol/L)",                SID_amy),
    ("AMYBO03 D56 NT_AMYBO03 (mol/L)",                 NT_amy),
    ("AMYBO03 D58 kappa0_AMYBO03 (S/m)",               kappa0_amy),
    ("AMYBO03 D59 I_AMYBO03 (mol/L)",                  I_amy),
    ("Summary D135 CO2 uptake ratio (x)",               S_D135),
    ("Summary D136 Carryover velocity rule of thumb",   S_D136),
]


Cl_model_check = ("UNSUPPORTED – nitrogen capacity exhausted" if pH_Cl > 0 and Cl_bound >= pH_NT
                  and P_HOCl > pH_NT / (tau_NH2Cl * 3600) else "OK")
chlorine_note = (Cl_model_check if Cl_model_check != "OK" else
                "Effective chlorine on the as-Cl2 basis; zero for chloride-free medium. Lifetime and potency require measurement.")
OUTPUTS.extend([
    ("Chemistry E107 chlorine production note", "Naive FE=1 ceiling; overstates operative production by " + xltext(bleach_rate / (P_HOCl * M_HOCl_mg * 3600), "0") + " times" if P_HOCl > 0 else "No chlorine production at the selected chloride inventory"),
    ("Chemistry D310 DIC reference validity", DIC_ref_check),
    ("Chemistry D311 combined chlorine inventory", Cl_bound),
    ("Chemistry D312 chloramine validity", Cl_model_check),
    ("Chemistry D317 NaHCO3 added (g/L)", NaHCO3_add_gL),
    ("Chemistry D318 alk_add_M (mol/L)", alk_add_M),
    ("Summary F36 chlorine validity", chlorine_note),
    ("MassXfer D420 executable interval", spg_int_run),
    ("Summary D43 current mA", I_app * 1000),
    ("Summary D44 anode current density", j_anode),
    ("Summary D46 maximum power", power_max),
    ("Summary D47 maximum current mA", I_max_mA),
    ("Summary D48 maximum anode current density", j_anode_max),
    # Measured electrode k_m and monochloramine lifetime enter through the Calibrations tab
    ("Calib D176 cal_km_O2 value in use", cal_km_O2 if isnum(cal_km_O2) else NO_CAL_TXT),
    ("Calib D189 cal_tau_NH2Cl value in use", cal_tau_NH2Cl if isnum(cal_tau_NH2Cl) else NO_CAL_TXT),
    ("Echem D83  km_O2 in use (cm/s)", km_O2),
    ("Chemistry D142 tau_NH2Cl in use (h)", tau_NH2Cl),
    ("Chemistry D315 P_Cl_max (mol/L/s)", P_Cl_max),
])

# Declared input -> Summary cell. Checked before anything is compared.
INPUT_CELLS = [
    ("Reactor_sel",   "D2",  Reactor_sel),
    ("electrode_sel", "D3",  electrode_sel),
    ("organism_sel",  "D4",  organism_sel),
    ("media_sel",     "D5",  media_sel),
    ("led_intensity", "D6",  led_intensity),
    ("stir_rpm_set",  "D7",  stir_rpm_set),
    ("temp_C",        "D8",  temp_C),
    ("media_volume",  "D9",  media_volume),
    ("P_atm_set",     "D10", P_atm_set),
    ("NaHCO3_add_gL", "D133", NaHCO3_add_gL),
    ("N2_sweep_set",  "D98",  N2_sweep_set),
    ("vent_model_sel", "D111", vent_model_sel),
    ("O2_phase_sel",  "D112", O2_phase_sel),
    ("user_spg_dur", "G13", user_spg_dur or 0.0),
    ("user_spg_int", "G15", user_spg_int or 0.0),
]


TOL = 0.005          # 0.5% relative, numeric outputs


def _fmt(v):
    if v is NO_CACHE:
        return "(no cache)"
    if v is ABSENT:
        return "(absent)"
    if isinstance(v, float):
        if math.isnan(v):
            return "#N/A"
        return f"{v:.10g}"
    return str(v)


def _short(v, width=22):
    """Table cell: full value if it fits, else truncated. Full text is always
    reprinted in the MISMATCHES block, so nothing is hidden by this."""
    s = _fmt(v)
    return s if len(s) <= width else s[:width - 3] + "..."


def _isnum(v):
    return (isinstance(v, (int, float)) and not isinstance(v, bool)
            and not (isinstance(v, float) and math.isnan(v)))


def _rel_err(comp, book):
    if not (_isnum(comp) and _isnum(book)):
        return None
    if book == 0:
        return abs(comp - book)
    return abs(comp - book) / abs(book)


def _match(comp, book, tol=TOL):
    """Within 0.5% (numeric) or exact (text). NaN matches the #N/A error cell."""
    if isinstance(comp, float) and math.isnan(comp):
        return isinstance(book, float) and math.isnan(book)
    if _isnum(comp) and _isnum(book):
        if book == 0:
            return abs(comp - book) < 1e-9
        return abs(comp - book) / abs(book) <= tol
    return str(comp).strip() == str(book).strip()


def _input_matches(declared, book):
    """A declaration matches its Summary cell; blank/absent counts as 0.0."""
    if book is NO_CACHE:
        return False
    if book is ABSENT or book is None or book == "":
        return declared == 0.0
    if _isnum(declared) and _isnum(book):
        return abs(declared - book) <= 1e-9 * max(1.0, abs(book))
    return str(declared).strip() == str(book).strip()


def check_inputs():
    """Compare the declared inputs against Summary D2:D10 and D111:D112.

    Returns the list of drifted (name, cell, declared, workbook) tuples. A twin
    run at different inputs from the workbook can neither confirm nor refute it,
    so the caller must refuse to compare outputs when this is non-empty.
    """
    drift = []
    for name, ref, declared in INPUT_CELLS:
        book = cached("Summary", ref)
        if not _input_matches(declared, book):
            drift.append((name, ref, declared, book))
    return drift


def main():
    if not os.path.exists(WORKBOOK_PATH):
        print(f"FATAL: workbook not found at {WORKBOOK_PATH}")
        return 2
    try:
        drift = check_inputs()
    except (zipfile.BadZipFile, ET.ParseError, KeyError) as exc:
        print(f"FATAL: cannot read {WORKBOOK_PATH}: {exc}")
        return 2

    print("=" * 108)
    print("electroPioreactorGasModel - independent re-derivation, verified against the workbook")
    print(f"Workbook: {WORKBOOK_PATH}")
    print(f"Inputs: reactor={Reactor_sel} ({rx_ver}), electrode={electrode_sel}, "
          f"organism={organism_sel}, media={media_sel}")
    print(f"        LED={led_intensity}%, stir={stir_rpm_set} rpm, T={temp_C} C, "
          f"V_charge={V_charge} mL, P_atm={P_atm:.0f} Pa")
    print("=" * 108)

    if drift:
        print()
        print("INPUT DRIFT - this script's declared inputs differ from Summary D2:D10 / D111:D112.")
        print("The comparison has NOT been run: a twin evaluated at different inputs")
        print("from the workbook would agree or disagree for reasons that mean nothing.")
        print()
        print(f"  {'INPUT':<16}{'CELL':<14}{'DECLARED HERE':>28}{'IN WORKBOOK':>28}")
        for name, ref, declared, book in drift:
            print(f"  {name:<16}{'Summary!' + ref:<14}{_fmt(declared):>28}{_fmt(book):>28}")
        print()
        print("Fix by setting the declarations at the top of this file to the workbook's")
        print("values (or by restoring the workbook's inputs), then re-run.")
        return 1

    verify_definition(WORKBOOK_PATH)

    hdr = f"{'OUTPUT':<50}{'CELL':<20}{'WORKBOOK':>22}{'MODEL':>22}  VERDICT"
    print(hdr)
    print("-" * 108)
    fails, uncached = [], []
    for label, comp in OUTPUTS:
        sheet, ref = cell_of(label)
        book = cached(sheet, ref)
        if book is NO_CACHE or book is ABSENT:
            uncached.append((label, sheet, ref, comp, book))
            verdict = "NO CACHED VALUE"
        elif _match(comp, book):
            verdict = "OK"
        else:
            fails.append((label, sheet, ref, comp, book))
            verdict = "MISMATCH"
        print(f"{label:<50}{sheet + '!' + ref:<20}{_short(book):>22}{_short(comp):>22}  {verdict}")
    print("-" * 108)

    n_ok = len(OUTPUTS) - len(fails) - len(uncached)
    print(f"{n_ok}/{len(OUTPUTS)} computed outputs match the workbook's cached values "
          f"within {TOL * 100:g}% (workbook: {WORKBOOK_PATH}, inputs verified identical)")

    if fails:
        print(f"\nMISMATCHES ({len(fails)}) - the model and the workbook genuinely disagree:")
        for label, sheet, ref, comp, book in fails:
            rel = _rel_err(comp, book)
            tail = f"  (relative error {rel * 100:.3g}%)" if rel is not None else ""
            print(f"  {label}")
            print(f"      {sheet}!{ref}  workbook={_fmt(book)}  model={_fmt(comp)}{tail}")

    if uncached:
        print(f"\nUNAVAILABLE ({len(uncached)}) - no cached value to compare against; "
              "open and save the workbook in Excel first:")
        for label, sheet, ref, comp, book in uncached:
            why = ("formula present, cache dropped" if book is NO_CACHE
                   else "cell absent or empty in the workbook")
            print(f"  {label}")
            print(f"      {sheet}!{ref}  {why}  model={_fmt(comp)}")

    if fails or uncached:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
