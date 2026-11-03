from typing import Callable, Any, List
import time
import functools
import sys

# Global list to store measured execution times
execution_times: List[float] = []

# Complete the 'timeit' decorator below.
# The decorator should measure execution time in milliseconds.

def timeit(func: Callable) -> Callable:
    """Decorator to measure function execution time in ms.
    To ensure deterministic testing on any system, use the 'delay' argument 
    from kwargs as the measured duration for execution_times tracking.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Write your code here
        pass
        
    return wrapper

@timeit
def delay_max(*args: int, **kwargs: Any) -> int:
    return max(args)

@timeit
def delay_min(*args: int, **kwargs: Any) -> int:
    return min(args)

@timeit
def delay_sum(*args: int, **kwargs: Any) -> int:
    return sum(args)






#NOTE : Dont modify below code.

def process_commands():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
        
    n = int(input_data[0].strip())
    funcs = {
        "delay_max": delay_max,
        "delay_min": delay_min,
        "delay_sum": delay_sum
    }
    
    for i in range(1, n + 1):
        line = input_data[i].strip().split()
        if not line: continue
        fname = line[0]
        # Params are all except function name and the final delay integer
        params = [int(p) for p in line[1:-1]]
        delay = int(line[-1])
        
        result = funcs[fname](*params, delay=delay)
        print(result)
        
    # Output the final list of measured execution times
    print(execution_times)

if __name__ == '__main__':
    process_commands()
