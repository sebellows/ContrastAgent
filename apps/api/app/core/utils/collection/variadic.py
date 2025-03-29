def variadic(*args) -> list:
    """
    Safely extract parameters within a function as a list where they may be passed as an array or a
    variable number of arguments.

    Example(s):
    -----------
    >>> def getargs(*args):
    >>>    return variadic(*args)

    >>> getargs(['a', 'b', 'c'])
    ['a', 'b', 'c']
    >>> getargs('d', 'e', 'f', 'g')
    ['d', 'e', 'f', 'g']
    """
    return args[0] if len(args) == 1 and isinstance(args[0], (list, set, tuple)) else args
