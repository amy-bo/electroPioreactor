#!/usr/bin/env python3
"""One-at-a-time (OAT) sensitivity analysis for electroPioreactorGasModel.xlsx.

WHAT THIS MODELS
    The path from each uncertain INPUT to the schedule-critical OUTPUTS of the gas
    model: the recommended CO2 pulse duration and sparge interval, the steady dissolved
    O2, the operating pH, the peroxide production rate, the estimated cell voltage, and
    the O2 lag time to the inhibition ceiling. Each input is swept over its plausible
    range with everything else held at the workbook's live baseline, so the outputs can
    be ranked by leverage x ignorance.

    The headline output is the INFEASIBILITY CLIFF: which inputs, over their plausible
    range, push DO_surf_excess above DO_target and so make the DO target unreachable at
    ANY sparge interval. That is the discontinuity this revision of the workbook has,
    and it replaces the old SURFACE-HELD / SPARGE-NEEDED regime flip entirely.

WHICH WORKBOOK VERSION IT MIRRORS
    electroPioreactorGasModel.xlsx (wave-4 logic, verified in Excel 2026-10-21), with the live
    selector state behind the values:
        ed04 / MMO tube / Xanthobacter tagetidis / AMYBO03, LED 3 %, stir 1000 rpm, T 30 C.
    (Summary D3 is read from SELECTORS['electrode']; the electrode tables cover the others.)
    Formula logic is read directly out of the workbook part XML (Mass Transfer D178-D200,
    Electrochemistry D79-D122, Chemistry D166-D220). The workbook is the authority for
    both LOGIC and BASELINE INPUTS. The full twin (electroPioreactorGasModel.py) is the
    exhaustive cell-by-cell check; this script is the reduced model the sweeps run on.

WHAT CHANGED IN THIS RE-BASE (vs the previous revision of this script)
    (a) The SURFACE-HELD / SPARGE-NEEDED branch is gone. Dissolved O2 now carries a
        headspace back-pressure term: DO_ss = DO_hs_floor + DO_surf_excess, with
        DO_hs_floor = H_O2*y_O2_actual*P_dry set by the CO2 flush rather than by stirring.
        The interval is MIN(spg_int_carbon, spg_int_DO), a continuous minimum, so no
        unmeasured coefficient switches one formula for another any more. The new
        discontinuity is spg_int_DO going #N/A when DO_target - DO_surf_excess <= 0.
    (b) The faradaic efficiencies are calculated, not asserted: etaF = 1 - i_ORR/I_app.
        etaF is therefore no longer a free sweep input; km_O2 is swept in its place. The
        workbook propagates the calculated values (Electrochemistry D18 and D26 are
        IF(ISNUMBER(cal_X), cal_X, calc)), and so does this script.
    (c) The CO2 limit cycle is mass-conserving (one pooled liquid+headspace inventory
        decaying through the vent) and the pH solve is activity-corrected, so both
        dissolved CO2 and pH respond strongly to the schedule. pH_meas is now a
        first-class critical output.
    (d) Water properties track temperature, so a T_C sweep moves sigma, rho, D_O2, D_CO2
        and both Henry constants, not only the Henry constants.
    (e) iterH: ONE headspace balance (Mass Transfer 300-382) drives the O2 sizing, the
        CO2 pool and the flammability fractions, under two owner selectors (Summary
        D111 vent_model, D112 O2_phase). The sizing targets the CYCLE-MEAN DO (sawtooth
        factor), CO2 fixation is a sink, an outflow-only vent removes CO2 only through
        net evolved gas (so the pool runs near saturation), and a pulse is a well-mixed
        flush. A short block evaluates the headline in all four selector states.
    (f) iterM: the pulse is a delivered VOLUME, V = V0 + Q*t (least-squares fit over the CO2
        flows points, 34 of them, so the pulse time is (headspace - V0)/Q and every duty ->
        interval conversion goes through the full-flow-equivalent time); the liquid stores CO2
        as bicarbonate (DIC_cap, Chemistry D296); every gas partial pressure in a Henry term
        is on the dry basis P_dry = P_atm - p_sat_w; O2 solubility carries a salting-out
        factor; and the PCET credit in the cell voltage is withdrawn past the buffer limit.
        Q_CO2 is no longer a pure input: sweeping it rescales the fitted slope with it, and
        the intercept V0 gets its own sweep (pulse_V0_factor). The three non-live selector
        states in the four-combination block are checked against the twin, not transcribed.

STANDING RULE -- RE-BASE THIS FILE WHENEVER THE WORKBOOK MOVES
    This script is a reduced re-implementation, not a live read of the workbook. It MUST
    be re-based whenever either of the following changes:
      (a) the guard/optimiser logic (Mass Transfer D84-D94, D112, D131-D135, D178-D200, D300-D382)
      (b) the baseline inputs (Summary D2:D10 -- reactor, electrode, organism, medium,
          LED %, stir rpm, temperature, volume, pressure -- and the D111:D112 selectors)
    Every percentage this script prints becomes wrong the moment it drifts. The runtime
    self-check fails loudly if the baseline stops reproducing the workbook, and the
    sweep-bracket assertion fails loudly if a baseline input drifts outside its own sweep
    range. Do not silence either; re-base instead.

SELF-CHECK CONTRACT
    The workbook's own cached values (computed by Excel) are read from the .xlsx beside
    this script at run time; nothing is transcribed. Before any analysis the BASE inputs
    are compared with Summary D2:D10 (and the Geometry / Electrochemistry / Mass Transfer
    cells they feed); on drift the offending pairs are printed and the script exits 1.
    The baseline model() outputs are then compared with their workbook cells at 5e-5
    relative; a missing cache, error value or mismatch is a failure, never a pass.

Standard library only.  Run with:  python3 electroPioreactorGasModel-sensitivity.py

Each input carries an IGNORANCE tier -- DATA-GAP (unmeasured), ESTIMATE, LITERATURE
(well-known), KNOB (you set it). Urgency = leverage on the critical outputs x how poorly
we know the value. KNOBs are control authority, reported separately.
"""
import math
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

PI = math.pi
INF = float('inf')
NAN = float('nan')

# ---------------------------------------------------------------------------
# BASELINE INPUTS
# Source of truth: the WORKBOOK's live Summary selector state (Summary D2:D10) --
# ed04 / MMO tube (SELECTORS['electrode']) / Xanthobacter tagetidis / AMYBO03, LED 3 %, stir 1000 rpm, T 30 C.
#
# NOTE target_DO_frac = 0.2261 (DO_opt 2.6 / DO_toxic 11.5), NOT the 0.5 this script carried
# before. Biology D60/D61
# now derives it from C. necator's measured 3.0 / 11.5 mg/L band instead of an unsourced
# 0.5, which makes the DO target 1.9x more protective and roughly halves the headroom
# before the infeasibility cliff below.
# ---------------------------------------------------------------------------
BASE = dict(
  # --- geometry (measured / estimated for the build; MEP0.3 / AEP0.1.1-class vial) ---
  vial_OD=27.48, vial_wall=1.1, D_int=55, V_max=16, V_vial_total=20,
  rod_d=6, rod_n=2, elec_clear=22, spg_OD=3.175, spg_ID=1.5875,
  eff_OD=3.175, eff_ID=1.5875, xtube_n=3, xtube_pro=5,
  elec_gap=14.0,                          # Geometry D92, DATA GAP -- measure with calipers
  # --- electrolysis ---
  intensity=3, gerrit_slope=1.03, gerrit_int=2.6, F=96485.33212,
  z_e_H2=2, z_e_O2=4, z_e_ORR=2,          # z_e_ORR=2: peroxide pathway, SS cathode lookup
  km_O2=4.0e-3, km_exp=0.644,             # Eisenberg-Tobias-Wilke; k_m scales as D^0.644
  f_HOOH=0.15, k_cat_cells=0.0041, M_H2O2=34.0147,
  FE_CER=0.5, km_Cl=0.00405, corr_I_frac=0.0,
  # --- biology ---
  bio_H2=6, bio_O2=2, bio_CO2=1,
  # --- O2 ceiling / Henry ---
  T_C=30, P_atm=101325, H_O2ref=1.2e-5, H_O2T=1500, T_ref=298.15, O2_ceil_atm=0.3,
  # --- CO2 dosing (ed04 calibrated: 3.33 mL/s = 199.8 mL/min) ---
  DO_lag_ref=0.194,   # Echem D129: typed reference lag DO (mol/m3) for the lag cathodic loss
  Q_CO2=199.8, Q_CO2_cal=199.8, fit_n_min=3, pulse_V0_factor=1.0, pulse_floor=0.25, flush_factor=1.0, R=8.314462618, M_CO2=44.0095,
  # --- water properties (now temperature-tracking, not frozen constants) ---
  sigma_0=0.07589, sigma_k=-0.000157,     # IAPWS R1-76(2014) linear fit, 15-40 C
  rho_0=1003.33, rho_k=-0.2556,           # IAPWS-95 linear fit, 15-40 C
  HB_a=-4.41, HB_b=773.8, HB_c=506.4,     # Han & Bartels 1996 log10 D_O2 fit
  D_O2_fit=1.0,                           # multiplier carrying the fit's own uncertainty
  D_CO2_ref=1.92e-9, Ea_D_CO2=19000.0,
  # --- bubble / strip ---
  g=9.80665, mend_a=2.14, mend_b=0.505,
  # --- surface / stirring ---
  stir_rpm=1000, stir_len=12, kL_surf_factor=1.0,   # factor = order-of-magnitude uncertainty
  # --- dissolved CO2 / H2 / vent ---
  ks_O2=0.14,                             # Biology D122: O2 Setschenow coefficient (L/mol per unit ionic strength)
  pH_ref_DIC=6.09,                        # Chemistry D291: reference pH of the DIC capacity
  pw_A=610.94, pw_B=17.625, pw_C=243.04,  # MT D203:D205 Magnus coefficients (Pa, -, degC)
  H_CO2ref=3.3e-4, H_CO2T=2400, Km_CO2=50,
  H_H2ref=7.8e-6, H_H2T=500,
  Q_vent=0.5, Q_backdraw=0.015, pCO2_air=40.0,   # Q_backdraw: MT D385, open-vent back-draw air (mL/min) - MEASURE
  # --- iterH headspace balance: owner selectors (Summary D111:D112) + dry-air O2 ---
  vent_model='Open vent',                 # 'Outflow only' | 'Open vent' (Q_backdraw) | 'Air exchange' (Q_vent = TOTAL air ingress)
  O2_phase='Growth',                      # 'Growth' | 'Lag': the phase the O2 schedule is sized on
  y_O2_air=0.2095,                        # MT D307
  # --- optimiser inputs ---
  target_DO_frac=0.226086956521739, carbon_margin_min=2,
  DO_opt=None,                            # mg/L; None = unmeasured (UdG) -> DO target from the fraction rule (MT D179)
  # --- cell-voltage budget ---
  b_anode=0.12, j0_anode=1e-10, b_cath=0.14, j0_cath=1.5e-6, pcet_credit=-0.15,
  E0_OER=1.229, k_geom=1.0, kappa_fI=0.78, kappa_TC=0.02,
  # --- local-pH (buffer) verdict ---
  D_HPO4=7.59e-10, D_Cl=2.032e-9,                        # film thickness delta is now DERIVED: D_O2/km_O2 (Chemistry D215)
  # --- UdG recipe (g/L) ---
  udg_KH2PO4=2.3, udg_Na2HPO4=2.9, udg_NaHCO3=1.05,
  udg_MgSO4=0.5, udg_NH42SO4=0.47, udg_CaCl2=0.01,
  # --- chlorine chain ---
  f_local=10.0, k1_NH2Cl=4.2e6, tau_NH2Cl=1.0, R_chloramine=25.0,
)

