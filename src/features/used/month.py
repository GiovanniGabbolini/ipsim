"""
Created on --

@author Giovanni Gabbolini
"""

from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def month(date) -> 'month':
    """Extracts month from a date e.g. January.
    
    The edge produced by this feature is not counted in interestingess's shortness heuristics"""
    return {'value': date['value'].month}
