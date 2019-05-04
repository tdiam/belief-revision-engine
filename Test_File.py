from revision import resolve_base
from sympy.logic.boolalg import to_cnf, Or


#print(to_cnf("A|~B").args)

#Test_1
resolve_base(to_cnf("A|B|C"), to_cnf("A|~B|F"))
#Test_2
#resolve_base(to_cnf("A|B"), to_cnf("A|~B|F"))
#Test_3
#resolve_base(to_cnf("A|B|C"), to_cnf("~A|~B|F"))
#Test_4
#resolve_base(to_cnf("A"), to_cnf("~A|~B"))
#Test_5
#resolve_base(to_cnf("A|B"), to_cnf("~A"))


'''
cnf = to_cnf("A|B")
to_print = cnf.atoms()
for variable in to_print: print(variable)
#ops = cnf.remove(to_print)
print(cnf.args)
print(isinstance(cnf, Or))
'''