from collections import OrderedDict
import sys
import os

class TopKCache:
    def __init__(self, k):
        pass

    def put(self, key, value):
        pass

    def get(self, key):
        pass

    def get_status(self, key):
        pass    

#NOTE: This is the main function that processes the cache operations.
#Do Not Modify below function.

def process_cache_ops():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    try:
        q = int(input_data[0])
    except:
        return
    cache = None
    for i in range(1, q + 1):
        if i >= len(input_data): break
        line = input_data[i].split()
        if not line: continue
        cmd = line[0]
        try:
            if cmd == "init":
                cache = TopKCache(int(line[1]))
            elif cmd == "put":
                cache.put(line[1], line[2])
            elif cmd == "get":
                res = cache.get(line[1])
                print(res if res is not None else "None")
            elif cmd == "status":
                res = cache.get_status(line[1])
                print(res if res is not None else "None")
        except Exception as e:
            pass

if __name__ == "__main__":
    process_cache_ops()
