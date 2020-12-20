import abc
from typing import Dict, List, Tuple


class _MatchBase(abc.ABC):
    def __init__(self, storage: '_RulesList'):
        self._storage = storage

    @abc.abstractmethod
    def validate(self, message: str, rules: List[str]) -> bool:
        pass


class _TextMatch(_MatchBase):
    def __init__(self, storage: '_RulesList', text: str):
        super().__init__(storage)
        self._text = text[1:-1]
        self._length = len(self._text)

    def _try_apply(self, message: str) -> Tuple[bool, str]:
        is_applied = message.startswith(self._text)
        return is_applied, message[self._length:] if is_applied else None

    def validate(self, message: str, rules: List[str]) -> bool:
        is_applied, tail = self._try_apply(message)
        return is_applied and self._storage.validate(tail, rules)


class _SequenceMatch(_MatchBase):
    def __init__(self, storage: '_RulesList', text: str):
        super().__init__(storage)
        self._rules = [rule_no for rule_no in text.split()]

    def validate(self, message: str, rules: List[str]) -> bool:
        return self._storage.validate(message, self._rules + rules)


class _VariantsMatch(_MatchBase):
    def __init__(self, storage: '_RulesList', text: str):
        super().__init__(storage)
        self._variants = [_SequenceMatch(storage, part) for part in text.split('|')]

    def validate(self, message: str, rules: List[str]) -> bool:
        return any(match.validate(message, rules) for match in self._variants)


class _RuleInfo:
    match: _MatchBase

    def __init__(self, storage: '_RulesList', text: str):
        if self._is_quoted(text):
            self.match = _TextMatch(storage, text)
        else:
            self.match = _VariantsMatch(storage, text)

    @staticmethod
    def _is_quoted(text: str) -> bool:
        return text.startswith('"') and text.endswith('"')

    def validate(self, message: str, rules: List[str]) -> bool:
        return self.match.validate(message, rules)


class _RulesList:
    def __init__(self):
        self._rules = {}  # type: Dict[str, _RuleInfo]

    def add_rule(self, text: str) -> None:
        rule_no, rule_text = text.split(': ')
        self._rules[rule_no] = _RuleInfo(self, rule_text)

    def validate(self, message: str, rules: List) -> bool:
        if not rules:
            return not message
        rule_no = rules[0]
        return self._rules[rule_no].validate(message, rules[1:])

    def is_match(self, message: str):
        return self.validate(message, ['0'])


def _load_input_data(filename) -> Tuple[_RulesList, List[str]]:
    with open(filename) as fp:
        text = fp.read()

    lines = text.splitlines()
    line_no = 0

    rules_list = _RulesList()
    while lines[line_no]:
        rules_list.add_rule(lines[line_no])
        line_no += 1

    # pass empty string between sections
    line_no += 1

    messages = []
    while line_no < len(lines):
        messages.append(lines[line_no])
        line_no += 1

    return rules_list, messages


def _main():
    for filename in ('test_0.txt', 'test_1.txt', 'test_2.txt', 'input_0.txt', 'input_1.txt'):
        print('\n', filename)
        rules_list, messages = _load_input_data(filename)

        count = 0
        is_test = 'test' in filename

        for message in messages:
            is_match = rules_list.is_match(message)
            if is_test and is_match:
                print(message)
            if is_match:
                count += 1
        print('count of matched', count)


if __name__ == '__main__':
    _main()
