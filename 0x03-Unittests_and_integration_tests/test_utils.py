#!/usr/bin/env python3
"""
Unit tests for utils.py
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import Mapping, Sequence, Any


class TestAccessNestedMap(unittest.TestCase):
    """Tests the `access_nested_map` function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
            self,
            nested_map: Mapping,
            path: Sequence,
            expected: Any
    ) -> None:
        """Test that the method returns the correct value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Mapping,
            path: Sequence,
            expected_key: str
    ) -> None:
        """Test that a KeyError is raised with the expected message."""
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        self.assertEqual(str(e.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """Tests the `get_json` function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: Mapping) -> None:
        """
        Test that `get_json` returns the expected result
        and mocks the HTTP call.
        """
        # Create a mock response object
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Use patch as a context manager
        with patch('utils.requests.get',
                   return_value=mock_response) as mock_get:
            # Call the function
            result = get_json(test_url)

            # Assert that requests.get was called exactly once
            mock_get.assert_called_once_with(test_url)

            # Assert that the function returned the test_payload
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests the `memoize` decorator."""

    def test_memoize(self) -> None:
        """
        Test that `a_method` is only called once when `a_property`
        is accessed twice.
        """
        class TestClass:
            """A test class for memoization."""
            def a_method(self) -> int:
                """A method that returns 42."""
                return 42

            @memoize
            def a_property(self) -> int:
                """A property that memoizes `a_method`."""
                return self.a_method()

        # Use patch.object as a context manager to mock `a_method`
        with patch.object(
                TestClass, 'a_method', return_value=42
        ) as mock_a_method:
            obj = TestClass()

            # Access the property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Assert that the results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert that `a_method` was called only once
            mock_a_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()