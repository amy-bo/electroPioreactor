#!/usr/bin/env python3
"""
electroPioreactorGasModel.py

Independent first-principles re-derivation of the electroPioreactor CO2/gas
spreadsheet (Media/electroPioreactorGasModel.xlsx). Every FINAL output - any
derived numeric cell that nothing else references, plus every cell on the
Summary tab - is computed here from the input parameters and physical/chemical
constants, NOT read back from the workbook's cached values.

Standard library only. Run with:  python3 electroPioreactorGasModel.py

The model mirrors the workbook's sheet structure (Summary -> Geometry ->
Electrochemistry -> Chemistry -> Biology -> Mass Transfer -> CO2 flows) but the
arithmetic is re-implemented cleanly from the documented formula logic.
"""

import math

# ============================================================================
# SUMMARY TAB - user inputs (the only free variables in the model)
# ============================================================================
Reactor_sel    = "ed04"            # D2
electrode_sel  = "Pt/Ti rod"       # D3
organism_sel   = "UdG (mixed)"     # D4
media_sel      = "UdG phosphate"   # D5
led_intensity  = 3.0               # D6  (%)
stir_rpm_set   = 500.0             # D7  (rpm)
temp_C         = 30.0              # D8  (degC)
media_volume   = 0.0               # D9  (mL; 0/blank -> use recommended max)
P_atm_set      = 0.0               # D10 (Pa; 0/blank -> default 101325)

NA = float("nan")                  # spreadsheet #N/A sentinel for unmeasured data


def isnum(x):
    """Mirror Excel ISNUMBER: True for a real (non-NaN) float."""
    return isinstance(x, (int, float)) and not (isinstance(x, float) and math.isnan(x))


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
elec_sub_L   = max(0.0, h_datum - elec_clear)      # D35 (mm)
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


# ============================================================================
# ELECTROCHEMISTRY TAB
#   (T_K, P_atm, R_gas imported from Biology / Mass Transfer; defined below but
#    listed here in workbook order - constants used immediately are fixed.)
# ============================================================================
# Electrode lookup (Electrochemistry A35:I37): sparger, sinter porosity, z_e_ORR
ELECTRODE = {
    "Pt/Ti rod": dict(sparger="Tube",     por="n/a", z_e_ORR=2),
    "MMO rod":   dict(sparger="Tube",     por="n/a", z_e_ORR=2),
    "MMO tube":  dict(sparger="Sintered", por=0,     z_e_ORR=2),
}
gerrit_slope = 1.03            # D11 (mA/%)
gerrit_int   = 2.6            # D12 (mA)
gerrit_min   = 3.0           # D13 (%)
gerrit_max   = 25.0          # D14 (%)
F_const      = 96485.33212   # D15 (C/mol)
z_e_H2       = 2             # D16
z_e_O2       = 4             # D17
etaF         = 1.0           # D18  (cathodic H2 Faradaic efficiency)
etaF_OER     = 1.0           # D26  (anodic O2 Faradaic efficiency)
intensity    = led_intensity # D10 (%)
I_app        = (gerrit_slope * intensity + gerrit_int) / 1000   # D19 (A)
I_valid      = "OK" if (gerrit_min <= intensity <= gerrit_max) else "OUT"  # D20
e            = ELECTRODE[electrode_sel]
sparger_e    = e["sparger"]                                     # D31
por_grade_e  = e["por"] if isnum(e["por"]) else 0              # D32
z_e_ORR      = e["z_e_ORR"]                                     # D27


# ============================================================================
# BIOLOGY TAB  (sets temperature, pressure, Henry solubilities, gas budget)
# ============================================================================
T_C        = temp_C                                  # D17 (degC)
T_K        = T_C + 273.15                             # D18 (K)
P_atm      = P_atm_set if P_atm_set > 0 else 101325.0  # D19 (Pa)
Pa_per_atm = 101325.0                                 # D20
T_ref      = 298.15                                   # D23 (K)

