"""
Created on Mon Jan 11 2021

@author Giovanni Gabbolini
"""


def trunc(number, n_digits):
    return '{:.{prec}f}'.format(number, prec=n_digits)
