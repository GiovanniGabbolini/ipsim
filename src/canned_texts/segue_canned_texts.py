import re
from src.utils.utils_ngx_graph import father
from src.sparql.get_label_entity_wikidata import get_label_entity
from src.out.get_value_musicbrainz import *
from src.utils.utils_ngx_graph import artist_id, track_chorus
from src.utils.canned_texts import album_name, track_name, artist_name
from src.canned_texts.phrase import phrase
from src.utils.canned_texts import resolve_form
from src.knowledge_graph.segues_filtering import _node_originating_lemma, _node_originating_synset


"""
    Readme!

    TL-DR: all the texts shown to the user are specified in the dictionaries:
    - in this file: _description_dichotomic, _line_atomic, _line_dichotomic, _short_atomic, _short_dichotomic
    - in phrase.py: _phrase
    The texts in _phrase are used in this file by means of the keywords d['phrase_n1'] and d['phrase_n2']
    The dictionaries in this files make also use of the function in the Utils and Templates sections.



    Texts (being those shorts, lines or descriptions) are specified into dictionaries indexed using the two nodes linked in a segue,
    i.e. the node from entity 1 (n1) that can be connected to the another node from entity 2 (n2).
    Those two nodes are stored in a dictionary (segue), together with the name of the function that certify that such a link exists (compare_function).

    The text can be specified in an atomic way or in a dicothomic way:
    - Atomic: a single text is specified for every two nodes and a compare function
    - Dichotomic: a single text is specified for n1 and n2, and those two texts are joined afterwards.


    Texts are written as functions, and, once excecuted, return the actual text.
    So, texts are not composed of just plain characters, but also of function calls.

    The functions in Utils are helpful in constructing little sections of texts.
    The function in Templates specify texts templates that can be filled from inside the dictionaries. This is helpful
        to avoid code repetitions when a similar texts are repeated multiple times into the dictionaries.


    Texts can exploit particular keys that might be present inside the segue dictionary, 'phrase_n1' and 'phrase_n2'.
    The phrases are specified in the file phrase.py.
    Phrases are useful because they allows to specify a little text relative to a segue type. Then, those can be filled
    into templates from this file, reducing code repetitions.
"""

###
# Utils
###


def from_type(n, target_type):
    """Says whether n comes from a target_type or not

    Args:
        n (ngx graph node)
        target_type (str

    Returns:
        bool
    """
    while n['id'] != 'source':
        n = father(n)
        if n['type'] == target_type:
            return True
    return False


def dots():
    return "..."


def get_month_name(month_number):
    _d = {
        '1': 'January',
        '2': 'February',
        '3': 'March',
        '4': 'April',
        '5': 'May',
        '6': 'June',
        '7': 'July',
        '8': 'August',
        '9': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December',
    }
    return _d[str(month_number)]


def day_number(number):
    if number == 1:
        return '1st'
    elif number == 21:
        return '21st'
    elif number == 31:
        return '31st'
    elif number == 2:
        return '2nd'
    elif number == 22:
        return '22nd'
    elif number == 3:
        return '3rd'
    elif number == 23:
        return '23rd'
    else:
        return f"{number}th"


def get_country_descriptor(country):
    name = get_area_value(country)
    if name in ['Alabama',
                'Alaska',
                'Arizona',
                'Arkansas',
                'California',
                'Colorado',
                'Connecticut',
                'Delaware',
                'Florida',
                'Georgia',
                'Hawaii',
                'Idaho',
                'Illinois',
                'Indiana',
                'Iowa',
                'Kansas',
                'Kentucky',
                'Louisiana',
                'Maine',
                'Maryland',
                'Massachusetts',
                'Michigan',
                'Minnesota',
                'Mississippi',
                'Missouri',
                'Montana',
                'Nebraska',
                'Nevada',
                'New Hampshire',
                'New Jersey',
                'New Mexico',
                'New York',
                'North Carolina',
                'North Dakota',
                'Ohio',
                'Oklahoma',
                'Oregon',
                'Pennsylvania',
                'Rhode Island',
                'South Carolina',
                'South Dakota',
                'Tennessee',
                'Texas',
                'Utah',
                'Vermont',
                'Virginia',
                'Washington',
                'West Virginia',
                'Wisconsin',
                'Wyoming']:
        return 'state'
    else:
        return 'country'


def undeline_word(word, text):
    """Place an underline html tag in a every string that matches the word variable in a text

    Arguments:
        word {str} --
        text {str} --
    """
    def func(match):
        g = match.group()
        if g.islower():
            return replacement.lower()
        if g.istitle():
            return replacement.title()
        if g.isupper():
            return replacement.upper()
        return replacement
    replacement = f"<u>{word}</u>"
    s = re.sub(
        word, func, text, flags=re.I)
    return s.replace("<U>", "<u>").replace("</U>", "</u>")


def capitalize_first_word(s):
    return s[0].capitalize()+s[1:]


###
# Templates
###


def word_play_line_1(word_play, n1, n2):
    if from_type(n1, 'album_name') and from_type(n2, 'album_name'):
        return f"{track_name(n1)} appeared on the album {album_name(n1)}, and {word_play}, so, from the album called {album_name(n2)}{dots()}"
    if from_type(n1, 'album_name') and not from_type(n2, 'album_name'):
        return f"{track_name(n1)} appeared on the album {album_name(n1)}, and {word_play}{dots()}"
    if not from_type(n1, 'album_name') and from_type(n2, 'album_name'):
        return f"{word_play}, so, from the album called {album_name(n2)}{dots()}"
    if not from_type(n1, 'album_name') and not from_type(n2, 'album_name'):
        return f"{word_play}{dots()}"


def word_play_line_2(word_play, n1, n2):
    if from_type(n1, 'album_name') and from_type(n2, 'album_name'):
        return f"{track_name(n1)} appeared on the album {album_name(n1)}, and {word_play}, here's a track from {artist_name(n2)}'s album {album_name(n2)}{dots()}"
    if from_type(n1, 'album_name') and not from_type(n2, 'album_name'):
        return f"{track_name(n1)} appeared on the album {album_name(n1)}, and {word_play}{dots()}"
    if not from_type(n1, 'album_name') and from_type(n2, 'album_name'):
        return f"{word_play}, here's a track from {artist_name(n2)}'s album {album_name(n2)}"
    if not from_type(n1, 'album_name') and not from_type(n2, 'album_name'):
        return f"{word_play}{dots()}"


def word_play_line_3(word_play, n1, n2):
    if from_type(n1, 'album_name') and from_type(n2, 'album_name'):
        return f"{word_play}, between the albums {album_name(n1)} and {album_name(n2)}{dots()}"
    if from_type(n1, 'album_name') and not from_type(n2, 'album_name'):
        return f"{word_play}, from the album {album_name(n1)} to{dots()}"
    if not from_type(n1, 'album_name') and from_type(n2, 'album_name'):
        return f"{word_play}, to a song from the album {album_name(n2)}{dots()}"
    if not from_type(n1, 'album_name') and not from_type(n2, 'album_name'):
        return f"{word_play}{dots()}"


def from_date_line(fst, snd, n1, n2, d):
    if d['phrase_n1'] == d['phrase_n2']:
        return f"That was {artist_name(n1)}, {d['phrase_n1']} {fst}, and so {'was' if re.match(r'(^| )was($| )', d['phrase_n1']) else 'did'} {artist_name(n2)}. Now, we listen to {track_name(n2)} by {artist_name(n2)}."
    else:
        return f"That was {artist_name(n1)}, {d['phrase_n1']} {fst}. Now, we listen to {track_name(n2)} by {artist_name(n2)}, {d['phrase_n2']} {snd}."


def from_date_short(fst, snd, n1, n2, d):
    if d['phrase_n1'] == d['phrase_n2']:
        return f"{artist_name(n1)} {d['phrase_n1']} {fst}, and so {'was' if re.match(r'(^| )was($| )', d['phrase_n1']) else 'did'} {artist_name(n2)}{dots()}"
    else:
        return f"{artist_name(n1)} {d['phrase_n1']} {fst} and {artist_name(n2)} {d['phrase_n2']} {snd}{dots()}"


right_relationships = ['7ddb04ae-6c8a-41bd-95c2-392994d663db',
                       '26131498-00e8-4136-b937-22a4be01a63d', '5cc8cfb5-cca0-4395-a44b-b7d3c1777608',
                       '7231dcac-d2dc-4b4a-b218-ecea4123a4cd', 'fff4640a-0819-49e9-92c5-1e3b5134fd95',
                       '8a3994fd-71ec-4443-9882-2192801241f2', '83f72956-2007-4bca-8a97-0ae539cca99d',
                       'a7e408a1-8c64-4122-9ec2-906068955187', '5e2907db-49ec-4a48-9f11-dfb99d2603ff',
                       'b41e7530-cde4-459c-b8c5-dfef08fc8295', '0b58dc9b-9c49-4b19-bb58-9c06d41c8fbf']


