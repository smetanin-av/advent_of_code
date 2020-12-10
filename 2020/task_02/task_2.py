from typing import List, NamedTuple
import re


class _PasswordInfo(NamedTuple):
    low: int
    high: int
    char: str
    text: str


def _load_input_data() -> List[_PasswordInfo]:
    re_line_tpl = re.compile(r'(?P<low>\d+)-(?P<high>\d+) (?P<char>[a-z]): (?P<text>\w+)\n?')
    with open('input.txt') as fp:
        lines = fp.readlines()
    results = []
    for line in lines:
        match = re_line_tpl.fullmatch(line)
        results.append(
            _PasswordInfo(
                low=int(match.group('low')),
                high=int(match.group('high')),
                char=match.group('char'),
                text=match.group('text')
            )
        )
    return results


def _count_of_valid_by_old_policy(infos: List[_PasswordInfo]):
    count = 0
    for info in infos:
        if info.low <= info.text.count(info.char) <= info.high:
            count += 1
    return count


def _count_of_valid_by_new_policy(infos: List[_PasswordInfo]):
    count = 0
    for info in infos:
        low = info.low - 1
        high = info.high - 1
        count_of_chars = len(info.text)
        if low >= count_of_chars or high >= count_of_chars:
            continue
        if (info.text[low] == info.char) != (info.text[high] == info.char):
            count += 1
    return count


def _main():
    infos = _load_input_data()

    print('count of valid by old policy', _count_of_valid_by_old_policy(infos))
    print('count of valid by new policy', _count_of_valid_by_new_policy(infos))


if __name__ == '__main__':
    _main()
