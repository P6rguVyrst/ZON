"""
Roundtrip tests for all benchmark datasets.

Validates that ZON encoding is lossless by checking encode -> decode -> compare.
"""
import json
import unittest
from pathlib import Path

import zon


BENCHMARKS_DATA_DIR = Path(__file__).parent.parent.parent / 'benchmarks' / 'data'


def get_json_files():
    """Return all JSON files in benchmarks/data except questions."""
    return sorted(
        f for f in BENCHMARKS_DATA_DIR.glob('*.json')
        if 'questions' not in f.name
    )


class TestRoundtripBenchmarks(unittest.TestCase):
    """Test roundtrip encoding for all benchmark datasets."""
    pass


def _make_test(filepath):
    def test_roundtrip(self):
        with open(filepath) as f:
            original = json.load(f)

        encoded = zon.encode(original)
        decoded = zon.decode(encoded)

        orig_json = json.dumps(original, sort_keys=True)
        dec_json = json.dumps(decoded, sort_keys=True)

        self.assertEqual(
            orig_json, dec_json,
            f"Roundtrip failed for {filepath.name}"
        )
    return test_roundtrip


for filepath in get_json_files():
    test_name = f'test_roundtrip_{filepath.stem.replace("-", "_")}'
    setattr(TestRoundtripBenchmarks, test_name, _make_test(filepath))


if __name__ == '__main__':
    unittest.main()
