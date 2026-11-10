#!/usr/bin/env python3
"""Capture repeatable CLI and dependency checks from an installed package.

Run using the Python executable from the target virtual environment:
  python tools/verification_record.py --output reports/verification_record.json --full
This tool never reports itself as physical validation and never publishes files.
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def execute(command):
    try:
        run = subprocess.run(command, check=False, capture_output=True, text=True,
                             encoding='utf-8', errors='replace')
    except OSError as exc:
        return {'passed': False, 'exit_code': -1, 'error': str(exc)}
    return {'passed': run.returncode == 0, 'exit_code': run.returncode,
            'stdout': run.stdout.strip(), 'stderr': run.stderr.strip()}


def main(argv=None):
    ap = argparse.ArgumentParser(description='Reproducible CLI verification record')
    ap.add_argument('--full', action='store_true', help='Run 64 historical regression scenarios')
    ap.add_argument('--output', required=True, help='JSON record destination')
    args = ap.parse_args(argv)
    base = [sys.executable, '-m', 'contactimpactbench']
    actions = {
        'environment': base + ['env'],
        'pip_check': [sys.executable, '-m', 'pip', 'check'],
        'impact': base + ['impact', '--spin', '20'],
        'normal': base + ['normal', '--pressure-psi', '8'],
        'friction': base + ['friction', '--q', '1', '--alpha', '0'],
        'regression': base + ['verify'] + (['--full'] if args.full else []),
    }
    steps = {name: execute(cmd) for name, cmd in actions.items()}
    passed = all(x['passed'] for x in steps.values())
    record = {
        'schema_version': '1',
        'capture_timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'software': 'ContactImpactBench', 'is_physical_validation': False,
        'all_steps_passed': passed, 'scope': 'full_64' if args.full else 'fast_9',
        'checks': steps,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({'all_steps_passed': passed, 'output': str(out),
                      'steps': {k:v['exit_code'] for k,v in steps.items()}}, indent=2))
    return 0 if passed else 1

if __name__ == '__main__':
    raise SystemExit(main())
