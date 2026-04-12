"""Tests for boolean-like dictionary keys.

This module tests the fix for a bug where dictionary keys like "f", "t",
"true", "false", "null" were incorrectly parsed as boolean/null values
instead of being preserved as strings.

"""

import unittest
import zon


class TestBooleanLikeKeys(unittest.TestCase):
    """Test that boolean-like strings are preserved as dictionary keys."""

    def test_single_char_f_key(self):
        """Key 'f' should not become False."""
        data = {"f": 1}
        encoded = zon.encode(data)
        decoded = zon.decode(encoded)
        self.assertEqual(decoded, data)
        self.assertIn("f", decoded)
        self.assertNotIn(False, decoded)

    def test_single_char_t_key(self):
        """Key 't' should not become True."""
        data = {"t": 1}
        encoded = zon.encode(data)
        decoded = zon.decode(encoded)
        self.assertEqual(decoded, data)
        self.assertIn("t", decoded)
        self.assertNotIn(True, decoded)

    def test_nested_f_key(self):
        """Nested key 'f' should not become False."""
        data = {"a": {"b": {"c": {"d": {"e": {"f": 1}}}}}}
        encoded = zon.encode(data)
        decoded = zon.decode(encoded)
        self.assertEqual(decoded, data)
        # Verify the innermost key is string "f", not False
        inner = decoded["a"]["b"]["c"]["d"]["e"]
        self.assertIn("f", inner)
        self.assertNotIn(False, inner)

    def test_true_key(self):
        """Key 'true' should not become True."""
        data = {"true": 1}
        encoded = zon.encode(data)
        decoded = zon.decode(encoded)
        self.assertEqual(decoded, data)
        self.assertIn("true", decoded)

    def test_false_key(self):
        """Key 'false' should not become False."""
        data = {"false": 1}
        encoded = zon.encode(data)
        decoded = zon.decode(encoded)
        self.assertEqual(decoded, data)
        self.assertIn("false", decoded)

    def test_null_key(self):
        """Key 'null' should not become None."""
        data = {"null": 1}
        encoded = zon.encode(data)
        decoded = zon.decode(encoded)
        self.assertEqual(decoded, data)
        self.assertIn("null", decoded)
        self.assertNotIn(None, decoded)

    def test_none_key(self):
        """Key 'none' should not become None."""
        data = {"none": 1}
        encoded = zon.encode(data)
        decoded = zon.decode(encoded)
        self.assertEqual(decoded, data)
        self.assertIn("none", decoded)

    def test_nil_key(self):
        """Key 'nil' should not become None."""
        data = {"nil": 1}
        encoded = zon.encode(data)
        decoded = zon.decode(encoded)
        self.assertEqual(decoded, data)
        self.assertIn("nil", decoded)

    def test_case_insensitive_keys(self):
        """Case variants should also be preserved as strings."""
        test_cases = [
            {"F": 1},
            {"T": 1},
            {"True": 1},
            {"False": 1},
            {"TRUE": 1},
            {"FALSE": 1},
            {"NULL": 1},
            {"NONE": 1},
            {"Null": 1},
        ]
        for data in test_cases:
            with self.subTest(data=data):
                encoded = zon.encode(data)
                decoded = zon.decode(encoded)
                self.assertEqual(decoded, data)

    def test_multiple_boolean_like_keys(self):
        """Multiple boolean-like keys in same dict."""
        data = {"t": 1, "f": 2, "true": 3, "false": 4, "null": 5}
        encoded = zon.encode(data)
        decoded = zon.decode(encoded)
        self.assertEqual(decoded, data)

    def test_boolean_like_keys_with_boolean_values(self):
        """Boolean-like keys with actual boolean values."""
        data = {"t": True, "f": False, "null": None}
        encoded = zon.encode(data)
        decoded = zon.decode(encoded)
        self.assertEqual(decoded, data)
        # Keys should be strings
        self.assertIn("t", decoded)
        self.assertIn("f", decoded)
        self.assertIn("null", decoded)
        # Values should be booleans/None
        self.assertIs(decoded["t"], True)
        self.assertIs(decoded["f"], False)
        self.assertIs(decoded["null"], None)

    def test_in_table_context(self):
        """Boolean-like keys in tabular data."""
        data = [
            {"f": 1, "t": 2, "value": "a"},
            {"f": 3, "t": 4, "value": "b"},
        ]
        encoded = zon.encode(data)
        decoded = zon.decode(encoded)
        self.assertEqual(decoded, data)


if __name__ == "__main__":
    unittest.main()
