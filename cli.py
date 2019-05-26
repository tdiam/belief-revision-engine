import argparse
import logging

from sympy import to_cnf, SympifyError

from belief_base import BeliefBase


def print_help():
    print(
f"""Available actions:
r: Belief revision
a: Add a belief
d: Calculate degree of belief
e: Empty belief base
p: Print belief base
h: Print this help dialog
q: Quit
"""
    )


def handle_input(bb):
    action = input('Select action: ')
    action = action.lower()

    if action == 'r':
        print('--- Revision ---')
        frm = input('Enter a formula: ')
        try:
            frm = to_cnf(frm)
            order = input('Select order (real number from 0 to 1): ')
            bb.revise(frm, float(order))
        except SympifyError:
            print('Invalid formula')
        except ValueError:
            print('Order could not be parsed into a real number')
        print()

    elif action == 'a':
        print('--- Add a belief ---')
        print('--- Warning: This may result in an inconsistent belief base ---')
        frm = input('Enter a formula: ')
        try:
            frm = to_cnf(frm)
            order = input('Select order (real number from 0 to 1): ')
            bb.add(frm, float(order))
        except SympifyError:
            print('Invalid formula')
        except ValueError:
            print('Order could not be parsed into a real number')
        print()

    elif action == 'd':
        print('--- Calculate degree ---')
        frm = input('Enter a formula: ')
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
