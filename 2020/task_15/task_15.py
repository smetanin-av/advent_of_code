from typing import List, NamedTuple
from datetime import datetime


class _TestInfo(NamedTuple):
    initials: List[int]
    turns: int
    answer: int


_TESTS = (
    _TestInfo(initials=[0, 3, 6], turns=2020, answer=436),
    _TestInfo(initials=[1, 3, 2], turns=2020, answer=1),
    _TestInfo(initials=[2, 1, 3], turns=2020, answer=10),
    _TestInfo(initials=[1, 2, 3], turns=2020, answer=27),
    _TestInfo(initials=[2, 3, 1], turns=2020, answer=78),
    _TestInfo(initials=[3, 2, 1], turns=2020, answer=438),
    _TestInfo(initials=[3, 1, 2], turns=2020, answer=1836),
    _TestInfo(initials=[0, 3, 6], turns=30000000, answer=175594),
    _TestInfo(initials=[1, 3, 2], turns=30000000, answer=2578),
    _TestInfo(initials=[2, 1, 3], turns=30000000, answer=3544142),
    _TestInfo(initials=[1, 2, 3], turns=30000000, answer=261214),
    _TestInfo(initials=[2, 3, 1], turns=30000000, answer=6895259),
    _TestInfo(initials=[3, 2, 1], turns=30000000, answer=18),
    _TestInfo(initials=[3, 1, 2], turns=30000000, answer=362)
)


class _NumbersGame:
    def __init__(self):
        self._number = None
        self._next = None
        self._turn = 0
        self._results = {}

    def _clear(self) -> None:
        self._number = None
        self._next = None
        self._turn = 0
        self._results.clear()

    def initialize(self, initials: List[int]) -> None:
        self._clear()
        for number in initials[:-1]:
            self._results[number] = self._turn
            self._turn += 1

        self._next = initials[-1]
        self._play_turn()

    def _get_next(self):
        return self._turn - self._results.get(self._number, self._turn)

    def _play_turn(self):
        self._number = self._next
        self._next = self._get_next()
        self._results[self._number] = self._turn
        self._turn += 1

    def play_to_nth_turn(self, turn):
        while self._turn < turn:
            self._play_turn()
        return self._number


def _main():
    game = _NumbersGame()

    for test in _TESTS:
        print(datetime.now(), 'test', test)
        game.initialize(test.initials)
        number = game.play_to_nth_turn(test.turns)
        print(datetime.now(), 'answer is', number)
        assert number == test.answer

    game.initialize([15, 5, 1, 4, 7, 0])
    print(datetime.now(), 'puzzle play to 2020')
    number = game.play_to_nth_turn(2020)
    print('turn 2020, number is', number)

    print(datetime.now(), 'puzzle play to 30000000')
    number = game.play_to_nth_turn(30000000)
    print('turn 30000000, answer is', number)


if __name__ == '__main__':
    _main()
