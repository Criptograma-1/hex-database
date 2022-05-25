#!/usr/bin/env python3


from typing import Callable
from functools import wraps
import redis
import requests


def requests_counter(method: Callable) -> Callable:
    r = redis.Redis()

    @wraps(method)
    def wrapper(url):
        cached = r.get(f"cached:{url}")
        if cached:
            return cached.decode('utf-8')

        html = method(url)
        r.incr(f"count:{url}")
        r.set(f"cached:{url}", html)
        r.expire(f"cached:{url}", timedelta(seconds=10))
        return html

    return wrapper

@requests_counter
def get_page(url: str) -> str:
    resp = requests.get(url)
    return resp.text
