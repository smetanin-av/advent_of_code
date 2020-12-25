import operator
import re
from collections import deque
from typing import Deque, Iterable, List, Optional


class _ExpressionsInterpreter:
    _ACTIONS = {'+': operator.add, '*': operator.mul}
    _RE_PARTS_TMPL = re.compile(r'\s*([0-9]+|[+*()])\s*')

    def __init__(self, priority: Optional[str]) -> None:
        self.priority = priority

    def evaluate(self, text: str) -> int:
        stack = []  # type: List[Deque]
        actions = deque()

        for part in self._tokenize(text):
            if part.isdigit():
                actions.append(int(part))
            elif part in ('+', '*'):
                actions.append(part)
            elif part == '(':
                stack.append(actions)
                actions = deque()
            elif part == ')':
                value = self._do_actions(actions)
                actions = stack.pop()
                actions.append(value)
            else:
                raise Exception('Unknown expression part!')

        result = self._do_actions(actions)
        return result

    def _tokenize(self, text: str) -> Iterable[str]:
        parts = self._RE_PARTS_TMPL.split(text)
        return filter(None, parts)

    def _get_priority(self, action: str) -> int:
        is_priority_action = bool(self.priority) and action == self.priority
        return int(is_priority_action)

    def _do_actions(self, items: Deque) -> int:
        first = items.popleft()
        defered = deque()

        actions_priorities = set(self._get_priority(x) for x in items if x in self._ACTIONS)
        higher_priority = max(actions_priorities)

        while items:
            action = items.popleft()
            second = items.popleft()
            if len(actions_priorities) > 1 and self._get_priority(action) != higher_priority:
                defered += first, action
                first = second
            else:
                first = self._ACTIONS[action](first, second)

        if defered:
            defered.append(first)
            return self._do_actions(defered)
        else:
            return first

    @staticmethod
    def evaluate_all(texts: List[str], priority: Optional[str], verbose: bool) -> None:
        self = _ExpressionsInterpreter(priority)
        print('priority is', self.priority)
        summa = 0
        for text in texts:
            result = self.evaluate(text)
            if verbose:
                print(text, 'is', result)
            summa += result
        print('summa is', summa)


def _load_input_data(filename) -> List[str]:
    with open(filename) as fp:
        text = fp.read()
    return text.splitlines()


def _main():
    for filename in ('test.txt', 'puzzle.txt'):
        print('\n', filename)

        texts = _load_input_data(filename)
        is_test = filename == 'test.txt'

        _ExpressionsInterpreter.evaluate_all(texts, priority=None, verbose=is_test)
        _ExpressionsInterpreter.evaluate_all(texts, priority='+', verbose=is_test)
        _ExpressionsInterpreter.evaluate_all(texts, priority='*', verbose=is_test)


if __name__ == '__main__':
    _main()