# --- electrochemistry rates that depend on T_K / P_atm / R_gas ---
R_gas_mt   = 8.314462618                              # Mass Transfer D101 (J/mol/K)
rH2_gen    = I_app * etaF / (z_e_H2 * F_const) * 3600          # Echem D21 (mol/h)
rO2_gen    = I_app * etaF_OER / (z_e_O2 * F_const) * 3600      # Echem D22 (mol/h)
O2_cathode_ORR = I_app * (1 - etaF) / (z_e_ORR * F_const) * 3600  # Echem D28 (mol/h)
O2_net_gen = rO2_gen - O2_cathode_ORR                         # Echem D29 (mol/h)
V_H2_gen   = rH2_gen / 60 * R_gas_mt * T_K / P_atm * 1e6       # Echem D23 (mL/min)
V_O2_gen   = rO2_gen / 60 * R_gas_mt * T_K / P_atm * 1e6       # Echem D24 (mL/min)
V_gas_total = V_H2_gen + V_O2_gen                             # Echem D25 (mL/min)

# --- gas requirement ratios & consumption (Biology) ---
bio_H2  = 6.0                                         # D10
bio_O2  = 2.0                                         # D11
bio_CO2 = 1.0                                         # D12
H2_cons  = rH2_gen                                    # D13 (mol/h)
O2_cons  = H2_cons * bio_O2 / bio_H2                  # D14 (mol/h)
CO2_cons = H2_cons * bio_CO2 / bio_H2                 # D15 (mol/h)
O2_excess = O2_net_gen - O2_cons                      # D16 (mol/h)

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
t_H2_sat = C_H2_sat * (V_charge / 1e6) / rH2_gen * 60          # D42 (min)
H2_turnover = rH2_gen / (V_charge / 1e6) / C_H2_sat   # D43 (1/h)
H2_safety = "EXPLOSIVE" if H2_turnover > 1 else "watch"        # D44

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


# ============================================================================
# CHEMISTRY TAB  (buffered pH solve + anodic bleaching)
# ============================================================================
TKc   = T_K                                           # D4 (K)
CO2aqc = CO2_diss / 1000                              # D5 (mol/L)
Iappc = I_app                                         # D6 (A)
Fcc   = F_const                                       # D7 (C/mol)
VLc   = V_charge / 1000                               # D8 (L)
R_gas_chem = 8.314                                    # D9 (J/mol/K)

def vant_hoff(K25, dH_kJ):
    """K(T) = K25 * exp(-dH/R * (1/T - 1/298.15)), dH in kJ/mol."""
    return K25 * math.exp(-dH_kJ * 1000 / R_gas_chem * (1 / TKc - 1 / 298.15))

