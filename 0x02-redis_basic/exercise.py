#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module defines a Cache class.

Example:
    cache = Cache()

"""


import uuid
from functools import wraps
from typing import Union, Optional
from collections.abc import Callable
import redis


def count_calls(method: Callable) -> Callable:
    """count how many times methods of the Cache class are called.

    Args:
        method (object): Cache method.

    Returns:
        incrementing wrapper.

    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Count how many times methods of the Cache class are called.

        Args:
            self: instance.
            *args: Variable length argument list.
            **kwds: keyword arguments.

        Returns:
            value returned by original method.

        """
        if self._redis.exists(method.__qualname__):
            self._redis.incr(method.__qualname__)
        else:
            self._redis.set(method.__qualname__, 1)
        return method(self, *args, **kwds)
    return wrapper


class Cache:
    """Cache class."""

    def __init__(self) -> None:
        """__init__ method."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the input data in Redis using a random key.

        Args:
            data (object): input data.

        Returns:
            the key.

        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    @count_calls
    def get(self, key: str,
            fn:Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Retrieve from the server.

        Args:
            key (str): key to be retrieved.
            fn: (object): data format converter.

        Returns:
            data.

        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    @count_calls
    def get_str(self, key: str) -> str:
        """Retrieve from the server.

        Args:
            key (str): key to be retrieved.

        Returns:
            data.

        """
        return str(self._redis.get(key))
    
    @count_calls
    def get_int(self, key: str) -> int:
        """Retrieve from the server.

        Args:
            key (str): key to be retrieved.

        Returns:
            data.

        """
        return int(self._redis.get(key))
