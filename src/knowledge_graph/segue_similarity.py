from src.knowledge_graph.segue_type import segue_type


def segue_similarity(s1, s2):
    if s1 is None or s2 is None:
        return 0
    else:
        typeset_s1 = set(segue_type(s1))
        typeset_s2 = set(segue_type(s2))
        return len(typeset_s1 & typeset_s2)/len(typeset_s1 | typeset_s2)
