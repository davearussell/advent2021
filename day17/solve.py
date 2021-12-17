#! /usr/bin/python3
import re
import sys


def plot(xv, yv, x0, y0, x1, y1):
    x = y = ymax = 0
    while True:
        x += xv
        if xv:
            xv -= 1
        y += yv
        yv -= 1
        ymax = max(y, ymax)
        if x0 <= x <= x1 and y0 <= y <= y1:
            return ymax
        if x > x1 or (x < x0 and not xv) or (y < y0 and yv < 0):
            return None


def main(input_file):
    s = open(input_file).read()
    x = re.search(r'x=([-0-9]+)[.][.]([-0-9]+), y=([-0-9]+)[.][.]([-0-9]+)$', s)
    x0, x1, y0, y1 = map(int, x.groups())
    assert x0 > 0 and y0 < 0 
    hits = ymax = 0
    for xv in range(x1 + 1):
        for yv in range(y0, -y0):
            _ymax = plot(xv, yv, x0, y0, x1, y1)
            if _ymax is not None:
                hits += 1
                if _ymax  > ymax:
                    ymax = _ymax
    print("Part 1:", ymax)
    print("Part 2:", hits)
    

if __name__ == '__main__':
    main(sys.argv[1])
