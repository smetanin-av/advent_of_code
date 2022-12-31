import heapq
from typing import List, Iterable, Any

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


def load_data(path: str) -> List[TCalories]:
    with open(path) as fp:
        lines = map(str.strip, fp.readlines())
        return [x for x in _split_by_empty_lines(lines) if x]


def check_answer(actual: Any, expected: Any):
    assert expected is None or actual == expected, (actual, expected)
    print("answer is", actual)


def solve_part1(path: str, expected: Any):
    print("solve part1", path)
    answer = 0
    for calories in load_data(path):
        total = sum(calories)
        answer = max(answer, total)
    check_answer(answer, expected)


def solve_part2(path: str, expected: Any):
    print("solve", path)
    tops = []
    for calories in load_data(path):
        total = sum(calories)
        heapq.heappush(tops, total)
        if len(tops) > 3:
            heapq.heappop(tops)
    check_answer(sum(tops), expected)


def main():
    solve_part1("test.txt", expected=24000)
    solve_part1("puzzle.txt", expected=72017)

    solve_part2("test.txt", expected=45000)
    solve_part2("puzzle.txt", expected=212520)


if __name__ == '__main__':
    main()