# ed04 pulse-volume points (volume mL, time s) from CO2 flows E/F, excluding the two red outliers
# flagged in column N (rows 36 and 46) and the rows with no time: the 34 points behind the
# workbook's V = V0 + Q*t fit (Mass Transfer D401-D408).
CO2_FIT_PTS = [
    (50.0, 15.0), (12.0, 4.0), (14.0, 4.0), (14.0, 4.0), (6.0, 2.0), (9.0, 2.0),
    (6.0, 2.0), (8.0, 2.0), (6.0, 2.0), (10.0, 2.0), (4.0, 1.0), (4.0, 1.0),
    (3.0, 1.0), (4.0, 1.0), (4.0, 1.0), (4.0, 1.0), (2.0, 0.5), (2.0, 0.5),
    (2.0, 0.5), (2.0, 0.5), (2.0, 0.5), (1.0, 0.25), (1.0, 0.25), (1.0, 0.25),
    (1.0, 0.25), (1.0, 0.25), (0.8, 0.2), (1.0, 0.2), (0.8, 0.2), (0.4, 0.1),
    (0.4, 0.1), (0.6, 0.1), (0.6, 0.1), (0.6, 0.1),
]

MW = dict(KH2PO4=136.086, Na2HPO4=141.96, NaHCO3=84.007,
          MgSO4=246.48, NH42SO4=132.14, CaCl2=110.98,
          NaH2PO4_2H2O=156.01, K2SO4=174.26, CaSO4_2H2O=172.17)
# CRC Handbook (Vanysek), limiting molar conductivities at 25 C, S cm2/mol, PER MOLE OF ION
LAM = dict(Na=50.08, K=73.48, NH4=73.5, Mg=106.0, Ca=118.94,
           H2PO4=36.0, HPO4=114.0, SO4=160.0, HCO3=44.5, Cl=76.31)
# (K25, dH kJ/mol) -- van 't Hoff corrected to the reactor temperature (Chemistry D13:D19)
KA = dict(Ka1c=(4.45e-7, 9.15), Ka2c=(4.69e-11, 14.9), Ka1p=(7.1e-3, -8.0),
          Ka2p=(6.31e-8, 3.6), Ka3p=(4.2e-13, 16.0), KaN=(5.6e-10, 52.2),
          Kw=(1e-14, 55.8))
M_HOCl = 52460.0   # mg/mol
M_Cl2 = 70906.0    # mg/mol (Chemistry D223); thresholds are on the as-Cl2 basis
M_O2 = 31.998      # g/mol, Mass Transfer D231 (2 x 15.999)
D_HCO3 = 1.185e-9  # m2/s, Chemistry D251 (CRC)
MW_N = 14007.0     # mg/mol
CL_PER_N = 5.06    # mg Cl2 per mg ammonium-N (breakpoint)
# Electrode lookups keyed on Summary D3 (same tables as the twin): Electrochemistry A35:N38
ELECTRODE = {
    'Pt/Ti rod': dict(sparger='Tube',     por=None, z_e_ORR=2),   # Echem D31 sparger, D32 sinter grade, D27 z_e_ORR
    'MMO rod':   dict(sparger='Tube',     por=None, z_e_ORR=2),
    'MMO tube':  dict(sparger='Sintered', por=0,    z_e_ORR=2),
}
ELECTRODE_GEOM = {  # anode/cathode shape + dia (mm), Echem D42/D44; plating limits jc/jm (mA/cm2) D50/D51
    'Pt/Ti rod':    dict(a_shape='rod',  a_d=6.0, c_shape='rod', c_d=6.0, jc=100, jm=500, mat='Pt/Ti'),
    'MMO rod':      dict(a_shape='rod',  a_d=6.0, c_shape='rod', c_d=6.0, jc=50,  jm=500, mat='MMO'),
    'MMO tube':     dict(a_shape='tube', a_d=6.0, c_shape='rod', c_d=6.0, jc=10,  jm=60,  mat='MMO'),
    'Graphite rod': dict(a_shape='rod',  a_d=6.0, c_shape='rod', c_d=6.0, jc=35,  jm=50,  mat='Graphite'),
}
POR_UM = [205, 130, 70, 28, 13, 1.3]   # MT D33:D38, sinter pore (um) by grade 0..5


def _by_media(media, mc02_val, udg_val, amy_val):
    """Exact selector branches, as in Chemistry D44:D47; reject unknown media."""
    return {'MC02': mc02_val, 'UdG phosphate': udg_val,
            'AMYBO03': amy_val}[media]


def medium_chemistry(p):
    """Derive analytical ions from each recipe, independently of the workbook caches.

    Concentrations are mol/L. Sulfate salts cancel from strong-ion difference
    except ammonium sulfate; ammonium is handled by the charge-balance solve.
    AMYBO03 stock acid removes two equivalents per mole. Trace metal sulfates
    cancel in SID but contribute to ionic strength and sulfate conductivity.
    """
    mc = dict(Na2HPO4=2.895, NaH2PO4_2H2O=3.06, K2SO4=0.17,
              CaSO4_2H2O=0.097, MgSO4=0.8, NH42SO4=0.943)
    udg = {salt: p['udg_' + salt] for salt in
           ('KH2PO4', 'Na2HPO4', 'NaHCO3', 'MgSO4', 'NH42SO4', 'CaCl2')}
    amy = dict(Na2HPO4=4.26, NaH2PO4_2H2O=4.68, K2SO4=0.17,
               CaSO4_2H2O=0.097, MgSO4=0.8, NH42SO4=0.943, NaHCO3=3.36)
    recipe = _by_media(p['media'], mc, udg, amy)
    n = {salt: mass / MW[salt] for salt, mass in recipe.items()}
    q = lambda salt: n.get(salt, 0.0)
    ions = dict(Na=2*q('Na2HPO4') + q('NaH2PO4_2H2O') + q('NaHCO3'),
                K=q('KH2PO4') + 2*q('K2SO4'), NH4=2*q('NH42SO4'),
                Mg=q('MgSO4'), Ca=q('CaSO4_2H2O') + q('CaCl2'),
                H2PO4=q('KH2PO4') + q('NaH2PO4_2H2O'), HPO4=q('Na2HPO4'),
                SO4=q('MgSO4') + q('CaSO4_2H2O') + q('NH42SO4') + q('K2SO4'),
                HCO3=q('NaHCO3'), Cl=2*q('CaCl2'))
    SID = ions['Na'] + ions['K'] + 2*(ions['Mg'] + ions['Ca']) - 2*ions['SO4'] - ions['Cl']
    I_ion = sum(c * (4 if ion in ('Mg', 'Ca', 'HPO4', 'SO4') else 1)
                for ion, c in ions.items()) / 2
    kappa0 = sum(c * LAM[ion] for ion, c in ions.items()) / 10
    if p['media'] == 'AMYBO03':
        # AMYBO03 B15:B16 dose mL/L; stock g/L / molar mass * dose / 1000.
        Fe = 15 / 278.01 * 0.68 / 1000
        acid = 0.2 * (0.68 + 0.05) / 1000
        trace = sum(c / mw * 0.05 / 1000 for c, mw in
                    ((2.4, 287.54), (2.4, 169.02), (0.48, 249.68),
                     (1.5, 262.85), (0.0402, 281.1)))
        Mo = 1.8 / 241.95 * 0.05 / 1000
        SID -= 2 * acid
        I_ion += 4*(Fe + trace) + 3*Mo + 3*acid
        # Same explicit trace approximation as AMYBO03 D58: sulfate only.
        kappa0 += (Fe + trace + acid) * LAM['SO4'] / 10
    return SID, ions['H2PO4'] + ions['HPO4'], ions['NH4'], ions['Cl'], I_ion, kappa0


