#!/usr/bin/env python3
"""Writing strings to Redis"""

from typing import Union
import redis
import uuid


class Cache:

    def __init__(self):
        """Constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()


    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store the input data in Redis using the random key
            Args:
                -data: data to be stored
            Return:
                -the random generate key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key
