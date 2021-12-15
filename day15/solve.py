#! /usr/bin/python3
import heapq
import numpy
import sys


def parse_input(path):
    rows = [[int(c) for c in line] for line in open(path).read().strip().split('\n')]
    return numpy.array(rows).transpose()


def expand_grid(grid, factor):
    w, h = len(grid), len(grid[0])
    new_grid = numpy.zeros((w * factor, h * factor), dtype=numpy.uint8)
    for i in range(factor):
        for j in range(factor):
            new_grid[i * w : i * w + w, j * h : j * h + h] = grid + i + j
    for x in range(len(new_grid)):
        for y in range(len(new_grid[0])):
            while new_grid[x][y] > 9:
                new_grid[x][y] -= 9
    return new_grid


def make_edges(grid):
    edges = {}
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            edges[(x, y)] = [(i, j) for (i, j) in neighbours if
                             0 <= i < len(grid) and 0 <= j < len(grid[0])]
    return edges


def find_risk(grid):
    edges = make_edges(grid)
    queue = [(0, (0, 0))] # [ (cost_to_reach_node, node), ... ]
    cost_to = {(0, 0): 0} # node -> cost_to_reach_node
    while queue:
        current_node = heapq.heappop(queue)[1]
        for neighbour in edges[current_node]:
            cost = cost_to[current_node] + grid[neighbour]
            if neighbour not in cost_to or cost < cost_to[neighbour]:
                cost_to[neighbour] = cost
                heapq.heappush(queue, (cost, neighbour) )
    goal = (len(grid) - 1, len(grid[0]) - 1)
    return cost_to[goal]


def main(input_file):
    grid = parse_input(input_file)
    print("Part 1:", find_risk(grid))
    print("Part 2:", find_risk(expand_grid(grid, 5)))


if __name__ == '__main__':
    main(sys.argv[1])
