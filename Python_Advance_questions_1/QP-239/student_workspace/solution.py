class DataProcessor:
    def calculate_sum(self, data: list) -> float:
        # TODO: Return sum of numeric list
        pass

    def calculate_average(self, data: list) -> float:
        # TODO: Return average of numeric list. Return 0.0 if empty.
        pass

class AnalyticsManager:
    def __init__(self, processor: DataProcessor):
        # TODO: Initialize with a processor instance (Composition)
        # TODO: Initialize self.records as empty list
        pass

    def add_record(self, value: float):
        # TODO: Append value to self.records
        pass

    def get_stats(self) -> dict:
        # TODO: Use self.processor to get sum and average
        # Return {"sum": total, "avg": avg}
        pass

    def get_performance_flag(self, threshold: float) -> str:
        # TODO: If average > threshold, return "High Performance"
        # Otherwise return "Standard Performance"
        pass
