import time
import functools

class RateLimitExceededError(Exception):
    # TODO: Implement this class
    pass

class RateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        # TODO: Initialize capacity, refill_rate, current tokens, and last refill time
        pass

    def _refill(self):
        # TODO: Calculate time elapsed since last refill
        # TODO: Add tokens based on refill_rate * elapsed_time
        # TODO: Do not exceed capacity
        pass

    def consume(self) -> bool:
        # TODO: Call _refill()
        # TODO: If tokens >= 1, decrement and return True, else return False
        pass

def rate_limited(limiter: RateLimiter):
    # TODO: Implement a decorator that uses the limiter to control function calls
    # TODO: If consume() is False, raise RateLimitExceededError
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Add rate limiting logic
            pass
        return wrapper
    return decorator
