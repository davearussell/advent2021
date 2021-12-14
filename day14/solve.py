#! /usr/bin/python3
import sys


def parse_input(path):
    pairs = {}
    rules = {}
    for line in open(path):
        if not pairs:
            polymer = line.strip()
            for a, b in zip(polymer, polymer[1:]):
                pairs[a + b] = pairs.get(a + b, 0) + 1
        elif line.strip():
            k, v = line.split('->')
            outers = k.strip()
            inner = v.strip()
            rules[outers] = [outers[0] + inner, inner + outers[1]]
    return pairs, rules


def iterate(pairs, rules):
    new_pairs = {}
    for pair, count in pairs.items():
        a, b = rules[pair]
        new_pairs[a] = new_pairs.get(a, 0) + count
        new_pairs[b] = new_pairs.get(b, 0) + count
    return new_pairs


def get_freqs(pairs):
    freqs = {}
    for pair, count in pairs.items():
        freqs[pair[0]] = freqs.get(pair[0], 0) + count
        freqs[pair[1]] = freqs.get(pair[1], 0) + count
    for k, v in freqs.items():
        if v & 1: # The first and last element in the polymer will match this case
            v += 1
        freqs[k] = v // 2 # Account for every element (except first/last) being in 2 pairs
    return sorted(freqs.values())


def main(input_file):
    pairs, rules = parse_input(input_file)
    for i in range(40):
        if i == 10:
            freqs = get_freqs(pairs)
            print("Part 1:", freqs[-1] - freqs[0])
        pairs = iterate(pairs, rules)
    freqs = get_freqs(pairs)
    print("Part 2:", freqs[-1] - freqs[0])


if __name__ == '__main__':
    main(sys.argv[1])
