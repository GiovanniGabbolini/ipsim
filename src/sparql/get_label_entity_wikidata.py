from src.sparql.query_sparql_wikidata import query_sparql


def get_label_entity(entity):
    r = query_sparql(
        'select ?l where {' + entity + ' rdfs:label ?l . FILTER(langMatches(lang(?l),"en")) }')

    if len(r) > 0:
        return r[0]['l']['value']
    else:
        return '(label not found)'
