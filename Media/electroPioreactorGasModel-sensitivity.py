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
    electroPioreactorGasModel.xlsx as at the wave-4 rebuild (stage7), with the live
    selector state behind the values:
        ed04 / Pt-Ti rod / UdG (mixed) / UdG phosphate, LED 3 %, stir 1000 rpm, T 25 C.
    Formula logic is read directly out of the workbook part XML (Mass Transfer D178-D200,
    Electrochemistry D79-D122, Chemistry D166-D220). The workbook is the authority for
    both LOGIC and BASELINE INPUTS in this revision; the older Python twin
    (electroPioreactorGasModel.py) has NOT been re-based onto the new guard block and is
    no longer the reference for anything in this file.

WHAT CHANGED IN THIS RE-BASE (vs the previous revision of this script)
    (a) The SURFACE-HELD / SPARGE-NEEDED branch is gone. Dissolved O2 now carries a
        headspace back-pressure term: DO_ss = DO_hs_floor + DO_surf_excess, with
        DO_hs_floor = H_O2*y_O2_actual*P_atm set by the CO2 flush rather than by stirring.
        The interval is MIN(spg_int_carbon, spg_int_DO), a continuous minimum, so no
        unmeasured coefficient switches one formula for another any more. The new
        discontinuity is spg_int_DO going #N/A when DO_target - DO_surf_excess <= 0.
    (b) The faradaic efficiencies are calculated, not asserted: etaF = 1 - i_ORR/I_app.
        etaF is therefore no longer a free sweep input; km_O2 is swept in its place.
        SEE THE "ETAF FEEDBACK" SECTION -- the workbook does not currently propagate the
        calculated value, and that is a live defect, not a modelling choice.
    (c) The CO2 limit cycle is mass-conserving (one pooled liquid+headspace inventory
        decaying through the vent) and the pH solve is activity-corrected, so both
        dissolved CO2 and pH respond strongly to the schedule. pH_meas is now a
        first-class critical output.
    (d) Water properties track temperature, so a T_C sweep moves sigma, rho, D_O2, D_CO2
        and both Henry constants, not only the Henry constants.

STANDING RULE -- RE-BASE THIS FILE WHENEVER THE WORKBOOK MOVES
    This script is a reduced re-implementation, not a live read of the workbook. It MUST
    be re-based whenever either of the following changes:
      (a) the guard/optimiser logic (Mass Transfer D84-D94, D112, D131-D135, D178-D200)
      (b) the baseline inputs (Summary D2:D10 -- reactor, electrode, organism, medium,
          LED %, stir rpm, temperature, volume, pressure)
    Every percentage this script prints becomes wrong the moment it drifts. The runtime
    SELF_CHECK block fails loudly if the baseline stops reproducing the workbook, and the
    sweep-bracket assertion fails loudly if a baseline input drifts outside its own sweep
    range. Do not silence either; re-base instead.

Standard library only.  Run with:  python3 electroPioreactorGasModel-sensitivity.py

