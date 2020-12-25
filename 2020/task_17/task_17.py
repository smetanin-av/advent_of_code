import abc
import functools
import itertools
from collections import defaultdict
from datetime import datetime
from typing import Dict, Generic, Iterable, List, NamedTuple, Optional, Tuple, TypeVar


class _Coords3D(NamedTuple):
    z: int
    y: int
    x: int


class _Coords4D(NamedTuple):
    w: int
    z: int
    y: int
    x: int


_TCoords = TypeVar('_TCoords', _Coords3D, _Coords4D)


class _ICube(abc.ABC, Generic[_TCoords]):
    @abc.abstractmethod
    def _get_value(self, coords: _TCoords) -> Optional[bool]:
        pass

    def is_state_defined(self, coords: _TCoords) -> bool:
        return self._get_value(coords) is not None

    def is_active(self, coords: _TCoords) -> bool:
        return self._get_value(coords) is True

    @abc.abstractmethod
    def set_value(self, coords: _TCoords, value: bool) -> None:
        pass

    @abc.abstractmethod
    def _iterate_data(self) -> Iterable[Tuple[_TCoords, bool]]:
        pass

    def get_all_coords(self) -> Iterable[_TCoords]:
        for coords, _ in self._iterate_data():
            yield coords

    def get_all_values(self) -> Iterable[bool]:
        for _, is_active in self._iterate_data():
            yield is_active

    @staticmethod
    def _get_neighbors(coords: _TCoords) -> Iterable[_TCoords]:
        for offsets in itertools.product((-1, 0, 1), repeat=len(coords)):
            if any(offsets):
                yield tuple(sum(x) for x in zip(offsets, coords))

    @functools.lru_cache(maxsize=None)
    def get_neighbors(self, coords: _TCoords) -> List[_TCoords]:
        return list(self._get_neighbors(coords))

    def get_active_nearby(self, coords: _TCoords) -> int:
        return sum(self.is_active(neighbor) for neighbor in self.get_neighbors(coords))


class _Cube3D(_ICube[_Coords3D]):
    def __init__(self):
        self._data = self.build_cube3d()

    @staticmethod
    def build_cube3d() -> Dict[int, Dict[int, Dict[int, bool]]]:
        return defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: False)))

    def _get_value(self, coords: _Coords3D) -> Optional[bool]:
        z, y, x = coords
        layer = self._data.get(z)
        if not layer:
            return None
        row = layer.get(y)
        if not row:
            return None
        return row.get(x)

    def set_value(self, coords: _Coords3D, value: bool) -> None:
        z, y, x = coords
        self._data[z][y][x] = value

    def _iterate_data(self) -> Iterable[Tuple[_Coords3D, bool]]:
        for z, layer in self._data.items():
            for y, row in layer.items():
                for x, is_active in row.items():
                    yield (z, y, x), is_active


class _Cube4D(_ICube[_Coords4D]):
    def __init__(self):
        self._data = self.build_cube4d()

    @staticmethod
    def build_cube4d() -> Dict[int, Dict[int, Dict[int, Dict[int, bool]]]]:
        return defaultdict(_Cube3D.build_cube3d)

    def _get_value(self, coords: _Coords4D) -> Optional[bool]:
        w, z, y, x = coords
        cube = self._data.get(w)
        if not cube:
            return None
        layer = cube.get(z)
        if not layer:
            return None
        row = layer.get(y)
        if not row:
            return None
        return row.get(x)

    def set_value(self, coords: _Coords4D, value: bool) -> None:
        w, z, y, x = coords
        self._data[w][z][y][x] = value

    def _iterate_data(self) -> Iterable[Tuple[_Coords4D, bool]]:
        for w, cube in self._data.items():
            for z, layer in cube.items():
                for y, row in layer.items():
                    for x, is_active in row.items():
                        yield (w, z, y, x), is_active


class _ConwayCubes(abc.ABC):
    def __init__(self):
        self._cube = self._build_cube()

    @abc.abstractmethod
    def _build_cube(self) -> _ICube:
        pass

    def set_active(self, coords: _TCoords, is_active: bool) -> None:
        self._cube.set_value(coords, is_active)

    def do_cycle(self) -> None:
        cube_new = self._build_cube()
        for coords in self._cube.get_all_coords():
            for neighbor in self._cube.get_neighbors(coords):
                if cube_new.is_state_defined(neighbor):
                    continue
                state_old = self._cube.is_active(neighbor)
                active_nearby = self._cube.get_active_nearby(neighbor)
                if state_old:
                    state_new = active_nearby in (2, 3)
                else:
                    state_new = active_nearby == 3
                cube_new.set_value(neighbor, state_new)
        self._cube = cube_new

    def count_of_active(self) -> int:
        return sum(self._cube.get_all_values())


class _ConwayCubes3D(_ConwayCubes):
    def _build_cube(self) -> _ICube:
        return _Cube3D()


class _ConwayCubes4D(_ConwayCubes):
    def _build_cube(self) -> _ICube:
        return _Cube4D()


def _load_input_data(filename) -> List[List[bool]]:
    with open(filename) as fp:
        text = fp.read()

    data = []
    for line in text.splitlines():
        data.append([char == '#' for char in line])

    return data


def _main():
    for filename in ('test.txt', 'puzzle.txt'):
        print('\n', filename)

        initials = _load_input_data(filename)
        cubes3d = _ConwayCubes3D()
        for y, line in enumerate(initials):
            for x, is_active in enumerate(line):
                cubes3d.set_active(_Coords3D(z=0, y=y, x=x), is_active)
        for cycle in range(6):
            print('cycle', cycle, 'started at', datetime.now())
            cubes3d.do_cycle()
            print('finished at', datetime.now())
        print('cubes 3d, answer is', cubes3d.count_of_active())

        cubes4d = _ConwayCubes4D()
        for y, line in enumerate(initials):
            for x, is_active in enumerate(line):
                cubes4d.set_active(_Coords4D(w=0, z=0, y=y, x=x), is_active)
        for cycle in range(6):
            print('cycle', cycle, 'started at', datetime.now())
            cubes4d.do_cycle()
            print('finished at', datetime.now())
        print('cubes 4d, answer is', cubes4d.count_of_active())


if __name__ == '__main__':
    _main()
