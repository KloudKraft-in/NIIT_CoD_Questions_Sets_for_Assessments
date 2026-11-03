import sys

class DataProcessor:
    def calculate_sum(self, data: list) -> float:
        # Implementation here
        pass

    def calculate_average(self, data: list) -> float:
        # Implementation here
        pass

class AnalyticsManager:
    def __init__(self, processor: DataProcessor):
        # Implementation here: use composition
        pass

    def add_record(self, value: float):
        # Implementation here
        pass

    def get_stats(self) -> dict:
        # Implementation here: use self.processor
        pass

    def get_performance_flag(self, threshold: float) -> str:
        # Implementation here: use self.processor
        pass

if __name__ == "__main__":
    # Command processor for standardized evaluation
    processor = DataProcessor()
    manager = AnalyticsManager(processor)
    input_data = sys.stdin.read().splitlines()
    for line in input_data:
        parts = line.strip().split()
        if not parts: continue
        cmd = parts[0]
        if cmd == "ADD": manager.add_record(float(parts[1]))
        elif cmd == "STATS":
            stats = manager.get_stats()
            print(f"Sum: {stats['sum']:.1f}, Avg: {stats['avg']:.1f}")
        elif cmd == "PERF": print(manager.get_performance_flag(float(parts[1])))
