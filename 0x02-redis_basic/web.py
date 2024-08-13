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


def cache_and_track(method: Callable) -> Callable:
    """
    Decorator to cache the result of a function and track access count.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: The decorator function.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        The wrapper function for caching the output and tracking.
        Args:
            url (str): The URL to fetch and cache.
        Returns:
            str: The HTML content of the URL.
        """
        redis_client.incr(f'count:{url}')
        result = redis_client.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_client.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@cache_and_track
def get_page(url: str) -> str:
    """
    Get the HTML content of a particular URL.
    Args:
        url (str): The URL to fetch.
    Returns:
        str: The HTML content of the URL.
    """
    return requests.get(url).text
