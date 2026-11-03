import sys

# Complete the 'sequence_generator' class below.
#
# The class should be a context manager and expose 'generate' and 'reset' methods.

class sequence_generator:
    def __init__(self, start, step):
        """Initializes the sequence with start and step."""
        # Implementation here
        pass
        
    def __enter__(self):
        """
        1. Prints: [CONTEXT] Initializing Sequence
        2. Returns: The instance of sequence_generator.
        """
        # Implementation here
        pass
        
    def generate(self, n):
        """
        A generator method that yields the next n numbers in the sequence.
        Updates internal state and total count.
        """
        # Implementation here
        pass
            
    def reset(self):
        """Resets the current sequence value back to start."""
        # Implementation here
        pass
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Prints: [CONTEXT] Final Count: {total_count}"""
        # Implementation here
        pass

def main():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
        
    try:
        ptr = 0
        start = int(input_data[ptr].strip())
        ptr += 1
        step = int(input_data[ptr].strip())
        ptr += 1
        num_batches = int(input_data[ptr].strip())
        ptr += 1
        
        with sequence_generator(start, step) as sg:
            for _ in range(num_batches):
                if ptr >= len(input_data):
                    break
                line = input_data[ptr].strip().split()
                if not line:
                    ptr += 1
                    continue
                    
                n = int(line[0])
                # Check for RESET keyword in the line
                if "RESET" in [x.upper() for x in line]:
                    sg.reset()
                
                # Use the generator method
                for val in sg.generate(n):
                    print(val)
                ptr += 1
                
    except Exception as e:
        # Traceback will be captured by driver
        raise e

if __name__ == "__main__":
    main()
