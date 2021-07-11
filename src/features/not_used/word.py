"""
Created on --

@author Giovanni Gabbolini
"""
from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def word(token_phrase) -> 'word':
    """Extract the word field from a token dictionary.
    
    The edge produced by this feature is not counted in interestingess's shortness heuristics."""
    return {'value': token_phrase['value']}
