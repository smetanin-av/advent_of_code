import enum
import functools
import re
from collections import defaultdict
from typing import Dict, List, NamedTuple, Set, Tuple


class _Coords(NamedTuple):
    x: int
    y: int

    def __add__(self, other: '_Coords') -> '_Coords':
        return _Coords(x=self.x + other.x, y=self.y + other.y)

    def __iadd__(self, other):
        return self + other

    def __str__(self) -> str:
        return f'x: {self.x}, y: {self.y}'


OFFSETS = {
    'ne': _Coords(x=1, y=1),
    'e': _Coords(x=2, y=0),
    'se': _Coords(x=1, y=-1),
    'nw': _Coords(x=-1, y=1),
    'w': _Coords(x=-2, y=0),
    'sw': _Coords(x=-1, y=-1)
}


class _StepsList:
    _RE_CODES = re.compile(r'(e|se|sw|w|nw|ne)')

    def __init__(self, text):
        self.offsets = [OFFSETS[x] for x in self._RE_CODES.findall(text)]


class _TileState(enum.Enum):
    WHITE = enum.auto()
    BLACK = enum.auto()

    def __str__(self) -> str:
        return self._name_


class _TilesInfo:
    _FLIPS = {
        _TileState.WHITE: _TileState.BLACK,
        _TileState.BLACK: _TileState.WHITE
    }

    def __init__(self):
        self._data = self._build_tiles_grid()
        self._blacks = set()  # type: Set[_Coords]

    def _build_tiles_grid(self) -> Dict[int, Dict[int, _TileState]]:
        return defaultdict(self._build_tiles_row)

    @staticmethod
    def _build_tiles_row() -> Dict[int, _TileState]:
        return defaultdict(lambda: _TileState.WHITE)

    def walk_tiles(self, steps_list: _StepsList):
        coords = _Coords(x=0, y=0)
        for offset in steps_list.offsets:
            coords += offset
        self.flip_tile(coords)

    def get_state(self, coords: _Coords) -> _TileState:
        is_black = coords in self._blacks
        return _TileState.BLACK if is_black else _TileState.WHITE

    def flip_tile(self, coords: _Coords) -> None:
        state = self._FLIPS[self.get_state(coords)]
        if state == _TileState.BLACK:
            self._blacks.add(coords)
        else:
            self._blacks.discard(coords)

    @functools.lru_cache(maxsize=None)
    def get_coords_nearby(self, coords: _Coords) -> List[_Coords]:
        list_of_coords = []
        for offset in OFFSETS.values():
            list_of_coords.append(coords + offset)
        return list_of_coords

    def get_neighbors(self, coords: _Coords) -> Tuple[List[_Coords], List[_Coords]]:
        blacks = []
        whites = []
        for neighbor in self.get_coords_nearby(coords):
            if neighbor in self._blacks:
                blacks.append(neighbor)
            else:
                whites.append(neighbor)
        return blacks, whites

    def emulate_day(self):
        tiles_to_flip = []
        whites_to_check = set()

        for coords in self._blacks:
            blacks, whites = self.get_neighbors(coords)
            whites_to_check.update(whites)
            if len(blacks) == 0 or len(blacks) > 2:
                tiles_to_flip.append(coords)

        for coords in whites_to_check:
            blacks, _ = self.get_neighbors(coords)
            if len(blacks) == 2:
                tiles_to_flip.append(coords)

        for coords in tiles_to_flip:
            self.flip_tile(coords)

    def count_of_blacks(self):
        return len(self._blacks)


def _load_input_data(filename: str) -> List[_StepsList]:
    with open(filename) as fp:
        text = fp.read()
    return [_StepsList(x) for x in text.splitlines()]


def _main():
    for filename in ('test.txt', 'puzzle.txt'):
        print('\n', filename)

        steps_series = _load_input_data(filename)
        tiles_info = _TilesInfo()

        for steps_list in steps_series:
            tiles_info.walk_tiles(steps_list)

        count_of_blacks = tiles_info.count_of_blacks()
        print('count of blacks', count_of_blacks)

        for day in range(100):
            tiles_info.emulate_day()
        print('count of blacks', tiles_info.count_of_blacks())


if __name__ == '__main__':
    _main()
