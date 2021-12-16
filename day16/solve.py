#! /usr/bin/python3
import sys
from functools import reduce


def parse_input(path):
    bits = []
    with open(path) as f:
        while True:
            char = f.read(1).strip()
            if not char:
                break
            n = int(char, base=16)
            bits += [( n >> i) & 1 for i in range(3, -1, -1)]
    return bits


def pop(bits, n, raw=False):
    popped = [bits.pop(0) for _ in range(n)]
    if raw:
        return popped
    value = 0
    for bit in popped:
        value = (value << 1) | bit
    return value


def sum_versions(pkt):
    version, pkt_type, children = pkt
    if pkt_type != 4:
        version += sum(sum_versions(child) for child in children)
    return version


def evaluate(pkt):
    _, pkt_type, payload = pkt
    if pkt_type == 4:
        return payload
    ops = {
        0: sum,
        1: lambda values: reduce(int.__mul__, values),
        2: min,
        3: max,
        5: lambda x: x[0] > x[1],
        6: lambda x: x[0] < x[1],
        7: lambda x: x[0] == x[1],
    }
    return ops[pkt_type]([evaluate(child) for child in payload])


def parse_pkt(bits):
    version = pop(bits, 3)
    pkt_type = pop(bits, 3)
    if pkt_type == 4:
        value = 0
        while True:
            is_last = not pop(bits, 1)
            value = (value << 4) | pop(bits, 4)
            if is_last:
                return (version, pkt_type, value)
    else:
        length_type = pop(bits, 1)
        sub_pkts = []
        if length_type == 0:
            pkt_len = pop(bits, 15)
            sub_bits = pop(bits, pkt_len, raw=True)
            while sub_bits:
                sub_pkts.append(parse_pkt(sub_bits))
        else:
            sub_pkt_count = pop(bits, 11)
            for _ in range(sub_pkt_count):
                sub_pkts.append(parse_pkt(bits))
        return (version, pkt_type, sub_pkts)


def main(input_file):
    bits = parse_input(input_file)
    pkt = parse_pkt(bits)
    print("Part 1:", sum_versions(pkt))
    print("Part 2:", evaluate(pkt))


if __name__ == '__main__':
    main(sys.argv[1])
