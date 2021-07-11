'''
Created on Thu Jan 30 2020

@author Giovanni Gabbolini
'''

from src.sparql.query_sparql import query_sparql

def get_abstract_uri(uri):
    # return 'debug'
    return query_sparql('select ?a where {'+ uri + ' dbo:abstract ?a . FILTER(langMatches(lang(?a),"en")) }')[0]['a']['value']
