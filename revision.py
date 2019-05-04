from sympy.logic.boolalg import Or, to_cnf

"""
Revises belief base using the given formula
Only necessary when formula was found to be inconsistent with the belief base
"""

def resolve_base(ci, cj):
    """Return the first clauses that can be obtained by resolving clauses ci and cj."""
    clauses = []
    for di in disjuncts(ci):
        #print("Here_1")
        for dj in disjuncts(cj):
            #print("Here_2")
            #print(di)
            #print(dj)
            if di == ~dj or ~di == dj:
                #print("Here_3")
                ##REMOVE CLAUSES WHICH ARE RESOLVED
                ci = list(ci.args)
                if len(ci) > 1:
                    ci.remove(di)
                else:
                    ci = []
                cj = list(cj.args)
                if len(cj) > 1:
                    cj.remove(dj)
                else:
                    cj = []
                
                ##CREATE RESOLVED BASE
                part1 = ""
                part2 = ""
                if len(ci) == 0:
                    part1 = ""
                elif len(ci) == 1:
                    part1 += str(ci[0])
                else:
                    for var in range(len(ci)-1):
                        part1 += str(to_cnf(ci[var] | ci[var+1]))
                if len(cj) == 0:
                    part2 = ""
                elif len(cj) == 1:
                    part2 += str(cj[0])
                else:
                    for var in range(len(cj)-1):
                        part2 += str(to_cnf(cj[var] | cj[var+1]))
                        
                if part1 == "":
                    clauses = to_cnf(part2)
                elif part2 == "":
                    clauses = to_cnf(part1)
                else:
                    clauses = (to_cnf(to_cnf(part1) | to_cnf(part2)))
                return {clauses}
    
    return clauses

def disjuncts(s):
    """Return a list of the disjuncts in s."""
    if isinstance(s, Or):
        return list(s.args)
    else:
        return [s]