def artist_relationships_short(subj, adj, n1, n2, d, part='f', subj_artist_id='', introduce_f_with_adj=True):
    if 'phrase_n1' in d and 'phrase_n2' in d and d['phrase_n1'] == d['phrase_n2']:
        if re.match(r'^(is|was|were|have|has|does|do) ', d['phrase_n2']):
            d['phrase_n2'] = ' '.join(d['phrase_n2'].split(' ')[:1]+['also']+d['phrase_n2'].split(' ')[1:])
        else:
            d['phrase_n2'] = f"also {d['phrase_n2']}"

    article = 'the'
    new_subj = subj
    if subj_artist_id != '':
        if artist_id(n1['graph']) == subj_artist_id:
            article = f"{resolve_form('(his/s/her)/n/their', n1)}"
        else:
            new_subj = f"{subj} by {get_artist_name(subj_artist_id)}"

    skip_s = False
    if subj_artist_id != '' and artist_id(n2['graph']) == subj_artist_id:
        skip_s = True

    # Handle cases in which the artist is at the right hand side of the relationship
    if part == 'f':
        if n1['graph'][father(n1)['id']][n1['id']]['type'] in right_relationships:
            return f"the {adj} {new_subj} {d['phrase_n1']} {artist_name(n1)}"
        else:
            if introduce_f_with_adj:
                return f"{artist_name(n1)} {d['phrase_n1']} {article} {adj} {new_subj}"
            else:
                return f"{artist_name(n1)} {d['phrase_n1']} {new_subj}"

    elif part == 's':
        if skip_s:
            return ""
        else:
            if n2['graph'][father(n2)['id']][n2['id']]['type'] in right_relationships:
                return f", and the same {adj} {d['phrase_n2']} {artist_name(n2)}"
            else:
                return f", and {artist_name(n2)} {d['phrase_n2']} the same {adj}"

    elif part == 'b':
        return f"{artist_relationships_short(subj, adj, n1, n2, d, part='f',subj_artist_id=subj_artist_id, introduce_f_with_adj=introduce_f_with_adj)}{artist_relationships_short(subj, adj, n1, n2, d, part='s',subj_artist_id=subj_artist_id,introduce_f_with_adj=introduce_f_with_adj)}"


def artist_relationships_line(subj, adj, n1, n2, d, part='f', subj_artist_id='', introduce_f_with_adj=True):
    if part == 'f':
        return f"That was {artist_name(n1)}. {artist_relationships_short(subj, adj, n1, n2, d, 'f', subj_artist_id,introduce_f_with_adj=introduce_f_with_adj)}"
    elif part == 's':
        return f"{artist_relationships_short(subj, adj, n1, n2, d, 's',subj_artist_id,introduce_f_with_adj=introduce_f_with_adj)}. Now, we listen to {artist_name(n2)} with {track_name(n2)}"
    elif part == 'b':
        return f"{artist_relationships_line(subj, adj, n1, n2, d, 'f',subj_artist_id,introduce_f_with_adj=introduce_f_with_adj)} {artist_relationships_line(subj, adj, n1, n2, d, 's',subj_artist_id,introduce_f_with_adj=introduce_f_with_adj)}"


