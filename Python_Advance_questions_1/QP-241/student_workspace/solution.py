import functools

def validate_schema(schema: dict):
    # TODO: Implement a decorator factory that validates function keyword arguments
    def decorator(func):
        @functools.wraps(func)
        def wrapper(**kwargs):
            # TODO: Loop through schema and validate presence and type of each field
            # TODO: Raise TypeError with required messages
            pass
        return wrapper
    return decorator
