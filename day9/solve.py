#! /usr/bin/python3
import sys


class Grid:
    def __init__(self, text):
        self.rows = []
        for line in text.split('\n'):
            if line:
                self.rows.append([int(char) for char in line])
        self.width = len(self.rows[0])
        self.height = len(self.rows)

    def neighbours(self, x, y):
        if x > 0:
            yield (x - 1, y)
        if x < self.width - 1:
            yield (x + 1, y)
        if y > 0:
            yield (x, y - 1)
        if y < self.height - 1:
            yield (x, y + 1)

    def find_low_points(self):
        points = []
        for x in range(self.width):
            for y in range(self.height):
                cell = self.rows[y][x]
                neighbours = [self.rows[ny][nx] for (nx, ny) in self.neighbours(x, y)]
                if cell < min(neighbours):
                    points.append((x, y))
        return points

    def find_basin(self, lowx, lowy):
        basin = set([ (lowx, lowy) ])
        edges = basin.copy()
        while edges:
            x, y = edges.pop()
            for nx, ny in self.neighbours(x, y):
                if (nx, ny) in basin:
                    continue
                cell = self.rows[ny][nx]
                # NOTE: We should really check that this cell isn't lower than the
                # edge we just popped, but the input data is constructed such that
                # that never happens
                if cell != 9:
                    basin.add((nx, ny))
                    edges.add((nx, ny))
        return basin


def main(input_file):
    with open(input_file) as f:
        grid = Grid(f.read())

    low_points = grid.find_low_points()
    basins = [grid.find_basin(x, y) for (x, y) in low_points]

    risk_level_sum = sum(grid.rows[y][x] + 1 for (x, y) in low_points)
    print("Part 1:", risk_level_sum)

    basin_sizes = sorted(len(basin) for basin in basins)
    print("Part 2:", basin_sizes[-3] * basin_sizes[-2] * basin_sizes[-1])


if __name__ == '__main__':
    main(sys.argv[1])
