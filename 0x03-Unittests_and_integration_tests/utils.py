#!/usr/bin/env python3
"""
A module with utility functions.
"""
import requests
from functools import wraps
from typing import (
    Mapping,
    Sequence,
    Any,
    Callable
)


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access a value in a nested map using a sequence of keys.

    Args:
        nested_map (Mapping): The dictionary to access.
        path (Sequence): A sequence of keys representing the path.

    Returns:
        Any: The value at the end of the path.

    Raises:
        KeyError: If a key in the path is not found.
    """
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        try:
            nested_map = nested_map[key]
        except KeyError:
            raise KeyError(key)
    return nested_map


def get_json(url: str) -> Mapping:
    """
    Fetch JSON from a URL.

    Args:
        url (str): The URL to send a GET request to.

    Returns:
        Mapping: The JSON content of the response.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    return response.json()


def memoize(fn: Callable) -> Callable:
    """
    A decorator to memoize a function's output.
    """
    attr_name = f"_{fn.__name__}"

    @wraps(fn)
    def wrapper(self):
        """
        The wrapper function for memoization.
        It checks if the result is already stored in the instance.
        """
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(wrapper)