#!/usr/bin/env python3
"""
Web cache and tracker module.
"""

import redis
import requests
from functools import wraps
from typing import Callable


def cache_and_track(expiration_time: int = 10) -> Callable:
    """
    Decorator to cache the result of a function and track access count.

    Args:
        expiration_time (int): Cache expiration time in seconds.

    Returns:
        Callable: The decorator function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            redis_client = redis.Redis()
            count_key = f"count:{url}"
            content_key = f"content:{url}"

            redis_client.incr(count_key)

            cached_content = redis_client.get(content_key)
            if cached_content:
                return cached_content.decode('utf-8')

            result = func(url)

            redis_client.setex(content_key, expiration_time, result)

            return result
        return wrapper
    return decorator


@cache_and_track()
def get_page(url: str) -> str:
    """
    Get the HTML content of a particular URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = ("http://slowwly.robertomurray.co.uk/delay/1000/url/"
           "http://www.example.com")

    print("First call (not cached):")
    print(get_page(url)[:100])

    print("\nSecond call (should be cached):")
    print(get_page(url)[:100])

    redis_client = redis.Redis()
    print(f"\nAccess count: "
          f"{redis_client.get(f'count:{url}').decode('utf-8')}")

    print("\nWaiting for cache to expire...")
    import time
    time.sleep(10)

    print("\nCall after cache expiration:")
    print(get_page(url)[:100])

    print(f"\nUpdated access count: "
          f"{redis_client.get(f'count:{url}').decode('utf-8')}")
