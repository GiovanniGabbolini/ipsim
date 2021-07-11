from src.sparql.query_sparql import query_sparql
from src.sparql.query_sparql import ask_sparql
import logging


def identify_country_uri_attribute(uri, attribute):
    """Retrieve the dbpedia pages of the countries associated with a dbpedia page and
       an attribute contained in that page.

       The attribute can represent a general location. The feature checks if its value or the value of one of its
       parents represent a Country or not. eg: United Kingdom, Italy, Ireland ..

    Arguments:
        uri {str} --
        attribute {str} --

    Returns:
        list -- uris of the pages of the country
    """

    # The second last two conditions filter out country of the past times that can be catched every now and then
    query = "select distinct ?f where{\
                " + uri + " " + attribute + "  ?s .\
                ?s (dbo:wikiPageRedirects|dbo:wikiPageDisambiguates)* ?r .\
                ?r (dbo:country|dbo:isPartOf|dbo:state|dbo:region|dbo:archipelago)* ?u .\
                ?u (dbo:wikiPageRedirects|dbo:wikiPageDisambiguates)* ?f .\
                filter not exists { ?f dbo:dissolutionYear ?w } .\
                filter not exists { ?f dct:subject dbc:Imperialism } .\
                filter not exists { ?f dbo:wikiPageDisambiguates ?w } .\
                filter not exists { ?f dbo:wikiPageRedirects ?w } .\
            }"
    results = query_sparql(query)
    if len(results) > 0:
        ret = []
        results = [
            f"<{r['f']['value']}>" for r in results if r['f']['type'] == 'uri']
        for page in results:
            # USA not an interesting country, too common
            if page != '<http://dbpedia.org/resource/United_States>' and page not in ret:
                q = "ask{\
                        {" + page + " a dbo:Country}\
                        UNION\
                        {" + page + " dct:subject dbc:States_of_the_United_States}\
                    }"
                if ask_sparql(q):
                    ret.append(page)

        if len(ret) > 0:
            return ret
        else:
            logging.getLogger('root.features').warning(
                f"{uri} had a valid {attribute} value, but I was not able to associate a country to it.")
