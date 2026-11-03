import time
import functools
import sys

class RateLimitExceededError(Exception):
    def __init__(self, message="Rate limit exceeded - Try later"):
        # Implementation here
        pass

class RateLimiter:
    def __init__(self, capacity, refill_rate):
        # Implementation here
        pass

    def _refill(self):
        # Implementation here
        pass

    def consume(self) -> bool:
        # Implementation here
        pass

def rate_limited(limiter: RateLimiter):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Implementation here
            pass
        return wrapper
    return decorator

if __name__ == "__main__":
    # Command processor for standardized evaluation
    input_data = sys.stdin.read().splitlines()
    limiter = None
    
    # We use a MockLimiter in evaluation for timing predictability
    class MockLimiter(RateLimiter):
        def __init__(self, capacity, refill_rate):
            super().__init__(capacity, refill_rate)
            self.current_time = 1000.0
            self.last_refill_time = 1000.0
        def _refill(self):
            elapsed = self.current_time - self.last_refill_time
            new_tokens = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + new_tokens)
            self.last_refill_time = self.current_time

    for line in input_data:
        parts = line.strip().split()
        if not parts: continue
        cmd = parts[0]
        if cmd == "INIT":
            cap, rate = float(parts[1]), float(parts[2])
            limiter = MockLimiter(cap, rate)
            print(f"Limiter initialized: cap={cap}, rate={rate}")
        elif cmd == "CALL":
            try:
                if limiter.consume(): print("SUCCESS")
                else: raise RateLimitExceededError()
            except RateLimitExceededError as e:
                print(f"ERROR: {e}")
        elif cmd == "SLEEP":
            limiter.current_time += float(parts[1])
