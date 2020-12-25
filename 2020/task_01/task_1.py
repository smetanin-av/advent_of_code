import itertools
from typing import List, Iterable, Tuple
from functools import reduce


def _load_input_data() -> List[int]:
    with open('puzzle.txt') as fp:
        return [int(x) for x in fp.readlines()]


def _get_combinations(numbers: List[int], length: int) -> Iterable[Tuple[int]]:
    count_of_numbers = len(numbers)
    for indexes in itertools.combinations(range(count_of_numbers), length):
        yield tuple(numbers[index] for index in indexes)


def _find_combination_with_summa(numbers: List[int], length: int, summa: int) -> Tuple[int]:
    return next(x for x in _get_combinations(numbers, length) if sum(x) == summa)


def _multiply(numbers: Iterable[int]) -> int:
    return reduce((lambda x, y: x * y), numbers)


def _main():
    numbers = _load_input_data()

    combination = _find_combination_with_summa(numbers, 2, 2020)
    print(combination, sum(combination), _multiply(combination))

    combination = _find_combination_with_summa(numbers, 3, 2020)
    print(combination, sum(combination), _multiply(combination))


if __name__ == '__main__':
    _main()
