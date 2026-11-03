from typing import List
import sys

# Complete the classes below to demonstrate inheritance.

class Item:
    def __init__(self, title: str, author: str, year: int):
        # Implementation here
        pass
        
    def __str__(self) -> str:
        # Standard string representation
        return ""
        
    def display_info(self) -> None:
        # Implementation here
        pass

class Book(Item):
    def __init__(self, title: str, author: str, year: int, genre: str, isbn: str):
        # Implementation here
        pass

    def display_info(self) -> None:
        # Implementation here
        pass

class DVD(Item):
    def __init__(self, title: str, author: str, year: int, duration: int):
        # Implementation here
        pass

    def display_info(self) -> None:
        # Implementation here
        pass





#NOTE : Don't modify below codes.

def process_library_items():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
        
    n = int(input_data[0].strip())
    items: List[Item] = []

    for i in range(1, n + 1):
        if i >= len(input_data): break
        line = input_data[i].strip()
        if not line: continue
        data = line.split(",")
        item_type = data[0].strip()
        
        if item_type == "Book":
            items.append(Book(data[1].strip(), data[2].strip(), int(data[3]), data[4].strip(), data[5].strip()))
        elif item_type == "DVD":
            items.append(DVD(data[1].strip(), data[2].strip(), int(data[3]), int(data[4])))

    for i, item in enumerate(items):
        item.display_info()
        if i < len(items) - 1:
            print("\nDetails:")

if __name__ == '__main__':
    process_library_items()
