from src.features.used import *
from src.features import used
from inspect import signature, Parameter
import itertools
from src.utils.utils_ngx_graph import father
from src.features.inspector import in_node_types, out_node_types, edge_types
from unittest.mock import MagicMock
import re


class ActionsSupplier:

    """Class thought as a supplier of functions that allows to build the graph for an entity.
       Therefore, handles the functions that were already supplied (avoiding repetitions),
       considers recursive functions, ..
    """

    def __init__(self):
        # This set contains the functions already applied. It is formed by a set of tuples. Each tuple contains (key1, ... keyn, key1~function),
        # where keyi are the nodes which we used as argument for the function and function is the name of the function applied.
        # We use key1 as the last parameter following the logic behind all the features:  a feature can be associated to many variables,
        # but the first variable will be the index of the new one,  so the first variable share the domain with the new variable (node) that
        # we are creating. Infact in the graph every node contains a ref to the node fed as first variable in the function
        self.applied_actions = set()

    def eligible_actions(self):
        return used.__all__

    def set_graph(self, g):
        self.g = g

        # If g was at least partially built, self.applied_actions should be set up correctly
        for node in g.nodes():
            idxs = [m.start() for m in re.finditer('~', node)]+[len(node)]
            for i, j in zip(idxs, idxs[1:]):
                self.applied_actions.add((node[:i], node[:j]))

    def eligible_nodes_filter(self, node, func):
        """Used to eventually filter out nodes that would otherwise be considered as applicable to some features.
        Useful to limit the graph growth.

        Active filters:
        -avoid infinite loops
        -do not expand nodes that originate from an artist relationship
        -if the feature is entailment, then apply to a synset only if it directly discend from a word
        -if the feature is member_holonyms, then apply to a synset only if it directly discend from a word
        -if the feature is member_meronyms, then apply to a synset only if it directly discend from a word
        -if the feature is part_holonyms, then apply to a synset only if it directly discend from a word
        -if the feature is part_meronyms, then apply to a synset only if it directly discend from a word
        -if the feature is substance_holonyms, then apply to a synset only if it directly discend from a word
        -if the feature is substance_meronyms, then apply to a synset only if it directly discend from a word
        -if the feature is synset_also_sees, then apply to a synset only if it directly discend from a word
        -if the feature is synset_attributes, then apply to a synset only if it directly discend from a word
        -if the feature is synset_similar_tos, then apply to a synset only if it directly discend from a word
        -if the feature is synset_verb_groups, then apply to a synset only if it directly discend from a word
        -if the feature is hypernyms, then apply to a synset only if it directly discend from a word
        -if the feature is hyponyms, then apply to a synset only if it directly discend from a word

        Args:
            node (ngx Node): The eligible node to keep or filter out
            func (function): Feature to which node would be eventually fed

        Returns:
            Bool: True if keep it, False if discard it
        """
        # a => b is equivalent to not a or b
        if self.g[father(node)['id']][node['id']]['generating_function'] != func.__name__ and \
                self.g[father(node)['id']][node['id']]['generating_function'] != 'artist_relationships' and \
                (not func.__name__ == 'entailment' or father(node)['type'] == 'word') and \
                (not func.__name__ == 'member_holonyms' or father(node)['type'] == 'word') and \
                (not func.__name__ == 'member_meronyms' or father(node)['type'] == 'word') and \
                (not func.__name__ == 'part_holonyms' or father(node)['type'] == 'word') and \
                (not func.__name__ == 'part_meronyms' or father(node)['type'] == 'word') and \
                (not func.__name__ == 'substance_holonyms' or father(node)['type'] == 'word') and \
                (not func.__name__ == 'substance_meronyms' or father(node)['type'] == 'word') and \
                (not func.__name__ == 'synset_also_sees' or father(node)['type'] == 'word') and \
                (not func.__name__ == 'synset_attributes' or father(node)['type'] == 'word') and \
                (not func.__name__ == 'synset_similar_tos' or father(node)['type'] == 'word') and \
                (not func.__name__ == 'synset_verb_groups' or father(node)['type'] == 'word') and \
                (not func.__name__ == 'hypernyms' or father(node)['type'] == 'word') and \
                (not func.__name__ == 'hyponyms' or father(node)['type'] == 'word'):
            return True
        else:
            return False

    def applicable_actions(self):
        """Apply the function below to all the function in the folder
        src/features/specific and src/features/common.

        First, find all the functions withouth considering default values but trying to
        match a valid value to every field of the functions.
        If not function is found, this way, allow default values as well.

        Returns:
            list -- The concatenation of all the lists returned for any of the function in the folder
        """

        # Without default values
        l = []
        functions = self.eligible_actions()
        for f in functions:
            # Get the argument variables name for the function f
            func = getattr(globals()[f], f)
            l += self.applicable_actions_given_function(func, False)

        if len(l) > 0:
            return l
        else:
            # With default values
            l = []
            for f in functions:
                # Get the argument variables name for the function f
                func = getattr(globals()[f], f)
                l += self.applicable_actions_given_function(func, True)
            return l

    def applicable_actions_given_function(self, func, allow_default_values):
        """Finds all the possible combination of nodes in the graph that can be
        applied as arguments of the function func.

        A tuple of nodes is applicable if the type field on the tuple match the name
        of the function arguments, or, in case they are specified, its annotations

        Arguments:
            applied_actions {set} -- Set of tuples in the format (key1, key2, .. , key1~funcname).
                                    This is used to check if the function was already applied to the same graph nodes.
                                    Infact, if a function is applied the node which is generate will have the id as the
                                    first key in the argument tuple ~ function that generated it
            func {function} --
            allow_default_values {bool} -- Whether we allow for default value to be considered as function parameters or not

        Returns:
            list -- List containing [(func, (key1, .. keyn), func_signature), ...] where func is the function to apply
                    and the tuple contain the key of the graph nodes to consider as parameters of the function
        """
        sig = signature(func)

        # Find key of nodes with type equal to the type(s) associated to each function argument
        # The function argument type is either annotated, or, otherwise, we consider it to be the argument name
        feature_args_eligible_nodes = []
        for arg, v in sig.parameters.items():

            eligible_types_arg = in_node_types(func)[arg]
            eligible_nodes = []

            for k in self.g.nodes():
                node = self.g.nodes()[k]
                if node['type'] in eligible_types_arg:

                    if self.eligible_nodes_filter(node, func):
                        eligible_nodes.append(k)

            # If:
            # - default values are allowed AND
            # - no other eligible nodes are available AND
            # - the params allows default values THEN
            # we append a particular node, indicating that the param of the function can be used with its default value
            if allow_default_values and len(eligible_nodes) == 0 and v.default is not Parameter.empty:
                feature_args_eligible_nodes.append(['DEFAULTVALUE'])
            else:
                feature_args_eligible_nodes.append(eligible_nodes)

        # Consider all the possible combination of keys
        # Remark: if at least one of them is empty, no possible args will be available
        possible_args = list(itertools.product(*feature_args_eligible_nodes))

        # Filter combination based on if I have already applied that function to that keys
        filtered_args = []
        for arg in possible_args:
            if arg + (f"{arg[0]}~{func.__name__}",) not in self.applied_actions:
                filtered_args.append(arg)

                # Store the actual function together with the already applied ones
                self.applied_actions.add(arg + (f"{arg[0]}~{func.__name__}",))

        return [(func, arg, sig) for arg in filtered_args]


