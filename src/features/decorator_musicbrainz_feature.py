from functools import wraps
from src.utils.musicbrainz_setup import musicbrainzngs_setup

""" 
Useful to setup the musicbrainz libraries for api calls
"""


def musicbrainz_feature(func):

    @wraps(func)
    def func_wrapper(*args, **kwargs):

        musicbrainzngs_setup()

        r = func(*args, **kwargs)

        return r

    return func_wrapper
