from sympy.logic.boolalg import Or, to_cnf

"""
Revises belief base using the given formula
Only necessary when formula was found to be inconsistent with the belief base
"""

def resolve_base(ci, cj):
    """Return the first clauses that can be obtained by resolving clauses ci and cj."""
    clauses = []
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
                    part1 += str(ci_temp[0])
                else:
                    for var in range(len(ci_temp)-1):
                        part1 += str(to_cnf(ci_temp[var] | ci_temp[var+1]))
                if len(cj_temp) == 0:
                    part2 = ""
                elif len(cj_temp) == 1:
                    part2 += str(cj_temp[0])
                else:
                    for var in range(len(cj_temp)-1):
                        part2 += str(to_cnf(cj_temp[var] | cj_temp[var+1]))
                if part1 == "" and part2 == "":
                    break
                elif part1 == "":
                    #clauses = to_cnf(part2)
                    clauses.append(to_cnf(part2))
                elif part2 == "":
                    #clauses = to_cnf(part1)
                    clauses.append(to_cnf(part1))
                else:
                    #clauses = (to_cnf(to_cnf(part1) | to_cnf(part2)))
                    clauses.append((to_cnf(to_cnf(part1) | to_cnf(part2))))
                #return {clauses}
    
    return clauses

def disjuncts(s):
    """Return a list of the disjuncts in s."""
    if isinstance(s, Or):
        return list(s.args)
    else:
        return [s]