def model(p):
    T_K = p['T_C'] + 273.15
    R = p['R']

    # --- geometry (Geometry sheet) ---
    vial_ID = p['vial_OD'] - 2 * p['vial_wall']
    A_x = PI / 4 * vial_ID ** 2
    h_datum = p['V_max'] * 1000 / A_x
    elec_ins = p['D_int'] - p['elec_clear']
    spg_tip_h = p['elec_clear']
    disp = (p['rod_n'] * (PI / 4 * p['rod_d'] ** 2) * max(0, h_datum - p['elec_clear'])
            + (PI / 4 * p['spg_OD'] ** 2) * max(0, h_datum - spg_tip_h)
            + (PI / 4 * (p['eff_OD'] ** 2 - p['eff_ID'] ** 2))
            * ((p['eff_OD'] + p['eff_ID']) / 2)) / 1000
    V_charge = round(p['V_max'] - disp, 0)
    h_actual = (V_charge + disp) * 1000 / A_x
    interface_A = A_x - (p['rod_n'] * (PI / 4 * p['rod_d'] ** 2)
                         + (PI / 4 * p['spg_OD'] ** 2) + (PI / 4 * p['eff_OD'] ** 2))
    spg_len = p['D_int'] - spg_tip_h
    V_inserts = (p['rod_n'] * (PI / 4 * p['rod_d'] ** 2) * elec_ins
                 + (PI / 4 * p['spg_OD'] ** 2) * spg_len
                 + (PI / 4 * (p['eff_OD'] ** 2 - p['eff_ID'] ** 2)) * (p['D_int'] - h_actual)
                 + p['xtube_n'] * (PI / 4 * p['eff_OD'] ** 2) * p['xtube_pro']) / 1000
    headspace_V = p['V_vial_total'] - V_charge - V_inserts
    V_L = V_charge / 1e6                                    # m3
    hs_m3 = headspace_V / 1e6
    # Geometry D93: submerged length at the ACHIEVED level, not the bare datum
    L_sub = max(0.0, h_actual - p['elec_clear'])
    eg = ELECTRODE_GEOM[p['electrode']]                                  # Echem A35:N38 lookup on Summary D3
    wet = lambda shape, d: (PI * d * L_sub + (PI / 4 * d ** 2 if shape == 'rod' else 0)) / 100   # cm2, rod adds its end face, tube none
    A_wet = wet(eg['a_shape'], eg['a_d'])                                # Echem D46, anode wetted area (cm2)
    A_cath = wet(eg['c_shape'], eg['c_d'])                               # Echem D47, cathode wetted area (cm2)

    # --- water properties at the reactor temperature (Mass Transfer D29-D32, D138) ---
    sigma = p['sigma_0'] + p['sigma_k'] * p['T_C']
    rho_L = p['rho_0'] + p['rho_k'] * p['T_C']
    D_O2 = 10 ** (p['HB_a'] + p['HB_b'] / T_K - (p['HB_c'] / T_K) ** 2) / 10000 * p['D_O2_fit']
    D_CO2 = p['D_CO2_ref'] * math.exp(-p['Ea_D_CO2'] / R * (1 / T_K - 1 / 298.15))
    Ka = {k: v[0] * math.exp(-v[1] * 1000 / R * (1 / T_K - 1 / 298.15)) for k, v in KA.items()}
    SID, PT, NT, Cl_M, I_ion, kappa0 = medium_chemistry(p)
    f_salt_O2 = 10 ** (-p['ks_O2'] * I_ion)                              # Biology D123, O2 salting-out (Setschenow, I from Chemistry D185)
    H_O2_T = p['H_O2ref'] * math.exp(p['H_O2T'] * (1 / T_K - 1 / p['T_ref'])) * f_salt_O2   # Biology D24
    p_sat_w = p['pw_A'] * math.exp(p['pw_B'] * (T_K - 273.15) / ((T_K - 273.15) + p['pw_C']))   # MT D206, Magnus
    P_dry = p['P_atm'] - p_sat_w                                         # MT D418, dry-gas basis of every Henry term
    H_CO2_T = p['H_CO2ref'] * math.exp(p['H_CO2T'] * (1 / T_K - 1 / p['T_ref']))
    H_H2_T = p['H_H2ref'] * math.exp(p['H_H2T'] * (1 / T_K - 1 / p['T_ref']))
    O2_ceil_Pa = p['O2_ceil_atm'] * p['P_atm']
    O2_ceil_C = H_O2_T * O2_ceil_Pa

    # --- electrolysis, with CALCULATED faradaic efficiencies (Echem D86-D89, D101-D104) ---
    I_app = (p['gerrit_slope'] * p['intensity'] + p['gerrit_int']) / 1000
    DO_target = (p['DO_opt'] / M_O2 if p['DO_opt'] is not None
                 else p['target_DO_frac'] * O2_ceil_C)                   # MT D179
    DO_design = DO_target                                                # Echem D85 = the DO target (R5-m7)
    n_ORR_eff = p['z_e_ORR'] * p['f_HOOH'] + p['z_e_O2'] * (1 - p['f_HOOH'])   # D141, e-/O2 weighted by peroxide selectivity
    i_ORR = n_ORR_eff * p['F'] * (p['km_O2'] / 100) * DO_design * (A_cath / 10000)   # D86, cathode area D47
    i_ORR_ceil = n_ORR_eff * p['F'] * (p['km_O2'] / 100) * O2_ceil_C * (A_cath / 10000)   # D87
    etaF_calc = max(0.0, 1 - i_ORR / I_app)                              # D88
    etaF_calc_min = max(0.0, 1 - i_ORR_ceil / I_app)                     # D89
    km_Cl = p['km_O2'] * (p['D_Cl'] / D_O2) ** p['km_exp']                         # D129, scaled from km_O2
    k_Cl_turn = km_Cl * A_wet / 1000 / (V_charge / 1000)                 # D271, transport-limited turnover
    kt = k_Cl_turn * p['tau_NH2Cl'] * 3600
    I_Cl = min(I_app * p['FE_CER'], 2 * p['F'] * km_Cl * (Cl_M / (1 + kt) / 1000) * A_wet)   # D133, free chloride only (D278)
    etaF_OER_calc = max(0.0, 1 - I_Cl / I_app - p['corr_I_frac'])        # D104
    etaF = etaF_calc                                                     # D18 (no calibration override)
    etaF_OER = etaF_OER_calc                                             # D26
    rH2 = I_app * etaF / (p['z_e_H2'] * p['F']) * 3600
    rO2 = I_app * etaF_OER / (p['z_e_O2'] * p['F']) * 3600
    O2_cath = I_app * (1 - etaF) / (n_ORR_eff * p['F']) * 3600
    O2_net = rO2 - O2_cath                                               # Echem D29
    # R5-m2: lag-phase cathodic O2 loss at the typed reference lag DO (Echem D129-D133)
    O2_ORR_lag = min(I_app / (n_ORR_eff * p['F']) * 3600, O2_cath * p['DO_lag_ref'] / DO_design)   # D131
    O2_net_lag = rO2 - O2_ORR_lag                                        # D132 = MT D394 = MT D310
    rH2_lag = max(0.0, I_app - O2_ORR_lag / 3600 * n_ORR_eff * p['F']) / (p['z_e_H2'] * p['F']) * 3600   # D133 = MT D395
    O2_cons = rH2 * p['bio_O2'] / p['bio_H2']
    CO2_cons = rH2 * p['bio_CO2'] / p['bio_H2']
    O2_excess = O2_net - O2_cons                                         # Biology D16

    # --- surface transfer (MT D67-D73, D98) ---
    tip = PI * (p['stir_len'] / 1000) * p['stir_rpm'] / 60
    s_ren = tip / (vial_ID / 1000)
    kL_surf = 2 * math.sqrt(D_O2 * s_ren / PI) * p['kL_surf_factor']
    a_surf = interface_A / V_charge
    kLa_surf_used = kL_surf * a_surf                          # kLa_meas = 0 in the workbook
    surf_strip = kLa_surf_used * V_L * O2_ceil_C * 3600
    surf_ratio = surf_strip / O2_excess if O2_excess > 0 else NAN

    # ------------------------------------------------------------------
    # SCHEDULE OPTIMISER -- the CURRENT workbook form (MT D178-D188).
    # Surface stripping can only move oxygen into the headspace, so the liquid can never
    # fall below equilibrium with it. DO_ss is a floor plus an excess, and the schedule
    # sets the floor by diluting the headspace with CO2.
    #   SUPERSEDED (do not reinstate): the SURFACE-HELD / SPARGE-NEEDED branch on D134,
    #   which chose between a 3 min and a 181 min schedule on the strength of an
    #   unmeasured kL_surf. D91 is now a plain MIN of two continuous bounds.
    # ------------------------------------------------------------------
    nCO2 = p['P_atm'] * (p['Q_CO2'] / 1e6 / 60) / (R * T_K)              # D104, mol/s
    CO2_rate_full = nCO2 * 3600                                          # D178, mol/h
    # R2-M3: delivered volume V = V0 + Q*t, least squares over the CO2 flows points (MT D401-D408).
    # The fit was taken at the calibration flow, so sweeping Q_CO2 rescales the slope with it
    # (V0, the valve-opening intercept, is flow-independent); pulse_V0_factor carries V0's own uncertainty.
    _n = len(CO2_FIT_PTS)
    _St = sum(t for v, t in CO2_FIT_PTS); _SV = sum(v for v, t in CO2_FIT_PTS)
    _Stt = sum(t * t for v, t in CO2_FIT_PTS); _StV = sum(t * v for v, t in CO2_FIT_PTS)
    _ok = _n >= p['fit_n_min'] and _n * _Stt - _St ** 2 > 0
    Q_fit_cal = (_n * _StV - _St * _SV) / (_n * _Stt - _St ** 2) if _ok else p['Q_CO2_cal'] / 60   # D407
    V0_cal = (_SV - Q_fit_cal * _St) / _n if _ok else 0.0                                          # D408
    Q_fit = Q_fit_cal * p['Q_CO2'] / p['Q_CO2_cal']                      # mL/s at the flow in use
    V0 = V0_cal * p['pulse_V0_factor']                                   # mL
    spg_dur = max(p['pulse_floor'], (p['flush_factor'] * headspace_V - V0) / Q_fit)   # D90
    spg_dur_eq_opt = (V0 + Q_fit * spg_dur) / (p['Q_CO2'] / 60)          # D409, full-flow-equivalent time

    # --- iterH: ONE headspace balance (MT 300-382). Steady flux-weighted composition
    #     y_i = (in_i + y_air,i F_vent_ex) / (F_vent_ex + CO2_supply + O2_src + H2_src - CO2_fix)
    #     shared by the O2 sizing, the CO2 pool and the flammability block. ---
    n_hs = p['P_atm'] * hs_m3 / (R * T_K)                                # D150, mol
    Q_used = {'Outflow only': 0.0, 'Open vent': p['Q_backdraw'],
              'Air exchange': p['Q_vent']}.get(p['vent_model'], NAN)     # D386, mL/min
    F_ex = p['P_atm'] * (Q_used / 1e6 / 60) / (R * T_K) * 3600           # D308, mol/h
    y_air = p['y_O2_air']
    H2_cons = rH2                                                        # Biology D13 (no anodic HOR)
    phases = {'Growth': (O2_excess, max(0.0, rH2 - H2_cons), CO2_cons),  # D309/D313/D315
              'Lag': (O2_net_lag, rH2_lag, 0.0)}                         # D310/D314/D316 (lag-DO sources)
    O2_s, H2_s, fix_s = phases.get(p['O2_phase'], (NAN, NAN, NAN))       # D317-D319, sizing phase
    flush_vol_opt = nCO2 * spg_dur_eq_opt / n_hs                         # D320
    flush_ret_opt = math.exp(-flush_vol_opt)                             # D321
    saw_factor = flush_vol_opt * (1 + flush_ret_opt) / (2 * (1 - flush_ret_opt))   # D322
    DO_surf_excess = O2_s / (kLa_surf_used * 3600 * V_L)                 # D180, sizing phase
    DO_surf_excess_g = O2_excess / (kLa_surf_used * 3600 * V_L)          # D339
    DO_surf_excess_lag = O2_net_lag / (kLa_surf_used * 3600 * V_L)           # D181
    hs_O2_allow = DO_target - DO_surf_excess                             # D182
    feasible = hs_O2_allow > 0
    if feasible:
        y_O2_star = hs_O2_allow / (H_O2_T * P_dry)                       # D183
        duty_DO = max(0.0, ((O2_s + y_air * F_ex) * saw_factor / y_O2_star
                            - F_ex - O2_s - H2_s + fix_s) / CO2_rate_full)   # D184
        spg_int_DO = (spg_dur_eq_opt / (60 * duty_DO) if duty_DO > 0
                      else None)                                     # D185 (duty 0 -> carbon-limited, set below)
    else:
        y_O2_star = duty_DO = spg_int_DO = NAN
    # the feasibility floor: measured kL_surf must exceed kL_surf_crit or nothing works
    kLa_surf_req = O2_s / (DO_target * 3600 * V_L)                       # D186, sizing phase
    kL_surf_crit = kLa_surf_req / a_surf                                 # D131
    # margin > 1 => DO target reachable; < 1 => UNREACHABLE at any interval
    do_margin = kLa_surf_used / kLa_surf_req if kLa_surf_req > 0 else INF

    duty_carbon = p['carbon_margin_min'] * CO2_cons / CO2_rate_full      # D86
    spg_int_carbon = spg_dur_eq_opt / (60 * duty_carbon) if duty_carbon > 0 else INF   # D112
    if spg_int_DO is None:
        spg_int_DO = spg_int_carbon                                      # D185 with duty_DO = 0
    O2_src_guard = O2_net                                                # D132
    duty_O2vent = (O2_src_guard / (p['target_DO_frac'] * (O2_ceil_Pa / p['P_atm']))
                   / CO2_rate_full)                                      # D87
    duty_opt = max(duty_carbon, duty_O2vent)                             # D88
    spg_int_max = ((p['target_DO_frac'] * O2_ceil_C * V_L / O2_src_guard * 60)
                   if O2_src_guard > 1e-15 else INF)                     # D89
    if feasible:
        spg_int = min(spg_int_carbon, spg_int_DO)                        # D91 branch 1
        opt_binding = ('O2-DILUTION (headspace O2 sets the interval)'
                       if spg_int_DO <= spg_int_carbon
                       else 'CARBON (CO2 supply sets the interval)')     # D94
        regime = 'DO REACHABLE (estimated kLa) -- DO-limited interval %.1f min' % spg_int_DO
    else:
        spg_int = min(spg_int_carbon, spg_int_max)                       # D91 fallback
        opt_binding = 'O2-INFEASIBLE (see D134)'
        regime = ('DO TARGET UNREACHABLE -- the surface cannot carry the O2 flux at this '
                  'kLa; no interval fixes it')
    duty_actual = spg_dur_eq_opt / (spg_int * 60)                        # D93, full-flow-equivalent duty
    duty = spg_dur / (spg_int * 60)                                      # D105, valve-time duty
    spg_dur_run = max(p['pulse_floor'], math.floor(spg_dur / 0.05 + 0.5 + 1e-12) * 0.05)   # MT D242 (pulse_res 0.05 s, MROUND)
    spg_dur_run_eq = (V0 + Q_fit * spg_dur_run) / (p['Q_CO2'] / 60)      # as-run pulse on the delivered-volume basis
    spg_int_run = math.floor(spg_dur_run_eq / (60 * duty_actual) + 0.5)  # Summary D16, whole minutes

    # --- both-phase sawtooth at the schedule in use (MT 323-374) ---
    V_pulse = V0 + Q_fit * spg_dur                                       # D411, mL
    CO2_pulse = p['P_atm'] * (V_pulse / 1e6) / (R * T_K)                 # D123
    CO2_supply = CO2_pulse * (60 / spg_int)                              # D100
    t_off = max(0.0, spg_int * 60 - spg_dur)                             # D152
    t_gap_h = t_off / 3600                                               # D325
    flush_ret = math.exp(-CO2_pulse / n_hs)                              # D323-D324, well-mixed flush
    tau_L_h = 1 / (kLa_surf_used * 3600)                                 # D326
    phi = lambda x: (1 - math.exp(-x)) / x if x > 0 else 1.0
    psi = lambda x: (x - 1 + math.exp(-x)) / x ** 2 if x > 0 else 0.5

    def _hs(O2_src, H2_src, fix, exc):
        S = O2_src + y_air * F_ex                                        # D327/D349
        F_all = F_ex + CO2_supply + O2_src + H2_src - fix                # F_vent_ex + F_hs_net
        y_mf = S / F_all if F_all > 0 else NAN                           # D329/D351
        yH2 = H2_src / F_all if F_all > 0 else NAN                       # D330/D352
        F_gap = F_ex + max(0.0, O2_src + H2_src - fix)                   # D331/D353
        x = F_gap * t_gap_h / n_hs                                       # D332/D354
        dy = S * t_gap_h / n_hs                                          # D335/D357
        y_end = dy * phi(x) / (1 - flush_ret * math.exp(-x))             # D336/D358
        y_avg = y_end * flush_ret * phi(x) + dy * psi(x)                 # D338/D360
        k = H_O2_T * P_dry
        return dict(y_mf=y_mf, yH2=yH2, F_gap=F_gap, DO_mf=exc + k * y_mf,
                    DO_avg=exc + k * y_avg,
                    DO_peak=exc + k * max(y_avg, y_end - (S - F_gap * y_end) / n_hs * tau_L_h))
    hs = {'Growth': _hs(*phases['Growth'], DO_surf_excess_g),
          'Lag': _hs(*phases['Lag'], DO_surf_excess_lag)}
    hs_s = hs.get(p['O2_phase'], dict(y_mf=NAN, F_gap=NAN, DO_avg=NAN, DO_peak=NAN))
    y_O2_actual = hs_s['y_mf']                                           # D187
    DO_hs_floor = H_O2_T * y_O2_actual * P_dry                           # D188
    DO_ss_sawtooth = DO_hs_floor + DO_surf_excess                        # D133, mol/m3
    DO_ss = hs_s['DO_avg'] * M_O2                                        # D108 = D372, mg/L cycle mean
    DO_peak = hs_s['DO_peak'] * M_O2                                     # D373, mg/L
    DO_ss_g, DO_peak_g = hs['Growth']['DO_avg'] * M_O2, hs['Growth']['DO_peak'] * M_O2   # Summary D114/D115
    DO_ss_lag, DO_peak_lag = hs['Lag']['DO_avg'] * M_O2, hs['Lag']['DO_peak'] * M_O2     # Summary D116/D117
    y_H2_lag = hs['Lag']['yH2']                                          # D352 = Biology D84
    t_lag = (O2_ceil_C * V_L / O2_net * 60) if O2_net > 1e-15 else INF   # D79

    # --- bubble / sparge strip; orifice from the electrode's sparger (MT D27:D41); sub-mm bubble -> strip 0 (D54) ---
    d_or = (p['spg_ID'] / 1000 if ELECTRODE[p['electrode']]['sparger'] == 'Tube'
            else POR_UM[ELECTRODE[p['electrode']]['por']] / 1e6)        # MT D41: tube bore or sinter pore (D39)
    d_b = (6 * d_or * sigma / (rho_L * p['g'])) ** (1 / 3)              # MT D42
    if d_b < 0.001:
        strip_avg = 0.0                                                  # MT D54/D55: sinter bubble excluded
        strip_ratio = 0.0 if O2_excess > 0 else NAN                      # MT D56
    else:
        u_rise = math.sqrt(p['mend_a'] * sigma / (rho_L * d_b) + p['mend_b'] * p['g'] * d_b)
        u_sg = (p['Q_CO2'] / 1e6 / 60) / (A_x / 1e6)
        holdup = u_sg / u_rise
        a_int = 6 * holdup / d_b
        t_c = d_b / u_rise
        kL = 2 * math.sqrt(D_O2 / (PI * t_c))
        strip_sparge = kL * a_int * V_L * O2_ceil_C * 3600
        strip_avg = strip_sparge * duty
        strip_ratio = strip_avg / O2_excess if O2_excess > 0 else NAN
    sa = 0 if (isinstance(strip_avg, float) and math.isnan(strip_avg)) else strip_avg
    removal_ratio = (sa + surf_strip) / O2_excess if O2_excess > 0 else NAN

    # ------------------------------------------------------------------
    # CO2 LIMIT CYCLE -- mass-conserving pooled inventory (MT D191-D200).
    # One pooled liquid+headspace CO2 inventory, decaying through the vent between
    # pulses. The SUPERSEDED form (D161) let the liquid absorb 2.4x the CO2 ever
    # delivered; this one is bounded by the pulse.
    # ------------------------------------------------------------------
    Vg = hs_m3 / (H_CO2_T * R * T_K)                                     # D192
    k_vent = hs_s['F_gap'] / 3600 / n_hs                                 # D143, headspace turnover between pulses
    A_DH = 1.82e6 * (78.54 * (298.15 / T_K) ** 1.368) ** -1.5 * T_K ** -1.5   # D186
    sI = math.sqrt(I_ion)
    dav = lambda z: 10 ** (-A_DH * z * z * (sI / (1 + sI) - 0.3 * I_ion))     # Davies
    g1, g2, g3 = dav(1), dav(2), dav(3)
    K1c, K2c = Ka['Ka1c'] / g1 ** 2, Ka['Ka2c'] / g2
    K1p, K2p = Ka['Ka1p'] / g1 ** 2, Ka['Ka2p'] / g2
    K3p = Ka['Ka3p'] * g2 / (g1 * g3)
    KN, Kw = Ka['KaN'], Ka['Kw'] / g1 ** 2
    # R2-m3: bicarbonate storage -- the liquid holds DIC_cap x its CO2(aq) volume (Chemistry D290-D296)
    h_ref = 10 ** -p['pH_ref_DIC']                                       # D292
    r_HCO3 = K1c / h_ref                                                 # D293
    HCO3_ref = (SID + NT * h_ref / (h_ref + KN) + h_ref
                - (PT * K1p * h_ref ** 2 + 2 * PT * K1p * K2p * h_ref + 3 * PT * K1p * K2p * K3p)
                / (h_ref ** 3 + K1p * h_ref ** 2 + K1p * K2p * h_ref + K1p * K2p * K3p)
                - Kw / h_ref) / (1 + 2 * K2c / h_ref)                    # D294
    beta_nonC = math.log(10) * (PT * K1p * h_ref / (K1p + h_ref) ** 2 + PT * K2p * h_ref / (K2p + h_ref) ** 2
                                + NT * KN * h_ref / (KN + h_ref) ** 2 + h_ref + Kw / h_ref)   # D295
    DIC_cap = 1 + r_HCO3 * beta_nonC / (beta_nonC + math.log(10) * HCO3_ref)   # D296
    V_L_CO2 = V_L * DIC_cap                                              # MT D416
    k_eff = k_vent * Vg / (V_L_CO2 + Vg)                                 # D195
    pool_a = V_L_CO2 / (V_L_CO2 + Vg)                                    # D193
    C_air = H_CO2_T * p['pCO2_air']                                      # D146
    C_sat = H_CO2_T * P_dry                                              # D145
    pool_b = C_sat * (1 - pool_a) * (1 - flush_ret)                      # D194, CO2 a pulse leaves behind
    kLa_CO2_off = kL_surf * a_surf * math.sqrt(D_CO2 / D_O2)             # D148
    pool_beta_ratio = (kLa_CO2_off * V_L / Vg) / k_vent if k_vent > 0 else NAN   # D196 (text 'no turnover between pulses' in the workbook)
    pool_x = k_eff * t_off                                               # D376
    pool_e = math.exp(-pool_x)                                           # D197
    D_raw = (C_air / C_sat * F_ex - fix_s) * t_gap_h / (V_L_CO2 + Vg)    # D375
    pool_ret = pool_a + (1 - pool_a) * flush_ret                         # D380
    C_start = (D_raw * phi(pool_x) + pool_b * pool_e) / (1 - pool_ret * pool_e)   # D198
    C_peak = pool_ret * C_start + pool_b                                 # D199
    CO2_cyc = C_peak * phi(pool_x) + D_raw * psi(pool_x)                 # D200
    CO2aqc = min(C_sat, max(C_air, CO2_cyc)) / 1000                      # D162, mol/L

    # ------------------------------------------------------------------
    # pH -- activity-corrected charge balance (Chemistry D50:D100, D103, D185-D197, D220).
    # The grid + linear interpolation is reproduced exactly (0.1 pH steps, 4.0 to 9.0),
    # not replaced by a root-find, because the workbook ships the grid.
    # ------------------------------------------------------------------
    def _resid(pH):
        h = 10 ** -pH
        return (SID + NT * h / (h + KN) + h
                - (PT * K1p * h ** 2 + 2 * PT * K1p * K2p * h + 3 * PT * K1p * K2p * K3p)
                / (h ** 3 + K1p * h ** 2 + K1p * K2p * h + K1p * K2p * K3p)
                - K1c * CO2aqc / h - 2 * K1c * K2c * CO2aqc / h ** 2 - Kw / h)

    grid = [4.0 + 0.1 * i for i in range(51)]
    res = [_resid(x) for x in grid]
    pH_op, n_cross = 0.0, 0
    for i in range(50):
        if res[i] >= 0 and res[i + 1] < 0:
            pH_op += grid[i] + 0.1 * res[i] / (res[i] - res[i + 1])
            n_cross += 1
    pH_meas = (pH_op - math.log10(g1)) if n_cross == 1 else NAN          # D220
    pKa2p_c = -math.log10(K2p)
    pKa_NH4 = -math.log10(KN)

    # --- local-pH (buffer) verdict at the anode (Chemistry D214-D219) ---
    j_anode = I_app * 1000 / A_wet                                       # Echem D48 mA/cm2
    j_cathode = I_app * 1000 / A_cath                                    # Echem D49 mA/cm2
    if n_cross == 1:
        C_HPO4 = PT / (1 + 10 ** (pKa2p_c - pH_op))                      # D253 (pH_op, concentration scale)
        C_HCO3 = K1c * CO2aqc / 10 ** -pH_op                             # D252
        km_HPO4 = p['km_O2'] * (p['D_HPO4'] / D_O2) ** p['km_exp']       # D275 cm/s
        km_HCO3 = p['km_O2'] * (D_HCO3 / D_O2) ** p['km_exp']            # D276 cm/s
        j_buffer_lim = (p['F'] * ((km_HPO4 / 100) * C_HPO4 + (km_HCO3 / 100) * C_HCO3) * 1000
                        / 10)                                            # D216 mA/cm2, phosphate + bicarbonate
        j_buffer_ratio = j_anode / j_buffer_lim
    else:
        j_buffer_lim = j_buffer_ratio = NAN

    # --- conductivity and the cell-voltage budget (Chemistry D177-D180, Echem D106-D119) ---
    kappa = kappa0 * p['kappa_fI'] * (1 + p['kappa_TC'] * (T_K - 298.15))
    R_cell = (p['k_geom'] * math.acosh(p['elec_gap'] / eg['a_d'])
              / (PI * kappa * (L_sub / 1000)))                           # D117
    V_IR = I_app * R_cell                                                # D118
    eta_a = p['b_anode'] * math.log10(j_anode / 1000 / p['j0_anode'])     # D111
    eta_c = p['b_cath'] * math.log10(j_cathode / 1000 / p['j0_cath'])     # D112, cathode density D49
    pcet_op = 0.0 if (n_cross == 1 and j_buffer_ratio > 1) else p['pcet_credit']   # Echem D162: credit withdrawn past the buffer limit
    V_cell = p['E0_OER'] + eta_a + eta_c + pcet_op + V_IR                 # D119

    # --- peroxide (Echem D93-D98) ---
    r_H2O2 = (p['f_HOOH'] * I_app * (1 - etaF) / (n_ORR_eff * p['F'])
              * p['M_H2O2'] * 1000 * 3600 / (V_charge / 1000))           # D93
    H2O2_ss = r_H2O2 / (p['k_cat_cells'] * 3600)                         # D95, growing culture
    k_anode = (p['km_O2'] / 100) * (A_wet / 10000) / (V_charge / 1e6)   # D151, 1/s: peroxide re-oxidised at the anode
    DO_lag = hs['Lag']['DO_avg']                                         # D150 = MT D135 = DO_avg_l, mol/m3
    r_H2O2_lag = r_H2O2 * DO_lag / DO_design                             # D152
    H2O2_lag_1h = (r_H2O2_lag / (k_anode * 3600) * (1 - math.exp(-k_anode * 3600)))   # D96, no biomass

    # --- dissolved CO2 / H2 diagnostics ---
    carbon_margin = CO2aqc * 1000 * 1000 / p['Km_CO2']
    carbon_margin_trough = C_start * 1000 / p['Km_CO2']                  # Biology D98 = Summary D41
    C_H2 = H_H2_T * p['P_atm']
    t_H2_sat = C_H2 * V_L / rH2 * 60 if rH2 > 0 else INF
    CO2_sd = (CO2_supply / CO2_cons) if CO2_cons > 0 else NAN
    CO2_uptake = ((C_peak - C_start) * V_L_CO2 * (60 / spg_int) / CO2_cons) if CO2_cons > 0 else NAN   # MT D417

    # --- chlorine chain (Chemistry D131-D149), now driven by THIS pH, not a cached one ---
    if n_cross == 1:
        NH3_free = NT / (1 + 10 ** (pKa_NH4 - pH_op))                    # D138
        P_HOCl = I_Cl / (2 * p['F'] * (V_charge / 1000))                 # D134, n_e_Cl = 2
        HOCl_mgL = P_HOCl / (p['k1_NH2Cl'] * NH3_free) * M_HOCl
        NH2Cl = min(Cl_M * M_HOCl * kt / (1 + kt),
                    CL_PER_N * NT * MW_N * M_HOCl / M_Cl2)               # D143, pool depletes as it turns over
        C_eff = p['f_local'] * HOCl_mgL + NH2Cl / p['R_chloramine']      # D145
    else:
        NH3_free = HOCl_mgL = NH2Cl = C_eff = NAN

    return dict(
        spg_dur=spg_dur, spg_int_opt=spg_int, spg_int_opt_s=spg_int * 60,
        spg_int_DO=spg_int_DO, spg_int_carbon=spg_int_carbon, spg_int_max=spg_int_max,
        duty_DO=duty_DO, duty_actual=duty_actual, duty_opt=duty_opt,
        opt_binding=opt_binding, spg_int_regime=regime, feasible=feasible,
        DO_target=DO_target, DO_surf_excess=DO_surf_excess,
        DO_surf_excess_lag=DO_surf_excess_lag, DO_hs_floor=DO_hs_floor,
        y_O2_star=y_O2_star, y_O2_actual=y_O2_actual,
        DO_ss=DO_ss, DO_ss_lag=DO_ss_lag, kLa_surf_req=kLa_surf_req,
        DO_peak=DO_peak, DO_ss_g=DO_ss_g, DO_peak_g=DO_peak_g, DO_peak_lag=DO_peak_lag,
        saw_factor=saw_factor, F_vent_ex=F_ex, k_vent=k_vent, y_H2_lag=y_H2_lag,
        pool_b=pool_b, C_start=C_start,
        kL_surf_crit=kL_surf_crit, kLa_surf_used=kLa_surf_used, do_margin=do_margin,
        t_O2_ceiling_lag=t_lag, O2_removal_ratio=removal_ratio, surf_ratio=surf_ratio,
        strip_ratio=strip_ratio, O2_excess=O2_excess, O2_net=O2_net, rH2=rH2, O2_net_lag=O2_net_lag, rH2_lag=rH2_lag,
        etaF_calc=etaF_calc, etaF_calc_min=etaF_calc_min, etaF_OER_calc=etaF_OER_calc,
        i_ORR_design=i_ORR, D_O2=D_O2, sigma=sigma, rho_L=rho_L,
        CO2_cyc_avg_new=CO2_cyc, CO2aqc=CO2aqc, CO2_supply=CO2_supply, CO2_sd=CO2_sd,
        pool_beta_ratio=pool_beta_ratio, carbon_margin=carbon_margin,
        carbon_margin_trough=carbon_margin_trough, k_Cl_turn=k_Cl_turn,
        spg_dur_run=spg_dur_run, spg_int_run=spg_int_run, r_H2O2_lag=r_H2O2_lag, n_ORR_eff=n_ORR_eff, t_H2_sat=t_H2_sat,
        pH_meas=pH_meas, pH_op=pH_op, n_cross=n_cross,
        j_anode=j_anode, j_buffer_lim=j_buffer_lim, j_buffer_ratio=j_buffer_ratio,
        kappa=kappa, R_cell=R_cell, V_IR=V_IR, V_cell_est=V_cell,
        r_H2O2=r_H2O2, H2O2_ss=H2O2_ss, H2O2_lag_1h=H2O2_lag_1h, C_eff=C_eff,
        C_eff_Cl2=C_eff * M_Cl2 / M_HOCl,
        Q_CO2_fit=Q_fit, pulse_V0=V0, spg_dur_eq_opt=spg_dur_eq_opt, V_pulse=V_pulse, DIC_cap=DIC_cap,
        P_dry=P_dry, f_salt_O2=f_salt_O2, pcet_credit_op=pcet_op, CO2_uptake=CO2_uptake, C_sat_CO2=C_sat,
    )


