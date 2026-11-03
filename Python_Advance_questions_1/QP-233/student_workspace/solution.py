from collections import OrderedDict
import functools

class LRUCache:
    def __init__(self, capacity: int):
        # TODO: Initialize OrderedDict with capacity
        pass

    def get(self, key):
        # TODO: If key exists, move to end (MRU) and return value
        # TODO: If key missing, return -1
        pass

    def put(self, key, value):
        # TODO: If key exists, update value and move to end
        # TODO: If new key: add to end, if over capacity pop first (LRU)
        pass

def lru_cache_custom(capacity: int):
    """
    A decorator that uses an LRUCache instance to cache function results.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Use cache to avoid re-calls
            pass
        return wrapper
    return decorator
