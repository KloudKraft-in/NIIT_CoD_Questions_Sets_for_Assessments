import functools
import sys

class CircuitOpenError(Exception):
    def __init__(self, message="Circuit is OPEN - Call Blocked"):
        # Implementation here
        pass

def circuit_breaker(failure_threshold: int):
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
    services = {}
    for line in input_data:
        parts = line.strip().split()
        if not parts: continue
        cmd = parts[0]
        if cmd == "CALL":
            s_name = parts[1]
            threshold = int(parts[2])
            action = parts[3]
            if s_name not in services:
                def base_task(act):
                    if act == "FAIL": raise ValueError("Service Error")
                    return "Success"
                services[s_name] = circuit_breaker(failure_threshold=threshold)(base_task)
            try:
                print(services[s_name](action))
            except CircuitOpenError as e:
                print(f"ERROR: {e}")
            except Exception as e:
                print(f"FAIL: {e}")
