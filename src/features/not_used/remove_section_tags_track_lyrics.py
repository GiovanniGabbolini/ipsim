import re
from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def remove_section_tags_track_lyrics(track_lyrics) -> 'track_lyrics_without_section_tags':
    t = re.sub('\[.+\]', '', track_lyrics['value'])
    return {'value': t}