_description_dichotomic = {
    'related_word_semantics_phrase': {
        'word': {
            'word': {
                'token_phrase': {
                    'token_phrase': {
                        'track_name': {
                            'first': lambda n1, n2, d: f"The word {d['word_1']}, belonging to the title of the previous track ({track_name(n1)}), has a strong semantical similarity with",
                            'second': lambda n1, n2, d: f"the word {d['word_2']}, belonging to the title of the next track ({track_name(n2)}).",
                        },
                        'album_name': {
                            'first': lambda n1, n2, d: f"The word {d['word_1']}, belonging to the title of the album from which the previous track was taken ({album_name(n1)}), has a strong semantical similarity with",
                            'second': lambda n1, n2, d: f"the word {d['word_2']}, belonging to the title of the album from which the next track is taken ({album_name(n2)}).",
                        },
                        'artist_name': {
                            'first': lambda n1, n2, d: f"The word {d['word_1']}, belonging to the name of the previous artist ({artist_name(n1)}), has a strong semantical similarity with",
                            'second': lambda n1, n2, d: f"the word {d['word_2']}, belonging to the name of the next artist ({artist_name(n2)}).",
                        },
                        'track_chorus': {
                            'first': lambda n1, n2, d: f"The word {d['word']}, belonging to the chorus of the previous track ({d1['track_chorus']}), has a strong semantical similarity with",
                            'second': lambda n1, n2, d: f"the word {d['word_2']}, belonging to the chorus of the next track ({d2['track_chorus']}).",
                        },
                    },
                },
            },
        },
    },
    'same_word_different_sense_phrase': {
        'token_phrase': {
            'token_phrase': {
                'track_name': {
                    'first': lambda n1, n2, d: f"The word {d['word']}, from the previous track name, also belongs",
                    'second': lambda n1, n2, d: f"to the title of the next track ({track_name(n2)}), but with a different meaning",
                },
                'album_name': {
                    'first': lambda n1, n2, d: f"The word {d['word']}, belonging to the title of the album from which the previous track was taken ({album_name(n1)}), also belongs",
                    'second': lambda n1, n2, d: f"to the title of the album from which the next track is taken ({album_name(n2)}), but with a different meaning",
                },
                'artist_name': {
                    'first': lambda n1, n2, d: f"The word {d['word']}, from the previous artist name, also belongs",
                    'second': lambda n1, n2, d: f"to the name of the next artist ({artist_name(n2)}), but with a different meaning",
                },
                'track_chorus': {
                    'first': lambda n1, n2, d: f"The word {d['word']}, belonging to the chorus of the previous track ({d1['track_chorus']}), also belongs",
                    'second': lambda n1, n2, d: f"to the chorus of the next track ({d2['track_chorus']}), but with a different meaning",
                },
            },
        },
    },
    'equal': {
        'lemma': {
            'first': lambda n1, n2, d: f"The word {_node_originating_lemma(n1)['value']} is the contrary of the word {_node_originating_lemma(n2)['value']}.",
            'second': lambda n1, n2, d: ""
        },
        'synset': {
            'synset': {
                'first': lambda n1, n2, d: f"{father(n1)['value']}, is a synonim of",
                'second': lambda n1, n2, d: f"the word {father(n2)['value']}.",
            },
            'hypernyms': {
                'first': lambda n1, n2, d: f"The word {father(father(n1))['value']}, is a synonim, in it's broader sense, of",
                'second': lambda n1, n2, d: f"the broader sense of word {father(father(n2))['value']}.",
            },
            'hyponyms': {
                'first': lambda n1, n2, d: f"{father(father(n1))['value']}, is a synonim, in its more narrow sense, of",
                'second': lambda n1, n2, d: f"the more narrow sense of word {father(father(n2))['value']}.",
            },
            'part_holonyms': {
                'first': lambda n1, n2, d: f"{father(father(n1))['value']}, is a synonim, in a is-part sense, of",
                'second': lambda n1, n2, d: f"the is-part sense of word {father(father(n2))['value']}.",
            },
            'part_meronyms': {
                'first': lambda n1, n2, d: f"{father(father(n1))['value']}, is a synonim, in a has-part sense, of",
                'second': lambda n1, n2, d: f"the has-part sense of word {father(father(n2))['value']}.",
            },
            'substance_holonyms': {
                'first': lambda n1, n2, d: f"{father(father(n1))['value']}, is a synonim, in a is-in sense, of",
                'second': lambda n1, n2, d: f"the is-in sense of word {father(father(n2))['value']}.",
            },
            'substance_meronyms': {
                'first': lambda n1, n2, d: f"{father(father(n1))['value']}, is a synonim, in a is-made sense, of",
                'second': lambda n1, n2, d: f"the is-made sense of word {father(father(n2))['value']}.",
            },
            'member_holonyms': {
                'first': lambda n1, n2, d: f"{father(father(n1))['value']}, is a synonim, in a is-member sense, of",
                'second': lambda n1, n2, d: f"the is-in sense of word {father(father(n2))['value']}.",
            },
            'member_meronyms': {
                'first': lambda n1, n2, d: f"{father(father(n1))['value']}, is a synonim, in a has-member sense, of",
                'second': lambda n1, n2, d: f"the is-made sense of word {father(father(n2))['value']}.",
            },
            'synset_attributes': {
                'first': lambda n1, n2, d: f"{father(father(n1))['value']}, has an attribute sense which is a synonim of",
                'second': lambda n1, n2, d: f"the attribute sense of word {father(father(n2))['value']}.",
            },
            'synset_also_sees': {
                'first': lambda n1, n2, d: f"{father(father(n1))['value']}, is linked through an also-sees relationships to a sense which is synonim of",
                'second': lambda n1, n2, d: f"the a sense linked to the word {father(father(n2))['value']} by an also-sees relationships.",
            },
            'synset_similar_tos': {
                'first': lambda n1, n2, d: f"{father(father(n1))['value']}, is linked through an similar-tos relationships to a sense which is synonim of",
                'second': lambda n1, n2, d: f"the a sense linked to the word {father(father(n2))['value']} by an similar-tos relationships.",
            },
            'synset_verb_groups': {
                'first': lambda n1, n2, d: f"{father(father(n1))['value']}, is linked through an verb-groups relationships to a sense which is synonim of",
                'second': lambda n1, n2, d: f"the a sense linked to the word {father(father(n2))['value']} by an verb-groups relationships.",
            },
            'entailment': {
                'first': lambda n1, n2, d: f"{father(father(n1))['value']} entails a sense which is synonim of",
                'second': lambda n1, n2, d: f"a sense entailed by the word {father(father(n2))['value']}.",
            },
        },
        'stem': {
            'first': lambda n1, n2, d: f"The word {father(n1)['value']} has the same stem as the word {father(n2)['value']}.",
            'second': lambda n1, n2, d: "",
        },
        'word': {
            'first': lambda n1, n2, d: f"The word {d['value']} is shared.",
            'second': lambda n1, n2, d: f"",
        },
        'phonetical_representation': {
            'word_phonetics': {
                'word': {
                    'word': {
                        'token_phrase': {
                            'token_phrase': {
                                'track_name': {
                                    'first': lambda n1, n2, d: f"The word {father(n1)['value']}, from the previous track name, sounds like",
                                    'second': lambda n1, n2, d: f"the word {father(n2)['value']}, from the next track name.",
                                },
                                'album_name': {
                                    'first': lambda n1, n2, d: f"The word {father(n1)['value']}, belonging to the title of the album from which the previous track \
                                                was taken ({album_name(n1)}), sounds like",
                                    'second': lambda n1, n2, d: f"the word {father(n2)['value']}, belonging to the title of the album from which the next track is taken ({album_name(n2)}).",
                                },
                                'artist_name': {
                                    'first': lambda n1, n2, d: f"The word {father(n1)['value']}, from the previous artist name, sounds like",
                                    'second': lambda n1, n2, d: f"the word {father(n2)['value']}, from the next artist name.",
                                },
                                'track_chorus': {
                                    'first': lambda n1, n2, d: f"The word {father(n1)['value']}, belonging to the chorus of the previous track ({d1['track_chorus']}), sounds like",
                                    'second': lambda n1, n2, d: f"the word {father(n2)['value']}, belonging to the chorus of the next track ({d2['track_chorus']}).",
                                },
                            },
                        },
                    },
                },
            },
        },
        'year': {
            'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} in {d['value']} and",
            'second': lambda n1, n2, d: f"{artist_name(n2)} {d['phrase_n2']} in the same year.",
        },
        'month': {
            'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} in the same month that",
            'second': lambda n1, n2, d: f"{artist_name(n2)} {d['phrase_n2']}: {get_month_name(d['value'])}.",
        },
        'day': {
            'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} on the same day of month that",
            'second': lambda n1, n2, d: f"{artist_name(n2)} {d['phrase_n2']}: {d['value']}.",
        },
        'day_name': {
            'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} on the same day of week that",
            'second': lambda n1, n2, d: f"{artist_name(n2)} {d['phrase_n2']}: {d['value']}.",
        },
        'day_month': {
            'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} on the same day and in the same month that",
            'second': lambda n1, n2, d: f"{artist_name(n2)} {d['phrase_n2']}: {get_month_name(d['value'][1])}, {d['value'][0]}.",
        },
        'month_year': {
            'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} in the same month and year that",
            'second': lambda n1, n2, d: f"{artist_name(n2)} {d['phrase_n2']}: {get_month_name(d['value'][0])} {d['value'][1]}.",
        },
        'day_month_year': {
            'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} on the same day and in the same month and year that",
            'second': lambda n1, n2, d: f"{artist_name(n2)} {d['phrase_n2']}: {d['value'][0]} of {get_month_name(d['value'][1])}, {d['value'][2]}.",
        },
        'city_musicbrainz': {
            'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} in the city of {get_area_value(d['value'])}, and",
            'second': lambda n1, n2, d: f"{artist_name(n2)} {d['phrase_n2']} in the city of {get_area_value(d['value'])}.",
        },
        'country_musicbrainz': {
            'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} in the {get_country_descriptor(d['value'])} of {get_area_value(d['value'])}, and",
            'second': lambda n1, n2, d: f"{artist_name(n2)} {d['phrase_n2']} in the {get_country_descriptor(d['value'])} of {get_area_value(d['value'])}.",
        },
        'record_label_musicbrainz_id': {
            'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} the record label {get_label_value(d['value'])}, and",
            'second': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} the record label {get_label_value(d['value'])}.",
        },
        'recording_musicbrainz_id': {
            'artist_relationships': {
                'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} the song {get_recording_title(n1['value'])}, while",
                'second': lambda n1, n2, d: f"{artist_name(n2)} {d['phrase_n2']} the song {get_recording_title(n2['value'])}.",
            },
        },
        'award_series': {
            'first': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} won a {d['value']},",
            'second': lambda n1, n2, d: f"and {artist_name(n2)} {resolve_form('has/n/have', n2)} won a {d['value']}.",
        },
        'award_id': {
            'first': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} won a {get_label_entity(d['value'])},",
            'second': lambda n1, n2, d: f"and {artist_name(n2)} {resolve_form('has/n/have', n2)} won a {get_label_entity(d['value'])}.",
        },
        'award_series_year': {
            'first': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} won a {d['value'][0]} in {d['value'][1]},",
            'second': lambda n1, n2, d: f"and {artist_name(n2)} {resolve_form('has/n/have', n2)} won a {d['value'][0]} in {d['value'][1]}.",
        },
        'award_id_year': {
            'first': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} won a {get_label_entity(d['value'][0])} in {d['value'][1]},",
            'second': lambda n1, n2, d: f"and {artist_name(n2)} {resolve_form('has/n/have', n2)} won a {get_label_entity(d['value'][0])} in {d['value'][1]}.",
        },
        'musical_genre_wikidata': {
            'musical_genre_musicbrainz_to_wikidata': {
                'musical_genre_musicbrainz_id': {
                    'album_genres': {
                        'first': lambda n1, n2, d: f"The previous track is identifiable with the musical genre: {get_label_entity(d['value'])}, while",
                        'second': lambda n1, n2, d: f"the next track belongs to the musical genre: {get_label_entity(d['value'])}",
                    },
                    'artist_genres': {
                        'first': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} made music identifiable with the musical genre: {get_label_entity(d['value'])}, while",
                        'second': lambda n1, n2, d: f"{artist_name(n2)} {resolve_form('has/n/have', n2)} made music belonging to the musical genre: {get_label_entity(d['value'])}",
                    },
                },
            },
            'musical_genre_ancestor_wikidata': {
                'musical_genre_wikidata': {
                    'musical_genre_musicbrainz_to_wikidata': {
                        'musical_genre_musicbrainz_id': {
                            'album_genres': {
                                'first': lambda n1, n2, d: f"The previous track is identifiable with the musical genre: {get_label_entity(father(n1)['value'])}. \
                        {get_label_entity(d['value'])} is an ancestor of {get_label_entity(father(n1)['value'])}. At the same time",

                                'second': lambda n1, n2, d: f"{get_label_entity(d['value'])} is an ancestor of {get_label_entity(father(n2)['value'])}, \
                        the musical genre to which the next track belongs",
                            },
                            'artist_genres': {
                                'first': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} made music identifiable with the musical genre: \
                        {get_label_entity(father(n1)['value'])}. {get_label_entity(d['value'])} is \
                            an ancestor of {get_label_entity(father(n1)['value'])}. At the same time",

                                'second': lambda n1, n2, d: f"{get_label_entity(d['value'])} is an ancestor of {get_label_entity(father(n2)['value'])}, and \
                        {artist_name(n2)} {resolve_form('has/n/have', n2)} made music belonging to the musical genre {get_label_entity(father(n2)['value'])}",
                            },
                        },
                    },
                },
            },
        },
        'artist_self_releasing_records': {
            'artist_self_releasing_records': {
                'first': lambda n1, n2, d: f"Both {artist_name(n1)} and {artist_name(n2)} have self-released music, so without any record label.",
                'second': lambda n1, n2, d: f"",
            },
        },
        'artist_uri_spotify': {
            'first': lambda n1, n2, d: f"The two tracks are from the same artist.",
            'second': lambda n1, n2, d: f"",
        },
        'album_uri_spotify': {
            'first': lambda n1, n2, d: f"The two tracks come from the same album",
            'second': lambda n1, n2, d: f"",
        },
        'artist_musicbrainz_id': {
            'artist_musicbrainz_id': {
                'first': lambda n1, n2, d: f"The previous artist is {artist_name(n1)}",
                'second': lambda n1, n2, d: f"and the next artist is {artist_name(n2)}",
            },
            'artist_relationships': {
                'first': lambda n1, n2, d: f"and {artist_name(n1)} {d['phrase_n1']} the artist {get_artist_name(n1['value'])}",
                'second': lambda n1, n2, d: f"and {artist_name(n2)} {d['phrase_n2']} the artist {get_artist_name(n2['value'])}",
            },
        },
        'event_musicbrainz_id': {
            'artist_relationships': {
                'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} the event {get_event_name(n1['value'])}",
                'second': lambda n1, n2, d: f"and {artist_name(n2)} {d['phrase_n2']} the event {get_event_name(n2['value'])}",
            },
        },
        'work_musicbrainz_id': {
            'artist_relationships': {
                'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} the song {get_work_title(n1['value'])}",
                'second': lambda n1, n2, d: f"and {artist_name(n2)} {d['phrase_n2']} the song {get_work_title(n2['value'])}",
            },
        },
        'place_musicbrainz_id': {
            'artist_relationships': {
                'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} the {get_place_type(n1['value'])} {get_place_name(n1['value'])}",
                'second': lambda n1, n2, d: f"and {artist_name(n2)} {d['phrase_n2']} the {get_place_type(n2['value'])} {get_place_name(n2['value'])}",
            },
        },
        'release_musicbrainz_id': {
            'artist_relationships': {
                'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} the record {get_release_title(n1['value'])}",
                'second': lambda n1, n2, d: f"and {artist_name(n2)} {d['phrase_n2']} the record {get_release_title(n2['value'])}",
            },
        },
        'release_group_musicbrainz_id': {
            'release_group_id': {
                'first': lambda n1, n2, d: f"The previous track comes from the album {album_name(n2)}",
                'second': lambda n1, n2, d: f"and the next track comes from the album {album_name(n2)}",
            },
            'artist_relationships': {
                'first': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} the record {get_release_group_title(n1['value'])}",
                'second': lambda n1, n2, d: f"and {artist_name(n2)} {d['phrase_n2']} the record {get_release_group_title(n2['value'])}",
            },
        },
        'artist_gender': {
            'artist_gender': {
                'first': lambda n1, n2, d: f"The previous artist is a {d['value']},",
                'second': lambda n1, n2, d: f"and the next artist is a {d['value']}.",
            },
        },
        'artist_type': {
            'artist_type': {
                'first': lambda n1, n2, d: f"Both the previous and the next artist can be idenfied with the same type.",
                'second': lambda n1, n2, d: f"",
            },
        },
    },
    'uncommon_words': {
        'track_name': {
            'first': lambda n1, n2, d: f"The word {d['words'][0]} can be found in the previous track's name",
            'second': lambda n1, n2, d: f"and can be also found in the next track's name.",
        },
        'album_name': {
            'first': lambda n1, n2, d: f"The word {d['words'][0]} can be found in the name of the album from which the previous track was taken",
            'second': lambda n1, n2, d: f"and can be also found in the name of the album from which the next track is taken.",
        },
        'artist_name': {
            'first': lambda n1, n2, d: f"The word {d['words'][0]} can be found in the previous artist's name",
            'second': lambda n1, n2, d: f"and can be also found in the next artist's name.",
        },
        'track_lyrics_without_section_tags': {
            'first': lambda n1, n2, d: f"The word {d['words'][0]} is contained in the previous track's lyrics",
            'second': lambda n1, n2, d: f"and can be also found in the  next track's lyrics.",
        },
    },
}

