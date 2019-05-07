from sympy.logic.boolalg import to_cnf, is_cnf
from consistency import is_consistent
from revision import resolve_base

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
                print("SYMBOLS:\n\t{a, b, ... , z}\n\t{A, B, ... , Z}\n\n" + 
                      "OPERATORS:\n\tAND:     a & b\n\tOR:      a | b\n\t" + 
                      "NOT:     ~a\n\tXOR:     a ^ b\n\tIMPLIES: a >> b, b << a" + 
                      "\n\tIFF:     Equivalent(a, b)")
            elif formula == 'print':
                for x in self.formulas:
                    print(x)
            elif formula == 'quit':
                return
            else:
                try:
                    is_cnf(formula)
                except:
                    print("Invalid formula syntax")
                    
                self.add_formula(formula)  
                                          
        
    """
    Add new formula to the belief base
    """
    def add_formula(self, formula):
        preposition = to_cnf(formula)
        
        if is_consistent(self.formulas, preposition):
            self.formulas.add(preposition)
        else:
            self.formulas = set(resolve_base(list(self.formulas)[0], preposition))

bb = belief_base()