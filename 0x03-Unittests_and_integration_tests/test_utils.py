#!/usr/bin/env python3
"""
Unit tests for utils.py
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


# --- Task 0 & 1 ---
class TestAccessNestedMap(unittest.TestCase):
    """Tests the `access_nested_map` function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that the method returns the correct value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that a KeyError is raised for the given inputs."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # Check that the exception message is the last key in the path
        self.assertEqual(cm.exception.args[0], path[-1])


# --- Task 2 ---
class TestGetJson(unittest.TestCase):
    """Tests the `get_json` function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test that `get_json` returns the expected result
        and mocks the HTTP call.
        """
        # Create a mock response object
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Use patch as a context manager
        with patch('utils.requests.get', return_value=mock_response) as mock_get:
            # Call the function
            result = get_json(test_url)

            # Assert that requests.get was called exactly once with the test_url
            mock_get.assert_called_once_with(test_url)
            
            # Assert that the function returned the test_payload
            self.assertEqual(result, test_payload)


# --- Task 3 ---
class TestMemoize(unittest.TestCase):
    """Tests the `memoize` decorator."""

    def test_memoize(self):
        """
        Test that `a_method` is only called once when `a_property`
        is accessed twice.
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Use patch.object as a context manager to mock `a_method`
        with patch.object(TestClass, 'a_method',
                         return_value=42) as mock_a_method:
            obj = TestClass()

            # Access the property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Assert that the results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert that `a_method` was called only once
            mock_a_method.assert_called_once()