_line_atomic = {
    'equal': {
        ('lemma', 'lemma'): {
            'text': lambda n1, n2, d: word_play_line_1(f"the opposite of {_node_originating_lemma(n1)['value']} is {_node_originating_lemma(n2)['value']}", n1, n2),
        },
        ('synset', 'synset'): {
            ('part_holonyms', 'synset'): {
                'text': lambda n1, n2, d: word_play_line_1(f"{_node_originating_synset(n1)['value']} is part of {_node_originating_synset(n2)['value']}", n1, n2),
            },
            ('synset', 'part_meronyms'): {
                'text': lambda n1, n2, d: word_play_line_1(f"{_node_originating_synset(n1)['value']} is part of {_node_originating_synset(n2)['value']}", n1, n2),
            },
            ('substance_holonyms', 'synset'): {
                'text': lambda n1, n2, d: word_play_line_1(f"{_node_originating_synset(n1)['value']} is in {_node_originating_synset(n2)['value']}", n1, n2),
            },
            ('synset', 'substance_meronyms'): {
                'text': lambda n1, n2, d: word_play_line_1(f"{_node_originating_synset(n1)['value']} is in {_node_originating_synset(n2)['value']}", n1, n2),
            },
            ('member_holonyms', 'synset'): {
                'text': lambda n1, n2, d: word_play_line_1(f"{_node_originating_synset(n1)['value']} is member of {_node_originating_synset(n2)['value']}", n1, n2),
            },
            ('synset', 'member_meronyms'): {
                'text': lambda n1, n2, d: word_play_line_1(f"{_node_originating_synset(n1)['value']} is member of {_node_originating_synset(n2)['value']}", n1, n2),
            },
            ('synset', 'entailment'): {
                'text': lambda n1, n2, d: word_play_line_1(f"{_node_originating_synset(n1)['value']} is entailed by {_node_originating_synset(n2)['value']}", n1, n2),
            },
            ('entailment', 'synset'): {
                'text': lambda n1, n2, d: word_play_line_1(f"{_node_originating_synset(n1)['value']} entails {_node_originating_synset(n2)['value']}", n1, n2),
            },
            'all': {
                'text': lambda n1, n2, d: word_play_line_2(f"from {_node_originating_synset(n1)['value']} to {_node_originating_synset(n2)['value']}", n1, n2)
            },
        },
        ('stem', 'stem'): {
            'text': lambda n1, n2, d: word_play_line_2(f"from {father(n1)['value']} to {father(n2)['value']}", n1, n2),
        },
        ('word', 'word'): {
            ('word', 'word'): {
                ('token_phrase', 'token_phrase'): {
                    ('token_phrase', 'token_phrase'): {
                        ('artist_name', 'artist_name'): {
                            'text': lambda n1, n2, d: word_play_line_3(f"from one {d['value'].title()} to another", n1, n2),
                        }
                    }
                }
            },
            'all': {
                'text': lambda n1, n2, d: word_play_line_3(f"{resolve_form('a/a/an', d['value'])} {d['value']} link", n1, n2),
            }
        },
        ('year', 'year'): {
            ('record_label_dissolution_year', 'record_label_dissolution_year'): {
                ('record_label_musicbrainz_id', 'record_label_musicbrainz_id'): {
                    ('artist_recorded_label', 'artist_recorded_label'): {
                        'text': lambda n1, n2, d: f"That was {artist_name(n1)}, who released records for {get_label_value(father(n1)['value'])}, a label dissolved in {d['value']}. Now, we listen to {track_name(n2)} by {artist_name(n2)}, who released records for {get_label_value(father(n2)['value'])}, another label dissolved in {d['value']}.",
                    },
                    ('album_record_label', 'album_record_label'): {
                        'text': lambda n1, n2, d: f"That was {artist_name(n1)}'s {album_name(n1)}, a record released by {get_label_value(father(n1)['value'])}, a label dissolved in {d['value']}. Now, we listen to {artist_name(n2)}'s {album_name(n2)}, another album released by a label dissolved in {d['value']}.",
                    },
                    ('artist_recorded_label', 'album_record_label'): {
                        'text': lambda n1, n2, d: f"That was {artist_name(n1)}, who released records for {get_label_value(father(n1)['value'])}, a label dissolved in {d['value']}. Now, we listen to {track_name(n2)} by {artist_name(n2)}, who released records for {get_label_value(father(n2)['value'])}, another label dissolved in {d['value']}.",
                    },
                    ('album_record_label', 'artist_recorded_label'): {
                        'text': lambda n1, n2, d: f"That was {artist_name(n1)}'s {album_name(n1)}, a record released by {get_label_value(father(n1)['value'])}, a label dissolved in {d['value']}. Now, we listen to {artist_name(n2)}'s {album_name(n2)}, an album released by another label dissolved in {d['value']}.",
                    }
                },
            },
            ('record_label_foundation_year', 'record_label_foundation_year'): {
                ('record_label_musicbrainz_id', 'record_label_musicbrainz_id'): {
                    ('artist_recorded_label', 'artist_recorded_label'): {
                        'text': lambda n1, n2, d: f"That was {artist_name(n1)}, who released records for {get_label_value(father(n1)['value'])}, a label founded in {d['value']}. Now, we listen to {track_name(n2)} by {artist_name(n2)}, who released records for {get_label_value(father(n2)['value'])}, another label founded in {d['value']}.",
                    },
                    ('album_record_label', 'album_record_label'): {
                        'text': lambda n1, n2, d: f"That was {artist_name(n1)}'s {album_name(n1)}, a record released by {get_label_value(father(n1)['value'])}, a label founded in {d['value']}. Now, we listen to {artist_name(n2)}'s {album_name(n2)}, another album released by a label founded in {d['value']}.",
                    },
                    ('artist_recorded_label', 'album_record_label'): {
                        'text': lambda n1, n2, d: f"That was {artist_name(n1)}, who released records for {get_label_value(father(n1)['value'])}, a label founded in {d['value']}. Now, we listen to {track_name(n2)} by {artist_name(n2)}, who released records for {get_label_value(father(n2)['value'])}, another label founded in {d['value']}.",
                    },
                    ('album_record_label', 'album_record_label'): {
                        'text': lambda n1, n2, d: f"That was {artist_name(n1)}'s {album_name(n1)}, a record released by {get_label_value(father(n1)['value'])}, a label founded in {d['value']}. Now, we listen to {artist_name(n2)}'s {album_name(n2)}, another album released by a label founded in {d['value']}.",
                    },
                },
            },
            ('year', 'year'): {
                ('date', 'date'): {
                    ('album_release_date', 'album_release_date'): {
                        'text': lambda n1, n2, d: f"That was {artist_name(n1)}'s {album_name(n1)}, a record released in {d['value']}. Now, we listen to {artist_name(n2)}'s {album_name(n2)}, another record released in {d['value']}.",
                    },
                },
            },
            'all': {
                'text': lambda n1, n2, d: f"That was {artist_name(n1)}, {d['phrase_n1']} in {d['value']}, and so {'was' if re.match(r'(^| )was($| )', d['phrase_n1']) else 'did'} {artist_name(n2)}. Now, we listen to {track_name(n2)} by {artist_name(n2)}."
                                          if d['phrase_n1'] == d['phrase_n2'] else
                                          f"That was {artist_name(n1)}, {d['phrase_n1']} in {d['value']}. Now, we listen to {track_name(n2)} by {artist_name(n2)}, {d['phrase_n2']} in the same year."
            },
        },
        ('month', 'month'): {
            'text': lambda n1, n2, d: from_date_line(f"in {get_month_name(d['value'])}", "in the same month", n1, n2, d)
        },
        ('day', 'day'): {
            'text': lambda n1, n2, d: from_date_line(f"on the {day_number(d['value'])} day of a month", "on the same day of a month", n1, n2, d)
        },
        ('day_name', 'day_name'): {
            'text': lambda n1, n2, d: from_date_line(f"on a {d['value']}", "on the same day", n1, n2, d)
        },
        ('day_month', 'day_month'): {
            'text': lambda n1, n2, d: from_date_line(f"on the {day_number(d['value'][0])} of {get_month_name(d['value'][1])}", "on the same day and in the same month", n1, n2, d)
        },
        ('month_year', 'month_year'): {
            'text': lambda n1, n2, d: from_date_line(f"in the {get_month_name(d['value'][0])} of {d['value'][1]}", "in the same month and year", n1, n2, d)
        },
        ('day_month_year', 'day_month_year'): {
            'text': lambda n1, n2, d: from_date_line(f"on {get_month_name(d['value'][1])} {day_number(d['value'][0])}, {d['value'][2]}", "on the very same day", n1, n2, d)
        },
        ('city_musicbrainz', 'city_musicbrainz'): {
            'text': lambda n1, n2, d: f"That was {artist_name(n1)}, {d['phrase_n1']} in {get_area_value(d['value'])}. Now, we listen to {artist_name(n2)} {d['phrase_n2']} in the same city."
        },
        ('country_musicbrainz', 'country_musicbrainz'): {
            'text': lambda n1, n2, d: f"That was {artist_name(n1)}, {d['phrase_n1']} in {get_area_value(d['value'])}. Now, we listen to {artist_name(n2)} {d['phrase_n2']} in the same {get_country_descriptor(d['value'])}."
        },
        ('record_label_musicbrainz_id', 'record_label_musicbrainz_id'): {
            'text': lambda n1, n2, d: f"That was {artist_name(n1)}, {d['phrase_n1']} {get_label_value(d['value'])}. Now, we listen to {artist_name(n2)}, {d['phrase_n2']} the same record label."
        },
        ('recording_musicbrainz_id', 'recording_musicbrainz_id'): {
            ('artist_relationships', 'artist_relationships'): {
                'text': lambda n1, n2, d: artist_relationships_line(f'"{get_recording_title(n1["value"])}"', 'song', n1, n2, d, 'b', subj_artist_id=get_recording_artist(n1['value']))
            },
        },
        ('place_musicbrainz_id', 'place_musicbrainz_id'): {
            ('artist_relationships', 'artist_relationships'): {
                'text': lambda n1, n2, d: artist_relationships_line(get_place_name(n1['value']), get_place_type(n1['value']), n1, n2, d)
            },
        },
        ('work_musicbrainz_id', 'work_musicbrainz_id'): {
            ('artist_relationships', 'artist_relationships'): {
                'text': lambda n1, n2, d: artist_relationships_line(f'"{get_work_title(n1["value"])}"', get_work_type(n1['value']).replace('concerto', 'concert'), n1, n2, d, introduce_f_with_adj=False)
            },
        },
        ('artist_musicbrainz_id', 'artist_musicbrainz_id'): {
            ('artist_musicbrainz_id', 'artist_relationships'): {
                'text': lambda n1, n2, d: f"That was {artist_name(n1)}, {artist_relationships_line(get_artist_name(n1['value']), get_artist_type(n1['value']) if get_artist_type(n1['value'])!='person' else 'artist', n1, n2, d, 's')}."
            },
            ('artist_relationships', 'artist_musicbrainz_id'): {
                'text': lambda n1, n2, d: f"{artist_relationships_line(get_artist_name(n1['value']), get_artist_type(n1['value']) if get_artist_type(n1['value'])!='person' else 'artist', n1, n2, d, 'f')}. Now, we listen to {artist_name(n2)} with {track_name(n2)}",
            },
            ('artist_relationships', 'artist_relationships'): {
                'text': lambda n1, n2, d: artist_relationships_line(get_artist_name(n1['value']), get_artist_type(n1['value']) if get_artist_type(n1['value']) != 'person' else 'artist', n1, n2, d, 'b'),
            },
            ('artist_musicbrainz_id', 'artist_musicbrainz_id'): {
                'text': lambda n1, n2, d: f"Here's another track by {artist_name(n1)}{dots()}"
            }
        },
        ('event_musicbrainz_id', 'event_musicbrainz_id'): {
            ('artist_relationships', 'artist_relationships'): {
                'text': lambda n1, n2, d: artist_relationships_line(get_event_name(n1['value']), get_event_type(n1['value']), n1, n2, d, introduce_f_with_adj=False)
            },
        },
        ('release_musicbrainz_id', 'release_musicbrainz_id'): {
            ('artist_relationships', 'artist_relationships'): {
                'text': lambda n1, n2, d: artist_relationships_line(f'"{get_release_title(n1["value"])}"', 'record', n1, n2, d, get_release_artist(n1['value']))
            },
        },
        ('release_group_musicbrainz_id', 'release_group_musicbrainz_id'): {
            ('release_group_id', 'artist_relationships'): {
                'text': lambda n1, n2, d: f"That was {artist_name(n1)}'s {album_name(n1)}, {artist_relationships_line(get_release_group_title(n1['value']), 'album', n1, n2, d, 's')}"
            },
            ('artist_relationships', 'release_group_id'): {
                'text': lambda n1, n2, d: artist_relationships_line(f'"{get_release_group_title(n1["value"])}"', 'album', n1, n2, d, 'f') + f" , and now, from that album{dots()}",
            },
            ('artist_relationships', 'artist_relationships'): {
                'text': lambda n1, n2, d: artist_relationships_line(f'"{get_release_group_title(n1["value"])}"', 'album', n1, n2, d, 'b', get_release_group_artist(n1['value'])) + dots(),
            },
            ('release_group_id', 'release_group_id'): {
                'text': lambda n1, n2, d: f"We stick with {artist_name(n1)}'s album {album_name(n1)}, here comes {track_name(n1)}{dots()}"
            },
        },
        ('award_series', 'award_series'): {
            'text': lambda n1, n2, d: f"From one {d['value']} winner to another, next up is {artist_name(n2)} \
                with {track_name(n2)}.",
        },
        ('award_id', 'award_id'): {
            'text': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} won {get_label_entity(d['value'])}, \
                            and so {resolve_form('has/n/have', n2)} {artist_name(n2)}. Now we hear him with {track_name(n2)}.",
        },
        ('award_series_year', 'award_series_year'): {
            'text': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} won a {d['value'][0]} in {d['value'][1]}, \
                    and so {resolve_form('has/n/have', n2)} {artist_name(n2)}. Now we hear him with {track_name(n2)}.",
        },
        ('award_id_year', 'award_id_year'): {
            'text': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} won {get_label_entity(d['value'][0])} in {d['value'][1]}, \
                    and so {resolve_form('has/n/have', n2)} {artist_name(n2)}. Now we hear him with {track_name(n2)}.",
        },
        ('artist_type', 'artist_type'): {
            'text': lambda n1, n2, d: f"We just heard a {'solo artist' if d['value']=='Person' else 'band' if d['value']=='Group' else 'finctional character' if d['value']=='Character' else d['value'].lower()}, and now we listen to another {'solo artist' if d['value']=='Person' else 'band' if d['value']=='Group' else 'finctional character' if d['value']=='Character' else d['value'].lower()}. Let's play {track_name(n2)} by {artist_name(n2)}.",
        },
        ('artist_self_releasing_records', 'artist_self_releasing_records'): {
            'text': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} self-released music, and so {resolve_form('has/n/have', n2)} \
                        {artist_name(n2)}. Let's hear {artist_name(n2)} with {track_name(n2)}.",
        },
        ('album_uri_spotify', 'album_uri_spotify'): {
            'text': lambda n1, n2, d: f"The next track, like the previous one, is from the album: {album_name(n1)}.",
        },
        ('artist_uri_spotify', 'artist_uri_spotify'): {
            'text': lambda n1, n2, d: f"And, for our next tack, let's stick with {artist_name(n1)}.",
        },
        ('artist_gender', 'artist_gender'): {
            'text': lambda n1, n2, d: f"We just heard a {d['value'].lower()} artist, and now we listen to another {d['value'].lower()} artist. Let's hear {track_name(n2)} by {artist_name(n2)}.",
        },
        ('musical_genre_wikidata', 'musical_genre_wikidata'): {
            ('musical_genre_musicbrainz_to_wikidata', 'musical_genre_musicbrainz_to_wikidata'): {
                ('musical_genre_musicbrainz_id', 'musical_genre_musicbrainz_id'): {
                    ('album_genres', 'album_genres'): {
                        'text': lambda n1, n2, d: f"We just heard a {get_label_entity(d['value'])} track, and now we play another {get_label_entity(d['value'])} track: {track_name(n2)} by {artist_name(n2)}.",
                    }
                }
            }
        },
        ('musical_genre_musicbrainz_id', 'musical_genre_musicbrainz_id'): {
            ('artist_genres', 'artist_genres'): {
                'text': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} made {get_genre_name(d['value'])} music, and so did {artist_name(n2)}...",
            }
        },
        ('area_musicbrainz_id', 'area_musicbrainz_id'): {
            'text': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} in {get_area_value(d['value'])} and {artist_name(n2)} {d['phrase_n2']} in the same {get_area_type(d['value'])}...",
        },
    },
}

