from typing import Tuple, List, cast

TArrayOfInts = List[int]
BOARD_SIZE = 5


class Numbers(TArrayOfInts):
    def __init__(self, serialized: str):
        super().__init__()
        values = map(int, serialized.split(','))
        self.extend(values)


class Board:
    def __init__(self, serialized: List[str]):
        self._data = [
            [int(x) for x in row.split() if x]
            for row in serialized
        ]
        self._marks = [
            [False for _ in range(BOARD_SIZE)]
            for _ in range(BOARD_SIZE)
        ]

    def mark_value(self, value: int):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self._data[row][col] == value:
                    self._marks[row][col] = True

    def is_winner(self) -> bool:
        lines = (*self._marks, *zip(*self._marks))
        return any(all(x) for x in lines)

    def __repr__(self):
        temp = [
            ','.join(f'{self._data[row][col]}={self._marks[row][col]}' for col in range(BOARD_SIZE))
            for row in range(BOARD_SIZE)
        ]
        return '\n'.join(temp)

    def score(self):
        result = 0
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if not self._marks[row][col]:
                    result += self._data[row][col]
        return result


class Boards(List[Board]):
    def __init__(self, serialized: List[str]):
        super().__init__()
        for offset in range(1, len(serialized), BOARD_SIZE + 1):
            board = serialized[offset:offset + BOARD_SIZE]
            self.append(Board(board))

    def mark_value(self, value: int):
        for board in self:
            board.mark_value(value)

    def get_winner(self):
        return next(filter(Board.is_winner, self), None)


def _load_file(filename: str) -> Tuple[Numbers, Boards]:
    with open(filename) as fp:
        numbers, *boards = map(str.strip, fp.readlines())
        return Numbers(numbers), Boards(boards)


def _main():
    for filename in ('test.txt', 'puzzle.txt'):
        print('loading', filename)
        numbers, boards = _load_file(filename)

        winner = cast(Board, None)
        number = cast(int, None)
        while numbers and not winner:
            number = numbers.pop(0)
            boards.mark_value(number)
            winner = boards.get_winner()
        print('first winner score', number * winner.score())

        boards.remove(winner)
        while numbers and boards:
            number = numbers.pop(0)
            boards.mark_value(number)
            for winner in [x for x in boards if x.is_winner()]:
                boards.remove(winner)
        print('last winner score', number * winner.score())


if __name__ == '__main__':
    _main()
