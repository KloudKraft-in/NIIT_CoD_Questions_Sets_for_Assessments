# import functools
# import sys

# class RetryManager:
#     _enabled = True

#     @staticmethod
#     def setEnabled(flag: bool):
#         # Implementation here
#         pass

#     @staticmethod
#     def isEnabled() -> bool:
#         # Implementation here
#         pass

# def retryable(maxRetries: int):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             # Implementation here
#             pass
#         return wrapper
#     return decorator
import functools
import sys

class RetryManager:
    _enabled = True

    @staticmethod
    def setEnabled(flag: bool):
        RetryManager._enabled = flag

    @staticmethod
    def isEnabled() -> bool:
        return RetryManager._enabled

def retryable(maxRetries: int):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not RetryManager.isEnabled():
                print("Retry disabled")
                return func(*args, **kwargs)
            
            last_exception = None
            for i in range(1, maxRetries + 1):
                try:
                    result = func(*args, **kwargs)
                    if i > 1:
                        print(f"Success after {i} attempts")
                    return result
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {i} failed: {e}")
                    if i == maxRetries:
                        print("ERROR: all retries failed")
                        raise last_exception
            return None
        return wrapper
    return decorator
if __name__ == "__main__":
    # Command processor for standardized evaluation
    input_data = sys.stdin.read().splitlines()
    for line in input_data:
        parts = line.strip().split()
        if not parts:
            continue
        
        cmd = parts[0]
        if cmd == "SET_ENABLED":
            RetryManager.setEnabled(parts[1].lower() == "true")
        elif cmd == "CALL":
            m_retries = int(parts[1])
            m_fails = int(parts[2])
            
            # Simple stateful task for testing
            class SimulatedTask:
                def __init__(self, fail_count):
                    self.fail_count = fail_count
                    self.attempts = 0
                def __call__(self):
                    self.attempts += 1
                    if self.attempts <= self.fail_count:
                        raise ValueError("Transient Error")
                    return "Success"
            
            task = SimulatedTask(m_fails)
            wrapped = retryable(maxRetries=m_retries)(task)
            try:
                wrapped()
            except Exception:
                pass