_line_dichotomic = {
    'equal': {
        'phonetical_representation': {
            'word_phonetics': {
                'word': {
                    'word': {
                        'token_phrase': {
                            'token_phrase': {
                                'track_name': {
                                    'first': lambda n1, n2, d: f"We just heard {undeline_word(father(d['n1'])['value'], track_name(n1))}",
                                    'second': lambda n1, n2, d: f"and now we'll play {undeline_word(father(d['n2'])['value'], track_name(n2))}.",
                                },
                                'album_name': {
                                    'first': lambda n1, n2, d: f"We just heard {track_name(n1)} from the album {undeline_word(father(d['n1'])['value'], album_name(n1))}",
                                    'second': lambda n1, n2, d: f"and now, from {undeline_word(father(d['n2'])['value'], album_name(n2))}, we have {track_name(n2)}.",
                                },
                                'artist_name': {
                                    'first': lambda n1, n2, d: f"We just heard {track_name(n1)} by {undeline_word(father(d['n1'])['value'],  artist_name(n1))}.",
                                    'second': lambda n1, n2, d: f"and now we listen to {undeline_word(father(d['n2'])['value'], artist_name(n2))}, with {track_name(n2)}.",
                                },
                                'track_chorus': {
                                    'first': lambda n1, n2, d: f"We just heard {artist_name(n1)} singing the words \"{undeline_word(father(d['n1'])['value'], d1['track_chorus'])}\",",
                                    'second': lambda n1, n2, d: f"and now, in {track_name(n2)}, {artist_name(n2)} will sing the \
                                words \"{undeline_word(father(d['n2'])['value'], d2['track_chorus'])}\"."
                                },
                            },
                        },
                    },
                },
            },
        },
        'musical_genre_wikidata': {
            'musical_genre_musicbrainz_to_wikidata': {
                'musical_genre_musicbrainz_id': {
                    'album_genres': {
                        'first': lambda n1, n2, d: f"We just heard a {get_label_entity(d['value'])} track, and",
                        'second': lambda n1, n2, d: f"now we play a {get_label_entity(d['value'])} track: {track_name(n2)} by {artist_name(n2)}.",
                    },
                    'artist_genres': {
                        'first': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} made {get_label_entity(d['value'])}, and",
                        'second': lambda n1, n2, d: f"{artist_name(n2)} recorded music of the same genre. Let's hear {artist_name(n2)} with {track_name(n2)}.",
                    },
                },
            },
            'musical_genre_ancestor_wikidata': {
                'musical_genre_wikidata': {
                    'musical_genre_musicbrainz_to_wikidata': {
                        'musical_genre_musicbrainz_id': {
                            'album_genres': {
                                'first': lambda n1, n2, d: f"We just heard a {get_label_entity(father(d['n1'])['value'])} track, \
                                a genre which derives from {get_label_entity(d['value'])}, and",
                                'second': lambda n1, n2, d: f"one kind of {get_label_entity(d['value'])} is {get_label_entity(father(d['n2'])['value'])}. \
                                Let's hear a {get_label_entity(father(d['n2'])['value'])} track: {track_name(n2)} by {artist_name(n2)}.",
                            },
                            'artist_genres': {
                                'first': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} made {get_label_entity(father(d['n1'])['value'])}, \
                                a genre which derives from {get_label_entity(d['value'])}, and",
                                'second': lambda n1, n2, d: f"one kind of {get_label_entity(d['value'])} is \
                                {get_label_entity(father(d['n2'])['value'])}, \
                                    a genre interpreted by {artist_name(n2)}. Let's hear {artist_name(n2)} with {track_name(n2)}.",
                            },
                        },
                    },
                },
            },
        },
    },
    'uncommon_words': {
        'track_name': {
            'first': lambda n1, n2, d: f"A {d['words'][0]} link: we just heard {track_name(n1)}",
            'second': lambda n1, n2, d: f"and now we hear {track_name(n2)} by {artist_name(n2)}.",
        },
        'album_name': {
            'first': lambda n1, n2, d: f"A {d['words'][0]} link: we just heard a track from the album {album_name(n1)}",
            'second': lambda n1, n2, d: f"and now, from {album_name(n2)}, we hear {track_name(n2)} by {artist_name(n2)}.",
        },
        'artist_name': {
            'first': lambda n1, n2, d: f"A {d['words'][0]} link: we just heard from {artist_name(n1)}",
            'second': lambda n1, n2, d: f"and next up is {artist_name(n2)}, with {track_name(n2)}.",
        },
        'track_lyrics_without_section_tags': {
            'first': lambda n1, n2, d: f"A {d['words'][0]} link: we heard {d['words'][0]} in the lyrics of {track_name(n1)}",
            'second': lambda n1, n2, d: f"and we'll find {d['words'][0]} in the lyrics of our next track, {track_name(n2)} by {artist_name(n2)}.",
        },
    },
    'related_word_semantics_phrase': {
        'word': {
            'word': {
                'token_phrase': {
                    'token_phrase': {
                        'track_name': {
                            'first': lambda n1, n2, d: f"We just heard {undeline_word(d['word_1'], track_name(n1))}",
                            'second': lambda n1, n2, d: f"and now we'll play {undeline_word(d['word_2'], track_name(n2))}.",
                        },
                        'album_name': {
                            'first': lambda n1, n2, d: f"We just heard {track_name(n1)} from the album {undeline_word(d['word_1'], album_name(n1))}",
                            'second': lambda n1, n2, d: f"and now, from {undeline_word(d['word_2'], album_name(n2))}, we have {track_name(n2)}.",
                        },
                        'artist_name': {
                            'first': lambda n1, n2, d: f"We just heard {track_name(n1)} by {undeline_word(d['word_1'], artist_name(n1))}.",
                            'second': lambda n1, n2, d: f"Now we listen to {undeline_word(d['word_2'], artist_name(n2))}, with {track_name(n2)}.",
                        },
                        'track_chorus': {
                            'first': lambda n1, n2, d: f"We just heard {artist_name(n1)} singing the words \"{undeline_word(d['word_1'], d1['track_chorus'])}\",",
                            'second': lambda n1, n2, d: f"and now, in {track_name(n2)}, {artist_name(n2)} will sing the \
                        words \"{undeline_word(d['word_2'], d2['track_chorus'])}\"."
                        },
                    },
                },
            },
        },
    },
    'same_word_different_sense_phrase': {
        'token_phrase': {
            'token_phrase': {
                'track_name': {
                    'first': lambda n1, n2, d: f"We just heard {track_name(n1)}",
                    'second': lambda n1, n2, d: f"and now we'll play {track_name(n2)}.",
                },
                'album_name': {
                    'first': lambda n1, n2, d: f"We just heard {track_name(n1)} from the album {album_name(n1)}",
                    'second': lambda n1, n2, d: f"and now, from {album_name(n2)}, we have {track_name(n2)}.",
                },
                'artist_name': {
                    'first': lambda n1, n2, d: f"We just heard {track_name(n1)} by {artist_name(n1)}",
                    'second': lambda n1, n2, d: f"and now we listen to {artist_name(n2)}, with {track_name(n2)}.",
                },
                'track_chorus': {
                    'first': lambda n1, n2, d: f"We just heard {artist_name(n1)} singing the words {track_chorus(n1['graph'])},",
                    'second': lambda n1, n2, d: f"and now, in {track_name(n2)}, {artist_name(n2)} will sing the words {track_chorus(n2['graph'])}."
                },
            },
        },
    },
}

