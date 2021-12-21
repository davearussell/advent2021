#! /usr/bin/python3
import sys


def part1(pos):
    score = [0, 0]
    die = 0
    rolls = 0
    while True:
        turn = rolls & 1
        roll = 3 * die + 6
        die += 3 # no need to check for >100, the % 10 below does that
        rolls += 3
        pos[turn] = (pos[turn] + roll) % 10
        score[turn] += pos[turn] or 10
        if score[turn] >= 1000:
            break
    return min(score) * rolls


def part2(pos):
    ways = [0, 0, 0, 1, 3, 6, 7, 6, 3, 1] # How many ways can 3 dice sum to each number?
    worlds = { # (p1_pos, p2_pos, p1_score, p2_score, next_player) -> n_worlds
        (pos[0], pos[1], 0, 0, 0): 1,
    }
    wins0 = wins1 = 0
    while worlds:
        new_worlds = {}
        for (p0, p1, s0, s1, turn), n in worlds.items():
            for roll in range(3, 10):
                if turn == 0:
                    _p0 = (p0 + roll) % 10
                    _s0 = s0 + (_p0 or 10)
                    if _s0 >= 21:
                        wins0 += n * ways[roll]
                    else:
                        state = (_p0, p1, _s0, s1, 1)
                        new_worlds[state] = new_worlds.get(state, 0) + n * ways[roll]
                else:
                    _p1 = (p1 + roll) % 10
                    _s1 = s1 + (_p1 or 10)
                    if _s1 >= 21:
                        wins1 += n * ways[roll]
                    else:
                        state = (p0, _p1, s0, _s1, 0)
                        new_worlds[state] = new_worlds.get(state, 0) + n * ways[roll]
        worlds = new_worlds
    return max(wins0, wins1)


def main(input_file):
    pos = [int(line.split()[-1]) for line in open(input_file)]
    print("Part 1:", part1(pos.copy()))
    print("Part 2:", part2(pos.copy()))


if __name__ == '__main__':
    main(sys.argv[1])
