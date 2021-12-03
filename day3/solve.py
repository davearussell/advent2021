#! /usr/bin/python3
import sys
from functools import reduce


def to_int(bits):
    return reduce(int.__or__, [1 << i for i, bit in enumerate(bits) if bit])


def count_ones(values, n_bits):
    ones = [0] * n_bits
    for value in values:
        for i in range(n_bits):
            if value & (1 << i):
                ones[i] += 1
    return ones


def mcb(values, n_bits):
    ones = count_ones(values, n_bits)
    mcb_bits = [1 if count >= len(values) / 2 else 0 for count in ones]
    return to_int(mcb_bits)


def lcb(values, n_bits):
    return (~mcb(values, n_bits)) & ((1 << n_bits) - 1)


def filter_values(_values, n_bits, fn):
    values = _values.copy()
    for i in range(n_bits)[::-1]:
        mask = 1 << i
        value_mask = fn(values, n_bits) & mask
        values = [value for value in values if value & mask == value_mask]
        if len(values) == 1:
            break
    assert len(values) == 1
    return values[0]


def main(input_file):
    strings = [line.strip() for line in open(input_file)]
    values = [int(s, base=2) for s in strings]
    n_bits = max(map(len, strings))

    gamma = mcb(values, n_bits)
    epsilon = lcb(values, n_bits)
    print("Part 1:", gamma * epsilon)

    oxy = filter_values(values, n_bits, mcb)
    co2 = filter_values(values, n_bits, lcb)
    print("Part 2:", oxy * co2)


if __name__ == '__main__':
    main(sys.argv[1])
