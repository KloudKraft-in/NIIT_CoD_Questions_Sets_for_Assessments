class PaginatedIterator:
    def __init__(self, data_source, page_size: int):
        # TODO: Initialize data_source, page_size, offset, and internal buffer
        pass

    def __iter__(self):
        # TODO: Return self
        pass

    def __next__(self):
        # TODO: If buffer is empty, fetch next page from data_source(offset, page_size)
        # TODO: If page is empty, raise StopIteration
        # TODO: Increment offset and total_fetched
        # TODO: Yield the next item from the buffer
        pass

    @property
    def total_fetched(self) -> int:
        # TODO: Return tracking of fetched items
        pass
