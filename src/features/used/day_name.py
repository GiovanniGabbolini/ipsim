"""
Created on --

@author Giovanni Gabbolini
"""

from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def day_name(date) -> 'day_name':
    """Extracts the day name from a date e.g. Monday.
    
    The edge produced by this feature is not counted in interestingess's shortness heuristics"""
    return {'value': date['value'].day_name()}
