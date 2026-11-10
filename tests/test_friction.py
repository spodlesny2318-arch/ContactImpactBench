import pytest
from contactimpactbench import distributed_friction,drilling_arm,weak_spin_slope,friction_ellipsoid
from contactimpactbench.reference import load_reference

@pytest.mark.parametrize('alpha',[0.,.5,1.,2.])
def test_n36_analytic(alpha):
    row=next(r for r in load_reference('n36_geometry') if float(r['alpha'])==alpha)
    assert drilling_arm(alpha)==pytest.approx(float(row['chi_over_a']),abs=1e-13)
    assert weak_spin_slope(alpha)==pytest.approx(float(row['low_q_M_slope_distributed']),abs=1e-13)

def test_distributed_vs_ellipse_at_q1():
    row=next(r for r in load_reference('n36_patch') if float(r['alpha'])==0. and float(r['q'])==1.)
    d=distributed_friction(1.,0.)
    e=friction_ellipsoid(1.,0.)
    assert d['Fx_over_muN']==pytest.approx(float(row['Fx_distributed_over_muN']),abs=5e-6)
    assert d['M_over_muNa']==pytest.approx(float(row['M_distributed_over_muNa']),abs=5e-6)
    assert d['dissipation_over_muNs']>=0
    assert abs(d['dissipation_over_muNs']+d['Fx_over_muN']+d['M_over_muNa'])<1e-12
    assert abs(e['M_over_muNa']-d['M_over_muNa'])>0.01