# ---------------------------------------------------------------------------
# (input, low, high, tier).  tiers: DATA-GAP, ESTIMATE, LITERATURE, KNOB
# EVERY range must bracket its own BASE value (asserted at runtime below); a sweep that
# does not straddle the live operating point cannot say anything about it.
#
# DROPPED in this re-base: etaF and etaF_OER (now calculated -- km_O2, km_Cl, z_e_ORR and
# corr_I_frac drive them instead); D_O2, sigma and rho_L as free inputs (now temperature-
# tracking -- D_O2_fit carries the correlation's own uncertainty); u_g_max (never read by
# the model, so its "sweep" only ever printed zeros).
# ---------------------------------------------------------------------------
SWEEP = [
 # ---- DATA-GAP (unmeasured) ----
 ('kL_surf_factor', 0.25, 4.0, 'DATA-GAP'),     # surface kLa is a coarse proxy: ~375 %
 ('Q_vent', 0.1, 2.0, 'DATA-GAP'),              # 'Air exchange' total air ingress; inert under the default 'Open vent' (see the four-combination block)
 ('Q_backdraw', 0.005, 0.15, 'DATA-GAP'),       # 'Open vent' back-draw air; schedule-dependent, measure
 ('elec_gap', 10.0, 20.0, 'DATA-GAP'),          # measure with calipers
 ('j0_anode', 1e-11, 1e-9, 'DATA-GAP'),         # OER on Pt spans +/-1 decade about 1e-10
 ('corr_I_frac', 0.0, 0.10, 'DATA-GAP'),        # 0 is the floor, so base sits at lo
 ('k_cat_cells', 0.001, 0.01, 'DATA-GAP'),      # whole-culture catalase clearance
 ('tau_NH2Cl', 1 / 60, 5.0, 'DATA-GAP'),    # chloramine lifetime: sets the free chloride share, hence the O2 surplus
 ('bio_O2', 1.6, 2.4, 'DATA-GAP'),
 ('bio_CO2', 0.8, 1.3, 'DATA-GAP'),
 ('pulse_floor', 0.2, 1.0, 'DATA-GAP'),
 ('pulse_V0_factor', 0.0, 2.0, 'DATA-GAP'),     # valve-opening intercept V0 of the pulse-volume fit; 0 = the old proportional model
 # ---- ESTIMATE ----
 ('km_O2', 0.002, 0.006, 'ESTIMATE'),           # ETW at 10-40 cm/s swirl past the rod
 ('f_HOOH', 0.10, 0.20, 'ESTIMATE'),            # Le Bozec 2001 peroxide selectivity band
 ('z_e_ORR', 2, 4, 'ESTIMATE'),                 # 2 is the physical floor, so base at lo
 ('k_geom', 1.0, 3.0, 'ESTIMATE'),              # cell-constant correction
 ('kappa_fI', 0.66, 0.90, 'ESTIMATE'),          # Kohlrausch finite-strength factor +/-15 %
 ('pcet_credit', -0.20, -0.10, 'ESTIMATE'),     # phosphate PCET credit, 100-200 mV
 ('b_anode', 0.06, 0.12, 'ESTIMATE'),           # 60 mV/dec buffered .. 120 bare; base at hi
 ('b_cath', 0.13, 0.15, 'ESTIMATE'),
 ('j0_cath', 1e-6, 2e-6, 'ESTIMATE'),
 ('O2_ceil_atm', 0.25, 0.35, 'ESTIMATE'),
 ('ks_O2', 0.07, 0.21, 'ESTIMATE'),              # O2 salting-out coefficient, +/-50 %
 ('vial_wall', 0.9, 1.3, 'ESTIMATE'),
 ('Km_CO2', 20, 80, 'ESTIMATE'),
 ('gerrit_slope', 0.95, 1.11, 'ESTIMATE'),      # empirical rig fit +/-8 %
 ('gerrit_int', 2.2, 3.0, 'ESTIMATE'),
 ('V_max', 14, 18, 'ESTIMATE'),
 ('FE_CER', 0.2, 0.8, 'ESTIMATE'),
 # ---- LITERATURE (well-known) ----
 ('D_O2_fit', 0.92, 1.08, 'LITERATURE'),        # Han & Bartels correlation scatter
 ('H_O2ref', 1.10e-5, 1.30e-5, 'LITERATURE'),
 ('H_O2T', 1275, 1725, 'LITERATURE'),           # temperature dependence relative to T_ref = 25 C
 ('H_CO2ref', 3.05e-4, 3.55e-4, 'LITERATURE'),
 ('H_H2ref', 7.2e-6, 8.4e-6, 'LITERATURE'),
 ('Ea_D_CO2', 15000.0, 23000.0, 'LITERATURE'),
 ('kappa_TC', 0.019, 0.022, 'LITERATURE'),      # ISO 7888 conductivity compensation
 ('E0_OER', 1.228, 1.230, 'LITERATURE'),
 ('mend_a', 2.03, 2.25, 'LITERATURE'),
 ('mend_b', 0.48, 0.53, 'LITERATURE'),
 # ---- KNOB (you set it) ----
 ('intensity', 3, 25, 'KNOB'),                  # gerrit_min..gerrit_max; base at the floor
 ('Q_CO2', 100, 300, 'KNOB'),
 ('target_DO_frac', 0.10, 0.60, 'KNOB'),        # re-ranged: base is now 0.261, not 0.5
 ('carbon_margin_min', 1.5, 3.0, 'KNOB'),
 ('flush_factor', 0.5, 2.0, 'KNOB'),
 ('stir_rpm', 125, 1500, 'KNOB'),               # 125 = the documented stall floor
 ('T_C', 20, 37, 'KNOB'),                       # brackets the 30 C workbook baseline
]

