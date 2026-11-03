# student_workspace/solution.py

class Library:
    def __init__(self):
        self.books = {}    # {title: {'author': str, 'available': bool}}
        self.history = []  # list of transaction strings

    def add_book(self, title: str, author: str) -> None:
        self.books[title] = {'author': author, 'available': True}
        self.history.append(f"Added: '{title}' by {author}")

    def borrow_book(self, title: str, user: str) -> str:
        if title in self.books and self.books[title]['available']:
            self.books[title]['available'] = False
            msg = f"Borrowed: '{title}' by {user}"
            self.history.append(msg)
            return msg
        else:
            return "Not Available"

    def return_book(self, title: str, user: str) -> str:
        if title in self.books and not self.books[title]['available']:
            self.books[title]['available'] = True
            msg = f"Returned: '{title}' by {user}"
            self.history.append(msg)
            return msg
            return "Invalid Return"

    def search_book(self, title: str) -> bool:
        # Return True if book is in the dictionary
        if title in self.books:
            return True
        else:
            return False

    def view_history(self) -> list:
        # Return history if there are any transactions
        if len(self.history) > 0:
            return self.history
        else:
            return ["No transactions yet."]
