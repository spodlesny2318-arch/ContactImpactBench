"""Platform/version metadata for transparent replication (no machine/user paths)."""
from platform import python_version, system, machine
from . import __version__

def environment_info():
    """Return reproducibility metadata without username or local directory paths."""
    import numpy, scipy
    return {
        'software': 'ContactImpactBench',
        'software_version': __version__,
        'python_version': python_version(),
        'platform_system': system(),
        'platform_machine': machine(),
        'numpy_version': numpy.__version__,
        'scipy_version': scipy.__version__,
        'is_physical_validation': False,
    }
