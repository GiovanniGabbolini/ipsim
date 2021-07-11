"""
Created on Tue Mar 03 2020

@author Giovanni Gabbolini
"""

from src.sparql.query_sparql import query_sparql
import pandas as pd
import logging


def identify_date_attribute(uri, attribute):
    """Given a dbpedia page and an attribute, we extract a date value from that attribute

    Arguments:
        uri {str} -- 
        attribute {str} -- 
    """
    query = 'SELECT DISTINCT ?s WHERE{' + \
        uri + ' ' + attribute + ' ?s . }'
    results = query_sparql(query)
    if len(results) > 0:
        date = results[0]['s']['value']
        try:
            date_converted = pd.to_datetime(date)
            return date_converted
        except Exception:
            logging.getLogger('root.features').warning(
                f"{uri} had a valid {attribute} value, but I was not able to extract a date from it.")
