#! /usr/bin/python3
import sys
import numpy


class Grid:
    def __init__(self, text):
        self.grid = numpy.array([[int(c) for c in r] for r in text.strip().split('\n')])
        self.width, self.height = self.grid.shape

    def tick(self):
        mask = self.grid.copy()
        mask.fill(-1)
        self.grid += 1
        keep_going = True
        while keep_going:
            keep_going = False
            for x in range(self.width):
                for y in range(self.height):
                    if mask[x][y] and self.grid[x][y] > 9:
                        mask[x][y] = 0
                        self.grid[max(x - 1, 0) : min(x + 2, self.width),
                                  max(y - 1, 0) : min(y + 2, self.height)] += 1
                        keep_going = True
        self.grid &= mask
        return self.width * self.height - numpy.count_nonzero(mask)


def main(input_file):
    grid = Grid(open(input_file).read())

    part1 = part2 = False
    step = 1
    flashes = 0
    while not (part1 and part2):
        new_flashes = grid.tick()
        flashes += new_flashes
        if step == 100:
            print("Part 1:", flashes)
            part1 = True
        if new_flashes == 100:
            print("Part 2:", step)
            part2 = True
        step += 1


if __name__ == '__main__':
    main(sys.argv[1])
