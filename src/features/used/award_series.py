"""
Created on --

@author Giovanni Gabbolini
"""

from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def award_series(award_wikidata) -> 'award_series':
    """Extracts a tuple from artist awards dictionary.
    
    The edge produced by this feature is not counted in interestingess's shortness heuristics
    """
    if 'award_series' in award_wikidata['value']:
        return {'value': award_wikidata['value']['award_series']}
