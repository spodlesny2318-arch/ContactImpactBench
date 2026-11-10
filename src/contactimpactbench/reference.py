"""Access to frozen reference CSV tables distributed with the package."""
from importlib.resources import files
import csv
_REFERENCE_FILES={
    'n33':'N33_validation_reference.csv',
    'n34':'N34_normal_reference.csv',
    'n36_geometry':'N36_geometry.csv',
    'n36_patch':'N36_patch.csv',
    'n36_convergence':'N36_convergence.csv',
    'n31_negative':'N31_known_failure.csv',
}

def load_reference(name):
    if name not in _REFERENCE_FILES:
        raise ValueError('Unknown data set. Choose: '+', '.join(sorted(_REFERENCE_FILES)))
    path=files('contactimpactbench.data').joinpath(_REFERENCE_FILES[name])
    with path.open(encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f))

def datasets(): return sorted(_REFERENCE_FILES)
