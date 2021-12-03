from typing import List, Callable, Collection

_TRecord = List[int]
_TRecords = List[_TRecord]


def _load_file(filename: str) -> _TRecords:
    with open(filename) as fp:
        return [
            [int(char) for char in line.strip()]
            for line in fp.readlines() if line
        ]


def _bits_to_int(bits: _TRecord) -> int:
    value = 0
    for bit in bits:
        value = _append_bit(value, bit)
    return value


def _append_bit(value: int, bit: int) -> int:
    return (value << 1) + bit


def _calc_most_common_bit(bits: Collection[int]) -> int:
    threshold = len(bits) / 2
    return int(sum(bits) >= threshold)


def _calc_power_consumption(records: _TRecords) -> int:
    gamma = 0
    epsilon = 0

    for bits in zip(*records):
        most_common_bit = _calc_most_common_bit(bits)
        gamma = _append_bit(gamma, most_common_bit)
        less_common_bit = 1 - most_common_bit
        epsilon = _append_bit(epsilon, less_common_bit)

    return gamma * epsilon


def _get_most_common_bit(records: _TRecords, col: int) -> int:
    bits = [records[col] for records in records]
    return _calc_most_common_bit(bits)


def _get_less_common_bit(records: _TRecords, col: int) -> int:
    return 1 - _get_most_common_bit(records, col)


def _filter_by_bit(records: _TRecords, col: int, bit: int) -> _TRecords:
    return [record for record in records if record[col] == bit]


def _find_record_by(records: _TRecords, filter_fn: Callable[[_TRecords, int], int], col: int) -> _TRecord:
    bit = filter_fn(records, col)
    filtered = _filter_by_bit(records, col, bit)
    return filtered[0] if len(filtered) == 1 else _find_record_by(filtered, filter_fn, col + 1)


def _calc_oxygen(records: _TRecords) -> int:
    record = _find_record_by(records, _get_most_common_bit, 0)
    return _bits_to_int(record)


def _calc_co2(records: _TRecords) -> int:
    record = _find_record_by(records, _get_less_common_bit, 0)
    return _bits_to_int(record)


def _main():
    for filename in ('test.txt', 'puzzle.txt'):
        print('loading', filename)
        records = _load_file(filename)

        power_consumption = _calc_power_consumption(records)
        print('power consumption is', power_consumption)

        oxygen = _calc_oxygen(records)
        co2 = _calc_co2(records)
        print('life support rating', oxygen * co2)


if __name__ == '__main__':
    _main()
