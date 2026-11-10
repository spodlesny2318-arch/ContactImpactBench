# Reproducibility protocol (v0.1.1)

## Windows PowerShell, Python 3.14

From the unpacked source folder (or the folder with the `.whl` file):

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install .\contactimpactbench-0.1.1-py3-none-any.whl
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m contactimpactbench env
.\.venv\Scripts\python.exe -m contactimpactbench verify --full
```

To capture a machine-readable report from the **source package folder**, run:

```powershell
.\.venv\Scripts\python.exe tools\verification_record.py --full --output reports\windows_verification.json
```

This creates `reports/windows_verification.json` locally. Review before sharing.

## Linux, Python 3.13+

```bash
python3 -m venv .venv
.venv/bin/python -m pip install ./contactimpactbench-0.1.1-py3-none-any.whl
.venv/bin/python -m pip check
.venv/bin/python -m contactimpactbench verify --full
.venv/bin/python tools/verification_record.py --full --output reports/linux_verification.json
```

If installation is offline, the wheel contains **only this package**, not NumPy/SciPy wheels. An offline installation therefore requires NumPy/SciPy pre-installed in the target environment or an offline wheelhouse; document this as *not* a clean independent dependency installation.

## Acceptance matrix

- `python -m pip check` returns success.
- Package CLI `env` runs without errors.
- `impact`, `normal`, `friction` examples work.
- Fast verification reports counts 4/1/4.
- Full verification reports counts 36/24/4 with `passed: true`.
- No known negative fixture is mistaken for validated physics.

## Cross-platform status

On 10 November 2026, v0.1.0 had a clean Windows/Python 3.14 virtual-environment install independently performed by the research user, and passed full 64-case verification. That fact **must not** be mislabeled as a separate user test of *v0.1.1*. Windows re-verification of the new wheel is still necessary.

The local Linux check should report its dependency provenance explicitly (fresh download vs pre-installed scientific packages). No independent third-party scientist usability review has yet been completed.
