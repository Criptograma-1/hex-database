#!/usr/bin/env python3
"""
sample use case of caching
"""

from requests import get
import redis
from functools import wraps


def count_decorator(method: callable) -> callable:
    """
    decorator to enable caching
    """
    @wraps(method)
    def cache(url):
        """
        wrapper function
        """
        cache = redis.Redis()
        key = "count:{}".format(url)
        if not cache.exists(key):
            cache.setex(key, 10, 1)
        else:
            cache.incr(key)
        return method(url)
    return cache


@count_decorator
def get_page(url: str) -> str:
    """
    retrives the content of an html page, and also caches it
    """
    html = get(url)
    return html.content
