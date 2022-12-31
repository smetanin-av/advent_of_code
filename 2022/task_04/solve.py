from typing import NamedTuple, Iterable, Any


class RangeInfo(NamedTuple):
    low: int
    high: int

    @staticmethod
    def build(text: str):
        parts = map(int, text.split("-"))
        return RangeInfo(*parts)

    def is_contains(self, other: 'RangeInfo'):
        return self.low <= other.low and self.high >= other.high

    def has_overlap(self, other: 'RangeInfo'):
        return max(self.low, other.low) <= min(self.high, other.high)


class RangesPair(NamedTuple):
    range1: RangeInfo
    range2: RangeInfo

    @staticmethod
    def build(text: str):
        parts = map(RangeInfo.build, text.split(","))
        return RangesPair(*parts)


def load_data(path: str) -> Iterable[RangesPair]:
    with open(path) as fp:
        lines = map(str.strip, fp.readlines())
    return map(RangesPair.build, lines)


def check_answer(actual: Any, expected: Any):
    assert expected is None or actual == expected, (actual, expected)
    print("answer is", actual)


def solve_part1(path: str, expected: Any):
    print("solve part1", path)
    answer = 0
    for pair in load_data(path):
        first, second = pair.range1, pair.range2
        if first.is_contains(second) or second.is_contains(first):
            answer += 1
    check_answer(answer, expected)


def solve_part2(path: str, expected: Any):
    print("solve part2", path)
    answer = 0
    for pair in load_data(path):
        first, second = pair.range1, pair.range2
        if first.has_overlap(second):
            answer += 1
    assert expected is None or answer == expected, (answer, expected)
    check_answer(answer, expected)


def main():
    solve_part1("test.txt", expected=2)
    solve_part1("puzzle.txt", expected=487)

    solve_part2("test.txt", expected=4)
    solve_part2("puzzle.txt", expected=849)


if __name__ == '__main__':
    main()
