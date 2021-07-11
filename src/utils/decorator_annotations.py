def annotations(arg):
    """Adds the dictionary passed in arg to the function annotations

    Args:
        arg (dict)
    """

    def wrapper(func):
        func.__annotations__ = {**arg, **func.__annotations__}
        return func

    return wrapper
