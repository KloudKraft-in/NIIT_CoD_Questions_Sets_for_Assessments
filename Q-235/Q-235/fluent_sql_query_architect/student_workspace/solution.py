import sys

class QueryBuilder:
    def __init__(self):
        # Implementation here
        pass

    def select(self, *columns):
        # Implementation here
        return self

    def from_table(self, table_name: str):
        # Implementation here
        return self

    def where(self, column: str, operator: str, value):
        # Implementation here
        return self

    def build(self) -> str:
        # Implementation here
        pass

if __name__ == "__main__":
    # Command processor for standardized evaluation
    input_data = sys.stdin.read().splitlines()
    for line in input_data:
        parts = line.strip().split()
        if not parts: continue
        if parts[0] == "QUERY":
            qb = QueryBuilder()
            idx = 1
            while idx < len(parts):
                if parts[idx] == "SELECT":
                    idx += 1
                    while idx < len(parts) and parts[idx] not in ["FROM", "WHERE", "BUILD"]:
                        qb.select(parts[idx]); idx += 1
                elif parts[idx] == "FROM":
                    qb.from_table(parts[idx+1]); idx += 2
                elif parts[idx] == "WHERE":
                    qb.where(parts[idx+1], parts[idx+2], parts[idx+3]); idx += 4
                elif parts[idx] == "BUILD":
                    try: print(qb.build())
                    except ValueError as e: print(f"ERROR: {e}")
                    idx += 1
                else: idx += 1
