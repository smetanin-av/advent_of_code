import string
from typing import List, NamedTuple, Any


class Rucksack(NamedTuple):
    cell1: str
    cell2: str


def get_priorities():
    yield from enumerate(string.ascii_lowercase, start=1)
    yield from enumerate(string.ascii_uppercase, start=27)


PRIORITIES = {
    char: index for index, char in get_priorities()
}


def load_data(path: str) -> List[str]:
    with open(path) as fp:
        lines = map(str.strip, fp.readlines())
        return list(lines)


def check_answer(actual: Any, expected: Any):
    assert expected is None or actual == expected, (actual, expected)
    print(actual)


def solve_part1(path: str, answer: Any):
    print("solve", path)
    total = 0
    for rucksack in load_data(path):
        half = len(rucksack) // 2
        cell1 = rucksack[:half]
        cell2 = rucksack[half:]
        commons = set(cell1) & set(cell2)
        assert len(commons) == 1, (cell1, cell2)
        item = next(iter(commons))
        total += PRIORITIES[item]
    check_answer(total, answer)


def solve_part2(path: str, answer: Any):
    print("solve", path)
    total = 0
    group = []
    for rucksack in load_data(path):
        group.append(rucksack)
        if len(group) < 3:
            continue
        first, second, third = group
        group = []
        commons = set(first) & set(second) & set(third)
        assert len(commons) == 1, (first, second, third)
        same_item = next(iter(commons))
        total += PRIORITIES[same_item]
    check_answer(total, answer)


def main():
    solve_part1("test.txt", answer=157)
    solve_part1("puzzle.txt", answer=7824)
    solve_part2("test.txt", answer=70)
    solve_part2("puzzle.txt", answer=2798)


if __name__ == '__main__':
    main()