_short_atomic = {
    'equal': {
        ('phonetical_representation', 'phonetical_representation'): {
            'text': lambda n1, n2, d: word_play_line_1(f"{father(d['n1'])['value']} sounds like {father(d['n2'])['value']}", n1, n2)
        },
        ('year', 'year'): {
            ('record_label_dissolution_year', 'record_label_dissolution_year'): {
                ('record_label_musicbrainz_id', 'record_label_musicbrainz_id'): {
                    ('artist_recorded_label', 'artist_recorded_label'): {
                        'text': lambda n1, n2, d: f"{artist_name(n1)} released records for {get_label_value(father(n1)['value'])}, a label dissolved in {d['value']}, and {artist_name(n2)} released records for {get_label_value(father(n2)['value'])}, another label dissolved in {d['value']}{dots()}",
                    },
                    ('album_record_label', 'artist_recorded_label'): {
                        'text': lambda n1, n2, d: f"{artist_name(n1)}'s {album_name(n1)} was released by {get_label_value(father(n1)['value'])}, a label dissolved in {d['value']}, and {artist_name(n2)} released records for {get_label_value(father(n2)['value'])}, another label dissolved in {d['value']}{dots()}",
                    },
                    ('artist_recorded_label', 'album_record_label'): {
                        'text': lambda n1, n2, d: f"{artist_name(n1)} released records for {get_label_value(father(n1)['value'])}, a label dissolved in {d['value']}, and {artist_name(n2)}'s {album_name(n2)} is from another label dissolved in {d['value']}{dots()}",
                    },
                    ('album_record_label', 'album_record_label'): {
                        'text': lambda n1, n2, d: f"{artist_name(n1)}'s {album_name(n1)} was released by {get_label_value(father(n1)['value'])}, a label dissolved in {d['value']}, and {artist_name(n2)}'s {album_name(n2)} is from another label dissolved in {d['value']}{dots()}",
                    },
                },
            },
            ('record_label_foundation_year', 'record_label_foundation_year'): {
                ('record_label_musicbrainz_id', 'record_label_musicbrainz_id'): {
                    ('artist_recorded_label', 'artist_recorded_label'): {
                        'text': lambda n1, n2, d: f"{artist_name(n1)} released records for {get_label_value(father(n1)['value'])}, a label founded in {d['value']}, and {artist_name(n2)} released records for {get_label_value(father(n2)['value'])}, another label founded in {d['value']}{dots()}",
                    },
                    ('album_record_label', 'artist_recorded_label'): {
                        'text': lambda n1, n2, d: f"{artist_name(n1)}'s {album_name(n1)} was released by {get_label_value(father(n1)['value'])}, a label founded in {d['value']}, and {artist_name(n2)} released records for {get_label_value(father(n2)['value'])}, another label founded in {d['value']}{dots()}",
                    },
                    ('artist_recorded_label', 'album_record_label'): {
                        'text': lambda n1, n2, d: f"{artist_name(n1)} released records for {get_label_value(father(n1)['value'])}, a label founded in {d['value']}, and {artist_name(n2)}'s {album_name(n2)} is from another label founded in {d['value']}{dots()}",
                    },
                    ('album_record_label', 'album_record_label'): {
                        'text': lambda n1, n2, d: f"{artist_name(n1)}'s {album_name(n1)} was released by {get_label_value(father(n1)['value'])}, a label founded in {d['value']}, and {artist_name(n2)}'s {album_name(n2)} is from another label founded in {d['value']}{dots()}",
                    },
                },
            },
            ('year', 'year'): {
                ('date', 'date'): {
                    ('album_release_date', 'album_release_date'): {
                        'text': lambda n1, n2, d: f"{artist_name(n1)}'s {album_name(n1)} was released in {d['value']} and so was {artist_name(n2)}'s {album_name(n2)}{dots()}",
                    },
                },
            },
            'all': {
                'text': lambda n1, n2, d:
                    f"{artist_name(n1)} {d['phrase_n1']} in {d['value']}, and so {'was' if re.match(r'(^| )was($| )', d['phrase_n1']) else 'did'} {artist_name(n2)}{dots()}"
                    if d['phrase_n1'] == d['phrase_n2'] else
                    f"{artist_name(n1)} {d['phrase_n1']} in {d['value']}, while {artist_name(n2)} {d['phrase_n2']} in the same year{dots()}"
            },
        },
        ('month', 'month'): {
            'text': lambda n1, n2, d: from_date_short(f"in {get_month_name(d['value'])}", "in the same month", n1, n2, d)
        },
        ('day', 'day'): {
            'text': lambda n1, n2, d: from_date_short(f"in the {day_number(d['value'])} day of a month", "on the same day of a month", n1, n2, d)
        },
        ('day_name', 'day_name'): {
            'text': lambda n1, n2, d: from_date_short(f"in a {d['value']}", "on the same day", n1, n2, d)
        },
        ('day_month', 'day_month'): {
            'text': lambda n1, n2, d: from_date_short(f"on the {day_number(d['value'][0])} of {get_month_name(d['value'][1])}", "on the same day and in the same month", n1, n2, d)
        },
        ('month_year', 'month_year'): {
            'text': lambda n1, n2, d: from_date_short(f"in the {get_month_name(d['value'][0])} of {d['value'][1]}", "in the same month and year", n1, n2, d)
        },
        ('day_month_year', 'day_month_year'): {
            'text': lambda n1, n2, d: from_date_short(f"on {get_month_name(d['value'][1])} {day_number(d['value'][0])}, {d['value'][2]}", "on the very same day", n1, n2, d)
        },
        ('area_musicbrainz_id', 'area_musicbrainz_id'): {
            'text': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} in {get_area_value(d['value'])} and {artist_name(n2)} {d['phrase_n2']} in the same {get_area_type(d['value'])}",
        },
        ('city_musicbrainz', 'city_musicbrainz'): {
            'text': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} in {get_area_value(d['value'])} and {artist_name(n2)} {d['phrase_n2']} in the same city{dots()}",
        },
        ('country_musicbrainz', 'country_musicbrainz'): {
            'text': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} in {get_area_value(d['value'])} and {artist_name(n2)} {d['phrase_n2']} in the same {get_country_descriptor(d['value'])}{dots()}",
        },
        ('record_label_musicbrainz_id', 'record_label_musicbrainz_id'): {
            ('artist_relationships', 'artist_relationships'): {
                'text': lambda n1, n2, d: artist_relationships_short(get_label_value(n1['value']), 'record label', n1, n2, d, 'b') + dots(),
            },
            'all': {
                'text': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} {get_label_value(d['value'])} and {artist_name(n2)} {d['phrase_n2']} the same record label{dots()}",
            }
        },
        ('recording_musicbrainz_id', 'recording_musicbrainz_id'): {
            ('artist_relationships', 'artist_relationships'): {
                'text': lambda n1, n2, d: artist_relationships_short(f'"{get_recording_title(n1["value"])}"', 'song', n1, n2, d, 'b', subj_artist_id=get_recording_artist(n1['value'])) + dots(),
            },
        },
        ('place_musicbrainz_id', 'place_musicbrainz_id'): {
            ('artist_relationships', 'artist_relationships'): {
                'text': lambda n1, n2, d: artist_relationships_short(get_place_name(n1['value']), get_place_type(n1['value']), n1, n2, d, 'b') + dots(),
            },
        },
        ('work_musicbrainz_id', 'work_musicbrainz_id'): {
            ('artist_relationships', 'artist_relationships'): {
                'text': lambda n1, n2, d: artist_relationships_short(f'"{get_work_title(n1["value"])}"', get_work_type(n1['value']).replace('concerto', 'concert'), n1, n2, d, 'b', introduce_f_with_adj=False) + dots(),
            },
        },
        ('artist_musicbrainz_id', 'artist_musicbrainz_id'): {
            ('artist_musicbrainz_id', 'artist_musicbrainz_id'): {
                'text': lambda n1, n2, d: f"And, for our next tack, let's stick with {artist_name(n1)}.",
            },
            ('artist_musicbrainz_id', 'artist_relationships'): {
                'text': lambda n1, n2, d: f"{artist_name(n2)} {d['phrase_n2']} {artist_name(n1)}{dots()}",
            },
            ('artist_relationships', 'artist_musicbrainz_id'): {
                'text': lambda n1, n2, d: f"{artist_name(n1)} {d['phrase_n1']} {artist_name(n2)}{dots()}",
            },
            ('artist_relationships', 'artist_relationships'): {
                'text': lambda n1, n2, d: artist_relationships_short(get_artist_name(n1['value']), get_artist_type(n1['value']) if get_artist_type(n1['value']) != 'person' else 'artist', n1, n2, d, 'b') + dots(),
            },
        },
        ('event_musicbrainz_id', 'event_musicbrainz_id'): {
            ('artist_relationships', 'artist_relationships'): {
                'text': lambda n1, n2, d: artist_relationships_short(get_event_name(n1['value']), get_event_type(n1['value']), n1, n2, d, 'b', introduce_f_with_adj=False) + dots(),
            }
        },
        ('release_musicbrainz_id', 'release_musicbrainz_id'): {
            ('artist_relationships', 'artist_relationships'): {
                'text': lambda n1, n2, d: artist_relationships_short(f'"{get_release_title(n1["value"])}"', 'record', n1, n2, d, 'b', get_release_artist(n1['value'])) + dots(),
            },
        },
        ('release_group_musicbrainz_id', 'release_group_musicbrainz_id'): {
            ('release_group_id', 'release_group_id'): {
                'text': lambda n1, n2, d: f"The next track, like the previous one, is from the album {album_name(n1)}{dots()}",
            },
            ('release_group_id', 'artist_relationships'): {
                'text': lambda n1, n2, d: f"That was {artist_name(n1)}'s {album_name(n1)}, {artist_relationships_short(get_release_group_title(n1['value']), 'album', n1, n2, d, 's')}{dots()}"
            },
            ('artist_relationships', 'release_group_id'): {
                'text': lambda n1, n2, d: artist_relationships_short(f'"{get_release_group_title(n1["value"])}"', 'album', n1, n2, d, 'f') + f" , and now, from that album{dots()}",
            },
            ('artist_relationships', 'artist_relationships'): {
                'text': lambda n1, n2, d: artist_relationships_short(f'"{get_release_group_title(n1["value"])}"', 'album', n1, n2, d, 'b', get_release_group_artist(n1['value'])) + dots(),
            },
        },
        ('award_series', 'award_series'): {
            'text': lambda n1, n2, d: f"From one {d['value']} winner to another{dots()}"
        },
        ('award_id', 'award_id'): {
            'text': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} won {get_label_entity(d['value'])}, \
                            and so {resolve_form('has/n/have', n2)} {artist_name(n2)}{dots()}",
        },
        ('artist_self_releasing_records', 'artist_self_releasing_records'): {
            'text': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} self-released music, and so {resolve_form('has/n/have', n2)} \
                        {artist_name(n2)}{dots()}",
        },
        ('award_series_year', 'award_series_year'): {
            'text': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} won a {d['value'][0]} in {d['value'][1]}, \
                    and so {resolve_form('has/n/have', n2)} {artist_name(n2)}{dots()}",
        },
        ('award_id_year', 'award_id_year'): {
            'text': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} won {get_label_entity(d['value'][0])} in {d['value'][1]}, \
                    and so {resolve_form('has/n/have', n2)} {artist_name(n2)}{dots()}",
        },
        ('artist_type', 'artist_type'): {
            'text': lambda n1, n2, d: f"{artist_name(n1)} is a {'solo artist' if d['value']=='Person' else 'band' if d['value']=='Group' else 'finctional character' if d['value']=='Character' else d['value'].lower()}, and {artist_name(n2)} is a {'solo artist' if d['value']=='Person' else 'band' if d['value']=='Group' else 'finctional character' if d['value']=='Character' else d['value'].lower()}{dots()}",
        },
        ('album_uri_spotify', 'album_uri_spotify'): {
            'text': lambda n1, n2, d: f"The next track, like the previous one, is from the album: {album_name(n1)}.",
        },
        ('artist_uri_spotify', 'artist_uri_spotify'): {
            'text': lambda n1, n2, d: f"And, for our next tack, let's stick with {artist_name(n1)}.",
        },
        ('artist_gender', 'artist_gender'): {
            'text': lambda n1, n2, d: f"From a {d['value'].lower()} artist to another{dots()}",
        },
        ('musical_genre_musicbrainz_id', 'musical_genre_musicbrainz_id'): {
            ('artist_genres', 'artist_genres'): {
                'text': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} made {get_genre_name(d['value'])}, and so did {artist_name(n2)}...",
            }
        },
        ('musical_genre_wikidata', 'musical_genre_wikidata'): {
            ('musical_genre_musicbrainz_to_wikidata', 'musical_genre_musicbrainz_to_wikidata'): {
                ('musical_genre_musicbrainz_id', 'musical_genre_musicbrainz_id'): {
                    ('album_genres', 'album_genres'): {
                        'text': lambda n1, n2, d: f"We just heard a {get_label_entity(d['value'])} track, and now we play another {get_label_entity(d['value'])} track{dots()}",
                    }
                }
            }
        }
    }
}