class MockedActionsSupplier(ActionsSupplier):

    """Shares the logic with ActionSupplier, but returns mocked function instead of real features.
       Useful for testing and debugging, to construct a graph where no calls and feature computations are needed
    """

    def applicable_actions(self):
        actions = super(MockedActionsSupplier, self).applicable_actions()

        actions_mocked = []
        for action in actions:
            func = action[0]

            return_value = []

            e_types = edge_types(func)
            for edge_type in e_types:
                for node_type in out_node_types(func, edge_type=edge_type):
                    return_value.append({'value': 'mocked', 'node_type': node_type, 'edge_type': edge_type})

            mock = MagicMock(return_value=return_value if len(return_value) > 1 else return_value[0])
            mock.__annotations__ = func.__annotations__
            mock.__name__ = func.__name__

            actions_mocked.append((mock, action[1], action[2]))

        return actions_mocked


class CustomReturnValueMockedActionsSupplier(MockedActionsSupplier):

    """A MockedActionSupplier customizable in the mocked values returned by mocked functions
       The dictionary d is shaped as follows:
       {
            'function_name': return value,
            ...
       }
       It considers elibible actions only the keys of d,
       exploits the logic of MockedActionsSupplier,
       and substitute mocked return values with values of d.
    """

    def __init__(self, d):
        super(CustomReturnValueMockedActionsSupplier, self).__init__()
        self.d = d

    def eligible_actions(self):
        return list(self.d.keys())

    def applicable_actions(self):
        v = super(CustomReturnValueMockedActionsSupplier, self).applicable_actions()
        for e in v:
            e[0].return_value['value'] = self.d[e[0].__name__]
        return v


class InformativeActionSupplier(ActionsSupplier):

    """Discard all funny segues, keep only the informative ones.
    This is the same as discarding all nodes from token_phrase.
    """

    def eligible_actions(self):
        return list(set(used.__all__)-set(['token_phrase']))
