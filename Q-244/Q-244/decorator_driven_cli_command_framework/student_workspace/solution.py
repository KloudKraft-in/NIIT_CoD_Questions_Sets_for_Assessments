import sys

class CLIApp:
    def __init__(self):
        # Implementation here
        pass

    def command(self, name: str):
        # Implementation here: return a decorator
        pass

    def run(self, args_list: list):
        # Implementation here: call function with args, handle errors
        pass

if __name__ == "__main__":
    # Command processor for standardized evaluation
    app = CLIApp()
    @app.command("greet")
    def greet(name): return f"Hello, {name}!"
    @app.command("add")
    def add(a, b): return str(int(a) + int(b))

    input_data = sys.stdin.read().splitlines()
    for line in input_data:
        parts = line.strip().split()
        if not parts: continue
        if parts[0] == "RUN": print(app.run(parts[1:]))
