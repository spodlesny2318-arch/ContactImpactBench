"""Validated input facade for the frozen N3.3 implementation.

Deliberately does not claim physical predictive validity or a new solver.
"""
from dataclasses import dataclass, asdict
from math import isfinite
from ._legacy import JoMMS_N3_3_kelvin_consistent as kernel

@dataclass(frozen=True)
class ReducedCase:
    spin_rad_s: float = 20.0
    velocity_m_s: tuple[float, float, float] = (4.0, 0.0, -4.0)
    pressure_pa: float = kernel.P0
    time_step_s: float = 2.0e-6
    maximum_time_s: float = 0.04
    normal_law: str = 'A'
    tangential_damping_ratio: float = 0.25

    def __post_init__(self):
        if not isinstance(self.velocity_m_s, (list, tuple)) or len(self.velocity_m_s) != 3:
            raise ValueError('velocity_m_s needs three components')
        values = [self.spin_rad_s,self.pressure_pa,self.time_step_s,
                  self.maximum_time_s,self.tangential_damping_ratio,*self.velocity_m_s]
        if not all(isfinite(x) for x in values):
            raise ValueError('Inputs must be finite')
        if self.pressure_pa <= 0 or self.time_step_s <= 0 or self.maximum_time_s <= 0:
            raise ValueError('Pressure and time scales must be positive')
        if self.tangential_damping_ratio < 0:
            raise ValueError('Tangential damping ratio must be nonnegative')
        if self.normal_law not in ('A','B'):
            raise ValueError('normal_law must be A or B')
        if self.velocity_m_s[2]>=0:
            raise ValueError('Reference impact requires initial downward normal velocity')
        if self.maximum_time_s/self.time_step_s>1_000_000:
            raise ValueError('Refusing more than 1 million steps in preview API')

def run_impact(case:ReducedCase, *, record=False):
    if not isinstance(case,ReducedCase):
        raise TypeError('Pass ReducedCase')
    return kernel.simulate(case.spin_rad_s,v0=case.velocity_m_s,
        p=case.pressure_pa,dt=case.time_step_s,tmax=case.maximum_time_s,
        normal=case.normal_law,zeta_t=case.tangential_damping_ratio,record=record)

def result_summary(r):
    """Compact, JSON-serializable result of the archived scheme."""
    values=asdict(r)
    values.pop('rows',None)
    values['contact_time_ms']=values.pop('tc')*1000.0
    return values