_short_dichotomic = {
    'equal': {
        'musical_genre_wikidata': {
            'musical_genre_musicbrainz_to_wikidata': {
                'musical_genre_musicbrainz_id': {
                    'album_genres': {
                        'first': lambda n1, n2, d: f"We just heard a {get_label_entity(d['value'])} track, and",
                        'second': lambda n1, n2, d: f"now we play a {get_label_entity(d['value'])} track{dots()}",
                    },
                    'artist_genres': {
                        'first': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} made {get_label_entity(d['value'])}, and",
                        'second': lambda n1, n2, d: f"{artist_name(n2)} recorded music of the same genre{dots()}",
                    },
                },
            },
            'musical_genre_ancestor_wikidata': {
                'musical_genre_wikidata': {
                    'musical_genre_musicbrainz_to_wikidata': {
                        'musical_genre_musicbrainz_id': {
                            'album_genres': {
                                'first': lambda n1, n2, d: f"We just heard a {get_label_entity(father(d['n1'])['value'])} track, \
                                a genre which derives from {get_label_entity(d['value'])}, and",
                                'second': lambda n1, n2, d: f"one kind of {get_label_entity(d['value'])} is {get_label_entity(father(d['n2'])['value'])}. \
                                Let's hear a {get_label_entity(father(d['n2'])['value'])} track{dots()}",
                            },
                            'artist_genres': {
                                'first': lambda n1, n2, d: f"{artist_name(n1)} {resolve_form('has/n/have', n1)} made {get_label_entity(father(d['n1'])['value'])}, \
                                a genre which derives from {get_label_entity(d['value'])}, and",

                                'second': lambda n1, n2, d: f"one kind of {get_label_entity(d['value'])} is \
                                {get_label_entity(father(d['n2'])['value'])}, \
                                    a genre interpreted by {artist_name(n2)}{dots()}",
                            },
                        },
                    },
                },
            },
        },
    },
}


