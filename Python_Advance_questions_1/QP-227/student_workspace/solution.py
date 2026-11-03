import functools

class RetryManager:
    _enabled = True

    @staticmethod
    def setEnabled(flag: bool):
        # TODO: Set the class-level _enabled flag
        pass

    @staticmethod
    def isEnabled() -> bool:
        # TODO: Return the current state of _enabled
        pass

def retryable(maxRetries: int):
    """
    A decorator that automatically retries failed operations.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: If RetryManager is disabled, print "Retry disabled" and run func once
            # TODO: If enabled, loop up to maxRetries times
            # TODO: On each failure: print "Attempt i failed: <error>"
            # TODO: On success after i attempts (where i > 1): print "Success after i attempts"
            # TODO: If all retries fail: print "ERROR: all retries failed" and re-raise
            pass
        return wrapper
    return decorator
