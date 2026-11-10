import pytest
from contactimpactbench import ReducedCase,run_impact
from contactimpactbench.reference import load_reference

def test_reduced_archived_spin_20():
    rows=load_reference('n33')
    row=next(r for r in rows if r['spin_rad_s']=='20.0' and r['dt_us']=='2.0' and
             r['zeta_t']=='0.25' and not r['normal_law'])
    r=run_impact(ReducedCase(spin_rad_s=20.0,pressure_pa=float(row['pressure_psi'])*6894.757293168))
    assert r.vy==pytest.approx(float(row['vy_out']),abs=1e-8)
    assert r.peakFt==pytest.approx(float(row['Ft_peak_N']),abs=1e-5)
    assert r.positive_sum<=1e-9
    assert r.residual_max<=1e-9
    assert r.max_phi<=1+1e-10

def test_invalid_parameters():
    with pytest.raises(ValueError):ReducedCase(time_step_s=-1.)
    with pytest.raises(ValueError):ReducedCase(normal_law='C')
    with pytest.raises(ValueError):ReducedCase(tangential_damping_ratio=-.2)
