"""
Created on Wed Jul 08 2020

@author Giovanni Gabbolini
"""


from src.utils.utils_ngx_graph import father
from src.sparql.get_label_entity_wikidata import get_label_entity
from src.out.get_value_musicbrainz import get_area_value, get_label_value, get_recording_title, get_artist_name, get_event_name, get_event_type, get_work_type, get_work_title, get_release_title, get_series_name, get_release_group_title
from src.utils.canned_texts import album_name, track_name
from src.data.data import preprocessed_dataset_path
import json
from src.utils.canned_texts import resolve_form


_phrase = {
    'equal': {
        # a tuple is matched if either one of the tuple elements matches
        ('record_label_musicbrainz_id', 'recording_musicbrainz_id', 'place_musicbrainz_id', 'work_musicbrainz_id', 'release_musicbrainz_id', 'release_group_musicbrainz_id', 'artist_musicbrainz_id', 'event_musicbrainz_id'): {
            'artist_recorded_label': {
                'short': lambda n, d: f"{resolve_form('has/n/have', n)} released music for",
                'line': lambda n, d: f"who {resolve_form('has/n/have', n)} released music for",
                'description': lambda n, d: f"{resolve_form('has/n/have', n)} released a former album with",
            },
            'album_record_label': {
                'short': lambda n, d: f"'s {track_name(n)} was released by",
                'line': lambda n, d: f"with the album {album_name(n)}, which was released by",
                'description': lambda n, d: f"'s album {album_name(n)} was released by",
            },
            'artist_relationships': {
                'short': lambda n, d: get_template_relationship(n),
                'line': lambda n, d: get_template_relationship(n),
                'description': lambda n, d: f"{get_template_relationship(n)}",
            },
        },
        ('area_musicbrainz_id', 'area_musicbrainz_id'): {
            'artist_based_in_area': {
                'short': lambda n, d: f"{resolve_form('(is/n/are)/p/(was/n/were)', n)} based",
                'line': lambda n, d: f"who {resolve_form('(is/n/are)/p/(was/n/were)', n)} based",
                'description': lambda n, d: f"{resolve_form('(is/n/are)/p/(was/n/were)', n)} actually based",
            },
            'artist_birth_place_area': {
                'short': lambda n, d: f"was born",
                'line': lambda n, d: f"who was born",
                'description': lambda n, d: f"was born",
            },
            'record_label_area': {
                'record_label_musicbrainz_id': {
                    'artist_recorded_label': {
                        'short': lambda n, d: f"released records with {get_label_value(father(father(n))['value'])}, a label based",
                        'line': lambda n, d: f"who released records with {get_label_value(father(father(n))['value'])}, a label based",
                        'description': lambda n, d: f"released a former record with {get_label_value(father(father(n))['value'])}, a label that has its headquarter",
                    },
                    'album_record_label': {
                        'short': lambda n, d: f"'s {track_name(n)} was released by {get_label_value(father(father(n))['value'])}, a label based",
                        'line': lambda n, d: f"with the album {album_name(n)}, which was released by {get_label_value(father(father(n))['value'])}, a label based",
                        'description': lambda n, d: f"'s {album_name(n)} was released by {get_label_value(father(father(n))['value'])}, a label that has its headquarter",
                    },
                },
            },
        },
        ('city_musicbrainz', 'country_musicbrainz'): {
            ('area_city', 'area_country'): {
                'area_musicbrainz_id': {
                    'artist_based_in_area': {
                        'short': lambda n, d: f"{resolve_form('(is/n/are)/p/(was/n/were)', n)} based",
                        'line': lambda n, d: f"who {resolve_form('(is/n/are)/p/(was/n/were)', n)} based",
                        'description': lambda n, d: f"{resolve_form('(is/n/are)/p/(was/n/were)', n)} actually based",
                    },
                    'artist_birth_place_area': {
                        'short': lambda n, d: f"was born",
                        'line': lambda n, d: f"who was born",
                        'description': lambda n, d: f"was born",
                    },
                    'record_label_area': {
                        'record_label_musicbrainz_id': {
                            'artist_recorded_label': {
                                'short': lambda n, d: f"released records with {get_label_value(father(father(n))['value'])}, a label based",
                                'line': lambda n, d: f"who released records with {get_label_value(father(father(n))['value'])}, a label based",
                                'description': lambda n, d: f"released a former record with {get_label_value(father(father(n))['value'])}, a label that has its headquarter",
                            },
                            'album_record_label': {
                                'short': lambda n, d: f"'s {track_name(n)} was released by {get_label_value(father(father(n))['value'])}, a label based",
                                'line': lambda n, d: f"with the album {album_name(n)}, which was released by {get_label_value(father(father(n))['value'])}, a label based",
                                'description': lambda n, d: f"'s {album_name(n)} was released by {get_label_value(father(father(n))['value'])}, a label that has its headquarter",
                            },
                        },
                    },
                },
            },
        },
        ('year', 'month', 'day', 'day_name', 'day_month', 'month_year', 'day_month_year'): {
            'artist_solo_end_activity_year': {
                'short': lambda n, d: f"ended {resolve_form('his/s/her', n)} music career",
                'line': lambda n, d: f"who ended {resolve_form('his/s/her', n)} music career",
                'description': lambda n, d: f"ended {resolve_form('his/s/her', n)} carrer in the music industry",
            },
            'artist_solo_start_activity_year': {
                'short': lambda n, d: f"started {resolve_form('his/s/her', n)} music career",
                'line': lambda n, d: f"who started {resolve_form('his/s/her', n)} music career",
                'description': lambda n, d: f"started {resolve_form('his/s/her', n)} carrer in the music industry",
            },
            'artist_band_end_activity_year': {
                'short': lambda n, d: f"broke up",
                'line': lambda n, d: f"who broke up",
                'description': lambda n, d: f"was formed as a band",
            },
            'artist_band_start_activity_year': {
                'short': lambda n, d: f"started being a band",
                'line': lambda n, d: f"who started being a band",
                'description': lambda n, d: f"started being a band",
            },
            'award_year': {
                'short': lambda n, d: f"received a {get_label_entity(father(n)['value']['award_id'])}",
                'line': lambda n, d: f"who received a {get_label_entity(father(n)['value']['award_id'])}",
                'description': lambda n, d: f"won the award known as {get_label_entity(father(n)['value']['award_id'])}",
            },
            'record_label_dissolution_year': {
                'record_label_musicbrainz_id': {
                    'artist_recorded_label': {
                        'short': lambda n, d: f"released records for {get_label_value(father(n)['value'])}, a label which dissolved",
                        'line': lambda n, d: f"who released records for {get_label_value(father(n)['value'])}, a label which dissolved",
                        'description': lambda n, d: f"released a former album with {get_label_value(father(n)['value'])}, a record label that stop existing",
                    },
                    'album_record_label': {
                        'short': lambda n, d: f"'s {track_name(n)} was released by {get_label_value(father(n)['value'])}, a record label which dissolved",
                        'line': lambda n, d: f"with the album {album_name(n)}, which was released by {get_label_value(father(n)['value'])}, a record label which dissolved",
                        'description': lambda n, d: f"'s {album_name(n)} was released by {get_label_value(father(n)['value'])}, a record label that stop existing",
                    },
                },
            },
            'record_label_foundation_year': {
                'record_label_musicbrainz_id': {
                    'artist_recorded_label': {
                        'short': lambda n, d: f"released records for {get_label_value(father(n)['value'])}, a label founded",
                        'line': lambda n, d: f"who released records for {get_label_value(father(n)['value'])}, a label founded",
                        'description': lambda n, d: f"released a former album with {get_label_value(father(n)['value'])}, a record label which was founded",
                    },
                    'album_record_label': {
                        'short': lambda n, d: f"'s {track_name(n)} was released by {get_label_value(father(n)['value'])}, a record label which was founded",
                        'line': lambda n, d: f"with the album {album_name(n)}, released by {get_label_value(father(n)['value'])}, a record label which was founded",
                        'description': lambda n, d: f"'s {album_name(n)} was released by {get_label_value(father(n)['value'])}, a record label which was founded",
                    },
                },
            },
            ('year', 'month', 'day', 'day_name', 'day_month', 'month_year', 'day_month_year'): {
                'date': {
                    'artist_birth_date': {
                        'short': lambda n, d: f"was born",
                        'line': lambda n, d: f"who was born",
                        'description': lambda n, d: f"was born",
                    },
                    'album_release_date': {
                        'short': lambda n, d: f"'s {track_name(n)} was released",
                        'line': lambda n, d: f"with the album {album_name(n)}, which was released",
                        'description': lambda n, d: f"'s {album_name(n)} was released",
                    },
                    'artist_death_date': {
                        'short': lambda n, d: f"sadly died",
                        'line': lambda n, d: f"who sadly died",
                        'description': lambda n, d: f"died",
                    },
                },
            },
        },
    },
}


