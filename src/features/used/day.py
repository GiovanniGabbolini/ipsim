"""
Created on --

@author Giovanni Gabbolini
"""

from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def day(date)->'day':
    """Extracts the day of the month from a date e.g. 5.
    
    The edge produced by this feature is not counted in interestingess's shortness heuristics"""
    return {'value': date['value'].day}
