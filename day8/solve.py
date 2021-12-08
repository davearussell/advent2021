#! /usr/bin/python3
import sys


def parse_input(path):
    entries = []
    for line in open(path):
        inputs, outputs = line.split('|')
        inputs = [set(x) for x in inputs.split()]
        outputs = [set(x) for x in outputs.split()]
        entries.append((inputs, outputs))
    return entries


def solve_entry(test_values, output_values):
    def pop_value(length, superset_of=None, subset_of=None):
        candidates = [v for v in test_values if len(v) == length]
        if superset_of:
            candidates = [v for v in candidates if not superset_of - v]
        if subset_of:
            candidates = [v for v in candidates if not v - subset_of]
        assert len(candidates) == 1
        test_values.remove(candidates[0])
        return candidates[0]

    digits_to_wires = [None] * 10

    digits_to_wires[1] = pop_value(length=2)
    digits_to_wires[4] = pop_value(length=4)
    digits_to_wires[7] = pop_value(length=3)
    digits_to_wires[8] = pop_value(length=7)
    digits_to_wires[3] = pop_value(length=5, superset_of=digits_to_wires[1])
    digits_to_wires[9] = pop_value(length=6, superset_of=digits_to_wires[3])
    digits_to_wires[5] = pop_value(length=5, subset_of=digits_to_wires[9])
    digits_to_wires[2] = pop_value(length=5)
    digits_to_wires[0] = pop_value(length=6, superset_of=digits_to_wires[7])
    digits_to_wires[6] = pop_value(length=6)

    wires_to_digits = {''.join(sorted(wires)): digit
                       for (digit, wires) in enumerate(digits_to_wires)}

    output_digits = [wires_to_digits[''.join(sorted(wires))] for wires in output_values]
    return sum((10 ** (3-i) * digit) for (i, digit) in enumerate(output_digits))


def main(input_file):
    entries = parse_input(input_file)
    print("Part 1:", len([x for (i,o) in entries for x in o if len(x) in (2, 3, 4, 7)]))
    print("Part 2:", sum(solve_entry(i, o) for (i, o) in entries))


if __name__ == '__main__':
    main(sys.argv[1])
