from typing import List


def _load_input_data(filename: str) -> List[int]:
    with open(filename) as fp:
        return [int(x) for x in fp.readlines() if x]


def _get_sum(depths: List[int], offset: int, length: int) -> int:
    result = 0
    for index in range(length):
        result += depths[offset + index]
    return result


def _main():
    for filename in ('test.txt', 'puzzle.txt'):
        print('loading', filename)
        depths = _load_input_data(filename)

        for maxlen in (1, 3):
            print('window size', maxlen)
            increases = 0

            previous = _get_sum(depths, 0, maxlen)
            for offset in range(1, len(depths) - maxlen + 1):
                current = _get_sum(depths, offset, maxlen)
                if current > previous:
                    increases += 1
                previous = current

            print('the number of increases', increases)


if __name__ == '__main__':
    _main()
