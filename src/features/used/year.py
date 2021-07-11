"""
Created on --

@author Giovanni Gabbolini
"""
from src.utils.decorator_annotations import annotations


@annotations({'entailed': True})
def year(date) -> 'year':
    """Extracts an year from a date.
    
    The edge produced by this feature is not counted in interestingess's shortness heuristics."""
    return {'value': str(date['value'].year)}
