import heapq
from typing import List, Iterable

TCalories = List[int]


def _split_by_empty_lines(lines: Iterable[str]):
    values = []
    for line in lines:
        if line:
            values.append(int(line))
        else:
            yield values
            values = []
    yield values


def _load_data(path: str) -> List[TCalories]:
    with open(path) as fp:
        lines = map(str.strip, fp.readlines())
        return [x for x in _split_by_empty_lines(lines) if x]


def part1(path: str):
    print("solve", path)
    maximum = 0
    for calories in _load_data(path):
        total = sum(calories)
        maximum = max(maximum, total)
    print(maximum)


def part2(path: str):
    print("solve", path)
    tops = []
    for calories in _load_data(path):
        total = sum(calories)
        heapq.heappush(tops, total)
        if len(tops) > 3:
            heapq.heappop(tops)
    print(sum(tops))


def main():
    part2("test.txt")
    part2("puzzle.txt")


if __name__ == '__main__':
    main()
