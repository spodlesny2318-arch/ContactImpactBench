import json
import math
import subprocess
import sys
import pytest
from contactimpactbench import __version__, ReducedCase, compare_normal, normal_reference
from contactimpactbench.environment import environment_info


def test_release_version_and_privacy_metadata():
    from importlib.metadata import version
    assert __version__ == version('contactimpactbench')
    data = environment_info()
    assert data['software_version'] == __version__
    assert data['is_physical_validation'] is False
    assert 'user' not in data and 'cwd' not in data and 'home' not in data


@pytest.mark.parametrize('value', [float('nan'), float('inf'), -1.])
def test_normal_rejects_nonphysical_pressure(value):
    with pytest.raises(ValueError):
        normal_reference(pressure_pa=value)


def test_normal_rejects_bad_step():
    with pytest.raises(ValueError):
        compare_normal(dt=math.nan)


def test_reduced_rejects_bad_velocity_shape():
    with pytest.raises(ValueError, match='three components'):
        ReducedCase(velocity_m_s=[0, -4])


def test_cli_env_output_is_json():
    run = subprocess.run([sys.executable, '-m', 'contactimpactbench', 'env'],
                         text=True, capture_output=True, check=True)
    assert json.loads(run.stdout)['software_version'] == __version__


def test_cli_invalid_input_has_clean_error():
    run = subprocess.run([sys.executable, '-m', 'contactimpactbench',
                          'impact', '--dt-us', '-2'],
                         text=True, capture_output=True)
    assert run.returncode != 0
    assert 'positive' in run.stderr
    assert 'Traceback' not in run.stderr
