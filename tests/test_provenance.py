from pathlib import Path
import hashlib,csv

def test_frozen_source_checksums_match_manifest():
    root=Path(__file__).resolve().parents[1]
    with (root/'provenance/SOURCES_SHA256.csv').open(newline='',encoding='utf-8') as fh:
        rows=list(csv.DictReader(fh))
    assert len(rows)==3
    for r in rows:
        path=root/r['relative_path']
        assert path.exists()
        assert hashlib.sha256(path.read_bytes()).hexdigest()==r['sha256']
