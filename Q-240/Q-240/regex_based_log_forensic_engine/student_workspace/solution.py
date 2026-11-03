import re
import sys

class LogForensics:
    def __init__(self):
        # Implementation here: use a regex with named groups
        pass

    def parse_line(self, line: str) -> dict:
        # Implementation here
        pass

    def process_logs(self, log_data: list):
        # Implementation here
        pass

    def get_level_statistics(self) -> dict:
        # Implementation here
        pass

    def get_component_report(self) -> dict:
        # Implementation here
        pass

    def find_errors_by_component(self, component_name: str) -> list:
        # Implementation here
        pass

if __name__ == "__main__":
    # Command processor for standardized evaluation
    forensics = LogForensics()
    input_data = sys.stdin.read().splitlines()
    for line in input_data:
        parts = line.strip().split(maxsplit=1)
        if not parts: continue
        cmd = parts[0]
        if cmd == "LOG": forensics.process_logs([parts[1]])
        elif cmd == "STATS":
            stats = forensics.get_level_statistics() or {}
            for k in sorted(stats.keys()): print(f"{k}: {stats[k]}")
        elif cmd == "REPORT":
            report = forensics.get_component_report() or {}
            for k in sorted(report.keys()): print(f"{k}: {report[k]}")
        elif cmd == "ERRORS":
            errors = forensics.find_errors_by_component(parts[1]) or []
            for e in errors: print(f"ERROR: {e}")
