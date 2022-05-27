import argparse
import logging
from decimal import Decimal

from sympy import to_cnf, SympifyError

from belief_base import BeliefBase


PROMPT = ">>> "

def print_help():
    print(
f"""Available actions:
r: Belief revision
d: Calculate degree of belief
e: Empty belief base
p: Print belief base
h: Print this help dialog
q: Quit
"""
    )


def handle_input(bb):
    print('Select action:')
    action = input(PROMPT)
    action = action.lower()

    if action == 'r':
        print('--- Revision ---')
        print('Enter a formula:')
        frm = input(PROMPT)
        try:
            frm = to_cnf(frm)
            print('Select order (real number from 0 to 1):')
            order = input(PROMPT)
            bb.revise(frm, Decimal(order))
        except SympifyError:
            print('Invalid formula')
        except ValueError:
            print('Order has to be a real number from 0 to 1')
        print()

    elif action == 'd':
        print('--- Calculate degree ---')
        print('Enter a formula:')
        frm = input(PROMPT)
        try:
            frm = to_cnf(frm)
            print(bb.degree(frm))
        except SympifyError:
            print('Invalid formula')
        print()

    elif action == 'e':
        bb.clear()
        print('--- Emptied belief base ---')
        print()

    elif action == 'p':
        print('--- Printing belief base ---')
        print(bb)
        print()

    elif action == 'h':
        print_help()

    elif action == 'q':
        exit()

    else:
        print('Sorry, the command was not recognized. Type \'h\' for help.')
        print()

    handle_input(bb)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Belief base revision CLI tool.')
    parser.add_argument('--debug', action='store_true', help='enable debugging')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    bb = BeliefBase()
    print_help()
    handle_input(bb)
