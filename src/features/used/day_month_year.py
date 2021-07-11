"""
Created on --

@author Giovanni Gabbolini
"""

from src.utils.decorator_annotations import annotations


@annotations({'entailed': True})
def day_month_year(date) -> 'day_month_year':
    """Extracts the day, month and year from a date.
    
    The edge produced by this feature is not counted in interestingess's shortness heuristics"""
    return {'value': (date['value'].day, date['value'].month, date['value'].year)}
