#! /usr/bin/python3
import sys


class Grid:
    def __init__(self, rows):
        self.rows = rows
        self.size = len(rows)
        self.unmarked = set(cell for row in rows for cell in row)
        self.lines = []
        for i in range(self.size):
            # For each possible winning line, track the numbers
            # we have *not* yet marked on that line
            self.lines.append(set(rows[i]))
            self.lines.append(set(row[i] for row in rows))

    def mark(self, number):
        s = set([number])
        self.unmarked -= s
        for line in self.lines:
            line -= s
            if not line: # We've filled a line, we win!
                return True
        return False


def parse_input(path):
    grids = []
    numbers = []
    with open(path) as f:
        number_line = f.readline()
        numbers = [int(x) for x in number_line.split(',')]
        for line in f:
            if not line.strip():
                grid = []
                grids.append(grid)
            else:
                grid.append([int(x) for x in line.split()])
    return numbers, [Grid(grid) for grid in grids]


def main(input_file):
    numbers, grids = parse_input(input_file)

    scores = []
    for number in numbers:
        winners = [grid for grid in grids if grid.mark(number)]
        for winner in winners:
            scores.append(number * sum(winner.unmarked))
            grids.remove(winner)
        if not grids:
            break

    print("Part 1:", scores[0])
    print("Part 2:", scores[-1])


if __name__ == '__main__':
    main(sys.argv[1])
