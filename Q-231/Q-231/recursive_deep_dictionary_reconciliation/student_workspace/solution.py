import copy
import json
import sys

class MergeConflictError(Exception):
    def __init__(self, message):
        # Implementation here
        pass

class ConfigMerger:
    def __init__(self, initial_data: dict):
        # Implementation here
        pass

    def recursive_merge(self, current: dict, update: dict) -> dict:
        # Implementation here
        pass

    def apply_update(self, update_data: dict) -> str:
        # Implementation here
        pass

    def get_config(self) -> dict:
        # Implementation here
        pass

if __name__ == "__main__":
    # Command processor for standardized evaluation
    input_data = sys.stdin.read().splitlines()
    merger = None
    for line in input_data:
        parts = line.strip().split(maxsplit=1)
        if not parts: continue
        cmd = parts[0]
        if cmd == "INIT":
            data = json.loads(parts[1])
            merger = ConfigMerger(data)
        elif cmd == "UPDATE":
            data = json.loads(parts[1])
            print(merger.apply_update(data))
        elif cmd == "GET":
            print(json.dumps(merger.get_config(), sort_keys=True))
