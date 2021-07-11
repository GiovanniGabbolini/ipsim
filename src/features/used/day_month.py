"""
Created on --

@author Giovanni Gabbolini
"""

from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def day_month(date) -> 'day_month':
    """Extracts month from a date.
    
    The edge produced by this feature is not counted in interestingess's shortness heuristics"""
    return {'value': (date['value'].day, date['value'].month)}
