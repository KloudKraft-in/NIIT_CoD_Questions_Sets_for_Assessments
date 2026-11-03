import sys

class PaginatedIterator:
    def __init__(self, data_source, page_size: int):
        # Implementation here
        pass

    def __iter__(self):
        # Implementation here
        return self

    def __next__(self):
        # Implementation here: fetch next page using data_source(offset, page_size)
        pass

if __name__ == "__main__":
    # Command processor for standardized evaluation
    input_data = sys.stdin.read().splitlines()
    for line in input_data:
        parts = line.strip().split()
        if not parts: continue
        if parts[0] == "ITERATE":
            total_items, psize = int(parts[1]), int(parts[2])
            def mock_source(offset, limit):
                data = list(range(total_items))
                res = data[offset : offset + limit]
                print(f"DEBUG: Fetching offset={offset}, limit={limit}, got {len(res)}")
                return res
            iterator = PaginatedIterator(mock_source, psize)
            for item in iterator: print(item)
            print(f"Total Fetched: {iterator.total_fetched}")