def get_template_relationship(n):
    with open(f"{preprocessed_dataset_path}/textual_templates_artist_relationships.json") as f:
        d = json.load(f)
        d = {k: inner_dict[k] for inner_dict in d.values() for k in inner_dict.keys()}
    template = d[n['graph'][father(n)['id']][n['id']]['type']]['preprocessed']
    return template


def phrase(n, compare_function, search_for):
    """Associates a phrase to a node n based upon its type, the generating function that generated it, 
    the type of the node to which we applied the generating function, the generating function before, .... and this way recursively.

    Args:
        n (ngx node)
        compare_function (str)
        search_for (str): either short, line or description
    """

    def phrase_recursive(n, node_type_level, search_for):
        if search_for in node_type_level:
            return node_type_level[search_for]

        for k in node_type_level.keys():
            k_as_tuple = (k,) if type(k) == str else k
            if n['type'] in k_as_tuple:

                edge_type_level = node_type_level[k]

                if search_for in edge_type_level:
                    return edge_type_level[search_for]

                if father(n) == None:
                    return None
                else:
                    gen_function = n['graph'][father(n)['id']][n['id']]['generating_function']
                    for k in edge_type_level.keys():
                        k_as_tuple = (k,) if type(k) == str else k
                        if gen_function in k_as_tuple:

                            node_type_level = edge_type_level[k]
                            return phrase_recursive(father(n), node_type_level, search_for)

    for k in _phrase.keys():
        k_as_tuple = (k,) if type(k) == str else k
        if compare_function in k_as_tuple:

            node_type_level = _phrase[k]
            phrase = phrase_recursive(n, node_type_level, search_for)

            if phrase is not None:
                return phrase
