"""
Created on Wed Apr 15 2020

@author Giovanni Gabbolini
"""

from src.features.decorator_timing_feature import timing_feature
from src.features.array_feature import array_feature
from src.features.decorator_cached_feature import cached_feature
from src.sparql.query_sparql_wikidata import query_sparql
import re
import logging


@cached_feature
@timing_feature
def artist_awards(artist_wikidata_id) -> 'award_wikidata':
    """Awards won by a musical artists, from WikiData

    Returns:
        list: List of dictionaries describing the awards
    """

    query = "SELECT ?award ?cerimony_label ?year {" + artist_wikidata_id['value'] + " p:P166 ?a . \
        ?a ps:P166 ?award . ?a pq:P585 ?year . OPTIONAL {?a pq:P805 ?cerimony . \
        ?cerimony rdfs:label ?cerimony_label . FILTER (lang(?cerimony_label) = 'en')} }"
    results = query_sparql(query)
    if len(results) > 0:
        awards = []
        for r in results:
            # For every award, we build a dictionary with three fields:
            # - award id: Eg the wikidata id of Grammy award for best Song
            # - year: The year the award was received
            # - award series: Eg Grammy Award, Brit award, ..

            d = {}

            year = r['year']['value']
            if re.match(r"^\d{4}-\d{2}-\d{2}T00:00:00Z$", year):
                d['year'] = year.split('-')[0]
            else:
                raise ValueError(
                    f"Year {year} associated with Award of artist {artist_wikidata_id['value']} is not well formated")

            award_id = r['award']['value']
            d['award_id'] = f"wd:{award_id.split('/')[-1]}"

            try:
                ceremony_label = r['cerimony_label']['value']

                if 'Grammy' in ceremony_label:
                    d['award_series'] = 'Grammy Award'
                elif 'MTV Video Music Awards' in ceremony_label:
                    d['award_series'] = 'MTV Video Music Award'
                elif 'MTV Music Awards' in ceremony_label:
                    d['award_series'] = 'MTV Music Award'
                elif 'American Music Awards' in ceremony_label:
                    d['award_series'] = 'American Music Award'
                elif 'World Music Awards' in ceremony_label:
                    d['award_series'] = 'World Music Award'
                elif 'Tony Award' in ceremony_label:
                    d['award_series'] = 'Tony Award'
                elif 'Golden Raspberry Awards' in ceremony_label:
                    d['award_series'] = 'Golden Raspberry Award'
                elif 'BRIT Awards' in ceremony_label or 'Brit Awards' in ceremony_label:
                    d['award_series'] = 'Brit Award'
                elif 'BET' in ceremony_label:
                    d['award_series'] = 'BET Award'
                elif "People's Choice Awards" in ceremony_label:
                    d['award_series'] = "People's Choice Award"
                elif 'Academy Award' in ceremony_label:
                    d['awards_series'] = "Oscar"
                else:
                    logging.getLogger('root.features').warning(
                        f"Not able to associate any award series to the award {ceremony_label}")
            except KeyError:
                pass

            awards.append(d)

        return [{'value': a} for a in awards]


if __name__ == "__main__":
    array_feature(artist_awards, mp=False)
