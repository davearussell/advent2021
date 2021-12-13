#! /usr/bin/python3
import sys
import numpy
import pygame, pygame.locals


def parse_input(path):
    dots = []
    folds = []
    for line in open(path):
        if ',' in line:
            x, y = line.split(',')
            dots.append((int(x), int(y)))
        if 'fold' in line:
            axis, n = line.split()[-1].split('=')
            folds.append((axis, int(n)))
    return dots, folds


def do_fold(grid, axis, value):
    if axis == 'x':
        left = grid[:value]
        right = numpy.flip(grid[value + 1:], axis=0)
        return left | right
    elif axis == 'y':
        top = grid[:, :value]
        bottom = numpy.flip(grid[:, value + 1:], axis=1)
        return top | bottom
    assert 0, axis


def display_code(grid):
    pygame.init()
    screen = pygame.display.set_mode((len(grid) + 10, len(grid[0]) + 10))
    surface = pygame.surfarray.make_surface(grid * 255)
    screen.blit(surface, (5, 5))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                sys.exit(0)
        pygame.display.update()


def main(input_file):
    dots, folds = parse_input(input_file)
    xmax = max(x for (x, y) in dots)
    ymax = max(y for (x, y) in dots)
    grid = numpy.zeros((xmax + 1, ymax + 1), dtype=numpy.uint8)
    for x, y in dots:
        grid[x, y] = 1

    for i, (axis, value) in enumerate(folds):
        grid = do_fold(grid, axis, value)
        if i == 0:
            print("Part 1:", grid.sum())

    display_code(grid)


if __name__ == '__main__':
    main(sys.argv[1])
