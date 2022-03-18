#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

import redis
import requests
from typing import Callable
from functools import wraps
from datetime import timedelta

re = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """ Counting with decorators how many times a request
        has been made
    """
    @wraps(method)
    def wrapper(*args, **kwds):
        re.incr("count:{}".format(args[0]), 1)
        return method(*args, **kwds)
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ requests module to obtain the HTML
        content of a particular URL and returns it.
    """
   if not re.exists(url):
        response = requests.get(url)
        re.setex(url, timedelta(seconds=10), response.content)
        return response.content
    return re.get(url)
