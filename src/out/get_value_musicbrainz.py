import requests
import musicbrainzngs
from bs4 import BeautifulSoup


def get_area_value(id):
    a = musicbrainzngs.get_area_by_id(id)
    return a['area']['name']


def get_area_value(id):
    a = musicbrainzngs.get_area_by_id(id)
    return a['area']['name']


def get_area_type(id):
    a = musicbrainzngs.get_area_by_id(id)
    return a['area']['type']


def get_label_value(id):
    l = musicbrainzngs.get_label_by_id(id)
    return l['label']['name']


def get_genre_name(id):
    req = requests.get(f"https://musicbrainz.org/genre/{id}")
    soup = BeautifulSoup(req.text, "html.parser")
    genre_name = soup.find_all('bdi')[0].next
    return genre_name


def get_recording_title(id):
    l = musicbrainzngs.get_recording_by_id(id)
    return l['recording']['title']


def get_recording_artist(id):
    l = musicbrainzngs.get_recording_by_id(id, includes=['artists'])
    return l['recording']['artist-credit'][0]['artist']['id']


def get_release_artist(id):
    l = musicbrainzngs.get_release_by_id(id, includes=['artists'])
    return l['release']['artist-credit'][0]['artist']['id']


def get_artist_name(id):
    l = musicbrainzngs.get_artist_by_id(id)
    return l['artist']['name']


def get_artist_type(id):
    l = musicbrainzngs.get_artist_by_id(id)
    try:
        return l['artist']['type'].lower()
    except KeyError:
        return 'person'


def get_series_name(id):
    l = musicbrainzngs.get_series_by_id(id)
    return l['series']['name']


def get_event_type(id):
    l = musicbrainzngs.get_event_by_id(id)
    try:
        t = l['event']['type'].lower()
    except KeyError:
        t = 'event'
    return t


def get_work_type(id):
    l = musicbrainzngs.get_work_by_id(id)
    try:
        t = l['work']['type'].lower()
    except KeyError:
        t = 'song'
    return t


def get_work_title(id):
    l = musicbrainzngs.get_work_by_id(id)
    return l['work']['title']


def get_release_title(id):
    l = musicbrainzngs.get_release_by_id(id)
    return l['release']['title']


def get_release_group_title(id):
    l = musicbrainzngs.get_release_group_by_id(id)
    return l['release-group']['title']


def get_release_group_artist(id):
    l = musicbrainzngs.get_release_group_by_id(id, includes=['artists'])
    return l['release-group']['artist-credit'][0]['artist']['id']


def get_event_name(id):
    l = musicbrainzngs.get_event_by_id(id)
    return l['event']['name']


def get_place_name(id):
    l = musicbrainzngs.get_place_by_id(id)
    return l['place']['name']


def get_place_type(id):
    l = musicbrainzngs.get_place_by_id(id)
    try:
        t = l['place']['type'].lower()
    except KeyError:
        t = 'place'
    return t
