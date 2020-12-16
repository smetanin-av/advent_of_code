import functools
import re
from typing import List, Tuple, Optional, Iterable, Set

_RE_RULE_TMPL = re.compile(r'(?P<name>[a-z ]+): (?P<low1>\d+)-(?P<high1>\d+) or (?P<low2>\d+)-(?P<high2>\d+)')


def _group_as_int(match: re.Match, name: str) -> int:
    value = match.group(name)
    return int(value)


class _RuleInfo:
    def __init__(self, text: str):
        match = _RE_RULE_TMPL.fullmatch(text)
        self.name = match.group('name')
        self.low1 = _group_as_int(match, 'low1')
        self.high1 = _group_as_int(match, 'high1')
        self.low2 = _group_as_int(match, 'low2')
        self.high2 = _group_as_int(match, 'high2')

    @functools.lru_cache(maxsize=None)
    def is_satisfy(self, value) -> bool:
        return (self.low1 <= value <= self.high1) or (self.low2 <= value <= self.high2)


class _RulesList:
    def __init__(self):
        self.items = []  # type: List[_RuleInfo]

    def add_rule(self, text: str) -> None:
        item = _RuleInfo(text)
        self.items.append(item)

    @staticmethod
    def _is_valid_order(rules: Iterable[_RuleInfo], tickets: Iterable['_TicketInfo']):
        return all(ticket.try_validate(rules) for ticket in tickets)

    def _get_filtered_rules(self, skipped: Set, value: int) -> Iterable[_RuleInfo]:
        for rule in self.items:
            if rule not in skipped and rule.is_satisfy(value):
                yield rule

    def find_order(self, validated: List['_TicketInfo']):
        rules_to_check = set(self.items)
        rules_to_skip = set()
        unresolved_rules = {}

        count_of_rules = len(self.items)
        for place in range(count_of_rules):
            allowed = rules_to_check.copy()
            unresolved_rules[place] = allowed
            for ticket in validated:
                value = ticket.values[place]
                allowed &= set(rule for rule in self._get_filtered_rules(rules_to_skip, value))
            if len(allowed) == 1:
                rules_to_skip |= allowed
                rules_to_check -= allowed

        place = 0
        ordered_rules = [None] * count_of_rules

        while place < count_of_rules:
            allowed = unresolved_rules.get(place)
            if allowed and len(allowed) == 1:
                rule = allowed.pop()
                ordered_rules[place] = rule
                del unresolved_rules[place]
                is_changed = False
                for allowed in unresolved_rules.values():
                    if rule in allowed:
                        allowed.discard(rule)
                        is_changed = True
                place = 0 if is_changed else place + 1
            else:
                place += 1

        is_successful = not unresolved_rules and all(ordered_rules)
        if is_successful:
            self.items = ordered_rules
        return is_successful


class _TicketInfo:
    def __init__(self, text: str):
        self.values = [int(x) for x in text.split(',')]

    def get_error(self, rules: Iterable[_RuleInfo]) -> Optional[int]:
        def _is_error(value: int) -> bool:
            return not any(rule.is_satisfy(value) for rule in rules)

        return next(filter(_is_error, self.values), None)

    def try_validate(self, rules: Iterable[_RuleInfo]) -> bool:
        return all(rule.is_satisfy(value) for value, rule in zip(self.values, rules))


class _TicketsList:
    def __init__(self):
        self.items = []  # type: List[_TicketInfo]

    def add_ticket(self, text: str) -> None:
        item = _TicketInfo(text)
        self.items.append(item)


def _load_input_data(filename) -> Tuple[_RulesList, _TicketInfo, _TicketsList]:
    with open(filename) as fp:
        text = fp.read()

    lines = text.splitlines()
    index = 0

    rules = _RulesList()
    while lines[index]:
        rules.add_rule(lines[index])
        index += 1

    while lines[index - 1] != 'your ticket:':
        index += 1
    my_ticket = _TicketInfo(lines[index])

    while lines[index - 1] != 'nearby tickets:':
        index += 1

    nearby_tickets = _TicketsList()
    while index < len(lines):
        nearby_tickets.add_ticket(lines[index])
        index += 1

    return rules, my_ticket, nearby_tickets


def _main():
    for filename in ('test_0.txt', 'test_1.txt', 'input.txt'):
        print('\n', filename)
        rules, my_ticket, nearby_tickets = _load_input_data(filename)

        validated = []
        errors_rate = 0
        for ticket in nearby_tickets.items:
            error = ticket.get_error(rules.items)
            if error is not None:
                errors_rate += error
            else:
                validated.append(ticket)
        print('answer is', errors_rate)

        if rules.find_order(validated):
            answer = 1
            for rule_no, rule in enumerate(rules.items):
                value = my_ticket.values[rule_no]
                print(rule.name, '=', value)
                if rule.name.startswith('departure'):
                    answer *= value
            print('answer is', answer)
        else:
            print('find order failed')


if __name__ == '__main__':
    _main()
