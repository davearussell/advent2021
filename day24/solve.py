#! /usr/bin/python3
import sys

# I didn't end up with a programmatic solution here, though it was useful to
# be able to run the program to verify candidate solutions.
#
# Inspecting the code reveals that each of the 14 stages does one of two things:
# A. Multiply by 26 and add a remainder based on the input digit's value
# B. Divide by 26 if the input digit is at a specific offset from  the remainder
# from the most recent multiply
#
# There are 7 MULs and 7 DIVs so to get 0 at the end, the digit for each DIV must be
# chosen to match the digit of the corresponding MUL.

# For my inputs the requirements were (labelling the digits A...N from left to right):
# E = D + 1
# G = F - 7
# J = I - 5
# K = H - 3
# L = C - 8
# M = B + 4
# N = A + 5

# To get the biggest and smallest overall inputs, just choose the maximal/minimal
# values for each pair of digits that keep both in the range 1-9


def run(prog, inputs):
    state = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    zs = []
    i = 0
    for op, args in prog:
        if op == 'inp':
            zs.append(state['z'])
            state[args[0]] = inputs[i]
            i += 1
        else:
            lhs = state[args[0]]
            rhs = args[1]
            if not isinstance(rhs, int):
                rhs = state[rhs]
            if op == 'add':
                state[args[0]] = lhs + rhs
            elif op == 'mul':
                state[args[0]] = lhs * rhs
            elif op == 'div':
                state[args[0]] = int(lhs / rhs)
            elif op == 'mod':
                state[args[0]] = lhs % rhs
            else:
                state[args[0]] = 1 if lhs == rhs else 0
    return zs[1:] + [state['z']]


def parse_input(path):
    prog = []
    for line in open(path):
        cmd = line.split()
        op, args = cmd[0], cmd[1:]
        args = tuple([arg if arg in 'wxyz' else int(arg) for arg in args])
        prog.append((op, args))
    return prog


def main(input_file):
    prog = parse_input(input_file)

    test_vectors = [
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        [4, 5, 9, 8, 9, 9, 2, 9, 9, 4, 6, 1, 9, 9],
        [1, 1, 9, 1, 2, 8, 1, 4, 6, 1, 1, 1, 5, 6],
    ]
    for test_inputs in test_vectors:
        print(''.join(map(str, test_inputs)), run(prog, test_inputs))



if __name__ == '__main__':
    main(sys.argv[1])
