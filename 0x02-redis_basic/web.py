#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

import redis
import requests

redis = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """
    Method to track how many times a particular URL was accessed
    and cache the result with an expiration time of 10 seconds.
    """
    redis.set(f"cached:{url}", count)
    response = requests.get(url)
    redis.incr(f"count:{url}")
    redis.setex(f"cached:{url}", 10, redis.get(f"cached:{url}"))

    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
