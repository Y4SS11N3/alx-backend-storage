#!/usr/bin/env python3
"""
Web cache and tracker module.
"""

import redis
import requests
from functools import wraps
from typing import Callable

redis_client = redis.Redis()
"""The module-level Redis instance."""


def cache_and_track(expiration_time: int = 10) -> Callable:
    """
    Decorator to cache the result of a function and track access count.
    Args:
        expiration_time (int): Cache expiration time in seconds.
    Returns:
        Callable: The decorator function.
    """
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str) -> str:
            """
            The wrapper function for caching the output and tracking.
            Args:
                url (str): The URL to fetch and cache.
            Returns:
                str: The HTML content of the URL.
            """
            count_key = f'count:{url}'
            result_key = f'result:{url}'
            # Increment the access count
            redis_client.incr(count_key)
            # Try to get the cached result
            result = redis_client.get(result_key)
            if result:
                return result.decode('utf-8')
            # If not in cache, fetch the page
            result = method(url)
            # Cache the result with expiration
            redis_client.setex(result_key, expiration_time, result)
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
    return requests.get(url).text


if __name__ == "__main__":
    url = (
        "http://slowwly.robertomurray.co.uk/delay/1000/"
        "url/http://www.example.com"
    )
    print(get_page(url))
    print(get_page(url))
    print(get_page(url))