Ka1c   = vant_hoff(4.45e-7, 9.15)                     # D13 carbonate Ka1
Ka2c   = vant_hoff(4.69e-11, 14.9)                    # D14 carbonate Ka2
Ka1p   = vant_hoff(7.1e-3, -8.0)                      # D15 phosphate Ka1
Ka2p   = vant_hoff(6.31e-8, 3.6)                      # D16 phosphate Ka2
Ka3p   = vant_hoff(4.2e-13, 16.0)                     # D17 phosphate Ka3
Ka_NH4 = vant_hoff(5.6e-10, 52.2)                     # D18 ammonium Ka
Kw_w   = vant_hoff(1e-14, 55.8)                       # D19 water Kw
Ka_HOCl = vant_hoff(2.8840315031266057e-8, 13.8)     # D20 hypochlorous Ka
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
SID_mc02 = ((2 * mc["Na2HPO4"] / MW["Na2HPO4"] + mc["NaH2PO4_2H2O"] / MW["NaH2PO4_2H2O"]
             + 2 * mc["K2SO4"] / MW["K2SO4"])
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

# pH solve grid (A50:A100 trial pH 4.0..9.0 step 0.1); root by linear interp.
def charge_residual(pH):
    h = 10 ** (-pH)
    return (pH_SID
            + pH_NT * h / (h + Ka_NH4)
            + h
            - (pH_PT * Ka1p * h ** 2 + 2 * pH_PT * Ka1p * Ka2p * h
               + 3 * pH_PT * Ka1p * Ka2p * Ka3p)
              / (h ** 3 + Ka1p * h ** 2 + Ka1p * Ka2p * h + Ka1p * Ka2p * Ka3p)
            - Ka1c * CO2aqc / h
            - 2 * Ka1c * Ka2c * CO2aqc / h ** 2
            - Kw_w / h)

_pH_grid = [round(4.0 + 0.1 * i, 10) for i in range(51)]  # 4.0 .. 9.0
_resid = [charge_residual(p) for p in _pH_grid]
_interp_sum = 0.0
for i in range(len(_pH_grid) - 1):
    b, bn = _resid[i], _resid[i + 1]
    if b >= 0 and bn < 0:                              # sign change (root bracket)
        _interp_sum += _pH_grid[i] + 0.1 * b / (b - bn)
pH_op = _interp_sum                                    # D103 (operating pH)

pH_fHOCl = 1 / (1 + 10 ** (pH_op - pKa_HOCl))          # D104
bleach_rate   = Iappc / (2 * Fcc) * 52460 * 3600 / VLc # D107 (mg/L/h)
bleach_t1ppm  = 1 / bleach_rate * 60                   # D108 (min)
HOCl_max = pH_Cl * pH_fHOCl * 52460                    # D125 (mg/L) - gate input for D109, pH-aware via D104
if HOCl_max > 0.2:                                     # D109 mirrors the workbook: HOCl_max gate, not a chloride gate
    bleach_flag = f"BLEACH RISK: HOCl {HOCl_max:.1f} mg/L (>0.2 first-impairment)"
elif HOCl_max > 0.02:
    bleach_flag = f"HOCl {HOCl_max:.1f} mg/L - watch"
else:
    bleach_flag = "no bleaching (negligible chloride)"
if pH_op < 6.5:
    pH_band_flag = "pH BELOW HOB optimum (<6.5) - reduce CO2 dose"
elif pH_op > 7.5:
    pH_band_flag = "pH above optimum (>7.5)"
else:
    pH_band_flag = "pH in HOB band 6.5-7.5"            # D110
# HOCl_max (D125) computed above, before bleach_flag (workbook D109 gates on it)


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
# ============================================================================
stir_len  = stir_bar_L                                # D5 (mm)  (from Geometry)
sigma     = 0.0712                                    # D29 (N/m)
rho_L     = 995.65                                    # D30 (kg/m3)
g_const   = 9.80665                                   # D31 (m/s2)
D_O2      = 2.249e-9                                  # D32 (m2/s)
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
target_DO_frac = (DO_opt / DO_toxic) if (isnum(DO_opt) and isnum(DO_toxic)) else 0.5  # D84
carbon_margin_min = 2.0                                # D85

# --- duty floors & optimum schedule ---
duty_carbon = carbon_margin_min * CO2_cons / (nCO2_rate * 3600)        # D86
# Worst-case O2 source the safety guards size on: net O2 generation with the
# surface-strip credit WITHHELD (kL_surf is a ~375%-uncertain best-case proxy
# and must never gate a safety guard).
O2_src_guard = O2_net_gen                              # D132 (mol/h)
duty_O2vent = O2_src_guard / (target_DO_frac * (O2_ceil_Pa / P_atm)) / (nCO2_rate * 3600)  # D87
duty_opt    = max(duty_carbon, duty_O2vent)            # D88
spg_int_max = (target_DO_frac * O2_ceil_C * (V_charge / 1e6)
               / O2_src_guard * 60)                                   # D89 (min)
spg_dur_opt = max(pulse_floor, flush_factor * headspace_V / (Q_CO2 / 60))  # D90 (s)
spg_int_opt = min(spg_dur_opt / (60 * duty_opt), spg_int_max)         # D91 (min)
spg_int_opt_s = spg_int_opt * 60                       # D92 (s)
duty_actual = spg_dur_opt / (spg_int_opt * 60)         # D93
if spg_int_opt >= spg_int_max - 0.0001:
    opt_binding = "O2-CEILING"
elif spg_int_opt < spg_dur_opt / (60 * duty_opt) - 0.0001:
    opt_binding = "O2-FREQ"
elif duty_O2vent >= duty_carbon:
    opt_binding = "O2-VENT"
else:
    opt_binding = "CARBON"                             # D94
od_ok = "OK" if (spg_int_opt * 60 - spg_dur_opt >= 5) else "TIGHT"    # D95

# --- schedule mode resolution (Optimal) ---
sched_mode = "Optimal"                                 # D81
spg_dur = spg_dur_opt if sched_mode == "Optimal" else (1.0 if sched_mode == "Manual" else NA)  # D121
spg_int = spg_int_opt if sched_mode == "Optimal" else (1.0 if sched_mode == "Manual" else NA)  # D122
duty    = spg_dur / (spg_int * 60)                     # D105
spg_int_carbon = spg_dur_opt / (60 * duty_carbon)      # D112 (min)

CO2_pulse  = nCO2_rate * spg_dur                        # D123 (mol)
pulses_h   = 60 / spg_int                               # D124 (/h)
pulses_d   = pulses_h * 24                              # D125 (/d)
CO2_supply = CO2_pulse * pulses_h                       # D100 (mol/h)
CO2_sd_ratio = CO2_supply / CO2_cons if CO2_cons > 0 else NA  # D126

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

# --- steady-state DO check ---
DO_ss = O2_excess / (kLa_surf_used * 3600 * (V_charge / 1e6)) * 32   # D108 (mg/L)
# --- steady-growth sawtooth diagnostics (surface-credited; NOT the shipped guard) ---
DO_ss_sawtooth = O2_excess / (kLa_surf_used * 3600 * (V_charge / 1e6))      # D133 (mol/m3, steady src)
spg_int_regime = "SURFACE-HELD" if DO_ss_sawtooth < target_DO_frac * O2_ceil_C else "SPARGE-NEEDED"  # D134
DO_ss_sawtooth_lag = O2_net_gen / (kLa_surf_used * 3600 * (V_charge / 1e6))  # D135 (mol/m3, LAG src — what the guard banks on)
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
kL_surf_crit = (O2_excess * 32 / (DO_impair * 3600 * (V_charge / 1e6) * a_surf)
                if isnum(DO_impair) else NA)            # D131


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
    """Excel: IF(x>0.5, ROUND(x,0), ROUND(x, 1-(1+INT(LOG10(ABS(x)))))) ."""
    if x > 0.5:
        return round(x)
    digits = 1 - (1 + int(math.log10(abs(x))))
    return round(x, digits)

S_D13 = iferror(lambda: spg_dur_opt,   # D13: ='Mass Transfer'!D90 (spg_dur_opt)
                "calibrate this reactor first (see CO2 flows)")
S_D14 = round_sig_or_int(S_D13) if isinstance(S_D13, float) else S_D13       # D14
S_D15 = iferror(lambda: spg_int_opt, "calibrate this reactor first (see CO2 flows)")  # D15
S_D16 = round_sig_or_int(S_D15) if isinstance(S_D15, float) else S_D15       # D16
S_D19 = geom_check                                      # D19 vial geometry
S_D20 = cal_warning                                     # D20 reactor calibrated
S_D21 = DO_ss_vs_opt                                    # D21 O2 at/under optimum
S_D22 = DO_ss_vs_min                                    # D22 O2 above minimum
S_D23 = sched_regime                                    # D23 interval relaxable
S_D24 = H2_safety                                       # D24 H2 headspace safe
S_D25 = bubble_regime                                   # D25 bubble model valid
S_D26 = iferror(lambda: ("OK" if CO2_sd_ratio >= 1 else "SHORTFALL (CO2 < demand)"),
                "calibrate this reactor first")         # D26 CO2 supply meets demand
S_D27 = iferror(lambda: dur_ok, "calibrate this reactor first (see CO2 flows)")  # D27 pulse >= floor
S_D28 = iferror(lambda: od_ok, "calibrate this reactor first (see CO2 flows)")   # D28 dosing window
S_D29 = carry_flag                                      # D29 carryover risk
S_D30 = tip_warn                                        # D30 tip-speed shear
S_D31 = media_vol_warn                                  # D31 media volume fits
S_D32 = depth_warn                                      # D32 liquid level OK
S_D33 = I_valid                                         # D33 LED current-law range
S_D34 = ("inputs present" if (isnum(DO_min) and isnum(DO_opt) and isnum(DO_impair) and isnum(DO_toxic))
         else "DATA GAP - organism DO thresholds unmeasured; DO & sparge results unreliable")  # D34
S_D35 = pH_op                                           # D35 endpoint pH
S_D36 = HOCl_max                                        # D36 max HOCl
S_D38 = DO_ss                                           # D38 steady-state DO
S_D39 = spg_int_carbon                                  # D39 interval if O2 handled
S_D40 = tip_speed                                       # D40 stir-bar tip speed
S_D41 = CO2_carbon_margin                               # D41 carbon margin


# ============================================================================
# OUTPUT  - final outputs grouped by sheet, with workbook cached values for
#           the printed comparison (cached values quoted from the formula dump).
# ============================================================================
# Each entry: (label, computed value, cached spreadsheet value)
OUTPUTS = [
    # --- Summary tab (every cell with a Value/result) ---
    ("Summary D13  CO2 pulse duration (s)",            S_D13, 0.78451304982496561),
    ("Summary D14  CO2 pulse duration rounded (s)",    S_D14, 1),
    ("Summary D15  CO2 sparge interval (min)",         S_D15, 2.846431710211678),
    ("Summary D16  CO2 sparge interval rounded (min)", S_D16, 3),
    ("Summary D19  Vial geometry consistent?",         S_D19, "VIAL GEOMETRY INCONSISTENT - measure true fill volume & bore depth"),
    ("Summary D20  Reactor calibrated?",               S_D20, "calibrated: ed04"),
    ("Summary D21  O2 at/under optimum?",              S_D21, "organism optimum unknown"),
    ("Summary D22  O2 above minimum?",                 S_D22, "minimum DO unknown - measure"),
    ("Summary D23  Interval relaxable?",               S_D23, "organism DO unknown"),
    ("Summary D24  H2 headspace safe?",                S_D24, "EXPLOSIVE"),
    ("Summary D25  Bubble model valid?",               S_D25, "Static"),
    ("Summary D26  CO2 supply meets demand?",          S_D26, "OK"),
    ("Summary D27  Pulse >= solenoid floor?",          S_D27, "OK"),
    ("Summary D28  Dosing window OK?",                 S_D28, "OK"),
    ("Summary D29  Carryover risk?",                   S_D29, "OK"),
    ("Summary D30  Tip-speed shear OK?",               S_D30, "OK"),
    ("Summary D31  Media volume fits vial?",           S_D31, "OK"),
    ("Summary D32  Liquid level OK?",                  S_D32, "OK"),
    ("Summary D33  LED current-law in range?",         S_D33, "OK"),
    ("Summary D34  Organism DO data present?",         S_D34, "DATA GAP - organism DO thresholds unmeasured; DO & sparge results unreliable"),
    ("Summary D35  Endpoint pH (worst-case)",          S_D35, 6.3125785894509363),
    ("Summary D36  Max HOCl (mg/L)",                   S_D36, 8.877523507988645),
    ("Summary D38  Steady-state DO (mg/L)",            S_D38, 1.9407611529861681),
    ("Summary D39  Sparge interval if O2 handled (min)", S_D39, 178.08128884816398),
    ("Summary D40  Stir-bar tip speed (m/s)",          S_D40, 0.31415926535897931),
    ("Summary D41  Carbon margin (x)",                 S_D41, 585.59956132513264),

    # --- Terminal numeric outputs on other sheets (referenced by nothing else) ---
    ("Geometry D42  Resulting liquid level (mm)",      h_actual, 31.18130412738023),
    ("Geometry D43  Sparge depth (mm)",                sparge_depth, 9.1813041273802298),
    ("Geometry D90  geom_check (text)",                geom_check, "VIAL GEOMETRY INCONSISTENT - measure true fill volume & bore depth"),
    ("Geometry D54  media_vol_warn",                   media_vol_warn, "OK"),
    ("Geometry D55  depth_warn",                       depth_warn, "OK"),
    ("Electrochem D23  V_H2_gen (mL/min)",             V_H2_gen, 4.4009594822921834e-2),
    ("Electrochem D24  V_O2_gen (mL/min)",             V_O2_gen, 2.2004797411460917e-2),
    ("Electrochem D25  V_gas_total (mL/min)",          V_gas_total, 6.6014392234382754e-2),
    ("Electrochem D20  I_valid",                       I_valid, "OK"),
    ("Chemistry D104  HOCl fraction at op pH",         pH_fHOCl, 0.93902741032842141),
    ("Chemistry D108  Time to ~1 ppm HOCl (min)",      bleach_t1ppm, 0.16161837945657148),
    ("Chemistry D109  bleach_flag",                    bleach_flag, "BLEACH RISK: HOCl 8.9 mg/L (>0.2 first-impairment)"),
    ("Chemistry D110  pH_band_flag",                   pH_band_flag, "pH BELOW HOB optimum (<6.5) - reduce CO2 dose"),
    ("Chemistry D125  HOCl_max (mg/L)",                HOCl_max, 8.877523507988645),
    ("Biology  D28  O2_ceil_uM (uM)",                  O2_ceil_uM, 335.72349444703224),
    ("Biology  D35  CO2_carbon_margin (x)",            CO2_carbon_margin, 585.59956132513264),
    ("Biology  D37  pH_CO2_unbuf",                     pH_CO2_unbuf, 3.9425346209821237),
    ("Biology  D42  t_H2_sat (min)",                   t_H2_sat, 6.5180515324831827),
    ("Biology  D43  H2_turnover (1/h)",                H2_turnover, 9.20520491453399),
    ("Biology  D44  H2_safety",                        H2_safety, "EXPLOSIVE"),
    ("MassXfer D53  kLa_avg (1/s)",                    kLa_avg, 7.578984762686915e-05),
    ("MassXfer D55  strip_avg (mol/h)",                strip_avg, 1.373999354400634e-06),
    ("MassXfer D56  strip_ratio (x)",                  strip_ratio, 0.07766302521500339),
    ("MassXfer D57  kLa_req (1/s)",                    kLa_req, 9.7588070278039642e-4),
    ("MassXfer D59  carry_flag",                       carry_flag, "OK"),
    ("MassXfer D64  bubble_regime",                    bubble_regime, "Static"),
    ("MassXfer D65  t_O2_ceiling (min)",               t_O2_ceiling, 17.078590261270065),
    ("MassXfer D66  t_O2_ceiling_strip (min)",         t_O2_ceiling_strip, 18.516649259617083),
    ("MassXfer D74  surf_ratio (x)",                   surf_ratio, 5.5355352747941149),
    ("MassXfer D76  DO_vent_eq (uM)",                  DO_vent_eq, 8.872702127418156),
    ("MassXfer D77  hs_flush_time (min)",              hs_flush_time, 2.846431710211678),
    ("MassXfer D78  O2_removal_ratio (x)",             O2_removal_ratio, 5.613198300009119),
    ("MassXfer D79  t_O2_ceiling_lag (min)",           t_O2_ceiling_lag, 5.6928634204233548),
    ("MassXfer D80  t_O2_ceiling_rem (min)",           t_O2_ceiling_rem, 9999),
    ("MassXfer D92  spg_int_opt_s (s)",                spg_int_opt_s, 170.78590261270065),
    ("MassXfer D93  duty_actual",                      duty_actual, 0.0045935468784214775),
    ("MassXfer D94  opt_binding",                      opt_binding, "O2-CEILING"),
    ("MassXfer D95  od_ok",                            od_ok, "OK"),
    ("MassXfer D108 DO_ss (mg/L)",                     DO_ss, 1.9407611529861681),
    ("MassXfer D109 DO_ss_vs_opt",                     DO_ss_vs_opt, "organism optimum unknown"),
    ("MassXfer D110 DO_ss_vs_min",                     DO_ss_vs_min, "minimum DO unknown - measure"),
    ("MassXfer D111 tip_warn",                         tip_warn, "OK"),
    ("MassXfer D113 sched_regime",                     sched_regime, "organism DO unknown"),
    ("MassXfer D124 pulses_h (/h)",                    pulses_h, 21.079023180056566),
    ("MassXfer D125 pulses_d (/d)",                    pulses_d, 505.8965563213576),
    ("MassXfer D126 CO2_sd_ratio (x)",                 CO2_sd_ratio, 125.12598718549323),
    ("MassXfer D127 O2_accum (mol)",                   O2_accum, 8.393087361175805e-07),
    ("MassXfer D128 O2_strip_pulse (mol)",             O2_strip_pulse, 6.5183255536272289e-8),
    ("MassXfer D129 sched_bal (x)",                    sched_bal, 0.07766302521500341),
    ("MassXfer D130 dur_ok",                           dur_ok, "OK"),
    ("MassXfer D131 kL_surf_crit (m/s)",               kL_surf_crit, NA),
    ("MassXfer D133 DO_ss_sawtooth (mol/m3)",         DO_ss_sawtooth, 0.060648786030817754),
    ("MassXfer D134 spg_int_regime",                  spg_int_regime, "SURFACE-HELD"),
    ("MassXfer D135 DO_ss_sawtooth_lag (mol/m3)",     DO_ss_sawtooth_lag, 0.1819463580924533),
]


def _fmt(v):
    if isinstance(v, float):
        if math.isnan(v):
            return "#N/A"
        return f"{v:.10g}"
    return str(v)


def _match(comp, cached, tol=0.005):
    """Within 0.5% (numeric) or exact (text). NaN matches #N/A."""
    cnum = isinstance(comp, (int, float)) and not (isinstance(comp, float) and math.isnan(comp))
    knum = isinstance(cached, (int, float)) and not (isinstance(cached, float) and math.isnan(cached))
    if isinstance(comp, float) and math.isnan(comp):
        return isinstance(cached, float) and math.isnan(cached)
    if cnum and knum:
        if cached == 0:
            return abs(comp - cached) < 1e-9
        return abs(comp - cached) / abs(cached) <= tol
    return str(comp).strip() == str(cached).strip()


def main():
    print("=" * 100)
    print("electroPioreactorGasModel - independent first-principles re-derivation")
    print(f"Inputs: reactor={Reactor_sel} ({rx_ver}), electrode={electrode_sel}, "
          f"organism={organism_sel}, media={media_sel}")
    print(f"        LED={led_intensity}%, stir={stir_rpm_set} rpm, T={temp_C} C, "
          f"V_charge={V_charge} mL, P_atm={P_atm:.0f} Pa")
    print("=" * 100)
    hdr = f"{'OUTPUT':<48}{'SPREADSHEET':>22}{'MODEL':>22}  MATCH"
    print(hdr)
    print("-" * 100)
    fails = []
    for label, comp, cached in OUTPUTS:
        ok = _match(comp, cached)
        if not ok:
            fails.append((label, comp, cached))
        print(f"{label:<48}{_fmt(cached):>22}{_fmt(comp):>22}  {'OK' if ok else 'MISMATCH'}")
    print("-" * 100)
    print(f"{len(OUTPUTS) - len(fails)}/{len(OUTPUTS)} outputs match the spreadsheet within 0.5%.")
    if fails:
        print("\nMISMATCHES:")
        for label, comp, cached in fails:
            print(f"  {label}: spreadsheet={_fmt(cached)}  model={_fmt(comp)}")


if __name__ == "__main__":
    main()
