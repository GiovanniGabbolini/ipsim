from src.sparql.query_sparql import query_sparql
from src.sparql.query_sparql import ask_sparql
import logging


def identify_city_uri_attribute(uri, attribute):
    """Retrieves the uris of the cities associated with a dbpedia page and an attribute contained in that page

       We simply consider city everything that is not a country.
       So we:
            1) Start from a page
            2) Retrieve all the pages that page disambiguates or redirect, recursively
            3) Filter out state and redirect and disambiguate pages


    Arguments:
        uri {str} --
        attribute {str} --

    Returns:
        list -- uris of the pages of the country
    """
    if ask_sparql("ask { " + uri + " " + attribute + "  ?s }"):
        query = "select distinct ?f where{\
                    " + uri + " " + attribute + "  ?s .\
                    ?s (dbo:wikiPageRedirects|dbo:wikiPageDisambiguates)*  ?f .\
                    filter not exists { ?f a dbo:Country } .\
                    filter not exists { ?f dct:subject dbc:States_of_the_United_States } .\
                    filter not exists { ?f dbo:wikiPageDisambiguates ?w } .\
                    filter not exists { ?f dbo:wikiPageRedirects ?w } .\
                }"
        results = query_sparql(query)
        ret = ['<' + r['f']['value'] + '>' for r in results]
        if len(ret) > 0:
            return ret
        else:
            logging.getLogger('root.features').warning(
                f"{uri} had a valid {attribute} value, but I was not able to associate a city to it.")
