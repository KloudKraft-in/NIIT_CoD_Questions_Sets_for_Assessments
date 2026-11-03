import functools

class CircuitOpenError(Exception):
    def __init__(self, message="Circuit is OPEN - Call Blocked"):
        # TODO: Initialize Exception with correct message
        super().__init__(message)

def circuit_breaker(failure_threshold: int):
    """
    A decorator that monitors failures and "trips" the circuit after threshold is reached.
    When the circuit is OPEN, calls should be blocked (raise CircuitOpenError).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: If circuit is open, raise CircuitOpenError
            # TODO: Try to execute func
            # TODO: On success: reset failure counter
            # TODO: On failure: increment counter, check if it hits threshold
            # TODO: If counter >= threshold, set circuit to OPEN
            pass
        
        # TODO: Initialize wrapper state (failures = 0, is_open = False)
        wrapper.failures = 0
        wrapper.is_open = False
        return wrapper
    return decorator