# Outputs that decide whether we reach growth / what schedule to run.
# pH and cell voltage are reported in NATURAL units, not per cent: a percentage change in
# a logarithmic quantity is meaningless, and a percentage of a voltage hides how close the
# rail is. For the urgency SCORE they are normalised -- pH against the 1.0-unit HOB band
# (6.5-7.5), voltage against its own baseline.
CRITICAL = ['spg_int_opt', 'DO_ss', 'pH_meas', 'r_H2O2', 'V_cell_est', 't_O2_ceiling_lag']
ABSOLUTE_OUT = {'pH_meas': 1.0, 'V_cell_est': None}   # None => score as % of baseline
WEIGHT = {'DATA-GAP': 1.0, 'ESTIMATE': 0.6, 'LITERATURE': 0.15, 'KNOB': 0.0}

# Baseline model keys checked against the workbook's cached (Excel-computed) cells, read
# at run time. (model key, label, sheet, cell). If any stops matching, this script has
# drifted -- re-base it, do not adjust the tolerance.
SELF_CHECK = [
    ('D_O2',            'D_O2 (m2/s)',              'Mass Transfer',    'D32'),
    ('kLa_surf_used',   'kLa_surf_used (1/s)',      'Mass Transfer',    'D98'),
    ('etaF_calc',       'etaF_calc (-)',            'Electrochemistry', 'D88'),
    ('DO_target',       'DO_target (mol/m3)',       'Mass Transfer',    'D179'),
    ('DO_surf_excess',  'DO_surf_excess (mol/m3)',  'Mass Transfer',    'D180'),
    ('y_O2_star',       'y_O2_star (-)',            'Mass Transfer',    'D183'),
    ('duty_DO',         'duty_DO (-)',              'Mass Transfer',    'D184'),
    ('spg_int_DO',      'spg_int_DO (min)',         'Mass Transfer',    'D185'),
    ('spg_int_opt',     'spg_int_opt (min)',        'Mass Transfer',    'D91'),
    ('spg_int_carbon',  'spg_int_carbon (min)',     'Mass Transfer',    'D112'),
    ('kLa_surf_req',    'kLa_surf_req (1/s)',       'Mass Transfer',    'D186'),
    ('DO_ss',           'DO_ss (mg/L)',             'Mass Transfer',    'D108'),
    ('V_cell_est',      'V_cell_est (V)',           'Electrochemistry', 'D119'),
    ('r_H2O2',          'r_H2O2 (mg/L/h)',          'Electrochemistry', 'D93'),
    ('CO2_cyc_avg_new', 'CO2_cyc_avg_new (mol/m3)', 'Mass Transfer',    'D200'),
    ('pH_meas',         'pH_meas (-)',              'Chemistry',        'D220'),
    ('j_buffer_ratio',  'j_buffer_ratio (-)',       'Chemistry',        'D218'),
    ('C_eff_Cl2',       'C_eff_Cl2 (mg/L)',         'Summary',          'D36'),
    ('n_ORR_eff',       'n_ORR_eff (e-/O2)',        'Electrochemistry', 'D141'),
    ('H2O2_lag_1h',     'H2O2_lag_1h (mg/L)',       'Electrochemistry', 'D96'),
    ('k_Cl_turn',       'k_Cl_turn (1/s)',          'Chemistry',        'D271'),
    ('j_buffer_lim',    'j_buffer_lim (mA/cm2)',    'Chemistry',        'D216'),
    ('carbon_margin_trough', 'carbon margin at trough (x)', 'Summary',  'D41'),
    ('spg_dur_run',     'spg_dur_run (s)',          'Mass Transfer',    'D242'),
    ('spg_int_run',     'spg_int_run (min)',        'Summary',          'D16'),
    ('saw_factor',      'saw_factor (-)',           'Mass Transfer',    'D322'),
    ('F_vent_ex',       'F_vent_ex (mol/h)',        'Mass Transfer',    'D308'),
    ('y_O2_actual',     'y_O2_actual (-)',          'Mass Transfer',    'D187'),
    ('k_vent',          'k_vent (1/s)',             'Mass Transfer',    'D143'),
    ('pool_b',          'pool_b (mol/m3)',          'Mass Transfer',    'D194'),
    ('C_start',         'C_cycle_start (mol/m3)',   'Mass Transfer',    'D198'),
    ('DO_peak',         'DO_peak sizing (mg/L)',    'Summary',          'D115'),
    ('DO_ss_lag',       'DO cycle-mean lag (mg/L)', 'Summary',          'D116'),
    ('DO_peak_lag',     'DO peak lag (mg/L)',       'Summary',          'D117'),
    ('y_H2_lag',        'y_H2 lag (-)',             'Biology',          'D84'),
    ('O2_net_lag',      'O2_net_lag (mol/h)',       'Electrochemistry', 'D132'),
    ('rH2_lag',         'rH2_lag (mol/h)',          'Electrochemistry', 'D133'),
    ('Q_CO2_fit',       'Q_CO2_fit (mL/s)',         'Mass Transfer',    'D407'),
    ('pulse_V0',        'pulse_V0 (mL)',            'Mass Transfer',    'D408'),
    ('spg_dur',         'spg_dur_opt (s)',          'Mass Transfer',    'D90'),
    ('spg_dur_eq_opt',  'spg_dur_eq_opt (s)',       'Mass Transfer',    'D409'),
    ('V_pulse',         'V_pulse (mL)',             'Mass Transfer',    'D411'),
    ('DIC_cap',         'DIC_cap (-)',              'Chemistry',        'D296'),
    ('P_dry',           'P_dry (Pa)',               'Mass Transfer',    'D418'),
    ('C_sat_CO2',       'C_sat_CO2 (mol/m3)',       'Mass Transfer',    'D145'),
    ('f_salt_O2',       'f_salt_O2 (-)',            'Biology',          'D123'),
    ('pcet_credit_op',  'pcet_credit_op (V)',       'Electrochemistry', 'D162'),
    ('CO2_uptake',      'CO2_uptake_ratio (x)',     'Mass Transfer',    'D417'),
    ('duty_actual',     'duty_actual (-)',          'Mass Transfer',    'D93'),
]

