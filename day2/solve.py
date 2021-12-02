#! /usr/bin/python3
import sys


def parse_input(path):
    steps = []
    for line in open(path):
        direction, count = line.split()
        steps.append( (direction[0], int(count)) )
    return steps


def follow(steps):
    x = y1 = y2 = 0
    for d, v in steps:
        if d == 'f':
            x += v
            y2 += y1 * v
        else:
            y1 += (1 if d == 'd' else -1) * v
    return x, y1, y2


def main(input_file):
    steps = parse_input(input_file)
    x, y1, y2 = follow(steps)
    print("Part 1:", x * y1)
    print("Part 2:", x * y2)


if __name__ == '__main__':
    main(sys.argv[1])
