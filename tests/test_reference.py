from contactimpactbench.reference import datasets,load_reference
from contactimpactbench.checks import verify_archive

def test_reference_tables_available():
    assert len(load_reference('n33'))==36
    assert len(load_reference('n34'))==24
    assert len(load_reference('n36_geometry'))==4

def test_fast_archive_verification():
    report=verify_archive(full=False)
    assert report['passed'],report['failures'][:5]
    assert report['counts']=={'n33':4,'n34':1,'n36':4}

def test_known_bad_n31_fixture_is_flagged_not_validated():
    rows=load_reference('n31_negative')
    assert len(rows) >= 3
    baseline=[r for r in rows if r['w3_initial_rad_s']=='0.0']
    assert len(baseline)>=3
    assert min(float(r['largest_step_gain_J']) for r in baseline)>0.49
    assert all(float(r['total_energy_change_J'])<0 for r in baseline)
