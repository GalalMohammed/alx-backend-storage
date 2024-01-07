#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module defines a Cache class.

Example:
    cache = Cache()

"""


import uuid
from typing import Union
import redis


class Cache:
    """Cache class."""

    def __init__(self) -> None:
        """__init__ method."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[bytes, str, int, float]) -> str:
        """Store the input data in Redis using a random key.

        Args:
            data (object): input data.

        Returns:
            the key.

        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
