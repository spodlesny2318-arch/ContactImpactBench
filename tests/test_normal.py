import pytest
from contactimpactbench import normal_reference,compare_normal
from contactimpactbench.normal import PSI_PA
from contactimpactbench.reference import load_reference

def test_dop853_reference_8psi_A():
    row=next(r for r in load_reference('n34') if r['pressure_psi']=='8.0' and
             r['normal_law']=='A' and r['dt_us']=='2.0')
    result=normal_reference(pressure_pa=8*PSI_PA,law='A')
    assert result['contact_time_ms']==pytest.approx(float(row['tc_ref_ms']),abs=2e-6)
    assert result['peak_normal_force_N']==pytest.approx(float(row['Nmax_ref_N']),abs=2e-3)
    assert result['outbound_normal_velocity_m_s']==pytest.approx(float(row['vz_ref']),abs=2e-6)

def test_normal_method_difference_within_archive():
    row=next(r for r in load_reference('n34') if r['pressure_psi']=='8.0' and
             r['normal_law']=='A' and r['dt_us']=='2.0')
    diff=compare_normal(pressure_pa=8*PSI_PA,law='A',dt=2e-6)['difference']
    assert diff['peak_normal_force_N']==pytest.approx(float(row['Nmax_error_N']),abs=2e-3)
