from src.utils.utils_ngx_graph import father


def segue_type(segue):
    """The segue type, as defined by the concatenation of nodes and edges types crossed in the KG by the segue, joined by the compare function used.

    Args:
        segue (d): dictionary form of a segue

    Returns:
        tuple: The segue type
    """
    if segue is None:
        return None
    else:
        r = _trace(segue['n1'])+[segue['compare_function']]+_trace(segue['n2'])[::-1]
        return tuple(r)


def _trace(n):
    """The node trace, i.e. the concatenation of all nodes and edge types that are ancerstor of n a tree.

    Args:
        n (node)

    Returns:
        list
    """
    tr = []
    while True:
        tr.insert(0, n['type'])
        father_n = father(n)
        if father_n is not None:
            tr.insert(0, n['graph'][father_n['id']][n['id']]['type'])
            n = father_n
        else:
            break
    return tr
