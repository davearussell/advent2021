#! /usr/bin/python3
import sys


def corrupt_score(char):
    return {')': 3, ']': 57, '}': 1197, '>': 25137}[char]


def incomplete_score(chars):
    scores = {')': 1, ']': 2, '}': 3, '>': 4}
    score = 0
    for char in reversed(chars):
        score = score * 5 + scores[char]
    return score


def score_line(line):
    stack = []
    openers = {'(': ')', '<': '>', '{': '}', '[': ']'}
    for i, char in enumerate(line):
        if char in openers:
            stack.append(openers[char])
        elif char != stack.pop():
            return ("corrupt", corrupt_score(char))
    if stack:
        return ("incomplete", incomplete_score(stack))
    return ("valid", 0)


def main(input_file):
    scores = {}
    for line in open(input_file):
        line_type, score = score_line(line.strip())
        scores.setdefault(line_type, []).append(score)
    print("Part 1:", sum(scores['corrupt']))
    print("Part 2:", sorted(scores['incomplete'])[len(scores['incomplete']) // 2])


if __name__ == '__main__':
    main(sys.argv[1])
