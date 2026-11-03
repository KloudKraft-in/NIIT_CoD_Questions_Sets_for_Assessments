import sys

# Already implemented Limit class
class Limit:
    _limit = 0
    @classmethod
    def set_limit(cls, value):
        cls._limit = value
    @classmethod
    def get_limit(cls):
        return cls._limit

# Complete the classes 'UserLimitExceeded' and 'Product' below.

class UserLimitExceeded(Exception):
    # Implement custom exception
    pass

class Product:
    # Tracks the number of active Product instances
    _active_instances = 0
    
    def __init__(self, name):
        """Initializes the product with a name.
        Checks if creating a new instance exceeds Limit.get_limit().
        Increments _active_instances on success.
        Raises UserLimitExceeded on failure.
        """
        # Implementation here
        pass

    def __del__(self):
        """Decrements _active_instances when the product instance is deleted."""
        # Implementation here
        pass

def main():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
        
    try:
        ptr = 0
        initial_limit = int(input_data[ptr].strip())
        Limit.set_limit(initial_limit)
        ptr += 1
        
        num_ops = int(input_data[ptr].strip())
        ptr += 1
        
        products = {} # name -> instance
        
        for _ in range(num_ops):
            if ptr >= len(input_data): break
            line = input_data[ptr].strip().split(None, 1)
            cmd = line[0]
            arg = line[1] if len(line) > 1 else ""
            ptr += 1
            
            try:
                if cmd == "new":
                    products[arg] = Product(arg)
                elif cmd == "del":
                    if arg in products:
                        # Explicitly delete the product to trigger __del__
                        del products[arg]
                        print(f"{arg} deleted successfully")
                    else:
                        print(f"{arg} not found")
                elif cmd == "limit":
                    Limit.set_limit(int(arg))
                    print(f"limit updated to {arg}")
                elif cmd == "print":
                    if arg in products:
                        print(f"{arg} found")
                    else:
                        print(f"{arg} not found")
            except UserLimitExceeded as e:
                print(e)
            except Exception:
                pass
                
    except Exception as e:
        raise e

if __name__ == "__main__":
    main()