# BASE inputs vs the workbook (Summary selectors D2:D10 and the cells they feed).
# (label, sheet, cell, value declared by this script). D9 / D10 are blank on Summary, so
# the effective volume and pressure are checked on the cells that resolve them.
SELECTORS = dict(reactor='ed04', electrode='MMO tube', organism='Xanthobacter tagetidis',
                 media='AMYBO03')
BASE['media'] = SELECTORS['media']
BASE['electrode'] = SELECTORS['electrode']                               # Summary D3 drives the electrode tables
BASE['z_e_ORR'] = ELECTRODE[SELECTORS['electrode']]['z_e_ORR']           # Echem D27
INPUT_CELLS = [
    ('Reactor_sel',   'Summary', 'D2', SELECTORS['reactor']),
    ('electrode_sel', 'Summary', 'D3', SELECTORS['electrode']),
    ('organism_sel',  'Summary', 'D4', SELECTORS['organism']),
    ('media_sel',     'Summary', 'D5', SELECTORS['media']),
    ('intensity',     'Summary', 'D6', BASE['intensity']),
    ('stir_rpm',      'Summary', 'D7', BASE['stir_rpm']),
    ('T_C',           'Summary', 'D8', BASE['T_C']),
    ('media_volume',  'Summary', 'D9', None),     # blank -> recommended fill (V_max etc.)
    ('P_atm_set',     'Summary', 'D10', None),    # blank -> 101325 Pa default
    ('vent_model',    'Summary', 'D111', BASE['vent_model']),
    ('O2_phase',      'Summary', 'D112', BASE['O2_phase']),
    ('V_max',         'Geometry', 'D23', BASE['V_max']),
    ('V_vial_total',  'Geometry', 'D24', BASE['V_vial_total']),
    ('D_int',         'Geometry', 'D22', BASE['D_int']),
    ('gerrit_slope',  'Electrochemistry', 'D11', BASE['gerrit_slope']),
    ('gerrit_int',    'Electrochemistry', 'D12', BASE['gerrit_int']),
    ('P_atm',         'Biology', 'D19', BASE['P_atm']),
    ('Q_CO2',         'Mass Transfer', 'D102', BASE['Q_CO2']),
]


# ---------------------------------------------------------------------------
# Minimal read-only .xlsx reader (standard library): the value Excel CACHED for a cell.
# ---------------------------------------------------------------------------
WORKBOOK_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "electroPioreactorGasModel.xlsx")
_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_RNS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
NO_CACHE = object()      # formula cell with no stored result
ABSENT = object()        # cell not present / empty


def _read_workbook(path):
    """-> {sheet name: {cell ref: float | str | NO_CACHE | ABSENT-less}}; errors stay str."""
    with zipfile.ZipFile(path) as z:
        rels = {r.get("Id"): r.get("Target")
                for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            shared = ["".join(t.text or "" for t in si.iter(_NS + "t"))
                      for si in ET.fromstring(z.read("xl/sharedStrings.xml"))]
        out = {}
        for sh in ET.fromstring(z.read("xl/workbook.xml")).iter(_NS + "sheet"):
            target = rels[sh.get(_RNS + "id")].lstrip("/")
            part = target if target.startswith("xl/") else "xl/" + target
            cells = {}
            for c in ET.fromstring(z.read(part)).iter(_NS + "c"):
                t, v = c.get("t"), c.find(_NS + "v")
                if t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter(_NS + "t"))
                elif v is None or v.text is None:
                    val = NO_CACHE if c.find(_NS + "f") is not None else ABSENT
                elif t == "s":
                    val = shared[int(v.text)]
                elif t in ("str", "e"):
                    val = v.text                      # t="e": '#N/A', '#VALUE!', ...
                else:
                    try:
                        val = float(v.text)
                    except ValueError:
                        val = v.text
                cells[c.get("r")] = val
            out[sh.get("name")] = cells
    return out


def _cell(wb, sheet, ref):
    return wb.get(sheet, {}).get(ref, ABSENT)


def _fmt(v):
    return ("no cached value" if v is NO_CACHE else "absent" if v is ABSENT
            else f"{v:.10g}" if isinstance(v, float) else repr(v))


def run(name, val):
    p = dict(BASE)
    p[name] = val
    return model(p)


# --- runtime guard 1: every sweep must bracket its own baseline ------------------
_bad = [(n, lo, hi, BASE[n]) for n, lo, hi, _t in SWEEP if not (lo <= BASE[n] <= hi)]
if _bad:
    raise SystemExit("SWEEP RANGE ERROR - baseline outside its own sweep range:\n" +
                     "\n".join(f"   {n}: base={b} not in [{lo}, {hi}]" for n, lo, hi, b in _bad) +
                     "\nWiden the range (or re-base BASE to the workbook) before trusting any output.")
_missing = [n for n, _lo, _hi, _t in SWEEP if n not in BASE]
if _missing:
    raise SystemExit(f"SWEEP RANGE ERROR - swept input not in BASE: {_missing}")

# --- runtime guard 2: BASE inputs must equal the workbook's, before anything runs ---
try:
    _wb = _read_workbook(WORKBOOK_PATH)
except (OSError, KeyError, zipfile.BadZipFile, ET.ParseError) as _e:
    raise SystemExit(f"CANNOT READ WORKBOOK {WORKBOOK_PATH}: {_e!r}")


def _input_ok(declared, book):
    if declared is None:                       # blank selector: workbook must be blank too
        return book is ABSENT or book == ""
    if isinstance(declared, str):
        return isinstance(book, str) and book.strip() == declared
    return isinstance(book, float) and abs(declared - book) <= 1e-9 * max(1.0, abs(book))


_drift = [(n, f"{sh}!{ref}", d, _cell(_wb, sh, ref)) for n, sh, ref, d in INPUT_CELLS
          if not _input_ok(d, _cell(_wb, sh, ref))]
