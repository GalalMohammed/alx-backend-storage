#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module defines a Cache class.

Example:
    cache = Cache()

"""


import uuid
from typing import Union, Optional
from collections.abc import Callable
import redis


class Cache:
    """Cache class."""

    def __init__(self) -> None:
        """__init__ method."""
        self._redis = redis.Redis()
        self._redis.flushdb()

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

    def get_str(self, key: str) -> str:
        """Retrieve from the server.

        Args:
            key (str): key to be retrieved.

        Returns:
            data.

        """
        return str(self._redis.get(key))
    
    def get_int(self, key: str) -> int:
        """Retrieve from the server.

        Args:
            key (str): key to be retrieved.

        Returns:
            data.

        """
        return int(self._redis.get(key))
