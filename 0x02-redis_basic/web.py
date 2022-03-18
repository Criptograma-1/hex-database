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
    def wrapper(url):
        key = "cached:" + url
        data = re.get(key)
        if data:
            return data.decode("utf-8")

        key = "count:" + url
        html = method(url)

        re.incr(count_key)
        re.set(key, html)
        re.expire(key, 10)
        return html
    return 


@count_requests
def get_page(url: str) -> str:
    """ requests module to obtain the HTML
        content of a particular URL and returns it.
    """
    response = requests.get(url)
    return response.text
