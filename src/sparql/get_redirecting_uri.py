"""
Created on Wed Mar 04 2020

@author Giovanni Gabbolini
"""
from src.sparql.query_sparql import query_sparql


def get_redirecting_uri(uri):
    """if this uri redirects to something, then return the redirecting uri, otherwise return the previous uri

    Arguments:
        uri {str} -- 
    """
    q = "SELECT ?s WHERE{" + uri + " dbo:wikiPageRedirects ?s . }"
    results = query_sparql(q)
    if len(results) > 0:
        assert len(
            results) == 1, f"The uri {uri} has more that two redirecting pages, behaviour not expected!"
        redirecting_uri = f"<{results[0]['s']['value']}>"
        return redirecting_uri
    else:
        return uri
