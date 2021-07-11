"""
Created on --

@author Giovanni Gabbolini
"""

from src.utils.decorator_annotations import annotations

@annotations({'entailed': True})
def month_year(date)-> 'month_year':
    """Extracts month and year from a date.
    
    The edge produced by this feature is not counted in interestingess's shortness heuristics"""
    return {'value': (date['value'].month, date['value'].year)}
