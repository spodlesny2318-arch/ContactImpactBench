from importlib.metadata import version, metadata
from pathlib import Path
import contactimpactbench


def test_package_version_matches():
    assert contactimpactbench.__version__ == '0.1.4'


def test_distributable_has_metadata():
    m = metadata('contactimpactbench')
    assert m['Name'] == 'contactimpactbench'
    assert m['Version'] == '0.1.4'
    assert m['License-Expression'] == 'MIT'


def test_citable_authors_in_distribution_metadata():
    m = metadata('contactimpactbench')
    author_text = ' '.join(m.get_all('Author') or [])
    for name in ('Serhii Podliesnyi', 'Oksana Chmykhova', 'Bohdan Vorobiov'):
        assert name in author_text
