"""
Implementation of entrenchment-based revision in belief bases.

The algorithms have been adapted from "Applications of Belief Revision"
by Mary-Anne Williams, 1996.
"""

import math
import logging
from operator import neg

from sympy.logic.boolalg import to_cnf, And, Or, Equivalent
from sortedcontainers import SortedList

from entailment import entails
from utils import associate


logger = logging.getLogger()

class BeliefBase:
    """
    Belief base that implements epistemic entrenchment
    with finite partial entrenchment ranking.

    Each belief is assigned an order (a real number between 0 and 1)
    which determines its entrenchment, i.e. the level of commitment
    to maintain it when applying a change function (contraction,
    revision, etc).
    """

    def __init__(self):
        # Sort by decreasing order
        self.beliefs = SortedList(key=lambda b: neg(b.order))

    def __len__(self):
        return len(self.beliefs)

    def __iter__(self):
        return iter(self.beliefs)

    def iter_by_order(self):
        """
        Generator that groups beliefs in belief base by decreasing order.

        Yields:
            Tuples of type (order, list of beliefs with that order).

        Example:
            >>> bb = BeliefBase()
            >>> bb.add('a', 0.7)
            >>> bb.add('a|b', 0.7)
            >>> bb.add('b', 0.5)
            >>> bb.add('a&f', 0.1)
            >>> for it in bb.iter_by_order():
            ...     print(it)
            (0.7, [Belief(a, order=0.7), Belief(a | b, order=0.7)])
            (0.5, [Belief(b, order=0.5)])
            (0.1, [Belief(a & f, order=0.1)])
        """

        result = []
        last_order = None

        for belief in self.beliefs:
            # If it is the first belief we examine, add it and set last_order
            if last_order is None:
                result.append(belief)
                last_order = belief.order
                continue

            # If the order of this belief is "equal" to the previous, add it to the group
            if isclose(belief.order, last_order):
                result.append(belief)
            # Otherwise, yield the group and reset
            else:
                yield last_order, result
                result = []
                result.append(belief)
                last_order = belief.order

        # Yield last result
        yield last_order, result

    def add(self, formula, order):
        formula = to_cnf(formula)
        belief = Belief(formula, order)
        self.beliefs.add(belief)

    def degree(self, formula):
        """
        Find maximum order j such that taking all beliefs in base
        with order >= j results in a belief set that entails formula.

        TODO: Implement with binary search.
        """

        formula = to_cnf(formula)
        if entails([], formula):
            # Tautologies have degree = 1
            return 1

        base = []
        for order, group in self.iter_by_order():
            # Get formulas from beliefs
            base += [b.formula for b in group]
            if entails(base, formula):
                return order
        return 0

    def expand(self, formula, order, add_on_finish=True):
        """
        Updates entrenchment ranking for belief base expansion.

        Params:
            - add_on_finish: If true, the formula will be added
            to the belief base after the ranking has been updated.
        """

        x = to_cnf(formula)
        logger.debug(f'Expanding with {x} and order {order}')

        if not entails([], ~x):
            # If x is a contradiction, ignore
            if entails([], x):
                # If x is a tautology, assign order = 1
                order = 1
            else:
                for belief in self.beliefs:
                    y = belief.formula
                    if belief.order > order:
                        # Don't change beliefs of higher order
                        continue

                    # Degree of implication x -> y
                    d = self.degree(x >> y)
                    if (entails([], Equivalent(x, y)) # if |- (x <-> y)
                            or belief.order <= order < d):
                        logger.debug(f'{belief} raised to order {order}')
                        belief.order = order
                    else:
                        belief.order = d

            if add_on_finish:
                self.add(x, order)

        logger.debug(f'New belief base:\n{self}')

    def contract(self, formula, order):
        """
        Updates entrenchment ranking for belief base contraction.
        """

        x = to_cnf(formula)
        logger.debug(f'Contracting with {x} and order {order}')

        for belief in self.beliefs:
            y = belief.formula
            # Lower entrenchment if x and x|y have same degree
            if (belief.order > order
                    and self.degree(x) == self.degree(associate(Or, [x, y]))):
                logger.debug(f'{belief} lowered to order {order}')
                belief.order = order

        logger.debug(f'New belief base:\n{self}')

    def revise(self, formula, order, add_on_finish=True):
        """
        Updates entrenchment ranking for belief base revision.

        Params:
            - add_on_finish: If true, the formula will be added
            to the belief base after the ranking has been updated.
        """

        x = to_cnf(formula)
        dx = self.degree(x)
        logger.debug(f'Revising with {x} and order {order} and degree {dx}')

        if not entails([], ~x):
            # If x is a contradiction, ignore
            if entails([], x):
                # If x is a tautology, assign order = 1
                order = 1
            elif order <= dx:
                self.contract(x, order)
            else:
                self.contract(~x, 0)
                self.expand(x, order, add_on_finish=False)

            if add_on_finish:
                self.add(x, order)

        logger.debug(f'New belief base:\n{self}')

    def clear(self):
        self.beliefs.clear()

    def __repr__(self):
        if len(self.beliefs) == 0:
            return 'empty'
        return '\n'.join(str(x) for x in self.beliefs)


class Belief:
    def __init__(self, formula, order=None):
        self.formula = formula
        self.order = order

    def __lt__(self, other):
        return self.order < other.order

    def __repr__(self):
        return f'Belief({self.formula}, order={self.order})'


def isclose(a, b):
    """
    Checks approximate equality of floating-point numbers a, b.
    We add 1 to the numbers, since if a ~= b ~= 0, then relative tolerance will be zero.
    """
    return math.isclose(a + 1, b + 1)
