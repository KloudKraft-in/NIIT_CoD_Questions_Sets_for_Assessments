import sys

class DIContainer:
    def __init__(self):
        # Implementation here
        pass

    def register(self, service_name: str, factory_func, singleton: bool = False):
        # Implementation here
        pass

    def resolve(self, service_name: str):
        # Implementation here
        pass

    def clear(self):
        # Implementation here
        pass

if __name__ == "__main__":
    # Command processor for standardized evaluation
    container = DIContainer()
    class Service:
        def __init__(self, name): self.name = name
    
    input_data = sys.stdin.read().splitlines()
    instances = {}
    for line in input_data:
        parts = line.strip().split()
        if not parts: continue
        cmd = parts[0]
        if cmd == "REGISTER":
            s_name, is_singleton = parts[1], parts[2].lower() == "true"
            container.register(s_name, lambda n=s_name: Service(n), is_singleton)
        elif cmd == "RESOLVE":
            try:
                obj = container.resolve(parts[1])
                instances[parts[2]] = obj
                print(f"Resolved {parts[1]} as {parts[2]}")
            except KeyError as e: print(f"ERROR: {e.args[0]}")
        elif cmd == "CHECK_IDENTITY":
            print(instances.get(parts[1]) is instances.get(parts[2]))
        elif cmd == "CLEAR":
            container.clear(); instances.clear()
