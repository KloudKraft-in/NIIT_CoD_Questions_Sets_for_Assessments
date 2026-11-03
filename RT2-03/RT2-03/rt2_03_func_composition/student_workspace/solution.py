import sys

# Complete the functions below as per the problem statement.

def add(*args):
    """Returns the sum of all arguments."""
    pass

def square(a):
    """Returns the square of a number."""
    pass

def splitter(a):
    """Divides a number by 2 and returns [(a + 1) // 2, (a + 1) // 2]"""
    pass

def my_max(a):
    """Returns the maximum value in a number or list."""
    pass

def my_min(a):
    """Returns the minimum value in a number or list."""
    pass

def compose(*functionsList):
    """Returns a new function representing the composition of functionsList.
    The first function in functionsList handles multiple arguments (*args); 
    subsequent functions take the previous output as a single argument.
    """
    def inner(*args):
        # Implement the composition logic here
        pass
    return inner

def main():
    # Helper map for functions
    func_map = {
        "add": add,
        "square": square,
        "splitter": splitter,
        "my_max": my_max,
        "my_min": my_min
    }
    
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    ptr = 0
    try:
        if ptr >= len(input_data): return
        num_funcs = int(input_data[ptr].strip())
        ptr += 1
        
        selected_funcs = []
        for _ in range(num_funcs):
            if ptr >= len(input_data): break
            fname = input_data[ptr].strip()
            if fname in func_map:
                selected_funcs.append(func_map[fname])
            ptr += 1
            
        composed_fn = compose(*selected_funcs)
        
        if ptr >= len(input_data): return
        num_queries = int(input_data[ptr].strip())
        ptr += 1
        
        for _ in range(num_queries):
            if ptr >= len(input_data): break
            query_args = [int(x) for x in input_data[ptr].strip().split()]
            if selected_funcs:
                print(composed_fn(*query_args))
            ptr += 1
            
    except Exception as e:
        # Traceback will be captured by the driver
        raise e

if __name__ == "__main__":
    main()