def search_dictionary_dicothomic(dict_dichotomic, d):
    """A dicothomic dictionary is indexed this way:
       1) Compare function that originate the segue
       2) A sequence of node types and generating_functions, of length >= 1

       A dicotomic dictionary is indexed two times.
       The first time, using the information relative to the first node that composes the segue
       The second time, same as before, but with the second node

       A dicthomic dictionary have a minimum of two levels, but it can exploit more levels
       in case the nodes associated share their type with many others, and so the text cannot be distinguished
       E.g: For every artist, we mine the birth date and the death date. Given one of this, the function year
            returns the year the date refers to. The node type won't suffice to determine
            the exact text, being for both of them 'year'. Therefore, we use the generating function of the nodes year
            and in this case we disambiguate the right text.
            In general, we continue to jump from type to generating function to type again until the text cannot be disambiguated.

       At the last level, we expect to find two keywords 'first' and 'second', that we access, depending whether we are considering
       the first node of second node that contribute to the association


       Starting from the second level, the keyword 'all' is allowed.
       E.g: If a type cannot be found in the dictionary, but the keywork 'all' is present (under that compare function),
            then the following level will be the one specified by the keyword 'all'.
       after an 'all' we expect to find the keys 'first' and 'second'

       'all' has the lowest precedence: if the type of generating function is present for that level, we go for it, even if
       an 'all' could be picked.

       If we reach a dead end (i.e. the sequence of node type, generating function does not lead to a text), we backtrack searching for an 'all'.
       We return the first 'all' that we find, if any.

    Arguments:
        dict_dichotomic {dict } -- Dicothomic dictionary containing the texts
        d {segue} -- Segue that needs a text
    """

    def go_recursive_on_type_level_dicothomic(node_type_level, n, search_for):
        """Realizes the disambiguation based on generating on type and generating function of nodes.

        Arguments:
            node_type_level {d} --
            n {ngx Node}
            search_for {str} -- Either 'first' or 'second'. Being it dicothomic, two accesses are needed to the dictionary

        """

        if n['type'] in node_type_level:
            edge_type_level = node_type_level[n['type']]

            if search_for in edge_type_level:
                return edge_type_level[search_for]
            else:

                gen_function = n['graph'][father(n)['id']][n['id']]['generating_function']
                if gen_function in edge_type_level:
                    node_type_level = edge_type_level[gen_function]

                    if search_for in node_type_level:
                        return node_type_level[search_for]
                    else:
                        try:
                            return go_recursive_on_type_level_dicothomic(node_type_level, father(n), search_for)
                        except IndexError:
                            pass

                elif 'all' in edge_type_level:
                    return edge_type_level['all'][search_for]

        elif 'all' in node_type_level:
            return node_type_level['all'][search_for]

    def get_part(dict_dichotomic, d, search_for):
        """Return either the first of the second part of the segue's text, using the strategy descibed.
           In case we want the first part, we have to supply first node related information (id, type and first graph),
           and the same goes for the second part

        Arguments:
            dict_dichotomic {dict} -- Dicothomic dictionary containing the texts
            d {dict} -- The segue
            search_for {str} -- Either first of second

        """
        if d['compare_function'] in dict_dichotomic:
            compare_function_level = dict_dichotomic[d['compare_function']]

            node = d['n1'] if search_for == 'first' else d['n2']
            return go_recursive_on_type_level_dicothomic(compare_function_level, node, search_for)

    first_part = get_part(dict_dichotomic, d, 'first')
    second_part = get_part(dict_dichotomic, d, 'second')

    if first_part is not None and second_part is not None:
        return (first_part, second_part)
    else:
        return None


def search_dictionary_atomic(dict_atomic, d):
    """Please refer to the documentation of search_dictionary_dichotomic.
       Few details change:

       - The dictionary is indexed once, with the two types of nodes as a tuple, as well as the generating functions
       - The all keyword is used as single string, with rules unchanged with respect to search_dictionary_dichotomic
       - The text is found under the keyword 'text' (instead of the two keywords 'first' and 'second')
    """

    def go_recursive_on_type_level_atomic(level, n1, n2, level_type, key):
        """Homologos function of the dichotomic case
        """
        val = None
        if key in level:
            next_level = level[key]
            if level_type == 'node':
                gen_function_1 = n1['graph'][father(n1)['id']][n1['id']]['generating_function']
                gen_function_2 = n2['graph'][father(n2)['id']][n2['id']]['generating_function']
                next_key = (gen_function_1, gen_function_2)
                next_level_type = 'edge'
                next_n1 = father(n1)
                next_n2 = father(n2)
            else:
                next_key = (n1['type'], n2['type'])
                next_level_type = 'node'
                next_n1 = n1
                next_n2 = n2

            val = go_recursive_on_type_level_atomic(next_level, next_n1, next_n2, next_level_type, next_key)

        if val is None:
            try:
                val = level['text']
            except KeyError:
                try:
                    val = level['all']['text']
                except KeyError:
                    pass

        return val

    if d['compare_function'] in dict_atomic:
        compare_function_level = dict_atomic[d['compare_function']]
        text = go_recursive_on_type_level_atomic(compare_function_level, d['n1'], d['n2'], 'node', (d['n1']['type'], d['n2']['type']))
        return text


def segue_canned_texts(segue, kind, excecute_code=True):
    """Return the canned text associated to the segue, and to a type.
    Canned texts can be either short (The Chain style), line (DJ-style) and description (i-Button style).

    We always specify desctiption and line. If not, this method throws an exception.
    We sometimes specify a short, in case we'd like to distinguish it from the line. Otherwise, the line type is used.

    The texts are retrieved traversing the dictionaries by means of the methods search_dictionary_dicothomic and search_dictionary_atomic,
    where they are specified in the form of lambdas. This function excecute the lambdas and gets the actual text to show.
    The excecute_code function controls whether the lambdas should be excecuted or not (defualt: True).


    Arguments:
        segue {dict} -- A dictionary with the two nodes that compose the segue ('n1' and 'n2') and the compare function (compare_function) according to which there is a path from 'n1' and 'n2'
        kind {str} -- Either line or description
        excecute_code {bool}
    """

    def enrich_with_phrases(segue, kind):
        """Retrieves the two phrases associated to the two nodes composing the segue
        The two phrases are added to the segue as two new keys, to be exploited in short, line and description texts.

        Args:
            segue (d)
            kind (str): whether short, line or description

        Returns:
            d: segue dictionary enriched with phrases
        """
        phrase_n1 = phrase(segue['n1'], segue['compare_function'], kind)
        phrase_n2 = phrase(segue['n2'], segue['compare_function'], kind)
        if phrase_n1 is not None:
            segue = {**{'phrase_n1': phrase_n1(segue['n1'], segue)}, **segue}
        if phrase_n2 is not None:
            segue = {**{'phrase_n2': phrase_n2(segue['n2'], segue)}, **segue}
        return segue

    assert kind in ['line', 'description', 'short']

    if kind == 'description':
        text = search_dictionary_dicothomic(_description_dichotomic, segue)

    elif kind == 'line':
        text = search_dictionary_atomic(_line_atomic, segue)
        text = search_dictionary_dicothomic(_line_dichotomic, segue) if text is None else text

    elif kind == 'short':
        text = search_dictionary_atomic(_short_atomic, segue)
        text = search_dictionary_dicothomic(_short_dichotomic, segue) if text is None else text
        if text is None:
            try:
                text = segue_canned_texts(segue, 'line', excecute_code=False)
            except KeyError:
                pass

    if text is not None:

        if excecute_code:
            segue = enrich_with_phrases(segue, kind)

            if type(text) == tuple:
                # dicothomic
                text = f"{text[0](segue['n1'], segue['n2'], segue)} {text[1](segue['n1'], segue['n2'], segue)}"
            else:
                # atomic
                text = text(segue['n1'], segue['n2'], segue)

            # Postprocessing
            # Fix multiple spaces
            text = ' '.join(text.split())
            # First letter is capital
            text = capitalize_first_word(text)
            # Fix spaces among word and 's in genitivo sassone
            text = re.sub(r"([a-zA-Z]+)\s+('s)", r"\1\2", text)
            text = text.replace(', ,', ',')

        return text
    else:
        raise KeyError(
            f"It was not possible to find a {kind} for node of types, respectively {segue['n1']['type']} and {segue['n2']['type']}, with compare function {segue['compare_function']}. The ids of the nodes are, respectively {segue['n1']['id']} and {segue['n2']['id']}")