if _drift:
    print("INPUT DRIFT - this script's BASE inputs differ from the workbook "
          "(Summary D2:D10, D111:D112 and dependants):")
    for n, where, d, bk in _drift:
        print(f"   {n:14} {where:26} script={_fmt(d) if d is not None else 'blank'}  "
              f"workbook={_fmt(bk)}")
    print("   Re-base BASE (or restore the workbook selectors); no analysis was run.")
    sys.exit(1)

b = model(BASE)

# --- runtime guard 3: the baseline must still reproduce the workbook's cached values ---
_fails, _checked = [], []
for k, lab, sh, ref in SELF_CHECK:
    v = _cell(_wb, sh, ref)
    _checked.append(f"{sh}!{ref}")
    if not isinstance(v, float):
        _fails.append(f"   {lab}: this={b[k]:.6g}  workbook {sh}!{ref}={_fmt(v)}"
                      + ("" if v is not NO_CACHE else "  (no cached value)"))
    elif not (abs(b[k] - v) <= 5e-5 * abs(v)):
        _fails.append(f"   {lab}: this={b[k]:.6g}  workbook {sh}!{ref}={v:.6g}")

print("=" * 100)
print(f"BASELINE - workbook live state: {SELECTORS['reactor']} / {SELECTORS['electrode']} / "
      f"{SELECTORS['organism']} / {SELECTORS['media']},")
print(f"           vent model '{BASE['vent_model']}', O2 sized on the {BASE['O2_phase']} phase,")
print(f"           LED {BASE['intensity']}%, stir {BASE['stir_rpm']} rpm, T {BASE['T_C']} C, "
      f"{ELECTRODE[SELECTORS['electrode']]['sparger'].lower()} sparger, Q_CO2 = {BASE['Q_CO2']} mL/min (ed04 calibration)")
print("=" * 100)
for k, unit in [('spg_dur', 's'), ('spg_int_opt', 'min'), ('spg_int_opt_s', 's'),
                ('spg_int_DO', 'min'), ('spg_int_carbon', 'min'), ('spg_int_max', 'min'),
                ('duty_actual', '-'), ('DO_target', 'mol/m3'),
                ('DO_surf_excess', 'mol/m3'), ('DO_hs_floor', 'mol/m3'),
                ('y_O2_star', '-'), ('y_O2_actual', '-'),
                ('saw_factor', '-'), ('F_vent_ex', 'mol/h'), ('k_vent', '1/s'),
                ('DO_ss', 'mg/L'), ('DO_peak', 'mg/L'), ('DO_ss_lag', 'mg/L'), ('DO_peak_lag', 'mg/L'),
                ('kLa_surf_used', '1/s'), ('kLa_surf_req', '1/s'), ('kL_surf_crit', 'm/s'),
                ('t_O2_ceiling_lag', 'min'), ('O2_removal_ratio', 'x'), ('surf_ratio', 'x'),
                ('t_H2_sat', 'min'), ('carbon_margin', 'x'), ('carbon_margin_trough', 'x'), ('CO2_sd', 'x'),
                ('CO2_cyc_avg_new', 'mol/m3'), ('pH_meas', '-'),
                ('etaF_calc', '-'), ('etaF_OER_calc', '-'),
                ('kappa', 'S/m'), ('R_cell', 'ohm'), ('V_IR', 'V'), ('V_cell_est', 'V'),
                ('r_H2O2', 'mg/L/h'), ('H2O2_ss', 'mg/L'), ('C_eff', 'mg/L as HOCl'), ('C_eff_Cl2', 'mg/L as Cl2'),
                ('j_anode', 'mA/cm2'), ('j_buffer_ratio', '-'), ('pool_beta_ratio', 'x')]:
    print(f"   {k:18}= {b[k]:>12.6g}  {unit}")
print(f"   {'opt_binding':18}= {b['opt_binding']}")
print(f"   {'DO feasibility':18}= margin x{b['do_margin']:.3f} "
      f"(kLa_surf_used / kLa_surf_req; < 1 => DO target unreachable at ANY interval)")
print(f"   => recommended schedule: {b['spg_dur']:.3g}s pulse every {b['spg_int_opt_s']:.0f}s "
      f"(~{b['spg_int_opt']:.1f} min)")
if _fails:
    print("\n!! WORKBOOK MISMATCH - this script has drifted from electroPioreactorGasModel.xlsx:")
    print("\n".join(_fails))
    raise SystemExit("Re-base BASE / model() against the workbook before using any number below.")
else:
    print(f"      self-check: all {len(SELF_CHECK)} baseline values reproduce the workbook "
          "cached values (rel tol 5e-5); inputs match Summary D2:D10, D111:D112")
    print("      cells checked: " + ", ".join(_checked))

# ============================================================================
# HEADSPACE SELECTORS -- the headline in all four vent-model / sizing-phase states.
#   The workbook caches only ONE selector state, so the live default is checked against
#   the workbook's own cached Summary D15 / D35 / D38. The three other states cannot be
#   recalculated here, so they are checked against the TWIN (electroPioreactorGasModel.py,
#   beside this script): it is an independent, full cell-by-cell implementation of the same
#   workbook, evaluated at the same selector state (its two selector lines are overridden in
#   a private copy of its source). Reduced model vs twin, tolerance 0.5 %.
# ============================================================================
TWIN_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "electroPioreactorGasModel.py")


def _twin_state(vent_model, O2_phase):
    """(Summary D15, D35, D38) from the full twin run at the given selector state."""
    with open(TWIN_PATH, encoding="utf-8") as fh:
        src = fh.read()
    src, n1 = re.subn(r'(?m)^vent_model_sel\s*=\s*"[^"]*"', f'vent_model_sel = "{vent_model}"', src)
    src, n2 = re.subn(r'(?m)^O2_phase_sel\s*=\s*"[^"]*"', f'O2_phase_sel = "{O2_phase}"', src)
    if (n1, n2) != (1, 1):
        raise SystemExit("CANNOT OVERRIDE THE TWIN'S SELECTORS - re-base _twin_state() against "
                         "electroPioreactorGasModel.py")
    ns = {"__name__": "twin_combo", "__file__": TWIN_PATH}
    exec(compile(src, TWIN_PATH, "exec"), ns)
    return (ns["S_D15"], ns["S_D35"], ns["S_D38"])


_live = (BASE['vent_model'], BASE['O2_phase'])
COMBO_REF = {}      # (vent_model, O2_phase) -> (reference triple, where it came from)
for _k in (('Open vent', 'Growth'), ('Outflow only', 'Growth'),
           ('Air exchange', 'Growth'), ('Open vent', 'Lag')):
    if _k == _live:
        _lv = tuple(_cell(_wb, 'Summary', r) for r in ('D15', 'D35', 'D38'))
        COMBO_REF[_k] = (_lv if all(isinstance(v, float) for v in _lv) else None, "workbook")
    else:
        _tw = _twin_state(*_k)
        COMBO_REF[_k] = (_tw if all(isinstance(v, float) for v in _tw) else None, "twin")
print("\n" + "=" * 100)
print("HEADSPACE SELECTORS -- headline in all four vent-model / sizing-phase states")
print("   reference: live state = workbook cached D15/D35/D38; the other three = the full twin")
print(f"{'vent_model':14}{'O2 phase':9}{'interval min':>14}{'pH':>8}{'DO mg/L':>9}"
      f"{'DO peak':>9}{'binding':>16}   vs reference (0.5 %)")
_combo_fail = []
for _vm, _ph in (('Open vent', 'Growth'), ('Outflow only', 'Growth'),
                 ('Air exchange', 'Growth'), ('Open vent', 'Lag')):
    _q = dict(BASE, vent_model=_vm, O2_phase=_ph)
    _r = model(_q)
    _x, _src = COMBO_REF[(_vm, _ph)]
    _got = (_r['spg_int_opt'], _r['pH_meas'], _r['DO_ss'])
    if _x is None:
        _v = f"no {_src} value"
        _combo_fail.append((_vm, _ph, 'missing'))
    else:
        _bad = [n for n, g, e in zip(('interval', 'pH', 'DO'), _got, _x)
                if not abs(g - e) <= 5e-3 * abs(e)]
        _dev = max(abs(g - e) / abs(e) for g, e in zip(_got, _x))
        _v = (f"OK vs {_src} (max dev {_dev * 100:.3f} %)" if not _bad else
              f"MISMATCH vs {_src} " + ",".join(_bad) + f" ({_x[0]:.4g} / {_x[1]:.4g} / {_x[2]:.4g})")
        if _bad:
            _combo_fail.append((_vm, _ph, _bad))
    _tag = " (live)" if (_vm, _ph) == _live else ""
    print(f"{_vm:14}{_ph:9}{_got[0]:>14.4f}{_got[1]:>8.4f}{_got[2]:>9.4f}{_r['DO_peak']:>9.3f}"
          f"{_r['opt_binding'].split(' ')[0]:>16}   {_v}{_tag}")
print("      four-combination check: " + ("all 4 states agree within 0.5 % (live vs workbook, other three vs twin)"
      if not _combo_fail else f"{len(_combo_fail)} FAILED: {_combo_fail}"))
if _combo_fail:
    raise SystemExit("Four-combination verification failed; no sensitivity analysis was run.")

# ============================================================================
# INFEASIBILITY CLIFF -- the single biggest non-linearity in the revised model.
#   Mass Transfer D182 is  hs_O2_allow = DO_target - DO_surf_excess.
#   When that goes <= 0, y_O2_star, duty_DO and spg_int_DO all go #N/A, D91 falls back to
#   the lag-accumulation cap, and D134 says the DO target is unreachable at ANY interval.
#   Equivalently: kLa_surf_used < kLa_surf_req. The margin below is the ratio of the two.
#   This is not a percentage effect. It is a cliff, and it is worth knowing which way each
#   input walks you toward it BEFORE the rig runs.
# ============================================================================
N_SCAN = 81


def _scan(name, lo, hi):
    """Sample the range; return (min margin, crossing value or None, direction)."""
    xs = [lo + (hi - lo) * i / (N_SCAN - 1) for i in range(N_SCAN)]
    res = [(x, run(name, x)) for x in xs]
    margins = [r['do_margin'] for _x, r in res]
    finite = [m for m in margins if not math.isinf(m) and not math.isnan(m)]
    min_margin = min(finite) if finite else INF
    feas = [r['feasible'] for _x, r in res]
    cross, direction = None, ''
    if len(set(feas)) > 1:
        for i in range(len(res) - 1):
            if feas[i] != feas[i + 1]:
                a, c = res[i][0], res[i + 1][0]
                for _ in range(60):
                    mid = (a + c) / 2
                    if run(name, mid)['feasible'] == feas[i]:
                        a = mid
                    else:
                        c = mid
                cross = (a + c) / 2
                direction = 'below' if feas[i + 1] else 'above'
                break
    return min_margin, cross, direction


SCAN = {name: _scan(name, lo, hi) for name, lo, hi, _t in SWEEP}

print("\n" + "=" * 100)
print("INFEASIBILITY CLIFF -- inputs that push DO_surf_excess above DO_target")
print(f"   baseline margin x{b['do_margin']:.3f}  "
      f"(kLa_surf_used {b['kLa_surf_used']:.4g} / kLa_surf_req {b['kLa_surf_req']:.4g} 1/s)")
print(f"   the surface coefficient behind that margin is UNMEASURED: kL_surf must exceed "
      f"kL_surf_crit = {b['kL_surf_crit']:.4g} m/s")
_cliff = [(n, t, SCAN[n][1], SCAN[n][2]) for n, _lo, _hi, t in SWEEP if SCAN[n][1] is not None]
if _cliff:
    for name, tier, cross, direction in _cliff:
        lo, hi = next((l, h) for n, l, h, _t in SWEEP if n == name)
        r_at = run(name, hi if direction == 'above' else lo)
        print(f"   CLIFF: {name} ({tier}) -- DO target becomes UNREACHABLE {direction} "
              f"{name} = {cross:.4g}")
        print(f"          swept {lo:g}..{hi:g}, baseline {BASE[name]:g}, "
              f"headroom x{abs(cross / BASE[name]) if BASE[name] else float('nan'):.2f} "
              f"from the live value")
        print(f"          past the cliff the schedule falls back to spg_int_max = "
              f"{r_at['spg_int_max']:.2f} min and DO_ss runs to {r_at['DO_ss']:.2f} mg/L")
