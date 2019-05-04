from sympy import And
from sympy.logic.inference import satisfiable

"""
Checks if a given formula is consistent with the current belief base
Given two cnfs a, b:
    if a U b is not satisfiable, b does not follow from a
"""
def is_consistent(bb, formula):
    for belief in bb:
        test = combine_cnfs(belief, formula)
        dictionary = satisfiable(test)
        if dictionary is False:
            return False
        for __, value in dictionary.items():
            if value is False:
                print("INCONSISTENT")
                return False
        
    return True

def combine_cnfs(a, b):
    return And(a, b)

    