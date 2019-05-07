from sympy import And
from sympy.logic.inference import satisfiable

"""
Checks if a given formula is consistent with the current belief base
Given two cnfs a, b:
    if a U b is not satisfiable, b does not follow from a
"""
def is_consistent(ci, cj):
    test = combine_cnfs(ci, cj)
    dictionary = satisfiable(test)
    if isinstance(dictionary, dict) is False:
        print("INCONSISTENT")
        return False

    return True

def combine_cnfs(a, b):
    return And(a, b)