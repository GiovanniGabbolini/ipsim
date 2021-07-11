"""
Created on Wed Mar 04 2020

@author Giovanni Gabbolini
"""
from src.sparql.query_sparql import query_sparql


def get_disambiguating_uri(uri):
    """given the uri, if that is a disambiguation page, returns the a list
       of uris to which it disambiguates to, otherwise it returns a void list

    Arguments:
        uri {str} -- 

    Returns:
        list -- 
    """
    q = "SELECT ?s WHERE{" + uri + "dbo:wikiPageDisambiguates ?s . }"
    results = query_sparql(q)
    disambiguating_uri = [f"<{r['s']['value']}>" for r in results]
    return disambiguating_uri