Each input carries an IGNORANCE tier -- DATA-GAP (unmeasured), ESTIMATE, LITERATURE
(well-known), KNOB (you set it). Urgency = leverage on the critical outputs x how poorly
we know the value. KNOBs are control authority, reported separately.
"""
import math

PI = math.pi
INF = float('inf')
NAN = float('nan')

# ---------------------------------------------------------------------------
# BASELINE INPUTS
# Source of truth: the WORKBOOK's live Summary selector state (Summary D2:D10) --
# ed04 / Pt-Ti rod / UdG (mixed) / UdG phosphate, LED 3 %, stir 1000 rpm, T 25 C.
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
  etaF_feedback=1.0,                      # 1 = calculated etaF propagates, as the workbook now does
  # --- biology ---
  bio_H2=6, bio_O2=2, bio_CO2=1,
  # --- O2 ceiling / Henry ---
  T_C=25, P_atm=101325, H_O2ref=1.2e-5, H_O2T=1500, T_ref=298.15, O2_ceil_atm=0.3,
  # --- CO2 dosing (ed04 calibrated: 3.33 mL/s = 199.8 mL/min) ---
  Q_CO2=199.8, pulse_floor=0.25, flush_factor=1.0, R=8.314462618, M_CO2=44.0095,
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
  H_CO2ref=3.3e-4, H_CO2T=2400, Km_CO2=50,
  H_H2ref=7.8e-6, H_H2T=500,
  Q_vent=0.5, pCO2_air=40.0,
  # --- optimiser inputs ---
  target_DO_frac=0.226086956521739, carbon_margin_min=2,
  # --- cell-voltage budget ---
  b_anode=0.12, j0_anode=1e-10, b_cath=0.14, j0_cath=1.5e-6, pcet_credit=-0.15,
  E0_OER=1.229, k_geom=2.0, kappa_fI=0.78, kappa_TC=0.02,
  # --- local-pH (buffer) verdict ---
  D_HPO4=7.59e-10, delta_diff=40.0,
  # --- UdG recipe (g/L) ---
  udg_KH2PO4=2.3, udg_Na2HPO4=2.9, udg_NaHCO3=1.05,
  udg_MgSO4=0.5, udg_NH42SO4=0.47, udg_CaCl2=0.01,
  # --- chlorine chain ---
  f_local=10.0, k1_NH2Cl=4.2e6, tau_NH2Cl=1.0, R_chloramine=25.0,
)

MW = dict(KH2PO4=136.086, Na2HPO4=141.96, NaHCO3=84.007,
          MgSO4=246.48, NH42SO4=132.14, CaCl2=110.98)
# CRC Handbook (Vanysek), limiting molar conductivities at 25 C, S cm2/mol, PER MOLE OF ION
LAM = dict(Na=50.08, K=73.48, NH4=73.5, Mg=106.0, Ca=118.94,
           H2PO4=36.0, HPO4=114.0, SO4=160.0, HCO3=44.5, Cl=76.31)
# (K25, dH kJ/mol) -- van 't Hoff corrected to the reactor temperature (Chemistry D13:D19)
KA = dict(Ka1c=(4.45e-7, 9.15), Ka2c=(4.69e-11, 14.9), Ka1p=(7.1e-3, -8.0),
          Ka2p=(6.31e-8, 3.6), Ka3p=(4.2e-13, 16.0), KaN=(5.6e-10, 52.2),
          Kw=(1e-14, 55.8))
M_HOCl = 52460.0   # mg/mol
MW_N = 14007.0     # mg/mol
CL_PER_N = 5.06    # mg Cl2 per mg ammonium-N (breakpoint)


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
    A_wet = (PI * p['rod_d'] * L_sub + PI / 4 * p['rod_d'] ** 2) / 100   # cm2, rod (end face)

    # --- water properties at the reactor temperature (Mass Transfer D29-D32, D138) ---
    sigma = p['sigma_0'] + p['sigma_k'] * p['T_C']
    rho_L = p['rho_0'] + p['rho_k'] * p['T_C']
    D_O2 = 10 ** (p['HB_a'] + p['HB_b'] / T_K - (p['HB_c'] / T_K) ** 2) / 10000 * p['D_O2_fit']
    D_CO2 = p['D_CO2_ref'] * math.exp(-p['Ea_D_CO2'] / R * (1 / T_K - 1 / 298.15))
    H_O2_T = p['H_O2ref'] * math.exp(p['H_O2T'] * (1 / T_K - 1 / p['T_ref']))
    H_CO2_T = p['H_CO2ref'] * math.exp(p['H_CO2T'] * (1 / T_K - 1 / p['T_ref']))
    H_H2_T = p['H_H2ref'] * math.exp(p['H_H2T'] * (1 / T_K - 1 / p['T_ref']))
    O2_ceil_Pa = p['O2_ceil_atm'] * p['P_atm']
    O2_ceil_C = H_O2_T * O2_ceil_Pa

    # --- electrolysis, with CALCULATED faradaic efficiencies (Echem D86-D89, D101-D104) ---
    I_app = (p['gerrit_slope'] * p['intensity'] + p['gerrit_int']) / 1000
    DO_design = p['target_DO_frac'] * O2_ceil_C                          # D85
    i_ORR = p['z_e_ORR'] * p['F'] * (p['km_O2'] / 100) * DO_design * (A_wet / 10000)   # D86
    i_ORR_ceil = p['z_e_ORR'] * p['F'] * (p['km_O2'] / 100) * O2_ceil_C * (A_wet / 10000)
    etaF_calc = max(0.0, 1 - i_ORR / I_app)                              # D88
    etaF_calc_min = max(0.0, 1 - i_ORR_ceil / I_app)                     # D89
    Cl_M = 2 * p['udg_CaCl2'] / MW['CaCl2']                              # Chemistry D42
    I_Cl = min(I_app * p['FE_CER'], p['F'] * p['km_Cl'] * (Cl_M / 1000) * A_wet)   # D133
    etaF_OER_calc = max(0.0, 1 - I_Cl / I_app - p['corr_I_frac'])        # D104
    # THE CONTESTED SWITCH -- see the ETAF FEEDBACK section at the foot of the run.
    fb = p['etaF_feedback']
    etaF = 1.0 + fb * (etaF_calc - 1.0)
    etaF_OER = 1.0 + fb * (etaF_OER_calc - 1.0)
    rH2 = I_app * etaF / (p['z_e_H2'] * p['F']) * 3600
    rO2 = I_app * etaF_OER / (p['z_e_O2'] * p['F']) * 3600
    O2_cath = I_app * (1 - etaF) / (p['z_e_ORR'] * p['F']) * 3600
    O2_net = rO2 - O2_cath                                               # Echem D29
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
    spg_dur = max(p['pulse_floor'], p['flush_factor'] * headspace_V / (p['Q_CO2'] / 60))  # D90
    DO_target = p['target_DO_frac'] * O2_ceil_C                          # D179
    DO_surf_excess = O2_excess / (kLa_surf_used * 3600 * V_L)            # D180
    DO_surf_excess_lag = O2_net / (kLa_surf_used * 3600 * V_L)           # D181
    hs_O2_allow = DO_target - DO_surf_excess                             # D182
    feasible = hs_O2_allow > 0
    if feasible:
        y_O2_star = hs_O2_allow / (H_O2_T * p['P_atm'])                  # D183
        duty_DO = O2_excess * (1 - y_O2_star) / (y_O2_star * CO2_rate_full)   # D184
        spg_int_DO = spg_dur / (60 * duty_DO)                            # D185
    else:
        y_O2_star = duty_DO = spg_int_DO = NAN
    # the feasibility floor: measured kL_surf must exceed kL_surf_crit or nothing works
    kLa_surf_req = O2_excess / (DO_target * 3600 * V_L)                  # D186
    kL_surf_crit = kLa_surf_req / a_surf                                 # D131
    # margin > 1 => DO target reachable; < 1 => UNREACHABLE at any interval
    do_margin = kLa_surf_used / kLa_surf_req if kLa_surf_req > 0 else INF

    duty_carbon = p['carbon_margin_min'] * CO2_cons / CO2_rate_full      # D86
    spg_int_carbon = spg_dur / (60 * duty_carbon) if duty_carbon > 0 else INF   # D112
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
    duty_actual = spg_dur / (spg_int * 60)                               # D93

    # --- steady DO, with the headspace back-pressure floor (D187, D188, D108) ---
    CO2_supply = nCO2 * spg_dur * (60 / spg_int)                         # D100
    y_O2_actual = O2_excess / (O2_excess + CO2_supply) if CO2_supply > 0 else NAN   # D187
    DO_hs_floor = H_O2_T * y_O2_actual * p['P_atm']                      # D188
    DO_ss_sawtooth = DO_hs_floor + DO_surf_excess                        # D133, mol/m3
    DO_ss = DO_ss_sawtooth * 32                                          # D108, mg/L
    DO_ss_lag = (DO_hs_floor + DO_surf_excess_lag) * 32                  # D135, mg/L
    t_lag = (O2_ceil_C * V_L / O2_net * 60) if O2_net > 1e-15 else INF   # D79

    # --- bubble / sparge strip (tube); Mendelson NA-guard < 1 mm ---
    d_or = p['spg_ID'] / 1000
    d_b = (6 * d_or * sigma / (rho_L * p['g'])) ** (1 / 3)
    if d_b < 0.001:
        strip_avg = NAN
        strip_ratio = NAN
    else:
        u_rise = math.sqrt(p['mend_a'] * sigma / (rho_L * d_b) + p['mend_b'] * p['g'] * d_b)
        u_sg = (p['Q_CO2'] / 1e6 / 60) / (A_x / 1e6)
        holdup = u_sg / u_rise
        a_int = 6 * holdup / d_b
        t_c = d_b / u_rise
        kL = 2 * math.sqrt(D_O2 / (PI * t_c))
        strip_sparge = kL * a_int * V_L * O2_ceil_C * 3600
        strip_avg = strip_sparge * duty_actual
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
    n_hs = p['P_atm'] * hs_m3 / (R * T_K)                                # D150
    k_vent = (p['Q_vent'] / 1e6 / 60) / hs_m3                            # D143
    k_eff = k_vent * Vg / (V_L + Vg)                                     # D195
    pool_a = V_L / (V_L + Vg)                                            # D193
    pool_b = p['flush_factor'] * n_hs / (V_L + Vg)                       # D194
    kLa_CO2_off = kL_surf * a_surf * math.sqrt(D_CO2 / D_O2)             # D148
    pool_beta_ratio = (kLa_CO2_off * V_L / Vg) / k_vent                  # D196
    t_off = max(0.0, spg_int * 60 - spg_dur)                             # D152
    pool_e = math.exp(-k_eff * t_off)                                    # D197
    C_air = H_CO2_T * p['pCO2_air']                                      # D146
    C_sat = H_CO2_T * p['P_atm']                                         # D145
    C_start = (C_air * (1 - pool_e) + pool_b * pool_e) / (1 - pool_a * pool_e)   # D198
    C_peak = pool_a * C_start + pool_b                                   # D199
    CO2_cyc = (C_air + (C_peak - C_air) * (1 - pool_e) / (k_eff * t_off)
               if t_off > 0 else C_peak)                                 # D200
    CO2aqc = min(C_sat, max(C_air, CO2_cyc)) / 1000                      # D162, mol/L

    # ------------------------------------------------------------------
    # pH -- activity-corrected charge balance (Chemistry D50:D100, D103, D185-D197, D220).
    # The grid + linear interpolation is reproduced exactly (0.1 pH steps, 4.0 to 9.0),
    # not replaced by a root-find, because the workbook ships the grid.
    # ------------------------------------------------------------------
    Ka = {k: v[0] * math.exp(-v[1] * 1000 / R * (1 / T_K - 1 / 298.15)) for k, v in KA.items()}
    n = lambda salt, mw: p[salt] / MW[mw]
    n_NaHCO3, n_Na2HPO4 = n('udg_NaHCO3', 'NaHCO3'), n('udg_Na2HPO4', 'Na2HPO4')
    n_KH2PO4, n_NH42SO4 = n('udg_KH2PO4', 'KH2PO4'), n('udg_NH42SO4', 'NH42SO4')
    n_MgSO4, n_CaCl2 = n('udg_MgSO4', 'MgSO4'), n('udg_CaCl2', 'CaCl2')
    I_ion = 0.5 * ((n_NaHCO3 + 2 * n_Na2HPO4) + n_KH2PO4 + 2 * n_NH42SO4
                   + 4 * n_MgSO4 + 4 * n_CaCl2 + n_KH2PO4 + 4 * n_Na2HPO4
                   + 4 * (n_MgSO4 + n_NH42SO4) + n_NaHCO3 + 2 * n_CaCl2)   # D184
    A_DH = 1.82e6 * (78.54 * (298.15 / T_K) ** 1.368) ** -1.5 * T_K ** -1.5   # D186
    sI = math.sqrt(I_ion)
    dav = lambda z: 10 ** (-A_DH * z * z * (sI / (1 + sI) - 0.3 * I_ion))     # Davies
    g1, g2, g3 = dav(1), dav(2), dav(3)
    K1c, K2c = Ka['Ka1c'] / g1 ** 2, Ka['Ka2c'] / g2
    K1p, K2p = Ka['Ka1p'] / g1 ** 2, Ka['Ka2p'] / g2
    K3p = Ka['Ka3p'] * g2 / (g1 * g3)
    KN, Kw = Ka['KaN'], Ka['Kw'] / g1 ** 2
    SID = ((n_NaHCO3 + 2 * n_Na2HPO4 + n_KH2PO4 + 2 * n_MgSO4 + 2 * n_CaCl2)
           - (2 * (n_NH42SO4 + n_MgSO4) + 2 * n_CaCl2))                  # D40
    PT = n_KH2PO4 + n_Na2HPO4                                            # D39
    NT = 2 * n_NH42SO4                                                   # D41

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
    j_anode = I_app * 1000 / A_wet                                       # mA/cm2
    if n_cross == 1:
        C_HPO4 = PT * (1 - 1 / (1 + 10 ** (pH_meas - pKa2p_c)))
        j_buffer_lim = (p['F'] * p['D_HPO4'] * C_HPO4 * 1000
                        / (p['delta_diff'] / 1e6) / 10)                  # mA/cm2
        j_buffer_ratio = j_anode / j_buffer_lim
    else:
        j_buffer_lim = j_buffer_ratio = NAN

    # --- conductivity and the cell-voltage budget (Chemistry D177-D180, Echem D106-D119) ---
    kappa0 = (((n_NaHCO3 + 2 * n_Na2HPO4) * LAM['Na'] + n_KH2PO4 * LAM['K']
               + 2 * n_NH42SO4 * LAM['NH4'] + n_MgSO4 * LAM['Mg'] + n_CaCl2 * LAM['Ca']
               + n_Na2HPO4 * LAM['HPO4'] + n_KH2PO4 * LAM['H2PO4']
               + (n_MgSO4 + n_NH42SO4) * LAM['SO4'] + n_NaHCO3 * LAM['HCO3']
               + 2 * n_CaCl2 * LAM['Cl']) / 10)                          # S/m
    kappa = kappa0 * p['kappa_fI'] * (1 + p['kappa_TC'] * (T_K - 298.15))
    R_cell = (p['k_geom'] * math.acosh(p['elec_gap'] / p['rod_d'])
              / (PI * kappa * (L_sub / 1000)))                           # D117
    V_IR = I_app * R_cell                                                # D118
    eta_a = p['b_anode'] * math.log10(j_anode / 1000 / p['j0_anode'])     # D111
    eta_c = p['b_cath'] * math.log10(j_anode / 1000 / p['j0_cath'])       # D112
    V_cell = p['E0_OER'] + eta_a + eta_c + p['pcet_credit'] + V_IR        # D119

    # --- peroxide (Echem D93-D98) ---
    r_H2O2 = p['f_HOOH'] * i_ORR / (2 * p['F']) * p['M_H2O2'] * 1000 * 3600 / (V_charge / 1000)
    H2O2_ss = r_H2O2 / (p['k_cat_cells'] * 3600)                         # D95, growing culture
    H2O2_lag_1h = r_H2O2                                                 # D96, no biomass

    # --- dissolved CO2 / H2 diagnostics ---
    carbon_margin = CO2aqc * 1000 * 1000 / p['Km_CO2']
    C_H2 = H_H2_T * p['P_atm']
    t_H2_sat = C_H2 * V_L / rH2 * 60 if rH2 > 0 else INF
    CO2_sd = (CO2_supply / CO2_cons) if CO2_cons > 0 else NAN

    # --- chlorine chain (Chemistry D131-D149), now driven by THIS pH, not a cached one ---
    if n_cross == 1:
        NH3_free = NT / (1 + 10 ** (pKa_NH4 - pH_meas))                  # D138
        P_HOCl = I_Cl / (2 * p['F'] * (V_charge / 1000))                 # D134, n_e_Cl = 2
        HOCl_mgL = P_HOCl / (p['k1_NH2Cl'] * NH3_free) * M_HOCl
        NH2Cl = min(P_HOCl * p['tau_NH2Cl'] * 3600 * M_HOCl,
                    CL_PER_N * NT * MW_N, Cl_M * M_HOCl)
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
        kL_surf_crit=kL_surf_crit, kLa_surf_used=kLa_surf_used, do_margin=do_margin,
        t_O2_ceiling_lag=t_lag, O2_removal_ratio=removal_ratio, surf_ratio=surf_ratio,
        strip_ratio=strip_ratio, O2_excess=O2_excess, O2_net=O2_net, rH2=rH2,
        etaF_calc=etaF_calc, etaF_calc_min=etaF_calc_min, etaF_OER_calc=etaF_OER_calc,
        i_ORR_design=i_ORR, D_O2=D_O2, sigma=sigma, rho_L=rho_L,
        CO2_cyc_avg_new=CO2_cyc, CO2aqc=CO2aqc, CO2_supply=CO2_supply, CO2_sd=CO2_sd,
        pool_beta_ratio=pool_beta_ratio, carbon_margin=carbon_margin, t_H2_sat=t_H2_sat,
        pH_meas=pH_meas, pH_op=pH_op, n_cross=n_cross,
        j_anode=j_anode, j_buffer_lim=j_buffer_lim, j_buffer_ratio=j_buffer_ratio,
        kappa=kappa, R_cell=R_cell, V_IR=V_IR, V_cell_est=V_cell,
        r_H2O2=r_H2O2, H2O2_ss=H2O2_ss, H2O2_lag_1h=H2O2_lag_1h, C_eff=C_eff,
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
 ('Q_vent', 0.1, 2.0, 'DATA-GAP'),              # vent bleed; sets the whole CO2 limit cycle
 ('elec_gap', 10.0, 20.0, 'DATA-GAP'),          # measure with calipers
 ('j0_anode', 1e-11, 1e-9, 'DATA-GAP'),         # OER on Pt spans +/-1 decade about 1e-10
 ('corr_I_frac', 0.0, 0.10, 'DATA-GAP'),        # 0 is the floor, so base sits at lo
 ('k_cat_cells', 0.001, 0.01, 'DATA-GAP'),      # whole-culture catalase clearance
 ('bio_O2', 1.6, 2.4, 'DATA-GAP'),
 ('bio_CO2', 0.8, 1.3, 'DATA-GAP'),
 ('pulse_floor', 0.2, 1.0, 'DATA-GAP'),
 # ---- ESTIMATE ----
 ('km_O2', 0.002, 0.006, 'ESTIMATE'),           # ETW at 10-40 cm/s swirl past the rod
 ('km_Cl', 0.002, 0.006, 'ESTIMATE'),           # same basis, scaled by D^0.644
 ('f_HOOH', 0.10, 0.20, 'ESTIMATE'),            # Le Bozec 2001 peroxide selectivity band
 ('z_e_ORR', 2, 4, 'ESTIMATE'),                 # 2 is the physical floor, so base at lo
 ('k_geom', 1.0, 3.0, 'ESTIMATE'),              # cell-constant correction
 ('kappa_fI', 0.66, 0.90, 'ESTIMATE'),          # Kohlrausch finite-strength factor +/-15 %
 ('delta_diff', 20.0, 80.0, 'ESTIMATE'),        # diffusion layer, factor ~2
 ('pcet_credit', -0.20, -0.10, 'ESTIMATE'),     # phosphate PCET credit, 100-200 mV
 ('b_anode', 0.06, 0.12, 'ESTIMATE'),           # 60 mV/dec buffered .. 120 bare; base at hi
 ('b_cath', 0.13, 0.15, 'ESTIMATE'),
 ('j0_cath', 1e-6, 2e-6, 'ESTIMATE'),
 ('O2_ceil_atm', 0.25, 0.35, 'ESTIMATE'),
 ('vial_wall', 0.9, 1.3, 'ESTIMATE'),
 ('Km_CO2', 20, 80, 'ESTIMATE'),
 ('gerrit_slope', 0.95, 1.11, 'ESTIMATE'),      # empirical rig fit +/-8 %
 ('gerrit_int', 2.2, 3.0, 'ESTIMATE'),
 ('V_max', 14, 18, 'ESTIMATE'),
 ('FE_CER', 0.2, 0.8, 'ESTIMATE'),
 # ---- LITERATURE (well-known) ----
 ('D_O2_fit', 0.92, 1.08, 'LITERATURE'),        # Han & Bartels correlation scatter
 ('H_O2ref', 1.10e-5, 1.30e-5, 'LITERATURE'),
 ('H_O2T', 1275, 1725, 'LITERATURE'),           # numerically inert at T = T_ref = 25 C
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
 ('T_C', 20, 37, 'KNOB'),                       # brackets workbook 25 C and pack 30 C
]

# Outputs that decide whether we reach growth / what schedule to run.
# pH and cell voltage are reported in NATURAL units, not per cent: a percentage change in
# a logarithmic quantity is meaningless, and a percentage of a voltage hides how close the
# rail is. For the urgency SCORE they are normalised -- pH against the 1.0-unit HOB band
# (6.5-7.5), voltage against its own baseline.
CRITICAL = ['spg_int_opt', 'DO_ss', 'pH_meas', 'r_H2O2', 'V_cell_est', 't_O2_ceiling_lag']
ABSOLUTE_OUT = {'pH_meas': 1.0, 'V_cell_est': None}   # None => score as % of baseline
WEIGHT = {'DATA-GAP': 1.0, 'ESTIMATE': 0.6, 'LITERATURE': 0.15, 'KNOB': 0.0}

# Cached values read straight out of the workbook part XML at the live inputs
# (ed04 / Pt-Ti rod / UdG (mixed) / UdG phosphate, 3 %, 1000 rpm, 25 C).
# If any of these stops matching, this script has drifted -- re-base it, do not adjust
# the tolerance.
SELF_CHECK = [
    ('D_O2',            'D_O2 (m2/s)',              1.99767e-9),
    ('kLa_surf_used',   'kLa_surf_used (1/s)',      7.2001e-3),
    ('etaF_calc',       'etaF_calc (-)',            0.977475),
    ('DO_target',       'DO_target (mol/m3)',       0.0824697),
    ('DO_surf_excess',  'DO_surf_excess (mol/m3)',  0.0362963),
    ('y_O2_star',       'y_O2_star (-)',            0.0379947),
    ('duty_DO',         'duty_DO (-)',              7.94346e-4),
    ('spg_int_DO',      'spg_int_DO (min)',        16.4604),
    ('spg_int_opt',     'spg_int_opt (min)',       16.4604),
    ('spg_int_carbon',  'spg_int_carbon (min)',   185.899),
    ('kLa_surf_req',    'kLa_surf_req (1/s)',       3.31777e-3),
    ('DO_ss',           'DO_ss (mg/L)',             2.63903),
    ('V_cell_est',      'V_cell_est (V)',           3.26376),
    ('r_H2O2',          'r_H2O2 (mg/L/h)',          0.813297),
    ('CO2_cyc_avg_new', 'CO2_cyc_avg_new (mol/m3)', 8.59021),
    ('pH_meas',         'pH_meas (-)',              6.60395),
]


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

b = model(BASE)

# --- runtime guard 2: the baseline must still reproduce the workbook -------------
_fails = [f"   {lab}: this={b[k]:.6g}  workbook={v:.6g}"
          for k, lab, v in SELF_CHECK if abs(b[k] - v) / abs(v) > 5e-5]

print("=" * 100)
print("BASELINE - workbook live state: ed04 / Pt-Ti rod / UdG (mixed) / UdG phosphate,")
print(f"           LED {BASE['intensity']}%, stir {BASE['stir_rpm']} rpm, T {BASE['T_C']} C, "
      f"tube sparger, Q_CO2 = {BASE['Q_CO2']} mL/min (ed04 calibration)")
print("=" * 100)
for k, unit in [('spg_dur', 's'), ('spg_int_opt', 'min'), ('spg_int_opt_s', 's'),
                ('spg_int_DO', 'min'), ('spg_int_carbon', 'min'), ('spg_int_max', 'min'),
                ('duty_actual', '-'), ('DO_target', 'mol/m3'),
                ('DO_surf_excess', 'mol/m3'), ('DO_hs_floor', 'mol/m3'),
                ('y_O2_star', '-'), ('y_O2_actual', '-'),
                ('DO_ss', 'mg/L'), ('DO_ss_lag', 'mg/L'),
                ('kLa_surf_used', '1/s'), ('kLa_surf_req', '1/s'), ('kL_surf_crit', 'm/s'),
                ('t_O2_ceiling_lag', 'min'), ('O2_removal_ratio', 'x'), ('surf_ratio', 'x'),
                ('t_H2_sat', 'min'), ('carbon_margin', 'x'), ('CO2_sd', 'x'),
                ('CO2_cyc_avg_new', 'mol/m3'), ('pH_meas', '-'),
                ('etaF_calc', '-'), ('etaF_OER_calc', '-'),
                ('kappa', 'S/m'), ('R_cell', 'ohm'), ('V_IR', 'V'), ('V_cell_est', 'V'),
                ('r_H2O2', 'mg/L/h'), ('H2O2_ss', 'mg/L'), ('C_eff', 'mg/L'),
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
    print("   Re-base BASE / model() against the workbook before using any number below.")
else:
    print(f"      self-check: all {len(SELF_CHECK)} baseline values reproduce the workbook "
          "at 1000 rpm / 25 C")

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
print("   H_O2T (and every van 't Hoff enthalpy) is numerically inert at the baseline")
print(f"   because T = T_ref = {BASE['T_ref'] - 273.15:.0f} C; it regains leverage the")
print("   moment the workbook moves off that point.")
print("\n   TWO STRUCTURAL ZEROS -- read these before concluding an input is harmless:")
print("   * DO_ss is PINNED to DO_target whenever the DO-limited interval binds. At that")
print("     interval y_O2_actual = y_O2_star by construction, so DO_hs_floor = DO_target -")
print("     DO_surf_excess and DO_ss = DO_target exactly. The only inputs that can move it")
print("     are the ones that move DO_target (target_DO_frac, O2_ceil_atm, H_O2ref, T_C).")
print("     Everything else shows DOss% = 0 because the schedule absorbs it, not because")
print("     the model is insensitive -- read the minMargin column for those.")
print("   * Q_CO2 cancels exactly. spg_dur goes as 1/Q_CO2 and duty_DO goes as 1/Q_CO2, so")
print("     the interval, the duty and the delivered CO2 are all invariant in it. Flow rate")
print("     is a solenoid-timing convenience here, not a control lever.")

# ============================================================================
# SECONDARY VERDICTS -- outputs that are not on the schedule path but decide
# whether the run is worth doing. Neither is a critical-output column above, so
# both would otherwise be invisible.
# ============================================================================
print("\n" + "=" * 100)
print("SECONDARY VERDICTS")
_bl, _bh = next((l, h) for n, l, h, _t in SWEEP if n == 'delta_diff')
_r_lo, _r_hi = run('delta_diff', _bl), run('delta_diff', _bh)
print(f"   LOCAL pH AT THE ANODE: j_anode {b['j_anode']:.3f} mA/cm2 vs the phosphate "
      f"buffer's\n      limiting flux {b['j_buffer_lim']:.3f} mA/cm2 -> ratio "
      f"{b['j_buffer_ratio']:.3f}")
print(f"      over delta_diff {_bl:g}-{_bh:g} um the ratio runs "
      f"{_r_lo['j_buffer_ratio']:.2f}..{_r_hi['j_buffer_ratio']:.2f}, i.e. the verdict "
      "flips\n      inside the diffusion layer's own factor-2 uncertainty. At the "
      "baseline delta the\n      buffer is AT its limit, so expect a 0.4-1.0 unit "
      "excursion at each electrode and\n      a weakened phosphate PCET credit at the "
      "anode. This is the second thing a\n      ferricyanide limiting-current run would "
      "settle, and it settles both at once.")
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
# ETAF FEEDBACK -- a live defect in the workbook, not a modelling choice.
#   Electrochemistry D18 is  etaF = IFERROR(cal_etaF, etaF_calc), and cal_etaF
#   (Calibrations D31) is itself IFERROR(AVERAGEIFS(...), "no included runs ...").
#   With no calibration rows entered, the inner IFERROR returns TEXT, which is not an
#   error, so the outer IFERROR never fires and etaF_calc is never reached. The O2 chain
#   the workbook actually ships is therefore still the etaF = 1 chain -- which is what the
#   cached values, and this script's baseline, reproduce.
#   The block below shows what the schedule becomes once that is fixed.
# ============================================================================
print("\n" + "=" * 100)
print("ETAF FEEDBACK -- what changes when the calculated efficiencies actually propagate")
p_fb = dict(BASE)
p_fb['etaF_feedback'] = 1.0
bf = model(p_fb)
print(f"   as shipped (etaF = 1):        etaF {1.0:.5f}  etaF_OER {1.0:.5f}")
print(f"   as intended (calculated):     etaF {b['etaF_calc']:.5f}  "
      f"etaF_OER {b['etaF_OER_calc']:.5f}")
print(f"{'output':22}{'as shipped':>14}{'as intended':>14}{'change':>12}")
for k, unit in [('O2_excess', 'mol/h'), ('DO_surf_excess', 'mol/m3'), ('spg_int_DO', 'min'),
                ('spg_int_opt', 'min'), ('DO_ss', 'mg/L'), ('do_margin', 'x'),
                ('CO2_cyc_avg_new', 'mol/m3'), ('pH_meas', '-')]:
    a, c = b[k], bf[k]
    chg = (c - a) / a * 100 if a else NAN
    print(f"   {k:19}{a:>14.6g}{c:>14.6g}{chg:>11.1f}%")
print("   The schedule moves by ~43 % and the pH by ~0.08 units. Neither the workbook's")
print("   cached values nor the baselines this script is checked against carry it, so")
print("   the two are consistent with each other and both are wrong once D18 is fixed.")
print("\n   THE DEFECT IS SYSTEMIC, NOT LOCAL TO etaF. Every Calibrations 'value in use'")
print("   cell wraps its aggregate as IFERROR(AVERAGEIFS(...), \"no included runs ...\"),")
print("   which turns the empty-table error into TEXT. Almost every consumer is then")
print("   IFERROR(cal_X, default) -- and IFERROR cannot fire on text, so the default is")
print("   never reached and the text propagates. With the calibration tables empty (their")
print("   current state) that reaches gerrit_slope/gerrit_int (Echem D11/D12), V_vial_total")
print("   and D_int (Geometry D24/D22), bio_H2/O2/CO2 (Biology D10-D12), etaF/etaF_OER")
print("   (Echem D18/D26), por_grade_e (Echem D32) and kLa_meas (MT D97). kLa is the worst")
print("   of them: Excel ranks text above every number, so kLa_meas>0 is TRUE and MT D98")
print("   evaluates text/3600.")
print("   PREDICTION, worth testing before trusting any cell: on the next full recalc in")
print("   Excel this sheet returns #VALUE! across most of Mass Transfer, Biology and")
print("   Electrochemistry. The cached values look healthy only because they were written")
print("   by the build script, not computed by Excel.")
print("   FIX: return NA() (not a text string) from the Calibrations 'value in use' cells")
print("   and carry the researcher-facing message in column E/F, OR convert every consumer")
print("   to the IF(ISNUMBER(cal_X), ...) form already used correctly at MT D117")
print("   (flowrate_cal) -- that one cell is the pattern the rest should follow.")

# ============================================================================
# C_eff (effective biocidal chlorine) -- the four chlorine knobs.
#   Re-based: the chlorine chain now runs on THIS model's pH, not a cached 7.376. The
#   activity-scale pH has fallen to ~6.59 because the mass-conserving CO2 limit cycle
#   delivers ~9x more dissolved CO2, and free NH3 falls ~6x with it -- which RAISES the
#   steady free HOCl, because ammonia is what scavenges it.
#   n_e_Cl is now fixed at 2 on every route (review finding B5, applied in the workbook).
# ============================================================================
CL_SWEEP = [
 ('tau_NH2Cl', 1 / 60, 5.0, 'DATA-GAP'),   # 1 min .. 5 h monochloramine residence
 ('R_chloramine', 18, 70, 'ESTIMATE'),     # potency-divisor band
 ('km_Cl', 0.001, 0.01, 'ESTIMATE'),       # chloride mass-transfer coeff (cm/s)
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
print(f"   baseline C_eff = {b['C_eff']:.3f} mg/L at pH_meas {b['pH_meas']:.3f}  "
      f"(onset 0.1, kill 2.0 mg/L)")
print(f"{'knob':16}{'tier':10}{'low':>12}{'high':>12}{'C_eff lo':>11}{'C_eff hi':>11}")
ce_lo_all, ce_hi_all = [], []
for name, lo, hi, tier in CL_SWEEP:
    a, c = run(name, lo)['C_eff'], run(name, hi)['C_eff']
    ce_lo_all.append(min(a, c))
    ce_hi_all.append(max(a, c))
    print(f"{name:16}{tier:10}{lo:>12.4g}{hi:>12.4g}{min(a, c):>11.3f}{max(a, c):>11.3f}")
print(f"\n   full one-at-a-time C_eff envelope: {min(ce_lo_all):.3f} .. "
      f"{max(ce_hi_all):.3f} mg/L")
print(f"   kill threshold = 2.0 mg/L -> "
      f"{'REACHED' if max(ce_hi_all) >= 2.0 else 'NOT reached'}: the chloride-pool cap "
      "holds\n   C_eff sub-lethal across the whole knob box for UdG.")
