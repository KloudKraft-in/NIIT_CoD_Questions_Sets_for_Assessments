import sys

class Database:
    @staticmethod
    def _init_db(username):
        # Already implemented static method
        print("Username matched, database connection initialized")
        return f"conn_id_for_{username}"

    @staticmethod
    def _close_db(connection_string):
        # Already implemented static method
        print("Connection string matched, database connection closed")

# Complete the 'database_context_manager' class below.
#
# The class should be a context manager.
# Use Database._init_db(username) in __enter__
# Use Database._close_db(connection_string) in __exit__

class database_context_manager:
    def __init__(self, username):
        """Initializes with the username."""
        # Implementation here
        pass

    def __enter__(self):
        """Initializes database and returns connection."""
        # Implementation here
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the database connection."""
        # Implementation here
        pass

def main():
    input_data = sys.stdin.read().strip()
    if not input_data:
        return
    
    username = input_data
    
    try:
        # Usage of the context manager
        with database_context_manager(username) as conn:
            print("Database running...")
    except Exception as e:
        # Traceback will be captured by driver
        raise e

if __name__ == "__main__":
    main()
