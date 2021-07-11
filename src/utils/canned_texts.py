import re
from src.utils.utils_ngx_graph import artist_gender, artist_type, artist_solo_end_activity_year, artist_band_end_activity_year
from nltk.corpus import cmudict
from src.utils.utils_ngx_graph import album_name as album_name_utils
from src.utils.utils_ngx_graph import track_name as track_name_utils
from src.utils.utils_ngx_graph import artist_name as artist_name_utils


def custom_title(s):
    return re.sub(r"[^'\s]([a-zA-Z]+)", lambda v: v.group().title(), s)


def starts_with_vowel_sound(word, pronunciations=cmudict.dict()):
    for syllables in pronunciations.get(word, []):
        return syllables[0][-1].isdigit()  # use only the first one


def album_name(n):
    return f"\"{album_name_utils(n['graph'])}\""


def track_name(n):
    return f"\"{track_name_utils(n['graph'])}\""


def artist_name(n):
    return f"{artist_name_utils(n['graph'])}"


def resolve_form(string, obj):
    """Given a formatted string representing nested binary alternatives for a text, pick one based on obj
    The string is formatted according to the following grammar:

    s->s1/t/s1
    s1->(s1/t/s1)|w
    t->s|n|p|a
    w->whetever sequence of characters

    Args:
        s (string)
        obj
    """

    def pick_one(s1, s2, t, obj):
        if t == 's':
            return s1 if artist_gender(obj['graph']) == 'male' else s2
        elif t == 'n':
            return s1 if artist_type(obj['graph']) in ['person', 'character'] else s2
        elif t == 'p':
            return s1 if artist_band_end_activity_year(obj['graph']) is None and artist_solo_end_activity_year(obj['graph']) is None else s2
        elif t == 'a':
            return s1 if not starts_with_vowel_sound(obj) else s2

    num = 0
    if string[0] == '(':
        num += 1
        for idx, s in enumerate(string[1:]):
            num += 1 if s == '(' else 0
            num -= 1 if s == ')' else 0
            if num == 0:
                break
        alternative_1 = resolve_form(string[1:idx+1], obj)
        j = idx+3
    else:
        idx = string.find('/')
        alternative_1 = string[:idx]
        j = idx+1

    t = string[j:j+1]

    if string[j+2] == '(':
        num += 1
        for idx, s in enumerate(string[j+3:]):
            num += 1 if s == '(' else 0
            num -= 1 if s == ')' else 0
            if num == 0:
                break
        alternative_2 = resolve_form(string[j+3:-1], obj)
    else:
        alternative_2 = string[j+2:]

    return pick_one(alternative_1, alternative_2, t, obj)
