#!/usr/bin/env python3


from typing import Callable
from functools import wraps
import redis
import requests


def requests_counter(method: Callable) -> Callable:
    r = redis.Redis()

    @wraps(method)
    def wrapper(url):
        r.incr(f"count:{url}")
        cached_ = r.get(f"cached:{url}")
        if cached:
            return cached.decode('utf-8')

        html = method(url)
        r.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


def get_page(url: str) -> str:
    resp = requests.get(url)
    return resp.text
