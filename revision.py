from sympy.logic.boolalg import And, Or, to_cnf
from consistency import is_consistent

"""
Revises belief base using the given formula
Only necessary when formula was found to be inconsistent with the belief base
"""

def resolve_base(bb, formula):
    "Propositional Logic Resolution: say if alpha follows from KB. [Fig. 7.12]"
    consistent = False
    result = set()
    
    ##Break up sentence by conjuncts
    clauses = conjuncts(to_cnf(formula))
    for clause in bb:
        clauses.append(clause)
    
    ##Assume no consistency and stop if belief's found to be consistent
    while not consistent:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i+1, n)]
        for (ci, cj) in pairs:
            resolvents = resolve_clauses(ci, cj)
            if is_consistent(ci, cj): consistent = True
            
            #Check special case where resolved to empty set
            if resolvents == False:
                clauses.remove(ci)
                clauses.remove(cj)
                return set(clauses)
            else:
                for x in resolvents:
                    result.add(x)
        #If result is consistent, break loop and return the initial clauses
        if result.issubset(set(clauses)): 
            consistent = True
    
    ##If any resolve results were found, return them. Otherwise, return the clauses
    if len(result) > 0: 
        return result
    else: 
        return clauses

def resolve_clauses(ci, cj):
    """Return the first clauses that can be obtained by resolving clauses ci and cj."""
    clauses = []
    #print("Clause1: ", ci)
    #print("Clause2: ", cj)
    ci_temp = ci
    cj_temp = cj
    for di in disjuncts(ci):
        #print("Here_1")
        for dj in disjuncts(cj):
            #print("Here_2")
            #print(di)
            #print(dj)
            if di == ~dj or ~di == dj:
                #print("Here_3")
                ##REMOVE CLAUSES WHICH ARE RESOLVED
                ci_temp = list(ci.args)
                if len(ci_temp) > 1:
                    ci_temp.remove(di)
                else:
                    ci_temp = []
                cj_temp = list(cj.args)
                if len(cj_temp) > 1:
                    cj_temp.remove(dj)
                else:
                    cj_temp = []
                
                ##CREATE RESOLVED BASE
                part1 = ""
                part2 = ""
                if len(ci_temp) == 0:
                    part1 = ""
                elif len(ci_temp) == 1:
                    part1 = str(ci_temp[0])
                else:
                    for var in range(len(ci_temp)):
                        if var == len(ci_temp)-1:
                            part1 += str(ci_temp[var])
                        else:
                            part1 += str(ci_temp[var]) + "|"
                if len(cj_temp) == 0:
                    part2 = ""
                elif len(cj_temp) == 1:
                    part2 = str(cj_temp[0])
                else:
                    for var in range(len(cj_temp)):
                        if var == len(cj_temp)-1:
                            part2 += str(cj_temp[var])
                        else:
                            part2 += str(cj_temp[var]) + "|"

                if len(part1) == 0 and len(part2) == 0:
                    return False
                elif len(part1) == 0:
                    clauses.append(to_cnf(part2))
                elif len(part2) == 0:
                    clauses.append(to_cnf(part1))
                else:
                    clauses.append((to_cnf(to_cnf(part1) | to_cnf(part2))))
                #print("Clauses: ", clauses)
    return clauses

def disjuncts(s):
    """Return a list of the disjuncts in s."""
    if isinstance(s, Or):
        return list(s.args)
    else:
        return [s]
    
def conjuncts(s):
    """Return a list of the conjuncts in s."""
    if isinstance(s, And):
        return list(s.args)
    else:
        return [s]

