from collections import defaultdict
from typing import Dict, Optional

_NEIGHBORS = [(row, col) for row in (-1, 0, 1) for col in (-1, 0, 1) if row != 0 or col != 0]


class _LayoutInfo:
    def __init__(self, text: str):
        self._data = defaultdict(dict)  # type: Dict[int, Dict[int, str]]
        self._seats_coords = []

        for row, seats in enumerate(text.splitlines()):
            for col, seat in enumerate(seats):
                self._data[row][col] = seat
                if seat != '.':
                    self._seats_coords.append((row, col))
        self._originals = self._data

    def _get_cell(self, row: int, col: int) -> Optional[str]:
        line = self._data.get(row)
        return line.get(col) if line else None

    def _get_neighbors(self, seat_row: int, seat_col: int, skip_floor: bool):
        neighbors = 0
        for v_step, h_step in _NEIGHBORS:
            row = seat_row + v_step
            col = seat_col + h_step
            state = self._get_cell(row, col)
            while skip_floor and state == '.':
                row += v_step
                col += h_step
                state = self._get_cell(row, col)
            if state == '#':
                neighbors += 1
        return neighbors

    def _make_next_change(self, skip_floor: bool, limit: int) -> bool:
        has_changes = False
        data_new = {row: {col: value for col, value in line.items()} for row, line in self._data.items()}
        for row, col in self._seats_coords:
            state = self._data[row][col]
            neighbors = self._get_neighbors(row, col, skip_floor)
            if state == 'L' and not neighbors:
                data_new[row][col] = '#'
                has_changes = True
            elif state == '#' and neighbors >= limit:
                data_new[row][col] = 'L'
                has_changes = True
        self._data = data_new
        return has_changes

    def _print_layout(self):
        for line in self._data.values():
            print(''.join(line.values()))
        print('\n')

    def guess_count_of_occupied(self, skip_floor: bool, limit: int):
        while self._make_next_change(skip_floor, limit):
            pass
            # self._print_layout()
        occupied = 0
        for row, col in self._seats_coords:
            if self._data[row][col] == '#':
                occupied += 1
        self._data = self._originals
        return occupied


def _load_input_data(filename) -> _LayoutInfo:
    with open(filename) as fp:
        text = fp.read()
    return _LayoutInfo(text)


def _main():
    for filename in ('test.txt', 'puzzle.txt'):
        print('\n', filename)
        layout = _load_input_data(filename)

        occupied = layout.guess_count_of_occupied(skip_floor=False, limit=4)
        print('count only direct, limit 4, answer is', occupied)

        occupied = layout.guess_count_of_occupied(skip_floor=True, limit=5)
        print('look visible, limit 5, answer is', occupied)


if __name__ == '__main__':
    _main()
