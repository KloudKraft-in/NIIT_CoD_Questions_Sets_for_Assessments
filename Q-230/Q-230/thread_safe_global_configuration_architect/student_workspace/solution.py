import json
import sys

class ConfigLoader:
    # Use __new__ to implement Singleton
    def __new__(cls):
        # Implementation here
        pass

    def load_from_dict(self, data: dict):
        # Implementation here
        pass

    def load_from_json(self, json_str: str):
        # Implementation here
        pass

    def get(self, key, default=None):
        # Implementation here
        pass

    def clear(self):
        # Implementation here
        pass

if __name__ == "__main__":
    # Command processor for standardized evaluation
    input_data = sys.stdin.read().splitlines()
    for line in input_data:
        parts = line.strip().split(maxsplit=1)
        if not parts: continue
        cmd = parts[0]
        if cmd == "LOAD_DICT":
            data = json.loads(parts[1])
            ConfigLoader().load_from_dict(data)
        elif cmd == "LOAD_JSON":
            ConfigLoader().load_from_json(parts[1])
        elif cmd == "GET":
            print(ConfigLoader().get(parts[1], "NOT_FOUND"))
        elif cmd == "CLEAR":
            ConfigLoader().clear()
        elif cmd == "CHECK_SINGLETON":
            c1 = ConfigLoader()
            c2 = ConfigLoader()
            print(c1 is c2)
