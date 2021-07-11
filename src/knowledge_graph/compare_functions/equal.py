def equal(n1, n2):
    """Default compare method for nodes of the same type in the graph
    In principle, it says that there is a match if the two nodes have same value. 
    Since the value of the nodes can be strings, lists ecc, we should distinguish different behaviours

    - type(n['value']) == str: match if equals
    - type(n['value']) == list: match if there is one shared item
    - type(n['value']) == bool: match if they are both true
    - type(n['value']) == int: match if equals
    - type(n['value']) == bool: match if equals
    - type(n['value']) == tuple: match if all the tuple elements match, with equal

    The types of the two values are assumed to be the same. In general, this is controlled by the method resolve_compare_function

    This function is mean to simimulate paths that converge to the same entity, which is stated to be equal by this function.
    Since this function compare only the type field, it is not suitable to compare nodes that have additional field other than value.
    For the same reason, only node with no additional field can be compared with equal, other than the default fields of a node: graph, id, value and type

    Arguments:
        n1 -- First node 
        n2 -- Second node
    """
    return {'outcome': n1['value'] == n2['value'], 'value': n1['value']}
