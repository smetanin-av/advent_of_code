import itertools

from typing import List, Tuple, Iterable


def _load_input_data(filename) -> List[int]:
    with open(filename) as fp:
        data = fp.read()
    return [int(x) for x in data.splitlines()]


def _get_pairs_of_indexes(length: int) -> Iterable[Tuple[int]]:
    for index_0, index_1 in itertools.combinations(range(length), 2):
        yield index_0, index_1


def _is_a_sum_of_any(value: int, numbers: List[int]):
    for index_0, index_1 in _get_pairs_of_indexes(len(numbers)):
        if value == (numbers[index_0] + numbers[index_1]):
            return True
    return False


def _found_not_a_sum_of_previous(numbers: List[int], length: int):
    for index in range(length, len(numbers)):
        value = numbers[index]
        if not _is_a_sum_of_any(value, numbers[index - length:index]):
            return value


def _found_sequence_with_sum(numbers: List[int], summa: int):
    founded = None
    low_ind = 0
    high_ind = 0

    while not founded and low_ind < (len(numbers) - 1):
        current = numbers[low_ind]
        if current < summa:
            high_ind = low_ind + 1
            while current < summa and high_ind < len(numbers):
                current += numbers[high_ind]
                high_ind += 1
            if current == summa:
                founded = numbers[low_ind:high_ind]
        low_ind += 1
        
    print('found sequence with sum', low_ind, high_ind, founded)
    return min(founded) + max(founded)


def _main():
    for filename, length in (('test.txt', 5), ('input.txt', 25)):
        print('\n', filename)
        numbers = _load_input_data(filename)

        invalid = _found_not_a_sum_of_previous(numbers, length)
        print('found not a sum of previous', length, invalid)

        answer = _found_sequence_with_sum(numbers, invalid)
        print('min + max in sequence', answer)


if __name__ == '__main__':
    _main()
