import string
from typing import List


class _GroupInfo:
    def __init__(self, group_answers: str):
        self.by_persons = [set(answers) for answers in group_answers.splitlines()]

    def count_of_any_yes(self):
        results = set()
        for answers in self.by_persons:
            results |= answers
        return len(results)

    def count_of_all_yes(self):
        results = set(string.ascii_lowercase)
        for answers in self.by_persons:
            results &= answers
        return len(results)


def _load_input_data(filename) -> List[_GroupInfo]:
    with open(filename) as fp:
        return [_GroupInfo(answers) for answers in fp.read().split('\n\n')]


def _main():
    for filename in ('test.txt', 'input.txt'):
        print('\n', filename)
        groups_infos = _load_input_data(filename)
        print('count of any yes', sum(x.count_of_any_yes() for x in groups_infos))
        print('count of all yes', sum(x.count_of_all_yes() for x in groups_infos))


if __name__ == '__main__':
    _main()
