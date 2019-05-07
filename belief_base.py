from sympy.logic.boolalg import to_cnf, is_cnf
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
        self.formulas = resolve_base(self.formulas, preposition)
        for x in self.formulas: print(x)

bb = belief_base()

"""
Test Cases Used so Far:
    Input_1:
        a|b|c, ~b|~c|f
    Expected Output:
        a | c | ~c | f, a | b | ~b | f
    Actual Output:
        a | c | f | ~c, a | b | f | ~b
        
    Input_2:
        p|q, p>>r, q>>r
    Expected Output:
        r
    Actual Output:
        r
    Input_3:
        a|b, ~a|c
    Expected Output:
        b|c
    Actual Output:
        b|c
    Input_4:
        d, ~d
    Expected Output:
        
    Actual Output:
    Input_5:
        a|b|c|d, ~a|d
    Expected Output:
        b|c|d
    Actual Output:
        b|c|d
"""