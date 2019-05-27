"""
The resolution functions here have been adapted from the
aima-python code repository, which contains implementations of
the algorithms in "Artificial Intelligence: A Modern Approach"
by Stuart Russell and Peter Norvig.

The MIT License (MIT)

Copyright (c) 2016 aima-python contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Link:
https://github.com/aimacode/aima-python
"""

from sympy.logic.boolalg import to_cnf, Or

from utils import (
    conjuncts, disjuncts,
    unique, removeall,
    associate,
)


def entails(base, formula):
    """
    Resolution-based entailment check for base |- formula.
    """

    # Split base into conjuncts
    clauses = []
    for f in base:
        clauses += conjuncts(f)
    # Add contradiction to start resolution
    clauses += conjuncts(~to_cnf(formula))

    # Special case if one clause is already False
    if False in clauses:
        return True

    result = set()
    while True:
        n = len(clauses)
        pairs = [
            (clauses[i], clauses[j])
            for i in range(n) for j in range(i + 1, n)
        ]

        for ci, cj in pairs:
            resolvents = resolve(ci, cj)
            if False in resolvents:
                return True
            result = result.union(set(resolvents))

        if result.issubset(set(clauses)):
            return False
        for c in result:
            if c not in clauses:
                clauses.append(c)


def resolve(ci, cj):
    """
    Generate all clauses that can be obtained by applying
    the resolution rule on ci and cj.
    """

    clauses = []
    dci = disjuncts(ci)
    dcj = disjuncts(cj)

    for di in dci:
        for dj in dcj:
            # If di, dj are complementary
            if di == ~dj or ~di == dj:
                # Create list of all disjuncts except di and dj
                res = removeall(di, dci) + removeall(dj, dcj)
                # Remove duplicates
                res = unique(res)
                # Join into new clause
                dnew = associate(Or, res)

                clauses.append(dnew)

    return clauses
