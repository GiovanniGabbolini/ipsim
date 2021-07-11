'''
Created on Tue Jan 28 2020

@author Giovanni Gabbolini
'''

from urllib.error import URLError
from SPARQLWrapper import SPARQLWrapper, JSON
import logging
import time
sparql = SPARQLWrapper('http://dbpedia.org/sparql')
sparql.setReturnFormat(JSON)


def query_sparql(query):
    sparql.setQuery(query)
    try_again = True
    while try_again:
        try:
            d = sparql.query().convert()
            try_again = False
        except URLError as e:
            logging.getLogger("root.sparql").warning(
                "Internet is down, failed to run a Sparql query. Trying again ...")
            time.sleep(0.5)

    return d['results']['bindings']


def ask_sparql(ask_query):
    sparql.setQuery(ask_query)
    d = sparql.query().convert()
    return d['boolean']
