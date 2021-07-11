'''
Created on Sun Feb 02 2020

@author Giovanni Gabbolini
'''


import re
from src.features.decorator_timing_feature import timing_feature
from src.features.array_feature import array_feature

from src.features.decorator_cached_feature import cached_feature


@cached_feature
@timing_feature
def track_chorus(track_lyrics) -> 'track_chorus':
    """ 
    simply uses the chorus annotation of genius to extract the chorus sections
    then, return the phrase of the chorus section which is more often present
    in this way, the chorus is found in 38% of the cases in which the track_lyrics are available.
    this is due by genius: only 38% of the times, the label [Chorus] appears in the track_lyrics
    """

    is_chorus = False
    phrase_chorus_repetition = {}
    for phrase in track_lyrics['value'].split('\n'):
        if re.search('\[.*.*\]', phrase):
            is_chorus = True if re.search(
                r'\[(.*Chorus.*)|(.*Hook.*)\]', phrase, re.I) else False
            continue
        if is_chorus:
            phrase_chorus_repetition[phrase] = phrase_chorus_repetition[phrase] + \
                1 if phrase in phrase_chorus_repetition else 1

    # if no chorus, return None
    if len(phrase_chorus_repetition.values()) == 0:
        return None
    highest_frequency = max(phrase_chorus_repetition.values())
    candidate_phrases = [key for key in phrase_chorus_repetition.keys(
    ) if phrase_chorus_repetition[key] == highest_frequency]

    assert len(
        candidate_phrases) >= 1, "At this point, we should have at least one candidate phrase"
    candidate_phrases = sorted(
        candidate_phrases, key=len, reverse=True)
    return {'value': candidate_phrases[0]}


if __name__ == '__main__':
    array_feature(track_chorus, mp=False)
