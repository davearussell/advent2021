#! /usr/bin/python3
import sys


def parse_input(path):
    lines = []
    for line in open(path):
        p0, p1 = line.split('->')
        x0, y0 = [int(n) for n in p0.split(',')]
        x1, y1 = [int(n) for n in p1.split(',')]
        lines.append( ((x0, y0), (x1, y1)) )
    return lines


def plot_line(p0, p1):
    def _range(v0, v1):
        return list(range(v0, v1 - 1, -1) if  v0 > v1 else range(v0, v1 + 1))
    x0, y0 = p0
    x1, y1 = p1
    xs = _range(x0, x1) if x0 != x1 else [x0] * (abs(y1 - y0) + 1)
    ys = _range(y0, y1) if y0 != y1 else [y0] * (abs(x1 - x0) + 1)
    return zip(xs, ys)


def make_grid(lines):
    grid = [[]]
    for line in lines:
        for x, y in plot_line(*line):
            while y >= len(grid[0]):
                for col in grid:
                    col.append(0)
            while x >= len(grid):
                grid.append([0] * len(grid[0]))
            grid[x][y] += 1
    return grid


def main(input_file):
    lines = parse_input(input_file)
    part1_lines = [line for line in lines if
                   line[0][0] == line[1][0] or line[0][1] == line[1][1]]

    part1_grid = make_grid(part1_lines)
    print("Part 1:", len([cell for col in part1_grid for cell in col if cell > 1]))

    part2_grid = make_grid(lines)
    print("Part 2:", len([cell for col in part2_grid for cell in col if cell > 1]))


if __name__ == '__main__':
    main(sys.argv[1])
