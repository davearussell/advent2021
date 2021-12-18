#! /usr/bin/python3
import json
import sys


class Snumber:
    def __init__(self, parent, depth):
        self.parent = parent
        self.depth = depth

    def copy(self, parent=None):
        raise NotImplementedError()

    def walk(self, reverse=False):
        raise NotImplementedError()

    def magnitude(self):
        raise NotImplementedError()

    def __add__(self, other):
        assert isinstance(other, Snumber) and self.depth == other.depth == 0
        pair = Pair(self.copy(), other.copy(), None, -1)
        pair.l.parent = pair.r.parent = pair
        for thing in pair.walk():
            thing.depth += 1
        pair.reduce()
        return pair

    def _reduce(self):
        for thing in self.walk():
            if (isinstance(thing, Pair) and thing.depth >= 4 and
                isinstance(thing.l, Number) and isinstance(thing.r, Number)):
                thing.explode()
                return True
        for thing in self.walk():
            if isinstance(thing, Number) and thing.value >= 10:
                thing.split()
                return True
        return False

    def reduce(self):
        while self._reduce():
            pass


class Pair(Snumber):
    def __init__(self, l, r, parent, depth):
        super().__init__(parent, depth)
        self.l = l
        self.r = r

    def __repr__(self):
        return repr([self.l, self.r])

    def magnitude(self):
        return 3 * self.l.magnitude() + 2 * self.r.magnitude()

    def copy(self, parent=None):
        p = Pair(None, None, parent, self.depth)
        p.l = self.l.copy(parent=p)
        p.r = self.r.copy(parent=p)
        return p

    def walk(self, reverse=False):
        first, second = (self.r, self.l) if reverse else (self.l, self.r)
        yield from first.walk(reverse)
        yield self
        yield from second.walk(reverse)

    def next_number(self, reverse=False):
        if not self.parent:
            return None
        sibling = self.parent.l if reverse else self.parent.r
        if self is sibling:
            return self.parent.next_number(reverse)
        for thing in sibling.walk(reverse=reverse):
            if isinstance(thing, Number):
                return thing
        assert 0, "unreachable"

    def explode(self):
        l = self.next_number(reverse=True)
        if l:
            l.value += self.l.value
        r = self.next_number(reverse=False)
        if r:
            r.value += self.r.value
        if self is self.parent.l:
            self.parent.l = Number(0, parent=self.parent, depth=self.depth)
        else:
            self.parent.r = Number(0, parent=self.parent, depth=self.depth)


class Number(Snumber):
    def __init__(self, value, parent, depth):
        super().__init__(parent, depth)
        self.value = value

    def __repr__(self):
        return repr(self.value)

    def magnitude(self):
        return self.value

    def copy(self, parent=None):
        return Number(self.value, parent, self.depth)

    def walk(self, reverse=False):
        yield self

    def split(self):
        pair = Pair(None, None, parent=self.parent, depth=self.depth)
        pair.l = Number(self.value // 2, parent=pair, depth=pair.depth + 1)
        pair.r = Number(self.value - pair.l.value, parent=pair, depth=pair.depth + 1)
        if self is self.parent.l:
            self.parent.l = pair
        else:
            self.parent.r = pair


def parse_expr(expr, parent=None, depth=0):
    if isinstance(expr, int):
        return Number(expr, parent, depth)
    assert isinstance(expr, list) and len(expr) == 2, expr
    pair = Pair(None, None, parent, depth)
    pair.l = parse_expr(expr[0], parent=pair, depth=depth + 1)
    pair.r = parse_expr(expr[1], parent=pair, depth=depth + 1)
    return pair


def main(input_file):
    snumbers = [parse_expr(json.loads(line)) for line in open(input_file)]
    print("Part 1:", sum(snumbers[1:], snumbers[0]).magnitude())
    magnitude = 0
    for a in snumbers:
        for b in snumbers:
            if a is not b:
                magnitude = max(magnitude, (a + b).magnitude())
    print("Part 2:", magnitude)


if __name__ == '__main__':
    main(sys.argv[1])
