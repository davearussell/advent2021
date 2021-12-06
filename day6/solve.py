#! /usr/bin/python3
import sys


def main(input_file):
    values = [int(x) for x in open(input_file).read().split(',')]
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1

    counts_by_day = [sum(counts.values())]
    for i in range(256):
        tmp = counts.get(0, 0)
        for days in range(8):
            counts[days] = counts.get(days + 1, 0)
        counts[8] = tmp
        counts[6] = counts.get(6, 0) + tmp
        counts_by_day.append(sum(counts.values()))

    print("Part 1:", counts_by_day[80])
    print("Part 2:", counts_by_day[256])


if __name__ == '__main__':
    main(sys.argv[1])
