#! /usr/bin/python3
import sys


def resolve_overlap(o, n):
    if (o.x0 > n.x1 or o.x1 < n.x0 or
        o.y0 > n.y1 or o.y1 < n.y0 or
        o.z0 > n.z1 or o.z1 < n.z0):
        return {o, n} # No overlap

    if o.x0 < n.x0:
        if o.x1 > n.x1: # n sits fully within o on the x axis
            oa = Region(o.state, o.x0,     n.x0 - 1, o.y0, o.y1, o.z0, o.z1)
            ob = Region(o.state, n.x0,     n.x1,     o.y0, o.y1, o.z0, o.z1)
            oc = Region(o.state, n.x1 + 1, o.x1,     o.y0, o.y1, o.z0, o.z1)
            return {oa, oc} | resolve_overlap(ob, n)
        else: # right side of o overlaps left side of n
            oa = Region(o.state, o.x0, n.x0 - 1, o.y0, o.y1, o.z0, o.z1)
            ob = Region(o.state, n.x0, o.x1,     o.y0, o.y1, o.z0, o.z1)
            return {oa} | resolve_overlap(ob, n)
    elif o.x1 > n.x1: # left side of o overlaps right side of n
        oa = Region(o.state, o.x0,     n.x1, o.y0, o.y1, o.z0, o.z1)
        ob = Region(o.state, n.x1 + 1, o.x1, o.y0, o.y1, o.z0, o.z1)
        return {ob} | resolve_overlap(oa, n)
    elif o.y0 < n.y0:
        if o.y1 > n.y1: # n sits fully within o on the y axis
            oa = Region(o.state, o.x0, o.x1, o.y0,     n.y0 - 1, o.z0, o.z1)
            ob = Region(o.state, o.x0, o.x1, n.y0,     n.y1,     o.z0, o.z1)
            oc = Region(o.state, o.x0, o.x1, n.y1 + 1, o.y1,     o.z0, o.z1)
            return {oa, oc} | resolve_overlap(ob, n)
        else: # top of o overlaps bottom of n
            oa = Region(o.state, o.x0, o.x1, o.y0, n.y0 - 1, o.z0, o.z1)
            ob = Region(o.state, o.x0, o.x1, n.y0, o.y1,     o.z0, o.z1)
            return {oa} | resolve_overlap(ob, n)
    elif o.y1 > n.y1: # bottom of o overlaps top of n
        oa = Region(o.state, o.x0, o.x1, o.y0,     n.y1, o.z0, o.z1)
        ob = Region(o.state, o.x0, o.x1, n.y1 + 1, o.y1, o.z0, o.z1)
        return {ob} | resolve_overlap(oa, n)
    elif o.z0 < n.z0:
        if o.z1 > n.z1: # n sits fully within o on the z axis
            oa = Region(o.state, o.x0, o.x1, o.y0, o.y1, o.z0,     n.z0 - 1)
            ob = Region(o.state, o.x0, o.x1, o.y0, o.y1, n.z0,     n.z1)
            oc = Region(o.state, o.x0, o.x1, o.y0, o.y1, n.z1 + 1, o.z1)
            return {oa, oc} | resolve_overlap(ob, n)
        else: # far side of o overlaps near side of n
            oa = Region(o.state, o.x0, o.x1, o.y0, o.y1, o.z0, n.z0 - 1)
            ob = Region(o.state, o.x0, o.x1, o.y0, o.y1, n.z0, o.z1)
            return {oa} | resolve_overlap(ob, n)
    elif o.z1 > n.z1: # near side of o overlaps far side of n
        oa = Region(o.state, o.x0, o.x1, o.y0, o.y1, o.z0,     n.z1)
        ob = Region(o.state, o.x0, o.x1, o.y0, o.y1, n.z1 + 1, o.z1)
        return {ob} | resolve_overlap(oa, n)

    return {n} # o sits fully within n, so can discard it


class Region:
    def __init__(self, state, x0, x1, y0, y1, z0, z1):
        assert x0 <= x1 and y0 <= y1 and z0 <= z1, (x0, x1, y0, y1, z0, z1)
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.z0 = z0
        self.z1 = z1
        self.state = state

    def volume(self):
        return (self.x1 + 1 - self.x0) * (self.y1 + 1 - self.y0) * (self.z1 + 1 - self.z0)


def run_steps(steps):
    regions = {steps[0]}
    for step in steps[1:]:
        new_regions = set()
        for region in regions:
            new_regions |= resolve_overlap(region, step)
        regions = {region for region in new_regions if region.state}
    return sum(region.volume() for region in regions)


def parse_input(path):
    steps = []
    for line in open(path):
        if line.strip():
            state, coords = line.split()
            region = [1 if state == 'on' else 0]
            axes = coords.split(',')
            for axis in axes:
                region += [int(x) for x in axis[2:].split('..')]
            steps.append(Region(*region))
    return steps


def main(input_file):
    steps = parse_input(input_file)

    part1_steps = [s for s in steps if (-50 <= s.x0 <= s.x1 <= 50 and
                                        -50 <= s.y0 <= s.y1 <= 50 and
                                        -50 <= s.z0 <= s.z1 <= 50)]
    print("Part 1:", run_steps(part1_steps))
    print("Part 2:", run_steps(steps))


if __name__ == '__main__':
    main(sys.argv[1])
