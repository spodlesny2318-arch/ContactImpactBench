from importlib.metadata import version, metadata
from pathlib import Path
import contactimpactbench


def test_package_version_matches():
    assert contactimpactbench.__version__ == '0.1.3'


def test_distributable_has_metadata():
    m = metadata('contactimpactbench')
    assert m['Name'] == 'contactimpactbench'
    assert m['Version'] == '0.1.3'
    assert m['License-Expression'] == 'MIT'
