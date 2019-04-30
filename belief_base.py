from sympy.logic.boolalg import to_cnf, is_cnf
from consistency import is_consistent
from revision import revise_base

"""
Belief base class to store all currently held beliefs in a set
"""
class belief_base:
    
    """
    Initialize belief base as empty
    Start listening for input
    """
    def __init__(self):
        self.formulas = set()
        
        while True:
            print("\nEnter a prepositional formula, \n'help' for instructions, \n'print' to view formulas, \n'quit' to exit")
            formula = input("Formula: ")
            if formula == 'help':
                print("TODO\n")
            elif formula == 'print':
                for x in self.formulas:
                    print(x)
            elif formula == 'quit':
                return
            else:
                try:
                    is_cnf(formula)
                    self.add_formula(formula)
                except:
                    print("Invalid formula syntax")
                    
        
    """
    Add new formula to the belief base
    """
    def add_formula(self, formula):
        preposition = to_cnf(formula)
        
        if is_consistent(self, preposition):
            self.formulas.add(preposition)
        else:
            self = revise_base(self, preposition)
            

bb = belief_base()
