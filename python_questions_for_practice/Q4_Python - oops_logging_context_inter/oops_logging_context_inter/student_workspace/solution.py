
#student_workspace/solution.py

import functools

def audit_log(func):
    """
    TODO: Implement a decorator that prints:
    - "LOG: Starting [func_name]"
    - "LOG: Finishing [func_name]"
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        """ WRITE HERE CODE HERE """
        
        pass
    return wrapper

class DatabaseSession:
    def __init__(self, db_name: str):
        # TODO: Initialize db_name and is_open=True
        
        """ WRITE HERE CODE HERE """

        pass

    def __enter__(self):
        # TODO: Print "Session Started: [db_name]" and return self
        
        """ WRITE HERE CODE HERE """
        
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: Print "Session Ended: [db_name]" and set is_open=False
        
        """ WRITE HERE CODE HERE """
        
        pass

class AuditManager:
    # TODO: Initialize a class-level variable 'query_count' to 0
    
    def __init__(self):
        pass
    
    @audit_log
    def execute_query(self, session, sql: str) -> str:
        # TODO: Print "Running query: [sql]"
        # TODO: Increment the class-level query_count
        # Return "Success"
        
        """ WRITE HERE CODE HERE """
        
        pass

    def session_integrity(self, session) -> bool:
        # TODO: Return True if session is_open is True
        
        """ WRITE HERE CODE HERE """
        
        pass

    def get_query_count(self) -> int:
        # TODO: Return the total query_count
        
        """ WRITE HERE CODE HERE """
        
        pass

