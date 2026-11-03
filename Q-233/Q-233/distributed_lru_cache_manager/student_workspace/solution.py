from collections import OrderedDict
import sys

class LRUCache:
    def __init__(self, capacity: int):
        # Implementation here
        pass

    def get(self, key):
        # Implementation here
        pass

    def put(self, key, value):
        # Implementation here
        pass

if __name__ == "__main__":
    # Command processor for standardized evaluation
    input_data = sys.stdin.read().splitlines()
    cache = None
    for line in input_data:
        parts = line.strip().split()
        if not parts: continue
        cmd = parts[0]
        if cmd == "INIT":
            cache = LRUCache(int(parts[1]))
        elif cmd == "PUT":
            cache.put(parts[1], parts[2])
        elif cmd == "GET":
            print(cache.get(parts[1]))
