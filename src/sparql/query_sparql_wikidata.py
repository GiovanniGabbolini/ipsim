'''
Created on Tue Jan 28 2020

@author Giovanni Gabbolini
'''


from SPARQLWrapper import SPARQLWrapper, JSON
import logging
import time
import sys

endpoint_url = "https://query.wikidata.org/sparql"
user_agent = "WDQS-example Python/%s.%s" % (
    sys.version_info[0], sys.version_info[1])
sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
sparql.setReturnFormat(JSON)


def query_sparql(query):
    sparql.setQuery(query)
    try_again = True
    while try_again:
        try:
            d = sparql.query().convert()
            try_again = False
        except Exception as e:
            logging.getLogger("root.sparql").warning(
                "Internet is down, failed to run a Sparql query. Trying again ...")
            time.sleep(0.5)

    return d['results']['bindings']


def ask_sparql(ask_query):
    sparql.setQuery(ask_query)
    d = sparql.query().convert()
    return d['boolean']
