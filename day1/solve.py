#! /usr/bin/python3
import sys


def main(input_file):
    depths = [int(x) for x in open(input_file).read().split()]

    inc_count = sum(b > a for (a, b) in zip(depths, depths[1:]))
    print(inc_count)

    sums = [sum(vals) for vals in zip(depths, depths[1:], depths[2:])]
    sum_incs = sum(b > a for (a, b) in zip(sums, sums[1:]))
    print(sum_incs)
    


if __name__ == '__main__':
    main(sys.argv[1])
