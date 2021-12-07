#! /usr/bin/python3
import sys


def main(input_file):
    values = [int(x) for x in open(input_file).read().split(',')]
    max_value = max(values)
    counts = [0] * (max_value + 1)
    for value in values:
        counts[value] += 1

    n_le = [0] * (max_value + 1) # number of crabs starting <= this pos
    p1_unit_cost_up = n_le  # cost of getting all crabs starting <= here 1 up from here
    p2_unit_cost_up = [0] * (max_value + 1)
    p1_cost_up = [0] * (max_value + 1) # cost to move all crabs starting below here to here
    p2_cost_up = [0] * (max_value + 1)

    n_ge = [0] * (max_value + 1) # number of crabs starting >= this pos
    p1_unit_cost_dn = n_ge # cost of getting all crabs starting >= here 1 down from here
    p2_unit_cost_dn = [0] * (max_value + 1)
    p1_cost_dn = [0] * (max_value + 1) # cost to move all crabs starting above here to here
    p2_cost_dn = [0] * (max_value + 1)

    n_le[0] = counts[0]
    p2_unit_cost_up[0] = counts[0]
    n_ge[max_value] = counts[max_value]
    p2_unit_cost_dn[max_value] = counts[max_value]

    for inc in range(max_value + 1):
        dec = max_value - inc
        if inc > 0:
            n_le[inc] = n_le[inc - 1] + counts[inc]
            p2_unit_cost_up[inc] = p2_unit_cost_up[inc - 1] + n_le[inc]
            p1_cost_up[inc] = p1_cost_up[inc - 1] + p1_unit_cost_up[inc - 1]
            p2_cost_up[inc] = p2_cost_up[inc - 1] + p2_unit_cost_up[inc - 1]
        if dec < max_value:
            n_ge[dec] = n_ge[dec + 1] + counts[dec]
            p2_unit_cost_dn[dec] = p2_unit_cost_dn[dec + 1] + n_ge[dec]
            p1_cost_dn[dec] = p1_cost_dn[dec + 1] + p1_unit_cost_dn[dec + 1]
            p2_cost_dn[dec] = p2_cost_dn[dec + 1] + p2_unit_cost_dn[dec + 1]

    p1_costs = [up + dn for up, dn in zip(p1_cost_up, p1_cost_dn)]
    p2_costs = [up + dn for up, dn in zip(p2_cost_up, p2_cost_dn)]
    print("Part 1:", min(p1_costs))
    print("Part 2:", min(p2_costs))

if __name__ == '__main__':
    main(sys.argv[1])
