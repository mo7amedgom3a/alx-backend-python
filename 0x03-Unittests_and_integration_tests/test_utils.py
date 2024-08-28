#!/usr/bin/env python3
import unittest
from utils import access_nested_map
import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """Test the access_nested_map function."""

    @parameterized.parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2)
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected):
        """Test the access_nested_map function."""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)
