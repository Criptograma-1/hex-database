#!/usr/bin/env python3

""" Implementing an expiring web cache and tracker
    obtain the HTML content of a particular URL and returns it """
import redis
import requests
rd = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """ track how many times a particular URL was accessed in the key
        "count:{url}"
        and cache the result with an expiration time of 10 seconds """
    rd.set(f"cached:{url}", count)
    resp = requests.get(url)
    rd.incr(f"count:{url}")
    rd.setex(f"cached:{url}", 10, rd.get(f"cached:{url}"))
    return resp.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