else:
    print("   no single input reaches the cliff on its own over its swept range")
_near = sorted([(SCAN[n][0], n, t) for n, _lo, _hi, t in SWEEP
                if SCAN[n][1] is None and not math.isinf(SCAN[n][0]) and SCAN[n][0] < 1.6])
if _near:
    print("   nearest misses (margin stays > 1 at the sweep extreme, so no cliff on their")
    print("   own -- but these are the inputs that would reach it in COMBINATION):")
    for mm, n, t in _near:
        print(f"      {n:18} {t:10} min margin x{mm:.2f}")
print("   NOTE the cliff is one-sided in current: O2_excess is proportional to I_app, so")
print("   kLa_surf_req is too. Turning the LED up walks you straight at it.")

# ============================================================================
# LEVERAGE
# ============================================================================


def span(name, lo, hi, k):
    rl, rh = run(name, lo), run(name, hi)
    a, c = rl[k], rh[k]
    if any(isinstance(x, float) and (math.isnan(x) or math.isinf(x)) for x in (a, c)):
        return NAN
    if k in ABSOLUTE_OUT:
        return abs(c - a)                       # natural units
    base = b[k]
    return abs(c - a) / abs(base) * 100 if base else NAN


def score_of(name, lo, hi, sp, flips):
    """Normalise the critical spans onto one comparable scale for ranking."""
    vals = []
    for k in CRITICAL:
        if flips and k in ('spg_int_opt', 'DO_ss'):
            continue                            # cliff crossing: not a percentage
        v = sp[k]
        if math.isnan(v):
            continue
        if k == 'pH_meas':
            vals.append(v / ABSOLUTE_OUT[k] * 100)     # 1 pH unit = the whole HOB band
        elif k == 'V_cell_est':
            vals.append(v / abs(b[k]) * 100)
        else:
            vals.append(v)
    return max(vals or [0])


print("\n" + "=" * 100)
print("LEVERAGE -- change in each critical output across the input's plausible range")
print("   sched/DOss/H2O2/tO2lag are % of baseline; pH is |delta pH| in pH units;")
print("   Vcell is |delta V| in volts. A row whose sweep crosses the cliff has its")
print("   sched and DOss cells suppressed (CLIFF), because they compare two regimes.")
print(f"{'input':18}{'tier':10}{'sched%':>8}{'DOss%':>7}{'dpH':>7}{'H2O2%':>7}"
      f"{'dVcell':>8}{'tO2lag%':>9}{'minMargin':>11}")
rows = []
for name, lo, hi, tier in SWEEP:
    sp = {k: span(name, lo, hi, k) for k in CRITICAL}
    min_margin, cross, _dirn = SCAN[name]
    flips = cross is not None
    crit = score_of(name, lo, hi, sp, flips)
    rows.append((name, tier, sp, crit, flips, min_margin, cross))
for name, tier, sp, crit, flips, min_margin, cross in rows:
    def f(k, w=7, dp=0, _sp=sp):
        v = _sp[k]
        return f"{v:>{w}.{dp}f}" if not math.isnan(v) else " " * (w - 3) + "n/a"
    sched = "CLIFF" if flips else f('spg_int_opt', 8).strip()
    doss = "CLIF" if flips else f('DO_ss').strip()
    mm = "inf" if math.isinf(min_margin) else f"{min_margin:.2f}"
    print(f"{name:18}{tier:10}{sched:>8}{doss:>7}{f('pH_meas', 7, 2)}"
          f"{f('r_H2O2')}{f('V_cell_est', 8, 3)}{f('t_O2_ceiling_lag', 9)}{mm:>11}")
print("   Temperature coefficients vanish only at their reference temperature (25 C);"
      " at this 30 C baseline they contribute to the sensitivity.")
print("\n   TWO STRUCTURAL ZEROS -- read these before concluding an input is harmless:")
print("   * DO_ss (cycle mean) is PINNED near DO_target whenever the DO-limited interval")
print("     binds: the sizing puts the flux-mean headspace O2 at y*/saw_factor, so the")
print("     sawtooth mean lands on the target (slow-vent limit; 0.4-0.7 % under it).")
print("     Mostly only inputs that move DO_target (target_DO_frac, O2_ceil_atm, H_O2ref,")
print("     T_C) or the pulse size (saw_factor) can move it; the PEAK is not pinned.")
print("     Everything else shows DOss% = 0 because the schedule absorbs it, not because")
print("     the model is insensitive -- read the minMargin column for those.")
print("   * Q_CO2 cancels exactly (the fitted slope rescales with it). spg_dur goes as 1/Q_CO2 and duty_DO goes as 1/Q_CO2, so")
print("     the interval, the duty and the delivered CO2 are all invariant in it. Flow rate")
print("     is a solenoid-timing convenience here, not a control lever.")

# ============================================================================
# SECONDARY VERDICTS -- outputs that are not on the schedule path but decide
# whether the run is worth doing. Neither is a critical-output column above, so
# both would otherwise be invisible.
# ============================================================================
print("\n" + "=" * 100)
print("SECONDARY VERDICTS")
_bl, _bh = next((l, h) for n, l, h, _t in SWEEP if n == 'km_O2')
_r_lo, _r_hi = run('km_O2', _bl), run('km_O2', _bh)
print(f"   LOCAL pH AT THE ANODE: j_anode {b['j_anode']:.3f} mA/cm2 vs the phosphate "
      f"buffer's\n      limiting flux {b['j_buffer_lim']:.3f} mA/cm2 -> ratio "
      f"{b['j_buffer_ratio']:.3f}")
print(f"      over km_O2 {_bl:g}-{_bh:g} cm/s (film thickness D/km, Chemistry D215, now derived "
      f"not typed)\n      the ratio runs {_r_lo['j_buffer_ratio']:.2f}..{_r_hi['j_buffer_ratio']:.2f}; "
      + ("the verdict flips inside that uncertainty." if (_r_lo['j_buffer_ratio'] > 1) != (_r_hi['j_buffer_ratio'] > 1)
         else "the buffer holds across the whole range.")
      + "\n      A ferricyanide limiting-current run would settle km_O2 and so this verdict.")
_k_lo, _k_hi = next((l, h) for n, l, h, _t in SWEEP if n == 'k_cat_cells')
print(f"\n   PEROXIDE EXPOSURE: r_H2O2 {b['r_H2O2']:.3f} mg/L/h; steady value with a "
      f"growing\n      culture H2O2_ss {b['H2O2_ss']:.4f} mg/L "
      f"({b['H2O2_ss'] / 34.0147 * 1000:.1f} uM), against a ~5 uM growth-inhibition\n"
      f"      threshold. Over k_cat_cells {_k_lo:g}-{_k_hi:g} 1/s that is "
      f"{run('k_cat_cells', _k_hi)['H2O2_ss'] / 34.0147 * 1000:.1f}-"
      f"{run('k_cat_cells', _k_lo)['H2O2_ss'] / 34.0147 * 1000:.1f} uM.")
print(f"      The exposed window is LAG, not steady growth: with no biomass to scavenge,"
      f"\n      {b['H2O2_lag_1h']:.2f} mg/L accumulates in the first hour. k_cat_cells "
      "scores zero in the\n      table above only because r_H2O2, not H2O2_ss, is the "
      "critical-output column.")

print("\n" + "=" * 100)
print("URGENT ATTENTION ranking = leverage x ignorance  (KNOBs excluded -- control levers)")
scored = [(name, tier, crit, crit * WEIGHT[tier], flips)
          for name, tier, _sp, crit, flips, _mm, _c in rows if tier != 'KNOB']
scored.sort(key=lambda r: -r[3])
print(f"{'rank':5}{'input':18}{'tier':10}{'max normalised span':>21}{'urgency score':>15}")
for i, (name, tier, crit, sc, flips) in enumerate(scored, 1):
    mark = " *reaches the cliff - span excludes sched/DOss" if flips else ""
    print(f"{i:<5}{name:18}{tier:10}{crit:>20.0f}%{sc:>15.1f}{mark}")

print("\nKNOBS (control authority -- biggest levers you turn deliberately):")
knobs = [(name, crit, flips, mm, cross)
         for name, tier, _sp, crit, flips, mm, cross in rows if tier == 'KNOB']
knobs.sort(key=lambda r: -r[1])
for name, crit, flips, mm, cross in knobs:
    extra = ""
    if flips:
        extra = f"   *REACHES THE CLIFF at {name} = {cross:.4g}"
    elif not math.isinf(mm) and mm < 1.6:
        extra = f"   (DO margin falls to x{mm:.2f})"
    print(f"   {name:18} max normalised span {crit:.0f}%" + extra)

# ============================================================================
# C_eff (effective biocidal chlorine) -- the four chlorine knobs.
#   Re-based: the chlorine chain now runs on THIS model's pH, not a cached value. With an
#   outflow-only vent (iterH) the pooled CO2 runs to ~94 % of saturation and the
#   activity-scale pH falls to ~6.16; free NH3 falls with it -- which RAISES the
#   steady free HOCl, because ammonia is what scavenges it.
#   n_e_Cl is now fixed at 2 on every route (review finding B5, applied in the workbook).
# ============================================================================
CL_SWEEP = [
 ('tau_NH2Cl', 1 / 60, 5.0, 'DATA-GAP'),   # 1 min .. 5 h monochloramine residence
 ('R_chloramine', 18, 70, 'ESTIMATE'),     # potency-divisor band
 ('FE_CER', 0.2, 0.8, 'DATA-GAP'),         # max CER faradaic efficiency
 ('f_local', 1.0, 30.0, 'DATA-GAP'),       # anode boundary-layer enrichment
]
_bad_cl = [(n, lo, hi, BASE[n]) for n, lo, hi, _t in CL_SWEEP if not (lo <= BASE[n] <= hi)]
if _bad_cl:
    raise SystemExit("CL_SWEEP RANGE ERROR - baseline outside its own sweep range:\n" +
                     "\n".join(f"   {n}: base={bv} not in [{lo}, {hi}]"
                               for n, lo, hi, bv in _bad_cl))
print("\n" + "=" * 100)
print("C_eff (effective biocidal chlorine) sensitivity -- the chlorine knobs")
print(f"   baseline C_eff = {b['C_eff_Cl2']:.3f} mg/L as Cl2 at pH_meas {b['pH_meas']:.3f}  "
      f"(onset 0.1, kill 2.0 mg/L)")
print(f"{'knob':16}{'tier':10}{'low':>12}{'high':>12}{'C_eff lo':>11}{'C_eff hi':>11}")
ce_lo_all, ce_hi_all = [], []
for name, lo, hi, tier in CL_SWEEP:
    a, c = run(name, lo)['C_eff_Cl2'], run(name, hi)['C_eff_Cl2']
    ce_lo_all.append(min(a, c))
    ce_hi_all.append(max(a, c))
    print(f"{name:16}{tier:10}{lo:>12.4g}{hi:>12.4g}{min(a, c):>11.3f}{max(a, c):>11.3f}")
print(f"\n   full one-at-a-time C_eff envelope: {min(ce_lo_all):.3f} .. "
      f"{max(ce_hi_all):.3f} mg/L")
print(f"   kill threshold = 2.0 mg/L -> "
      f"{'REACHED' if max(ce_hi_all) >= 2.0 else 'NOT reached'} over this OAT sweep "
      f"for {SELECTORS['media']}; this is a model estimate, not a toxicity assay.")
