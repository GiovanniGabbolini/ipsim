from collections import OrderedDict
from inspect import signature, _empty


def in_node_types(func):
    """Given a feature function, returns a dictionary containing the types allowed for each argument of the function.

       The types for arg are assigned in this way:
       - If arg is annotated with string s, return [s]
       - If arg is annotate with list of strings l, return l
       - If arg is not annotated, return [arg]

    Args:
        func (function)

    Returns:
        dict: For every arg, has a list of types
    """
    d = OrderedDict()

    sig = signature(func)
    for arg, v in sig.parameters.items():

        if v._annotation == _empty:
            types = [arg]
        else:
            if type(v._annotation) == list:
                types = v._annotation
            else:
                types = [v._annotation]

        d[arg] = types

    return d


def out_node_types(func, edge_type=None):
    """Given a feature function, return a list of the possible node types that can be generated from that feature.

       It is possible to specify an edge_type, so that this function will return only the node types to which a certain edge type can lead.

       The value returned is:
       - the return key in __annotation__ IF no edge_type is specified OR the (edge type,node type) mapping is not specified
       - The (edge type, node type) as specified in func.__annotations__['edge_type_to_node_type'], IF mapping is specified

    Args:
        func (function)

    Returns:
        list
    """
    try:
        types = func.__annotations__['edge_type_to_node_type'][edge_type]
    except KeyError:
        types = func.__annotations__['return']
    except KeyError:
        raise ValueError("A function should specify the out nodes for every edge type, or provide a return annotation.")

    return types if type(types) == list else [types]


def edge_types(func):
    """Given a feature function, returns the possible edge types that the application of that feature generates.

       If there is the key edge_types in the function annotations, returns it, converted to string.
       Else, return a list with only the function name inside.

    Args:
        func (function)

    Returns:
        list
    """
    if 'edge_types' in func.__annotations__:
        return func.__annotations__['edge_types'] if type(func.__annotations__['edge_types']) == list else [func.__annotations__['edge_types']]
    else:
        return [func.__name__]
