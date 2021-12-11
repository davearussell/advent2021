#! /usr/bin/python3
import sys


def parse_input(path):
    nodes = {}
    for line in open(path):
        src, dst = line.strip().split('-')
        nodes.setdefault(src, []).append(dst)
        nodes.setdefault(dst, []).append(src)
    return nodes


def all_paths(nodes, have_free_time):
    paths = [(have_free_time, ['start'])]
    done = []
    while paths:
        new_paths = []
        for (free_time, path) in paths:
            for next_step in nodes[path[-1]]:
                _free_time = free_time
                if next_step == 'start':
                    continue
                if next_step.islower() and next_step in path:
                    if free_time:
                        _free_time = False
                    else:
                        continue
                new_path = path + [next_step]
                if next_step == 'end':
                    done.append(new_path)
                else:
                    new_paths.append((_free_time, new_path))
        paths = new_paths
    return done


def main(input_file):
    nodes = parse_input(input_file)
    print("Part 1:", len(all_paths(nodes, have_free_time=False)))
    print("Part 2:", len(all_paths(nodes, have_free_time=True)))


if __name__ == '__main__':
    main(sys.argv[1])
