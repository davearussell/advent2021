#! /usr/bin/python3
import copy
import sys


def parse_input(path):
    data = open(path).read().rstrip('\n')
    going_east = set()
    going_south = set()
    for y, row in enumerate(data.split('\n')):
        for x, cell in enumerate(row):
            if cell == '>':
                going_east.add((x, y))
            elif cell == 'v':
                going_south.add((x, y))
    return going_east, going_south, x + 1, y + 1


def iterate(e, s, w, h):
    next_e = set()
    next_s = set()

    for (x, y) in e:
        target = ((x + 1) % w, y)
        if target in e or target in s:
            next_e.add((x, y))
        else:
            next_e.add(target)

    for (x, y) in s:
        target = (x, (y + 1) % h)
        if target in next_e or target in s:
            next_s.add((x, y))
        else:
            next_s.add(target)

    return next_e, next_s, (e, s) == (next_e, next_s)
    


def main(input_file):
    e, s, w, h = parse_input(input_file)

    i = 1
    while True:
        e, s, done = iterate(e, s, w, h)
        if done:
            print("Part 1:", i)
            break
        i += 1


if __name__ == '__main__':
    main(sys.argv[1])
