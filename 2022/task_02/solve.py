import enum
from typing import List, NamedTuple, Tuple, Any


class Shape(enum.Enum):
    Rock = enum.auto()
    Paper = enum.auto()
    Scissors = enum.auto()


SHAPE_by_CHAR = {
    "A": Shape.Rock,
    "X": Shape.Rock,
    "B": Shape.Paper,
    "Y": Shape.Paper,
    "C": Shape.Scissors,
    "Z": Shape.Scissors,
}

SCORE_by_SHAPE = {
    Shape.Rock: 1,
    Shape.Paper: 2,
    Shape.Scissors: 3,
}

BEATS_by_SHAPE = {
    Shape.Rock: Shape.Paper,
    Shape.Paper: Shape.Scissors,
    Shape.Scissors: Shape.Rock,
}

LOSE_by_SHAPE = {
    val: key for key, val in BEATS_by_SHAPE.items()
}


class Round(NamedTuple):
    col1: Shape
    col2: str


def parse_line(line: str) -> Round:
    cols = line.split()
    return Round(*cols)


def load_data(path: str) -> List[Round]:
    with open(path) as fp:
        lines = map(str.strip, fp.readlines())
        return [parse_line(x) for x in lines]


def get_my_turn_part1(col2: str) -> Shape:
    if col2 == "X":
        return Shape.Rock
    if col2 == "Y":
        return Shape.Paper
    if col2 == "Z":
        return Shape.Scissors


def check_answer(actual: Any, expected: Any):
    assert expected is None or actual == expected, (actual, expected)
    print("answer is", actual)


def solve_part1(path: str, expected: Any):
    print("solve part1", path)
    data = load_data(path)
    answer = 0
    for col1, col2 in data:
        shape1 = SHAPE_by_CHAR[col1]
        shape2 = get_my_turn_part1(col2)
        answer += SCORE_by_SHAPE[shape2]
        if shape1 == shape2:
            answer += 3
        elif shape2 == BEATS_by_SHAPE[shape1]:
            answer += 6
    check_answer(answer, expected)


def get_my_turn_part2(col2: str, shape1: Shape) -> Tuple[Shape, int]:
    if col2 == "X":
        return LOSE_by_SHAPE[shape1], 0
    if col2 == "Y":
        return shape1, 3
    if col2 == "Z":
        return BEATS_by_SHAPE[shape1], 6


def solve_part2(path: str, expected: Any):
    print("solve part2", path)
    data = load_data(path)
    answer = 0
    for col1, col2 in data:
        shape1 = SHAPE_by_CHAR[col1]
        shape2, bonus = get_my_turn_part2(col2, shape1)
        answer += SCORE_by_SHAPE[shape2] + bonus
    check_answer(answer, expected)


def main():
    solve_part1("test.txt", expected=15)
    solve_part1("puzzle.txt", expected=8890)

    solve_part2("test.txt", expected=12)
    solve_part2("puzzle.txt", expected=10238)


if __name__ == '__main__':
    main()
