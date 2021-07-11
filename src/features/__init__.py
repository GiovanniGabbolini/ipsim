"""
Entities (nodes) and relationships (edges) building up the Knowledge Graph (KG) are produced by features, that take the form of functions, and are stored in the `used` sub-module.

Nodes in KG have a type and a value. Edges in KG have a type.

After the KG is initialized with preliminar information (if items are songs: song name, artist name and album name), 
the construction happens by applying features iteratively.

Every feature has in-node types, edge types and out-node types:

* in-node types: types of nodes this feature is applicable to;
* edge types: types of edges this feature produces;
* out-node types: types of nodes this features produces.

Such properties are specified by annotations on features:

* in-node types: parameters annotation [1], if specified. Otherwise, parameters names.
* edge types: 'edge_types' annotation, if specified. Otherwise, function name.
* out-node types: 'return' annotation [1].

Refs:

* \[1\]: https://www.python.org/dev/peps/pep-3107/

"""

# Exluding files from documentation of features in graph.
__pdoc__ = {}
__pdoc__['array_feature'] = False
__pdoc__['create_feature'] = False
__pdoc__['decorator_cached_feature'] = False
__pdoc__['decorator_logging_to_mongo_feature'] = False
__pdoc__['decorator_musicbrainz_feature'] = False
__pdoc__['decorator_timing_feature'] = False
__pdoc__['inspector'] = False
__pdoc__['read_feature_dataframe'] = False
__pdoc__['read_feature_dictionary'] = False
__pdoc__['not_used'] = False
