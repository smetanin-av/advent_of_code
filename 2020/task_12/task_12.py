import abc
import math
from typing import List

"""
      N
      |
  W --+-- E
      |
      S
"""
_WAY_DIRECTIONS_DEGREES = {
    'N': 90,
    'S': 270,
    'E': 0,
    'W': 180
}

_ROTATE_DIRECTIONS_MULTIPLIERS = {
    'R': -1,
    'L': 1
}


def _get_sin(degrees: int) -> int:
    radians = math.radians(degrees)
    value = math.sin(radians)
    return int(value)


def _get_cos(degrees: int) -> int:
    radians = math.radians(degrees)
    value = math.cos(radians)
    return int(value)


def _coords_to_str(pos_x: int, pos_y: int) -> str:
    part_y = 'N' if pos_y >= 0 else 'S'
    part_x = 'E' if pos_x >= 0 else 'W'
    return f'{part_y}{abs(pos_y)}:{part_x}{abs(pos_x)}'


class _ShipStateBase(abc.ABC):
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0

    def __str__(self):
        return _coords_to_str(self.pos_x, self.pos_y)

    @abc.abstractmethod
    def on_direction(self, direction: str, distance: int) -> None:
        pass

    @abc.abstractmethod
    def on_forward(self, distance: int) -> None:
        pass

    @abc.abstractmethod
    def on_rotate(self, degrees: int) -> None:
        pass

    def apply_actions(self, actions: List['_ShipAction']) -> None:
        for action in actions:
            action.apply(self)

    def get_manhattan_distance(self) -> int:
        return abs(self.pos_x) + abs(self.pos_y)


class _ShipStateWithDirection(_ShipStateBase):

    def __init__(self, direction: str):
        super().__init__()
        self.degrees = _WAY_DIRECTIONS_DEGREES[direction]

    def __str__(self):
        coords = super().__str__()
        direction = next(key for key, value in _WAY_DIRECTIONS_DEGREES.items() if value == self.degrees)
        return f'{coords} -> {direction}'

    def _move(self, degrees: int, distance: int) -> None:
        self.pos_x += _get_cos(degrees) * distance
        self.pos_y += _get_sin(degrees) * distance

    def on_direction(self, direction: str, distance: int) -> None:
        degrees = _WAY_DIRECTIONS_DEGREES[direction]
        self._move(degrees, distance)

    def on_forward(self, distance: int) -> None:
        self._move(self.degrees, distance)

    def on_rotate(self, degrees: int) -> None:
        self.degrees = (self.degrees + degrees) % 360 % 360


class _Waypoint:
    def __init__(self, pos_x: int, pos_y: int):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def __str__(self):
        return _coords_to_str(self.pos_x, self.pos_y)

    def move(self, degrees: int, distance: int):
        self.pos_x += _get_cos(degrees) * distance
        self.pos_y += _get_sin(degrees) * distance

    def turn(self, degrees: int) -> None:
        # taken from https://en.wikipedia.org/wiki/Rotation_matrix
        pos_x = self.pos_x
        pos_y = self.pos_y
        cos = _get_cos(degrees)
        sin = _get_sin(degrees)
        self.pos_x = pos_x * cos - pos_y * sin
        self.pos_y = pos_x * sin + pos_y * cos


class _ShipStateWithWaypoint(_ShipStateBase):
    def __init__(self, pos_x: int, pos_y: int):
        super().__init__()
        self.waypoint = _Waypoint(pos_x, pos_y)

    def __str__(self):
        coords = super().__str__()
        return f'{coords} -> {self.waypoint}'

    def on_direction(self, direction: str, distance: int) -> None:
        degrees = _WAY_DIRECTIONS_DEGREES[direction]
        self.waypoint.move(degrees, distance)

    def on_forward(self, distance: int) -> None:
        self.pos_x += self.waypoint.pos_x * distance
        self.pos_y += self.waypoint.pos_y * distance

    def on_rotate(self, degrees: int) -> None:
        self.waypoint.turn(degrees)


class _ShipAction:
    def __init__(self, text):
        self.commmand = text[0]
        self.argument = int(text[1:])

    def _apply_turn(self, state: _ShipStateBase):
        degrees = _ROTATE_DIRECTIONS_MULTIPLIERS[self.commmand] * self.argument
        state.on_rotate(degrees)

    def apply(self, state: _ShipStateBase) -> None:
        if self.commmand in ('N', 'S', 'E', 'W'):
            state.on_direction(self.commmand, self.argument)
        if self.commmand == 'F':
            state.on_forward(self.argument)
        elif self.commmand in ('R', 'L'):
            self._apply_turn(state)
        print(state)


def _load_input_data(filename) -> List[_ShipAction]:
    with open(filename) as fp:
        text = fp.read()
    return [_ShipAction(x) for x in text.splitlines()]


def _main():
    for filename in ('test.txt', 'input.txt'):
        print('\n', filename)
        actions = _load_input_data(filename)

        ship_state = _ShipStateWithDirection(direction='E')
        ship_state.apply_actions(actions)
        distance = ship_state.get_manhattan_distance()
        print('use facing, answer is', distance)

        ship_state = _ShipStateWithWaypoint(pos_x=10, pos_y=1)
        ship_state.apply_actions(actions)
        distance = ship_state.get_manhattan_distance()
        print('use waypoint, answer is', distance)


if __name__ == '__main__':
    _main()
