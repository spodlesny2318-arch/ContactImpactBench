"""Independent DOP853 normal-contact ODE extracted from N3.4.

Same model A/B and parameter values; different time integrator and event
localisation. This is a numerical-method comparator, not an experiment.
"""
from math import pi, isfinite
import numpy as np
from scipy.integrate import solve_ivp
from .reduced import ReducedCase, run_impact
from ._legacy import JoMMS_N3_3_kelvin_consistent as k

PSI_PA=6894.757293168

def normal_reference(*,pressure_pa=8*PSI_PA, law='A', inbound_speed_m_s=4.0):
    if not all(isfinite(x) and x > 0 for x in (pressure_pa, inbound_speed_m_s)) or law not in ('A','B'):
        raise ValueError('Require positive pressure, speed and law A/B')
    kn=2*pi*k.R*pressure_pa
    def slope(d):
        return kn*d if law=='A' else pi*pressure_pa*(2*k.R*d-d*d)
    def rhs(t,y):
        indentation,v=y
        delta=max(0.0,indentation)
        force=max(0.0,slope(delta)+k.c_hc*delta*(-v))
        return [-v,force/k.m]
    def lift(t,y): return y[0]
    lift.direction=-1;lift.terminal=True
    init=[1e-10,-float(inbound_speed_m_s)]
    sol=solve_ivp(rhs,(0,0.04),init,method='DOP853',rtol=2e-11,
        atol=2e-13,max_step=1.5e-5,events=lift,dense_output=True)
    if not sol.success or len(sol.t_events[0])!=1:
        raise RuntimeError('Normal reference did not locate one lift-off event')
    duration=float(sol.t_events[0][0])
    samples=np.linspace(0,duration,10001)
    y=sol.sol(samples)
    force=np.maximum(0.0,np.array([slope(max(0.0,d)) for d in y[0]])+
        k.c_hc*np.maximum(0.0,y[0])*(-y[1]))
    return {'contact_time_ms':duration*1000.0,'peak_normal_force_N':float(np.max(force)),
            'outbound_normal_velocity_m_s':float(sol.y_events[0][0][1]),
            'method':'DOP853, event-located', 'physical_validation':False}

def compare_normal(*,pressure_pa=8*PSI_PA,law='A',dt=2e-6,
                   inbound_speed_m_s=4.0):
    if not isfinite(dt) or dt <= 0:
        raise ValueError('dt must be finite and positive')
    ref=normal_reference(pressure_pa=pressure_pa,law=law,inbound_speed_m_s=inbound_speed_m_s)
    r=run_impact(ReducedCase(spin_rad_s=0.,velocity_m_s=(0.,0.,-inbound_speed_m_s),
        pressure_pa=pressure_pa,normal_law=law,time_step_s=dt,tangential_damping_ratio=0.))
    return {'reference':ref,'discrete':{'contact_time_ms':r.tc*1000.0,
            'peak_normal_force_N':r.peakN,'outbound_normal_velocity_m_s':r.vz},
            'difference':{'contact_time_ms':r.tc*1000.0-ref['contact_time_ms'],
            'peak_normal_force_N':r.peakN-ref['peak_normal_force_N'],
            'outbound_normal_velocity_m_s':r.vz-ref['outbound_normal_velocity_m_s']}}
