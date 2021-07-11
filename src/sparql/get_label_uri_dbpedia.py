from src.sparql.query_sparql import query_sparql


def get_label_uri(uri):
    # return 'debug'
    r = query_sparql(
        'select ?l where {' + uri + ' rdfs:label ?l . FILTER(langMatches(lang(?l),"en")) }')
    if len(r) > 0:
        return r[0]['l']['value']
    else:
        r = query_sparql(
            'select ?l where {' + uri + ' foaf:name ?l . FILTER(langMatches(lang(?l),"en")) }')
        if len(r) > 0:
            return r[0]['l']['value']
        else:
            raise ValueError("cannot find uri label")
