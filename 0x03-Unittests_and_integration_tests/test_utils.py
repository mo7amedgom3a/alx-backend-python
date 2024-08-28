#!/usr/bin/env python3
import unittest
from utils import access_nested_map
import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2)
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected_output):
        """_summary_
        """
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected_output)
