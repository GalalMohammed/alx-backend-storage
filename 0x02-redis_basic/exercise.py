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
    """Count how many times methods of the Cache class are called.

    Args:
        method (object): Cache method.

    Returns:
        incrementing wrapper.

    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Count how many times methods of the Cache class are called.

        Args:
            self (object): instance.
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


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs for a particular function.

    Args:
        method (object): function.

    Returns:
        wrapper.

    """
    @wraps(method)
    def wrapper(self, *args):
        """add its input parameters to one list in redis
        and store its output into another list.

        Args:
            self (object): instance.
            *args: args list.

        Returns:
            output of wrapped function.

        """
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))
        output = method(self, *args)
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    """Display the history of calls of a particular function.

    Args:
        method (object): function.

    """
    rds = redis.Redis()
    print(method.__qualname__ + " was called "
          + rds.get(method.__qualname__).decode("utf-8") + " times:")
    for inpt, otpt in zip(rds.lrange(method.__qualname__ + ":inputs", 0, -1),
                          rds.lrange(method.__qualname__ + ":outputs", 0, -1)):
        print(f"{method.__qualname__}(*{inpt.decode('utf-8')})"
              + f" -> {otpt.decode('utf-8')}")


class Cache:
    """Cache class for redis client."""

    def __init__(self):
        """__init__ method of Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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

#    @count_calls
#    @call_history
#    def get(self, key: str,
#            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
#        """Retrieve from the server.

#        Args:
#            key (str): key to be retrieved.
#            fn: (object): data format converter.

#        Returns:
#            data.

#        """
#        data = self._redis.get(key)
#        if fn:
#            return fn(data)
#        return data

#    @count_calls
#    @call_history
#    def get_str(self, key: str) -> str:
#        """Retrieve from the server.

#        Args:
#            key (str): key to be retrieved.

#        Returns:
#            data.

#        """
#        return str(self._redis.get(key))

#    @count_calls
#    @call_history
#    def get_int(self, key: str) -> int:
#        """Retrieve from the server.
#
#        Args:
#            key (str): key to be retrieved.
#
#        Returns:
#            data.
#
#        """
#        return int(self._redis.get(key))
