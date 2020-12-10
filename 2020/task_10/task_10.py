from collections import defaultdict
from typing import Tuple, List


def _load_input_data(filename) -> List[int]:
    with open(filename) as fp:
        text = fp.read()
    numbers = sorted(int(x) for x in text.splitlines())
    numbers.insert(0, 0)
    numbers.append(numbers[-1] + 3)
    return numbers


def _count_of_diffs(numbers: List[int]) -> Tuple[int, int]:
    diffs_in_1 = 0
    diffs_in_3 = 0
    for index in range(1, len(numbers)):
        diff = numbers[index] - numbers[index - 1]
        if diff == 1:
            diffs_in_1 += 1
        elif diff == 3:
            diffs_in_3 += 1
    return diffs_in_1, diffs_in_3


def _is_diff_in_range(numbers: List[int], previous: int, current: int) -> bool:
    diff = numbers[current] - numbers[previous]
    return diff <= 3


def _count_of_variants(numbers: List[int]) -> int:
    count_of_ways = defaultdict(lambda: 0)
    count_of_ways[0] = 1
    count_of_ways[1] = 1

    current = 2
    while current < len(numbers):
        previous = current - 1
        while previous >= 0 and _is_diff_in_range(numbers, previous, current):
            count_of_ways[current] += count_of_ways[previous]
            previous -= 1
        current += 1

    return count_of_ways[current - 1]


def _main():
    for filename in ('test_0.txt', 'test_1.txt', 'input.txt'):
        print('\n', filename)
        jolts = _load_input_data(filename)

        diffs_in_1, diffs_in_3 = _count_of_diffs(jolts)
        print('diffs in 1 is', diffs_in_1, 'diffs in 3 is', diffs_in_3, 'answer is', diffs_in_1 * diffs_in_3)

        count_of_variants = _count_of_variants(jolts)
        print('count of variants', count_of_variants)


if __name__ == '__main__':
    _main()
