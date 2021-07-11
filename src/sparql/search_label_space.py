'''
Created on Mon Feb 17 2020

@author Giovanni Gabbolini
'''
from src.sparql.query_sparql import query_sparql, ask_sparql
import re


def _preprocess_label(label):
    """Prorocessing the label to search before feeding into the query

       The preprocessing steps that we apply are:

       - escape single quotes, so that the query engine can handle those
       - remove special characters from label if they are used as separating characters.
         This avoids error: "Free-text expression, line n: phrase consists of noise words exclusively"

       Then, we eliminate potential doubles spaces and heading and trailing spaces

    Arguments:
        label {str} --

    """
    # escale special characters
    preprocessed_label = label.replace("'", "\\\\'")

    # debug
    preprocessed_label = preprocessed_label.replace('"', '\\\\\\"')

    # remove special separating characters
    matches = re.finditer(r"(?=(\s|^)(&|-|÷|\+|/|\.|:)(\s|$))",
                          preprocessed_label, re.MULTILINE)
    acc = ''
    idx = 0
    for m in matches:
        acc += preprocessed_label[idx:m.start(2)]
        idx = m.end(2)
    acc += preprocessed_label[idx:len(preprocessed_label)]
    preprocessed_label = acc if idx else preprocessed_label

    # eliminate multiple spaces
    preprocessed_label = ' '.join(preprocessed_label.split())

    # eliminate heading and trailing spaces
    preprocessed_label = preprocessed_label.strip()

    return preprocessed_label


def search_label_space(label, narrowing_space_query='', selecting_results_query=''):
    """Searches in the whole dbpedia for the uris with the label which matches the variable label

       TODO: Beyoncé could not be found as label string, eventhough this is the label name of the actual page of the singer. 
             Neither substrings of the former cannot be found (Beyon or Beyo), as if the page couldn't be seen from sparql. 
             The same happens with the page of Aminé, José González, Jack Ü, Zhané, Björk. However, the dbpedia page is accessible.
             Apparently, we have problems with strange accents 

       This method guarantees that the uris found are neither disambiguation nor redirection pages

    Arguments:
        label {string} --
        narrowing_space_query {string} -- Query that define variable ?s. By default on this method,
                                          it can range on the space of all labels in dbpedia
        selection_results_query {string} -- Query that poses condition on variable ?f, selectiong
                                            the results that are returned by this method

    Returns:
        list -- uris found
    """
    preprocessed_label = _preprocess_label(label)
    if len(preprocessed_label):

        q = "SELECT DISTINCT ?f { " + narrowing_space_query + \
            " ?s rdfs:label ?label . FILTER(lang(?label)=\"en\") . ?label bif:contains "
        acc = ""
        for idx, token in enumerate(preprocessed_label.split(' ')):
            acc += f"'{token}'" if idx == 0 else f" and '{token}'"
        q += f"\"{acc}\" . "

        q += " ?s (dbo:wikiPageRedirects | dbo:wikiPageDisambiguates)* ?f . "

        q += " ?f rdfs:label ?l . FILTER(lang(?l)=\"en\") . ?l bif:contains "
        acc = ""
        for idx, token in enumerate(preprocessed_label.split(' ')):
            acc += f"'{token}'" if idx == 0 else f" and '{token}'"
        q += f"\"{acc}\" . "

        q += selecting_results_query

        q += "filter not exists { \
              ?f dbo:wikiPageRedirects|dbo:wikiPageDisambiguates ?dis \
              }"
        q += " }"
        results = query_sparql(q)
        uris_found = [f"<{results[c]['f']['value']}>"
                      for c in range(len(results))]

        # check, the uris found should not redirect or disambiguate
        for uri in uris_found:
            assert not ask_sparql('ask { {' + uri + ' dbo:wikiPageRedirects ?w } UNION {' + uri +
                                  ' dbo:wikiPageDisambiguates ?w } }'), "The result is not expect to be neither a disambiguation nor a redirection page, something is incoherent"

        return uris_found
    else:
        return []


if __name__ == "__main__":
    pass
