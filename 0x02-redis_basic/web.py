#!/usr/bin/env python3

"""
method that implements an expiring web cache and tracker
"""

from typing import Callable
from functools import wraps
import redis
import requests


def requests_counter(method: Callable) -> Callable:
    """ Counts how many times a request has been made
    """
    rd = redis.Redis()

    @wraps(method)
    def wrapper(url):
        """ wrapper fxn that counts actual no of requests made"""
        rd.incr(f"count:{url}")
        cached = rd.get(f"cached:{url}")
        if cached:
            return cached.decode('utf-8')

        cached = method(url)
        rd.setex(f"cached:{url}", 10, cached)
        return cached

    return wrapper


@requests_counter
def get_page(url: str) -> str:
    """ obtains html content for a given site url and returns it.
    """
    resp = requests.get(url)
    return resp.text
