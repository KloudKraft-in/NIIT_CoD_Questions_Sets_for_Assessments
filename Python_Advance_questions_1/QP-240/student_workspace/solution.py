import re

class LogForensics:
    def __init__(self):
        # TODO: Initialize internal storage for parsed logs
        pass

    def parse_line(self, line: str) -> dict:
        # TODO: Use regex with named groups (?P<timestamp>, ?P<level>, ?P<component>, ?P<message>)
        # TODO: Return dictionary with extracted fields or None
        pass

    def process_logs(self, log_data: list):
        # TODO: Loop through log_data and parse each line
        pass

    def get_level_statistics(self) -> dict:
        # TODO: Count occurrences of each level
        pass

    def get_component_report(self) -> dict:
        # TODO: Count occurrences of each component
        pass

    def find_errors_by_component(self, component_name: str) -> list:
        # TODO: Return messages with ERROR level for specific component
        pass
