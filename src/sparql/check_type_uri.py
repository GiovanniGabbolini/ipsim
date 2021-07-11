'''
Created on Mon Feb 17 2020

@author Giovanni Gabbolini
'''
from src.sparql.get_disambiguating_uri import get_disambiguating_uri
from src.sparql.get_redirecting_uri import get_redirecting_uri
from src.sparql.query_sparql import ask_sparql
import logging


def match_uri_against_kinds(uri, list_kinds):
    """given a uri and given a list of kiunds, eg: dbo:Genre
       checks if the uri matches at least one of these kinds

    Arguments:
        uri {str} -- 
        list_kinds {list} -- 

    Returns:
        bool -- 
    """
    q = "ASK { "
    for idx, k in enumerate(list_kinds):
        if idx == 0:
            q += "{ " + uri + " a "+k+" } "
        else:
            q += "UNION { " + uri + " a "+k+" } "
    q += "}"
    return ask_sparql(q)


def check_type_uri(uri, list_kinds, disambiguating_function=None):
    """ check if an uri is of a given type

        handles: - redirections
                 - disambiguating pages

        in particular: 1) starting from uri, gets the uri to which redirects, if any, and saves it into uri
                       2) if uri is a disambiguating page, check if one of them matches the list_kinds
                       2) finally, check if uri matches the list_kinds

        this is the order because a disambiguating pages matches all the kinds to which in disambiguate

    Arguments:
        uri {str} -- 
        list_kinds {list} -- pages types, eg: dbo:Genre

    Keyword Arguments:
        disambiguating_function {func} -- used in case more than one disambiguating page matches list_kinds

    Returns:
        str -- uri found
    """

    # get the uri to which this pages redirects, if any
    uri = get_redirecting_uri(uri)

    # get the disambiguating uris, if the uri represent a disambiguation page
    disambiguating_uri = get_disambiguating_uri(uri)

    # filter from the disambiguating uris only the uris which match the list of kinds
    eligible_disambiguating_uri = [
        u for u in disambiguating_uri if match_uri_against_kinds(u, list_kinds)]

    if len(eligible_disambiguating_uri) == 1:
        return eligible_disambiguating_uri[0]

    elif len(eligible_disambiguating_uri) > 1:
        if disambiguating_function:
            r = disambiguating_function(eligible_disambiguating_uri)
            # The disambiguating function could fail to disambiguate
            if r:
                return r
        else:
            logging.getLogger('root.features').warning(
                f"{uri} disambiguates to more than one possible uris and no disambiguation function is provided, skipping")

    # finally, check if the starting uri provided matches the list of kinds
    if match_uri_against_kinds(uri, list_kinds):
        return uri

    # if none of the former succeded, just return None
    return None
