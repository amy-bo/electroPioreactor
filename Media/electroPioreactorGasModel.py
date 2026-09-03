#!/usr/bin/env python3
"""
electroPioreactorGasModel.py

Independent first-principles re-derivation of the electroPioreactor CO2/gas
spreadsheet (Media/electroPioreactorGasModel.xlsx), together with a verification
harness that compares this twin against the workbook FILE - never against a
snapshot of it.

The contract
------------
* The physics is computed HERE, independently. Every FINAL output - any derived
  numeric cell that nothing else references, plus every cell on the Summary tab
  - is derived from the input parameters and physical/chemical constants, and is
  never read back from the workbook.
* The comparison target is the workbook itself. `cached(sheet, ref)` opens
  electroPioreactorGasModel.xlsx (path resolved relative to this script, so it
  works from any working directory), unzips it in memory and returns the value
  Excel cached for that cell. There are no hard-coded expected numbers anywhere
  in the harness, so a stale twin and a moved-on workbook can no longer agree
  with each other by construction - which is exactly how an earlier version of
  this file managed to report "92/92 match" against its own stale copy.
* The inputs are ASSERTED, not assumed. The declarations below correspond to
  Summary D2:D10 and are checked against the workbook before anything is
  compared. On any drift the harness names the offending pairs and exits
  non-zero WITHOUT comparing outputs: a twin evaluated at different inputs from
  the workbook produces meaningless agreement (and meaningless disagreement).
* A workbook shipped without formula caches - Excel recomputes on load and some
  save paths drop them - is reported per cell as "no cached value", counted
  separately from a mismatch, and still exits non-zero. It is never silently
  scored as a match. The wave-4 revision drops the cache on every changed cell,
  so a freshly-written workbook reports a large "no cached value" block until it
  has been opened and saved in Excel once. That is expected.

Standard library only; openpyxl is not installable in this container. Run with:
    python3 electroPioreactorGasModel.py
Exit status is 0 only when the inputs match the workbook AND every output agrees
with the workbook's cached value within 0.5%.

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

import math
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from decimal import Decimal, ROUND_HALF_UP

# ============================================================================
# SUMMARY TAB - user inputs (the only free variables in the model)
#   These mirror Summary D2:D10 and are verified against the workbook at
#   startup (see check_inputs() at the bottom). Change them only together with
#   the workbook: the harness refuses to compare a twin run at other inputs.
# ============================================================================
Reactor_sel    = "ed04"            # D2
electrode_sel  = "Pt/Ti rod"       # D3
organism_sel   = "UdG (mixed)"     # D4
media_sel      = "UdG phosphate"   # D5
led_intensity  = 3.0               # D6  (%)
stir_rpm_set   = 1000.0            # D7  (rpm)
temp_C         = 25.0              # D8  (degC)
media_volume   = 0.0               # D9  (mL; blank in workbook -> 0.0 -> use recommended max)
P_atm_set      = 0.0               # D10 (Pa; blank in workbook -> 0.0 -> default 101325)

NA = float("nan")                  # spreadsheet #N/A sentinel for unmeasured data


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
headspace_V  = V_vial_total - V_charge - V_inserts  # D49 (mL)
stir_bar_L   = g["stir_L"]                          # D52 (mm)
media_vol_warn = "MEDIA > MAX WORKING VOLUME" if V_charge > V_max else "OK"     # D54
depth_warn     = "LIQUID OVER USABLE DEPTH" if h_actual > D_int else "OK"       # D55
geom_check     = ("VIAL GEOMETRY INCONSISTENT - measure true fill volume & bore depth"
                  if abs(A_x * D_int / 1000 - V_vial_total) > 3 else "OK")      # D90
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

# --- Henry solubilities (van 't Hoff) ---
H_O2ref  = 1.2e-5                                     # D21 (mol/m3/Pa)
H_O2T    = 1500.0                                     # D22 (K)
H_O2_T   = H_O2ref * math.exp(H_O2T * (1 / T_K - 1 / T_ref))   # D24
O2_ceil_atm = 0.30                                    # D25 (atm)
O2_ceil_Pa  = O2_ceil_atm * Pa_per_atm                # D26 (Pa)
O2_ceil_C   = H_O2_T * O2_ceil_Pa                     # D27 (mol/m3)
O2_ceil_uM  = O2_ceil_C * 1000                        # D28 (uM)

H_CO2ref = 3.3e-4                                     # D29
H_CO2T   = 2400.0                                     # D30
H_CO2_T  = H_CO2ref * math.exp(H_CO2T * (1 / T_K - 1 / T_ref))  # D31
p_CO2_sparge = P_atm                                  # D32 (Pa)
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
ec_DO_frac   = DO_frac_target                          # D79 (-)     <- Biology D60
ec_O2_ceil   = O2_ceil_C                               # D80 (mol/m3) <- Biology D27
ec_V_L       = V_charge / 1000                         # D82 (L)      <- Biology D6 / 1000
km_O2        = 4.0e-3                                  # D83 (cm/s) Eisenberg-Tobias-Wilke, 6 mm rod in axial swirl
km_exp       = 0.644                                   # D84 (-) k_m ~ D^(1-0.356); documents the km_Cl scaling
ec_DO_design = ec_DO_frac * ec_O2_ceil                 # D85 (mol/m3)
i_ORR_design = z_e_ORR * F_const * (km_O2 / 100) * ec_DO_design * (A_cath_wet / 10000)   # D86 (A)
i_ORR_ceiling = z_e_ORR * F_const * (km_O2 / 100) * ec_O2_ceil * (A_cath_wet / 10000)    # D87 (A)
etaF_calc     = max(0.0, 1 - i_ORR_design / I_app)     # D88 (-)
etaF_calc_min = max(0.0, 1 - i_ORR_ceiling / I_app)    # D89 (-) worst case at the ceiling DO
etaF          = etaF_calc                              # D18 = IFERROR(cal_etaF, etaF_calc)


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
R_gas_chem = 8.314                                    # D9 (J/mol/K)


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

# Media ionic composition (g/L) and molar masses
MW = dict(KH2PO4=136.086, Na2HPO4=141.96, NaH2PO4_2H2O=156.01, NaHCO3=84.007,
          K2SO4=174.26, CaSO4_2H2O=172.17, MgSO4_7H2O=246.48, NH42SO4=132.14,
          CaCl2=110.98)
mc = dict(Na2HPO4=2.895, NaH2PO4_2H2O=3.06, K2SO4=0.17, CaSO4_2H2O=0.097,
          MgSO4_7H2O=0.8, NH42SO4=0.943)              # MC02 g/L
udg = dict(KH2PO4=2.3, Na2HPO4=2.9, NaHCO3=1.05, MgSO4_7H2O=0.5,
           NH42SO4=0.47, CaCl2=0.01)                  # UdG g/L

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


def _by_media(mc02_val, udg_val):
    if media_sel == "MC02":
        return mc02_val
    if media_sel == "UdG phosphate":
        return udg_val
    return NA


pH_SID = _by_media(SID_mc02, SID_udg)                 # D44
pH_PT  = _by_media(PT_mc02, PT_udg)                   # D45
pH_NT  = _by_media(NT_mc02, NT_udg)                   # D46
pH_Cl  = _by_media(Cl_mc02, Cl_udg)                   # D47

# --- chlorine current: the binding limit of efficiency vs chloride arrival ---
FE_CER   = 0.5                                         # D128 max CER efficiency (high-Cl plateau)
km_Cl    = 0.00405                                     # D129 (cm/s) = km_O2 x (D_Cl/D_O2)^0.644
A_anode  = A_anode_wet                                 # D130 (cm2) <- Electrochemistry D46
I_Cl_FE  = Iappc * FE_CER                              # D131 (A) efficiency-limited
I_Cl_mt  = Fcc * km_Cl * (pH_Cl / 1000) * A_anode      # D132 (A) chloride mass-transport limit
I_Cl     = min(I_Cl_FE, I_Cl_mt)                       # D133 (A) binding limit (mt-limited at trace Cl-)
# WAVE-4: n_e_Cl is now the constant 2 on every route (2Cl- -> Cl2 -> HOCl, and
# the direct Cl- + H2O -> HOCl route, are both 2 e- per HOCl). The n = 1 in the
# mass-transport limit above is a FLUX count of arriving chloride, not a
# stoichiometry, so the old 1-or-2 regime switch conflated two different things.
n_e_Cl   = 2                                           # D148 electrons per produced HOCl


# ============================================================================
# ELECTROCHEMISTRY TAB - part C: the CALCULATED anodic split, then gas rates
#   (Electrochemistry rows 100-104, then 21-29)
# ============================================================================
ec_I_Cl     = I_Cl                                     # D101 (A)  <- Chemistry D133
ec_corr_I   = NA                                       # D102 (-)  <- Chemistry D158 (DATA GAP)
f_Cl_anode  = ec_I_Cl / I_app                          # D103 (-)
etaF_OER_calc = max(0.0, 1 - f_Cl_anode
                    - (ec_corr_I if isnum(ec_corr_I) else 0.0))   # D104 (-)
etaF_OER    = etaF_OER_calc                            # D26 = IFERROR(cal_etaF_OER, etaF_OER_calc)

rH2_gen    = I_app * etaF / (z_e_H2 * F_const) * 3600          # D21 (mol/h)
rO2_gen    = I_app * etaF_OER / (z_e_O2 * F_const) * 3600      # D22 (mol/h)
O2_cathode_ORR = I_app * (1 - etaF) / (z_e_ORR * F_const) * 3600  # D28 (mol/h)
O2_net_gen = rO2_gen - O2_cathode_ORR                          # D29 (mol/h)
V_H2_gen   = rH2_gen / 60 * R_gas_mt * T_K / P_atm * 1e6       # D23 (mL/min)
V_O2_gen   = rO2_gen / 60 * R_gas_mt * T_K / P_atm * 1e6       # D24 (mL/min)
V_gas_total = V_H2_gen + V_O2_gen                              # D25 (mL/min)


# ============================================================================
# ELECTROCHEMISTRY TAB - part D: hydrogen peroxide (rows 90-99)
#   The 2-electron branch of the same cathodic O2 reduction that sets etaF.
#   A source term the model previously did not have at all.
# ============================================================================
f_HOOH        = 0.15                                   # D91 (-) peroxide selectivity on stainless (Le Bozec 2001)
M_H2O2        = 34.0147                                # D92 (g/mol)
r_H2O2        = f_HOOH * i_ORR_design / (2 * F_const) * M_H2O2 * 1000 * 3600 / ec_V_L  # D93 (mg/L/h)
k_cat_cells   = 4.1e-3                                 # D94 (1/s) whole-culture catalase clearance, ~1e8 cells/mL
H2O2_ss       = r_H2O2 / (k_cat_cells * 3600)          # D95 (mg/L) growing culture
H2O2_lag_1h   = r_H2O2                                 # D96 (mg/L) no catalase pool yet: 1 h of pure accumulation
H2O2_thresh   = 0.17                                   # D97 (mg/L) 5 uM sustained slows growth (Li & Imlay 2018)
t_H2O2_thresh = (H2O2_thresh / r_H2O2 * 60) if r_H2O2 > 0 else NA   # D98 (min)
if H2O2_ss > H2O2_thresh:
    H2O2_flag = ("PEROXIDE ABOVE THE GROWTH-INHIBITION THRESHOLD even with a full catalase pool ("
                 + xltext(H2O2_ss, "0.00") + " mg/L)")
elif H2O2_lag_1h > H2O2_thresh:
    H2O2_flag = ("watch — steady growth is clear (" + xltext(H2O2_ss, "0.000")
                 + " mg/L) but LAG PHASE is not: peroxide passes the threshold in "
                 + xltext(t_H2O2_thresh, "0") + " min before biomass can scavenge it")
else:
    H2O2_flag = "OK — peroxide stays below the growth-inhibition threshold in both phases"  # D99


# ============================================================================
# BIOLOGY TAB - part B: gas requirement ratios & consumption (rows 13-16, 42-44)
# ============================================================================
H2_cons  = rH2_gen                                    # D13 (mol/h)
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
kappa_fI  = 0.78                                      # D178 (-) Lambda/Lambda0 at I ~ 0.1 M
kappa_TC  = 0.02                                      # D179 (1/K) +2 %/K, ISO 7888
kappa_med = _by_media(kappa0_mc02, kappa0_udg) * kappa_fI * (1 + kappa_TC * (TKc - 298.15))  # D180

# --- ionic strength & Davies activity coefficients (rows 182-197) ---
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
I_ionic = _by_media(I_mc02, I_udg)                    # D185 (mol/L)
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
k_geom      = 2.0                                      # D116 (-) unbounded-electrolyte correction
R_cell      = k_geom * math.acosh(ec_gap / anode_dia) / (math.pi * ec_kappa * (L_sub / 1000))  # D117 (ohm)
V_IR        = I_app * R_cell                           # D118 (V)
V_cell_est  = ec_E_rev + eta_anode + eta_cath + pcet_credit + V_IR   # D119 (V)
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
_cal_rows = [r for r in CO2_CAL if r[0] == Reactor_sel and r[3] > 0]
has_cal      = len(_cal_rows)                          # MT D119
latest_date  = max((r[1] for r in _cal_rows), default=0)  # MT D116
_latest = [r for r in _cal_rows if r[1] == latest_date]
_n_latest = max(1, len(_latest))
flowrate_cal   = sum(r[3] for r in _latest) / _n_latest if _latest else 0.0  # MT D117 (ml/s)
min_sparge_cal = sum(r[2] for r in _latest) / _n_latest if _latest else 0.0  # MT D118 (s)


# ============================================================================
# MASS TRANSFER TAB
#   WAVE-4: the water properties are now functions of the reactor temperature
#   rather than constants frozen at 30 degC (rows 166-175).
# ============================================================================
stir_len  = stir_bar_L                                # D5 (mm)  (from Geometry)
sigma_0, sigma_k = 0.07589, -0.000157                 # D167, D168 IAPWS R1-76(2014) linear fit
rho_0,   rho_k   = 1003.33, -0.2556                   # D169, D170 IAPWS-95 linear fit
HB_a, HB_b, HB_c = -4.41, 773.8, 506.4                # D171-D173 Han & Bartels (1996)
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
spg_dur_opt = max(pulse_floor, flush_factor * headspace_V / (Q_CO2 / 60))  # D90 (s)
spg_int_carbon = spg_dur_opt / (60 * duty_carbon)      # D112 (min) - carbon-limited

# --- WAVE-4: headspace O2 balance and the DO-LIMITED interval (rows 177-188) --
# The SURFACE-HELD / SPARGE-NEEDED branch is gone. Dissolved O2 can never fall
# below equilibrium with the headspace, so the schedule's job is to dilute
# oxygen OUT of the headspace with CO2. kL_surf now moves the answer
# continuously instead of switching which formula runs.
CO2_rate_full = nCO2_rate * 3600                       # D178 (mol/h) sparge line at 100% duty
DO_target     = target_DO_frac * O2_ceil_C             # D179 (mol/m3)
DO_surf_excess = O2_excess / (kLa_surf_used * 3600 * (V_charge / 1e6))    # D180 (mol/m3)
DO_surf_excess_lag = O2_net_gen / (kLa_surf_used * 3600 * (V_charge / 1e6))  # D181 (mol/m3)
hs_O2_allow   = DO_target - DO_surf_excess             # D182 (mol/m3)
y_O2_star     = (hs_O2_allow / (H_O2_T * P_atm)) if hs_O2_allow > 0 else NA   # D183 (-)
duty_DO       = (O2_excess * (1 - y_O2_star) / (y_O2_star * CO2_rate_full)
                 if isnum(y_O2_star) else NA)          # D184 (-)
spg_int_DO    = (spg_dur_opt / (60 * duty_DO)) if isnum(duty_DO) else NA      # D185 (min)
kLa_surf_req  = O2_excess / (DO_target * 3600 * (V_charge / 1e6))             # D186 (1/s)

spg_int_opt = (min(spg_int_carbon, spg_int_DO) if isnum(spg_int_DO)
               else min(spg_int_carbon, spg_int_max))                  # D91 (min)
spg_int_opt_s = spg_int_opt * 60                       # D92 (s)
duty_actual = spg_dur_opt / (spg_int_opt * 60)         # D93
if not isnum(spg_int_DO):
    opt_binding = "O2-INFEASIBLE (see D134)"
elif spg_int_DO <= spg_int_carbon:
    opt_binding = "O2-DILUTION (headspace O2 sets the interval)"
else:
    opt_binding = "CARBON (CO2 supply sets the interval)"   # D94
if not isnum(spg_int_DO):
    spg_int_regime = ("DO TARGET UNREACHABLE — the surface cannot carry the O2 flux at this kLa; "
                      "no interval fixes it (raise kL_surf, lower the current, or accept a higher DO)")
elif kLa_meas > 0:
    spg_int_regime = "MEASURED kLa — DO-limited interval is " + xltext(spg_int_DO, "0.0") + " min"
else:
    spg_int_regime = ("ESTIMATED kLa — DO-limited interval is " + xltext(spg_int_DO, "0.0")
                      + " min; confirm by measuring kL_surf")   # D134

# --- schedule mode resolution: Summary 'Your setting' override > Manual cells > Optimal ---
sched_mode   = "Optimal"                               # D81
spg_dur_man  = 1.0                                     # D82 (s)
spg_int_man  = 1.0                                     # D83 (min)
user_spg_dur = None                                    # Summary G13 (blank -> recommended)
user_spg_int = None                                    # Summary G15 (blank -> recommended)
spg_dur = (user_spg_dur if (isnum(user_spg_dur) and user_spg_dur > 0)
           else (spg_dur_man if sched_mode == "Manual" else spg_dur_opt))   # D121
spg_int = (user_spg_int if (isnum(user_spg_int) and user_spg_int > 0)
           else (spg_int_man if sched_mode == "Manual" else spg_int_opt))   # D122
od_ok = "OK" if (spg_int * 60 - spg_dur >= 5) else "TIGHT"    # D95 (uses schedule in use)
duty    = spg_dur / (spg_int * 60)                     # D105

CO2_pulse  = nCO2_rate * spg_dur                        # D123 (mol)
pulses_h   = 60 / spg_int                               # D124 (/h)
pulses_d   = pulses_h * 24                              # D125 (/d)
CO2_supply = CO2_pulse * pulses_h                       # D100 (mol/h)
CO2_sd_ratio = CO2_supply / CO2_cons if CO2_cons > 0 else NA  # D126

# --- steady dissolved O2 = headspace floor + the excess that drives the surface flux ---
y_O2_actual = (O2_excess / (O2_excess + CO2_supply)) if CO2_supply > 0 else NA  # D187 (-)
DO_hs_floor = (H_O2_T * y_O2_actual * P_atm) if isnum(y_O2_actual) else NA      # D188 (mol/m3)
DO_ss = (DO_hs_floor + DO_surf_excess) * 32            # D108 (mg/L)
DO_ss_sawtooth = DO_hs_floor + DO_surf_excess          # D133 (mol/m3, growth-phase source)
DO_ss_sawtooth_lag = DO_hs_floor + DO_surf_excess_lag  # D135 (mol/m3, LAG source)

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
carry_flag = "RISK" if u_sg > u_g_max else "OK"         # D59

rho_CO2  = P_atm * (M_CO2 / 1000) / (R_gas * T_K)       # D60 (kg/m3)
n_pores_active = 1                                      # D61
v_orifice = (Q_CO2 / 1e6 / 60) / (n_pores_active * (math.pi / 4 * d_orifice ** 2))  # D62 (m/s)
We_orifice = rho_CO2 * v_orifice ** 2 * d_orifice / sigma  # D63
if d_bubble < 0.001:
    bubble_regime = "Sinter OOR - add fine-bubble model"
else:
    bubble_regime = "Static" if We_orifice < 2 else "Dynamic"   # D64

# --- O2 time-to-ceiling family ---
t_O2_ceiling = O2_ceil_C * (V_charge / 1e6) / O2_excess * 60   # D65 (min)
t_O2_ceiling_strip = (O2_ceil_C * (V_charge / 1e6) / (O2_excess - strip_avg) * 60
                      if (O2_excess - strip_avg) > 0 else 9999)  # D66
y_O2_vent = (O2_excess / (O2_excess + CO2_supply)) if CO2_supply > 0 else NA   # D75 (mole fraction)
DO_vent_eq = H_O2_T * y_O2_vent * P_atm * 1000          # D76 (uM)
hs_flush_time = headspace_V / (Q_CO2 * duty)            # D77 (min)
surf_ratio = (surf_strip / O2_excess) if O2_excess > 0 else NA   # D74
O2_removal_ratio = ((strip_avg + surf_strip) / O2_excess) if O2_excess > 0 else NA  # D78
t_O2_ceiling_lag = O2_ceil_C * (V_charge / 1e6) / O2_net_gen * 60   # D79 (min)
t_O2_ceiling_rem = (O2_ceil_C * (V_charge / 1e6) / (O2_net_gen - strip_avg - surf_strip) * 60
                    if (O2_net_gen - strip_avg - surf_strip) > 0 else 9999)  # D80

kinetic_caveat = "see note ->"                          # D96

if isnum(DO_opt):
    if DO_ss <= DO_opt:
        DO_ss_vs_opt = "at/under optimum"
    elif DO_ss < DO_impair:
        DO_ss_vs_opt = "above optimum, under impairment"
    else:
        DO_ss_vs_opt = "OVER IMPAIRMENT - surface strip insufficient"
else:
    DO_ss_vs_opt = "organism optimum unknown"           # D109
if isnum(DO_min):
    DO_ss_vs_min = "above minimum" if DO_ss >= DO_min else "BELOW MINIMUM"
else:
    DO_ss_vs_min = "minimum DO unknown - measure"        # D110
tip_warn = "TIP SPEED > 1.5 m/s" if tip_speed > 1.5 else "OK"  # D111
if isnum(DO_ss) and isnum(DO_impair):
    sched_regime = ("Surface stripping holds DO under impairment - sparge is CARBON-limited "
                    "(long interval); the O2-limited interval is the conservative fallback "
                    "until kL_surf is measured" if DO_ss < DO_impair
                    else "Surface stripping insufficient - sparge must vent O2 - use the O2-limited interval")
else:
    sched_regime = "organism DO unknown"                # D113
cal_warning = (f"calibrated: {Reactor}" if has_cal > 0
               else f"NO CALIBRATION for {Reactor} - add a row in CO2 flows with nominal flowrate + minimum sparge")  # D120

O2_accum = O2_excess / 60 * spg_int                     # D127 (mol)
O2_strip_pulse = strip_sparge / 3600 * spg_dur          # D128 (mol)
sched_bal = (O2_strip_pulse / O2_accum) if O2_accum > 0 else NA  # D129
dur_ok = "OK" if spg_dur >= pulse_floor else "LOW"      # D130
kL_surf_crit = kLa_surf_req / a_surf                    # D131 (m/s)


# ============================================================================
# MASS TRANSFER TAB - schedule -> dissolved CO2
#   The two-compartment closed form (rows 138-161) is retained where the
#   workbook retains it, but it is SUPERSEDED: it let the liquid absorb ~2.4x
#   the CO2 the sparge ever delivered, because the headspace vented
#   independently of what the liquid took up. Rows 190-200 replace it with ONE
#   pooled inventory (liquid + headspace at Henry equilibrium) decaying through
#   the vent, whose fixed point is closed-form and mass-conserving by
#   construction. CO2aqc (Chemistry D5) now reads the pooled cycle average.
# ============================================================================
D_CO2          = D_CO2_ref * math.exp(-Ea_D_CO2 / R_gas * (1 / T_K - 1 / 298.15))  # MT D138 (m2/s)
pCO2_air       = 40.0                                   # MT D139 (Pa) atmospheric pCO2 ~400 ppm INPUT
headspace_V_m3 = headspace_V / 1e6                      # MT D140 (m3)
V_L_m3         = V_charge / 1e6                         # MT D141 (m3)
Q_vent         = 0.5                                    # MT D142 (mL/min) slow restricted vent bleed - KEY UNCERTAIN PARAMETER, measure. INPUT
k_vent         = (Q_vent / 1e6 / 60) / headspace_V_m3   # MT D143 (1/s) headspace vent first-order rate
tau_hs         = headspace_V_m3 / (Q_vent / 1e6 / 60) / 60   # MT D144 (min) headspace residence time
C_sat_CO2      = H_CO2_T * P_atm                        # MT D145 (mol/m3) pure-CO2 sparge saturation
C_air_CO2      = H_CO2_T * pCO2_air                     # MT D146 (mol/m3) air-equilibrium
sqrtD_CO2      = math.sqrt(D_CO2 / D_O2)                # MT D147 penetration-theory diffusivity scaling
kLa_CO2_off    = kLa_surf * sqrtD_CO2                   # MT D148 (1/s) surface-path between pulses
tau_surf_floor = 1 / kLa_CO2_off / 60                   # MT D149 (min) surface-relaxation time
n_hs_gas       = P_atm * headspace_V_m3 / (R_gas * T_K) # MT D150 (mol) headspace gas inventory
t_on_CO2       = spg_dur                                # MT D151 (s) pulse duration
t_off_CO2      = max(0.0, spg_int * 60 - spg_dur)       # MT D152 (s) gap, GUARD floored at 0
# --- SUPERSEDED two-compartment closed form (kept where the workbook keeps it) ---
eon_CO2        = math.exp(-kLa_CO2_off * t_on_CO2)      # MT D153
e1_CO2         = math.exp(-kLa_CO2_off * t_off_CO2)     # MT D154
e2_CO2         = math.exp(-k_vent * t_off_CO2)          # MT D155
coef_CO2       = (C_sat_CO2 - C_air_CO2) * kLa_CO2_off / (kLa_CO2_off - k_vent)   # MT D156
Ca_CO2         = (e1_CO2 * C_sat_CO2 * (1 - eon_CO2) + C_air_CO2 * (1 - e1_CO2)
                  + coef_CO2 * (e2_CO2 - e1_CO2)) / (1 - e1_CO2 * eon_CO2)         # MT D157
Cb_CO2         = C_sat_CO2 + (Ca_CO2 - C_sat_CO2) * eon_CO2                        # MT D158
CO2_int_on     = C_sat_CO2 * t_on_CO2 + (Ca_CO2 - C_sat_CO2) / kLa_CO2_off * (1 - eon_CO2)   # MT D159
CO2_int_off    = (C_air_CO2 * t_off_CO2 + (Cb_CO2 - C_air_CO2) / kLa_CO2_off * (1 - e1_CO2)
                  + coef_CO2 * ((1 - e2_CO2) / k_vent - (1 - e1_CO2) / kLa_CO2_off))          # MT D160
CO2_cyc_avg    = (CO2_int_on + CO2_int_off) / (t_on_CO2 + t_off_CO2)              # MT D161 (mol/m3)

# --- OPERATIVE: mass-conserving pooled limit cycle (MT rows 190-200) ---
hs_H_CO2       = H_CO2_T                                # MT D191 (mol/m3/Pa) <- Biology D31
Vg_CO2         = headspace_V_m3 / (hs_H_CO2 * R_gas * T_K)   # MT D192 (m3) headspace as liquid-equivalent volume
pool_a         = V_L_m3 / (V_L_m3 + Vg_CO2)             # MT D193 (-) liquid share of a pooled inventory
pool_b         = CO2_pulse / (V_L_m3 + Vg_CO2)          # MT D194 (mol/m3) step from the pulse ACTUALLY delivered
k_eff_CO2      = k_vent * Vg_CO2 / (V_L_m3 + Vg_CO2)    # MT D195 (1/s) pool decay through the vent
pool_beta_ratio = (kLa_CO2_off * V_L_m3 / Vg_CO2) / k_vent    # MT D196 (x) quasi-equilibrium validity
pool_e         = math.exp(-k_eff_CO2 * t_off_CO2)       # MT D197 (-)
C_cycle_start  = ((C_air_CO2 * (1 - pool_e) + pool_b * pool_e)
                  / (1 - pool_a * pool_e))              # MT D198 (mol/m3) fixed point of the cycle
C_cycle_peak   = pool_a * C_cycle_start + pool_b        # MT D199 (mol/m3)
CO2_cyc_avg_new = (C_air_CO2 + (C_cycle_peak - C_air_CO2) * (1 - pool_e) / (k_eff_CO2 * t_off_CO2)
                   if k_eff_CO2 * t_off_CO2 > 0 else C_cycle_peak)   # MT D200 (mol/m3)
CO2aqc         = min(C_sat_CO2, max(C_air_CO2, CO2_cyc_avg_new)) / 1000   # MT D162 = Chemistry D5 (mol/L)
vent_floor_chk = ("vent is slow path - OK" if tau_hs >= tau_surf_floor
                  else "WARNING: surface clears faster than vent - run2 cannot stay acidic")  # MT D163
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

pH_fHOCl = 1 / (1 + 10 ** (pH_meas - pKa_HOCl))        # D104
# --- naive FE=1 cells (NOT operative; kept for contrast) ---
bleach_rate   = Iappc / (2 * Fcc) * 52460 * 3600 / VLc # D107 (mg/L/h, FE=1 ceiling)
bleach_t1ppm  = 1 / bleach_rate * 60                   # D108 (min)
HOCl_max = pH_Cl * pH_fHOCl * 52460                    # D125 (naive FE=1 ceiling, superseded)
# --- graded kinetic free-chlorine penalty model (operative; Chemistry rows 128-149) ---
P_HOCl   = I_Cl / (n_e_Cl * Fcc * VLc)                 # D134 (mol/L/s) volumetric free-Cl production
NH3_N    = pH_NT * 14007                               # D135 (mg/L) ammonium as N
k1_NH2Cl = 4.2e6                                       # D136 (M^-1 s^-1) HOCl+NH3 rate constant
pKa_NH4  = -math.log10(Ka_NH4)                         # D137 (from the van 't Hoff-corrected Ka_NH4)
NH3_free = pH_NT / (1 + 10 ** (pKa_NH4 - pH_meas))     # D138 (M) reactive free ammonia
HOCl_ss  = P_HOCl / (k1_NH2Cl * NH3_free)              # D139 (M) steady bulk free HOCl (already the undissociated acid)
HOCl_ss_mgL = HOCl_ss * 52460                          # D140 (mg/L)
f_local  = 10                                          # D141 anode boundary-layer enrichment (numerically inert: chloramine dominates ~1e4x)
tau_NH2Cl = 1                                          # D142 (h) monochloramine residence
# BUGFIX (review 2026-06-26) chloride mass balance: chlorine (free + combined)
# can never exceed the medium chloride pool. The old cap was on ammonium
# capacity (5.06*NH3_N, never binds) and let NH2Cl reach 17 mg/L from only
# ~9.45 mg/L of chloride - physically impossible. Cap by the chloride pool.
# (In a closed batch this pool also DEPLETES; a steady value at the cap presumes
#  chloride is regenerated as HOCl is reduced back to Cl- - stated, not proven.)
Cl_pool_mgL = pH_Cl * 52460                            # D149 (mg/L as HOCl-equiv) chloride-pool ceiling
NH2Cl_mgL = min(P_HOCl * tau_NH2Cl * 3600 * 52460, 5.06 * NH3_N, Cl_pool_mgL)  # D143 (mg/L) combined chlorine, pool-capped
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
NH2Cl_lo = min(P_HOCl * tau_NH2Cl_lo * 3600 * 52460, 5.06 * NH3_N, Cl_pool_mgL)  # D154
NH2Cl_hi = min(P_HOCl * tau_NH2Cl_hi * 3600 * 52460, 5.06 * NH3_N, Cl_pool_mgL)  # D155
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
if C_eff < Cl_onset:                                   # D109
    bleach_flag = (f"negligible free chlorine ({C_eff:.2f} mg/L < onset); "
                   "does NOT account for the Exp-2 death - see metal_flag")
elif C_eff < Cl_kill:
    bleach_flag = (f"sub-lethal {C_eff:.2f} mg/L (band {C_eff_lo:.2f}-{C_eff_hi:.2f}); chloride-pool-bounded, "
                   "cannot reach the kill threshold in this medium; does NOT explain the death - see metal_flag")
else:
    bleach_flag = f"SEVERE free chlorine: {C_eff:.1f} mg/L → biofilm/electrode damage (Baek 2021)"
if pH_meas < 6.5:
    pH_band_flag = "pH BELOW HOB optimum (<6.5) — reduce the CO₂ dose or lengthen the interval"
elif pH_meas > 7.5:
    pH_band_flag = "pH above optimum (>7.5)"
else:
    pH_band_flag = "pH in HOB band 6.5–7.5"       # D110

# --- electrode potentials at the operating pH (Chemistry rows 199-211) ---
nernst_slope = R_gas * TKc / Fcc * math.log(10)        # D200 (V/pH)
E0_HER  = 0.0                                          # D202 (V vs SHE) SHE convention
E0_Cl2  = 1.358                                        # D203
E0_ORR2 = 0.695                                        # D204 the parasitic cathode branch
E0_Cu   = 0.3419                                       # D205
E_OER   = E0_OER - nernst_slope * pH_meas              # D206
E_HER   = E0_HER - nernst_slope * pH_meas              # D207
E_Cl2   = E0_Cl2 + nernst_slope * (-math.log10(max(pH_Cl, 1e-12)))  # D208
E_Cl_margin = E_Cl2 - E_OER                            # D209 (V) chlorine headroom over O2 evolution
E_ORR2  = E0_ORR2 - nernst_slope * pH_meas             # D210
E_Cu_margin = E_OER - E0_Cu                            # D211 (V)

# --- buffer capacity at the electrode surface (Chemistry rows 213-219) ---
D_HPO4     = 7.59e-10                                  # D214 (m2/s) CRC tabulated
delta_diff = 40.0                                      # D215 (um) from k_m = D/delta at the assumed swirl
_f_HPO4    = 1 - 1 / (1 + 10 ** (pH_meas - (-math.log10(Ka2p_c))))   # HPO4(2-) share of the phosphate pool
j_buffer_lim = Fcc * D_HPO4 * (pH_PT * _f_HPO4) * 1000 / (delta_diff / 1e6) / 10   # D216 (mA/cm2)
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


def round_sig_or_int(x):
    """Excel: IF(NOT(ISNUMBER(x)),x, IF(x>0.5, ROUND(x,0), ROUND(x, 1-(1+INT(LOG10(ABS(x))))))) ."""
    if not isnum(x):
        return x
    if x > 0.5:
        return round(x)
    digits = 1 - (1 + int(math.log10(abs(x))))
    return round(x, digits)


S_D13 = iferror(lambda: spg_dur_opt,   # D13: ='Mass Transfer'!D90 (spg_dur_opt)
                "calibrate this reactor first (see CO2 flows)")
S_D14 = (user_spg_dur if (isnum(user_spg_dur) and user_spg_dur > 0)
         else (round_sig_or_int(S_D13) if isinstance(S_D13, float) else S_D13))   # D14
S_D15 = iferror(lambda: spg_int_opt, "calibrate this reactor first (see CO2 flows)")  # D15
S_D16 = (user_spg_int if (isnum(user_spg_int) and user_spg_int > 0)
         else (round_sig_or_int(S_D15) if isinstance(S_D15, float) else S_D15))   # D16
S_D19 = geom_check                                      # D19 vial geometry
S_D20 = cal_warning                                     # D20 reactor calibrated
S_D21 = DO_ss_vs_opt                                    # D21 O2 at/under optimum
S_D22 = DO_ss_vs_min                                    # D22 O2 above minimum
S_D23 = sched_regime                                    # D23 interval relaxable
S_D24 = H2_safety                                       # D24 H2 headspace safe
S_D25 = bubble_regime                                   # D25 bubble model valid
S_D26 = iferror(lambda: f"×{CO2_sd_ratio:.1f}" + (" OK" if CO2_sd_ratio >= 1 else " SHORTFALL (CO2 < demand)"),
                "calibrate this reactor first")         # D26 CO2 supply : demand (this schedule)
S_D27 = iferror(lambda: dur_ok, "calibrate this reactor first (see CO2 flows)")  # D27 pulse >= floor
S_D28 = iferror(lambda: od_ok, "calibrate this reactor first (see CO2 flows)")   # D28 dosing window
S_D29 = carry_flag                                      # D29 carryover risk
S_D30 = tip_warn                                        # D30 tip-speed shear
S_D31 = media_vol_warn                                  # D31 media volume fits
S_D32 = depth_warn                                      # D32 liquid level OK
S_D33 = I_valid                                         # D33 LED current-law range
S_D34 = ("inputs present" if (isnum(DO_min) and isnum(DO_opt) and isnum(DO_impair) and isnum(DO_toxic))
         else "DATA GAP - organism DO thresholds unmeasured; results unreliable")  # D34
S_D35 = pH_meas                                         # D35 endpoint pH (activity scale) = Chemistry D220
S_D36 = C_eff                                           # D36 effective biocidal chlorine (operative)
S_D38 = DO_ss                                           # D38 steady-state DO
S_D39 = spg_int_carbon                                  # D39 interval if O2 handled
S_D40 = tip_speed                                       # D40 stir-bar tip speed
S_D41 = CO2_carbon_margin                               # D41 carbon margin
# --- wave-4 block (Summary rows 81-90): hand these to an electrochemist ---
S_D82 = etaF_calc                                       # D82 cathodic faradaic efficiency (calculated)
S_D83 = V_cell_est                                      # D83 estimated cell voltage
S_D84 = V_flag                                          # D84 cell-voltage verdict
S_D85 = H2O2_flag                                       # D85 peroxide verdict
S_D86 = buffer_flag                                     # D86 electrode-surface pH verdict
S_D87 = E_Cl_margin                                     # D87 chlorine headroom above O2 evolution
S_D88 = E_Cu_margin                                     # D88 copper dissolution headroom
S_D89 = pH_meas                                         # D89 measured (activity-scale) pH
S_D90 = kLa_surf_req                                    # D90 surface kLa required for the DO target


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
                self._sheet_part[sh.get("name")] = "xl/" + target.lstrip("/")
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
    ("Summary D36  C_eff (mg/L)",                      S_D36),
    ("Summary D38  Steady-state DO (mg/L)",            S_D38),
    ("Summary D39  Sparge interval if O2 handled (min)", S_D39),
    ("Summary D40  Stir-bar tip speed (m/s)",          S_D40),
    ("Summary D41  Carbon margin (x)",                 S_D41),
    ("Summary D82  Cathodic faradaic efficiency",      S_D82),
    ("Summary D83  Estimated cell voltage (V)",        S_D83),
    ("Summary D84  Cell-voltage verdict",              S_D84),
    ("Summary D85  Peroxide verdict",                  S_D85),
    ("Summary D86  Electrode-surface pH verdict",      S_D86),
    ("Summary D87  Chlorine headroom (V)",             S_D87),
    ("Summary D88  Copper dissolution headroom (V)",   S_D88),
    ("Summary D89  Measured (activity-scale) pH",      S_D89),
    ("Summary D90  Surface kLa required (1/s)",        S_D90),

    # --- Chemistry ---
    ("Chemistry D103  pH_op (concentration scale)",    pH_op),
    ("Chemistry D104  HOCl fraction at op pH",         pH_fHOCl),
    ("Chemistry D108  Time to ~1 ppm HOCl (min)",      bleach_t1ppm),
    ("Chemistry D109  bleach_flag",                    bleach_flag),
    ("Chemistry D110  pH_band_flag",                   pH_band_flag),
    ("Chemistry D125  HOCl_max (mg/L)",                HOCl_max),
    ("Chemistry D133  I_Cl (A)",                       I_Cl),
    ("Chemistry D134  P_HOCl (mol/L/s)",               P_HOCl),
    ("Chemistry D139  HOCl_ss (M)",                    HOCl_ss),
    ("Chemistry D143  NH2Cl (mg/L)",                   NH2Cl_mgL),
    ("Chemistry D145  C_eff (mg/L)",                   C_eff),
    ("Chemistry D149  Cl_pool_mgL (mg/L)",             Cl_pool_mgL),
    ("Chemistry D156  C_eff_lo (mg/L)",                C_eff_lo),
    ("Chemistry D157  C_eff_hi (mg/L)",                C_eff_hi),
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
    ("Chemistry D216  j_buffer_lim (mA/cm2)",          j_buffer_lim),
    ("Chemistry D218  j_buffer_ratio (-)",             j_buffer_ratio),
    ("Chemistry D219  buffer_flag",                    buffer_flag),
    ("Chemistry D220  pH_meas (activity scale)",       pH_meas),

    # --- Biology ---
    ("Biology  D28  O2_ceil_uM (uM)",                  O2_ceil_uM),
    ("Biology  D35  CO2_carbon_margin (x)",            CO2_carbon_margin),
    ("Biology  D37  pH_CO2_unbuf",                     pH_CO2_unbuf),
    ("Biology  D42  t_H2_sat (min)",                   t_H2_sat),
    ("Biology  D43  H2_turnover (1/h)",                H2_turnover),
    ("Biology  D44  H2_safety",                        H2_safety),
    ("Biology  D60  DO_frac_target (-)",               DO_frac_target),

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
    ("MassXfer D76  DO_vent_eq (uM)",                  DO_vent_eq),
    ("MassXfer D77  hs_flush_time (min)",              hs_flush_time),
    ("MassXfer D78  O2_removal_ratio (x)",             O2_removal_ratio),
    ("MassXfer D79  t_O2_ceiling_lag (min)",           t_O2_ceiling_lag),
    ("MassXfer D80  t_O2_ceiling_rem (min)",           t_O2_ceiling_rem),
    ("MassXfer D92  spg_int_opt_s (s)",                spg_int_opt_s),
    ("MassXfer D93  duty_actual",                      duty_actual),
    ("MassXfer D94  opt_binding",                      opt_binding),
    ("MassXfer D95  od_ok",                            od_ok),
    ("MassXfer D98  kLa_surf_used (1/s)",              kLa_surf_used),
    ("MassXfer D108 DO_ss (mg/L)",                     DO_ss),
    ("MassXfer D109 DO_ss_vs_opt",                     DO_ss_vs_opt),
    ("MassXfer D110 DO_ss_vs_min",                     DO_ss_vs_min),
    ("MassXfer D111 tip_warn",                         tip_warn),
    ("MassXfer D113 sched_regime",                     sched_regime),
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
]


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
    if book is ABSENT or book is NO_CACHE or book is None or book == "":
        return declared == 0.0
    if _isnum(declared) and _isnum(book):
        return abs(declared - book) <= 1e-9 * max(1.0, abs(book))
    return str(declared).strip() == str(book).strip()


def check_inputs():
    """Compare the declared inputs against Summary D2:D10.

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
        print("INPUT DRIFT - this script's declared inputs differ from Summary D2:D10.")
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
