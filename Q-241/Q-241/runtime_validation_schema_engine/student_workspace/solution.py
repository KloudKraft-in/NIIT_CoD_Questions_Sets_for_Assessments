import functools
import sys
import json

def validate_schema(schema: dict):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(**kwargs):
            # Implementation here: validate types in kwargs against schema
            pass
        return wrapper
    return decorator

if __name__ == "__main__":
    # Command processor for standardized evaluation
    input_data = sys.stdin.read().splitlines()
    for line in input_data:
        parts = line.strip().split(maxsplit=2)
        if not parts: continue
        cmd = parts[0]
        if cmd == "VALIDATE":
            schema_raw, args = json.loads(parts[1]), json.loads(parts[2])
            type_map = {"int": int, "str": str, "float": float, "bool": bool}
            schema = {k: type_map[v] for k, v in schema_raw.items()}
            @validate_schema(schema)
            def test_func(**kwargs): return "SUCCESS"
            try: print(test_func(**args))
            except TypeError as e: print(f"ERROR: {e}")
