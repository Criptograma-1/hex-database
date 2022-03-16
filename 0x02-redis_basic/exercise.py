#!/usr/bin/env python3
"""Redis"""

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

    def get(self, key: str,
            fn: Optional[Callable] = None)
            -> Union[str, bytes, int, float]:
        """Convert the data back to the desired format
            Args:
                key: generated key
                fn:  Callable used to convert the data
            Return:
                Converted data
        """
        data = self._redis.get(key)
        
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Convert data to str"""
        data = self._redis.get(key)

        return data.decode("utf-8")

     def get_int(self, key: str) -> int:
         """Convert data to int"""
         data = self._redis.get(key)

         try:
             data = int(value.decode("utf-8"))
         except Exception:
             data = 0
         
         return data
