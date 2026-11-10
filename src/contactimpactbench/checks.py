"""Regression checks vs frozen numerical CSVs, not independent physics data."""
from .reference import load_reference
from .reduced import ReducedCase,run_impact
from .normal import normal_reference,PSI_PA
from .friction import drilling_arm,weak_spin_slope,distributed_friction

# Frozen tolerances refer to unchanged source code and stored outputs.
N33_ABS=1e-8
N34_ABS_TC_MS=2e-6
N34_ABS_N=2e-3
N34_ABS_V=2e-6

def _check_close(a,b,atol):
    return abs(a-b)<=atol

def verify_archive(*,full=False):
    fails=[]; counts={'n33':0,'n34':0,'n36':0}
    rows=load_reference('n33')
    if not full:
        # Four archived baseline spin cases at 2us and zeta=.25.
        rows=[r for r in rows if r['normal_law']=='' and r['dt_us']=='2.0' and r['zeta_t']=='0.25']
    for row in rows:
        pressure=float(row['pressure_psi'])*PSI_PA
        r=run_impact(ReducedCase(spin_rad_s=float(row['spin_rad_s']),
            pressure_pa=pressure,time_step_s=float(row['dt_us'])*1e-6,
            tangential_damping_ratio=float(row['zeta_t']),normal_law=row['normal_law'] or 'A'))
        # Reported pressures are rounded through psi conversion in CSV; direct double precision matching.
        for field,pred in [('vx_out',r.vx),('vy_out',r.vy),('omega3_out',r.w3),
                           ('duration_ms',r.tc*1e3),('dE_J',r.dE),('Npeak_N',r.peakN),
                           ('Ft_peak_N',r.peakFt),('M_peak_Nm',r.peakM)]:
            # peak/duration are discontinuous in event-time discretization:
            # still demand reference reproducibility with small tolerant margin.
            tol=3e-5 if field in ['Npeak_N','Ft_peak_N','M_peak_Nm'] else N33_ABS
            if not _check_close(pred,float(row[field]),tol):
                fails.append({'module':'N3.3','spin':row['spin_rad_s'],'field':field,
                              'actual':pred,'expected':float(row[field]),'atol':tol})
        if r.positive_sum>1e-9 or r.residual_max>1e-9 or r.max_phi>1+1e-10:
            fails.append({'module':'N3.3','spin':row['spin_rad_s'],'reason':'energy/limit invariant'})
        counts['n33']+=1
    n34=load_reference('n34')
    if not full:
        n34=[r for r in n34 if r['pressure_psi']=='8.0' and r['normal_law']=='A' and r['dt_us']=='2.0']
    # Cache independent references for each pressure/law combination.
    cache={}
    for row in n34:
        key=(row['pressure_psi'],row['normal_law'])
        if key not in cache:
            cache[key]=normal_reference(pressure_pa=float(key[0])*PSI_PA,law=key[1])
        ref=cache[key]
        for field,actual,expected,atol in [
            ('tc_ref_ms',ref['contact_time_ms'],float(row['tc_ref_ms']),N34_ABS_TC_MS),
            ('Nmax_ref_N',ref['peak_normal_force_N'],float(row['Nmax_ref_N']),N34_ABS_N),
            ('vz_ref',ref['outbound_normal_velocity_m_s'],float(row['vz_ref']),N34_ABS_V)]:
            if not _check_close(actual,expected,atol):
                fails.append({'module':'N3.4','law':key[1],'field':field,'actual':actual,'expected':expected})
        if full:
            discrete=run_impact(ReducedCase(spin_rad_s=0.,velocity_m_s=(0.,0.,-4.),
                pressure_pa=float(key[0])*PSI_PA,
                normal_law=key[1],time_step_s=float(row['dt_us'])*1e-6,
                tangential_damping_ratio=0.))
            for field,actual,expected,atol in [
                ('tc_ms',discrete.tc*1e3,float(row['tc_ms']),2e-7),
                ('Nmax_N',discrete.peakN,float(row['Nmax_N']),2e-5),
                ('vz_out',discrete.vz,float(row['vz_out']),2e-8)]:
                if not _check_close(actual,expected,atol):
                    fails.append({'module':'N3.4 discrete','law':key[1],
                                  'pressure_psi':key[0], 'dt_us':row['dt_us'],
                                  'field':field,'actual':actual,'expected':expected})
        counts['n34']+=1
    for row in load_reference('n36_geometry'):
        a=float(row['alpha'])
        if abs(drilling_arm(a)-float(row['chi_over_a']))>1e-12:
            fails.append({'module':'N3.6','alpha':a,'reason':'chi analytic'})
        if abs(weak_spin_slope(a)-float(row['low_q_M_slope_distributed']))>1e-14:
            fails.append({'module':'N3.6','alpha':a,'reason':'low q slope'})
        # Independent work identity test at q=.1 using preserved code.
        r=distributed_friction(.1,a,nr=64,nt=192)
        if abs(r['dissipation_over_muNs']+r['Fx_over_muN']+.1*r['M_over_muNa'])>1e-11:
            fails.append({'module':'N3.6','alpha':a,'reason':'power identity'})
        counts['n36']+=1
    return {'passed':not fails,'counts':counts,'failures':fails,
            'scope':'Full historical N3.3 grid and N3.4 reference' if full else 'Fast archived subset',
            'is_physical_validation':False}
