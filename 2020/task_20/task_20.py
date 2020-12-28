import enum
import functools
import itertools
import operator
import re
from collections import defaultdict
from typing import Dict, Iterable, List, NamedTuple, Set, Tuple

_RE_TITLE = re.compile(r'Tile (?P<code>\d+):')


class _Flags(enum.IntFlag):
    VERTICAL = 1  # left <-> bottom or top <-> right
    HIGHER = 2  # left <-> right or top <-> bottom
    INVERSED = 4  # inverse border value


# Using flags as bits to code border kinds:
class _Borders(enum.Enum):
    ACTUAL_LEFT = 0
    ACTUAL_BOTTOM = _Flags.VERTICAL
    ACTUAL_RIGHT = _Flags.HIGHER
    ACTUAL_TOP = _Flags.HIGHER | _Flags.VERTICAL

    INVERSED_LEFT = _Flags.INVERSED
    INVERSED_BOTTOM = _Flags.INVERSED | _Flags.VERTICAL
    INVERSED_RIGHT = _Flags.INVERSED | _Flags.HIGHER
    INVERSED_TOP = _Flags.INVERSED | _Flags.HIGHER | _Flags.VERTICAL

    def __str__(self):
        return self._name_

    def is_vertical(self) -> bool:
        """ True for vertical border eg TOP or BOTTOM """
        return bool(self.value & _Flags.VERTICAL)

    def is_horizontal(self) -> bool:
        """ True for horizontal border eg RIGHT or LEFT """
        return not self.is_vertical()

    def is_higher(self) -> bool:
        """ True for higher border eg TOP or RIGHT """
        return bool(self.value & _Flags.HIGHER)

    def is_lower(self) -> bool:
        """ True for lower border eg BOTTOM or LEFT """
        return not self.is_higher()

    def is_inversed(self) -> bool:
        """ True for inversed borders """
        return bool(self.value & _Flags.INVERSED)

    def get_inversed(self) -> '_Borders':
        return _Borders(self.value ^ _Flags.INVERSED)

    def get_opposite(self) -> '_Borders':
        return _Borders(self.value ^ _Flags.HIGHER)

    def get_diffs(self, other: '_Borders') -> Iterable[_Flags]:
        diffs = self.value ^ other.value
        return [flag for flag in _Flags if diffs & flag]


class _TileInfo:
    _STR_to_BITs = {'#': '1', '.': '0'}

    def __init__(self, code: int, data: List[List[str]]):
        self._code = code
        self._data = data
        self._size = len(data)

    @property
    def code(self):
        return self._code

    @functools.lru_cache()
    def _get_border_hash(self, border: _Borders) -> int:
        if border.is_vertical():
            value = self._get_bottom() if border.is_lower() else self._get_top()
        else:
            value = self._get_left() if border.is_lower() else self._get_right()

        if border.is_inversed():
            value = value[::-1]

        bits = ''.join(self._STR_to_BITs[x] for x in value)
        return int(bits, base=2)

    @functools.lru_cache()
    def find_border(self, border_hash: int) -> _Borders:
        return next(border for border in _Borders if self._get_border_hash(border) == border_hash)

    def _get_row_vals(self, index: int) -> List[str]:
        return self._data[index]

    def _get_bottom(self):
        return self._get_row_vals(-1)

    def _get_top(self):
        return self._get_row_vals(0)

    def _get_col_vals(self, index: int) -> List[str]:
        return [line[index] for line in self._data]

    def _get_left(self) -> Iterable[str]:
        return self._get_col_vals(0)

    def _get_right(self) -> Iterable[str]:
        return self._get_col_vals(-1)

    def _get_borders_hashes(self, borders: Iterable[_Borders]) -> Set[int]:
        values = map(self._get_border_hash, borders)
        return set(values)

    @functools.lru_cache()
    def get_actual_borders(self) -> Set[int]:
        borders = itertools.filterfalse(_Borders.is_inversed, _Borders)
        return self._get_borders_hashes(borders)

    @functools.lru_cache()
    def get_borders_variants(self) -> Set[int]:
        return self._get_borders_hashes(_Borders)

    def transform(self, border_hash: int, target_kind: _Borders):
        current_kind = self.find_border(border_hash)
        while current_kind != target_kind:
            diffs = current_kind.get_diffs(target_kind)
            is_vertical = current_kind.is_vertical()
            if all(flag in diffs for flag in _Flags):
                # changed all flags -> rotate and 2 flips equal to one counter-rotate
                self._rotate(to_left=is_vertical)
            elif _Flags.VERTICAL in diffs:
                # changed flag VERTICAL -> changed axis, need rotate (left <-> bottom or top <-> right)
                self._rotate(to_left=not is_vertical)
            elif _Flags.HIGHER in diffs:
                # changed flag HIGHER -> current and target is opposite, need flip by own axis
                self._flip(by_vertical=is_vertical)
            elif _Flags.INVERSED in diffs:
                # changed flag INVERSED -> inverse is flip by perpendicular axis
                self._flip(by_vertical=not is_vertical)
            current_kind = self.find_border(border_hash)

    def _rotate(self, to_left: bool):
        data_new = []
        if to_left:
            for index in range(self._size):
                values = self._get_col_vals(index)
                data_new.insert(0, values)
        else:
            for index in range(self._size):
                values = self._get_col_vals(index)[::-1]
                data_new.append(values)
        self._data = data_new
        self._clear_functions_cache()

    def _flip(self, by_vertical: bool):
        if by_vertical:
            data_new = self._data[::-1]
        else:
            data_new = [line[::-1] for line in self._data]
        self._data = data_new
        self._clear_functions_cache()

    def _clear_functions_cache(self):
        self._get_border_hash.cache_clear()
        self.find_border.cache_clear()
        self.get_actual_borders.cache_clear()
        self.get_borders_variants.cache_clear()

    def get_data_without_borders(self):
        data = []
        for row in range(1, self._size - 1):
            row_data = self._data[row][1:-1]
            data.append(row_data)
        return data


class _MaskInfo:
    def __init__(self, mask: List[List[str]]):
        self._mask = mask

    def process(self, image: List[List[str]]):
        image_height = len(image)
        image_width = len(image[0])
        for _ in ('normal', 'inversed'):
            for _ in ('0', '90', '180', '270'):
                mask_height = len(self._mask)
                mask_width = len(self._mask[0])
                for row in range(0, image_height - mask_height + 1):
                    for col in range(0, image_width - mask_width + 1):
                        if self._is_match_at(image, row, col):
                            self._apply_marks(image, row, col)
                self._rotate()
            self._flip()

    def _get_markers_in_mask(self) -> Iterable[Tuple[int, int]]:
        for row_no, row_data in enumerate(self._mask):
            for col_no, col_data in enumerate(row_data):
                if col_data == '#':
                    yield row_no, col_no

    def _is_match_at(self, image: List[List[str]], row: int, col: int) -> bool:
        for mask_row, mask_col in self._get_markers_in_mask():
            if image[row + mask_row][col + mask_col] != '#':
                return False
        return True

    def _apply_marks(self, image: List[List[str]], row: int, col: int):
        for mask_row, mask_col in self._get_markers_in_mask():
            image[row + mask_row][col + mask_col] = 'X'

    def _rotate(self):
        mask_new = []
        width = len(self._mask[0])
        for col in range(width):
            values = [line[col] for line in self._mask]
            mask_new.insert(0, values)
        self._mask = mask_new

    def _flip(self):
        self._mask = self._mask[::-1]


class _NeighborInfo(NamedTuple):
    tile: _TileInfo
    border: int


def _load_input_data(filename) -> List[_TileInfo]:
    with open(filename) as fp:
        text = fp.read()

    tiles = []
    for tile_text in text.split('\n\n'):
        lines = tile_text.split('\n')
        code = int(_RE_TITLE.fullmatch(lines[0]).group('code'))
        data = [list(line) for line in lines[1:]]
        tile = _TileInfo(code, data)
        tiles.append(tile)

    return tiles


def _find_tiles_neighbors(tiles: List[_TileInfo]) -> Dict[_TileInfo, List[_NeighborInfo]]:
    neighbors = defaultdict(list)
    for tile_src, tile_dst in itertools.combinations(tiles, 2):
        matched = tile_src.get_actual_borders() & tile_dst.get_borders_variants()
        if not matched:
            continue
        border = matched.pop()
        neighbors[tile_src].append(_NeighborInfo(tile=tile_dst, border=border))
        neighbors[tile_dst].append(_NeighborInfo(tile=tile_src, border=border))
    return neighbors


def _find_tiles_coords(neighbors: Dict[_TileInfo, List[_NeighborInfo]], initial: _TileInfo):
    tiles_to_coords = {initial: (0, 0)}  # type: Dict[_TileInfo,Tuple[int, int]]
    coords_to_tiles = defaultdict(dict)  # type: Dict[int, Dict[int, _TileInfo]]
    coords_to_tiles[0][0] = initial

    frontier = []  # type: List[Tuple[_TileInfo, _TileInfo, int]]
    for neighbor in neighbors[initial]:
        frontier.append((initial, neighbor.tile, neighbor.border))

    while frontier:
        prev_tile, next_tile, border = frontier.pop()
        if next_tile in tiles_to_coords:
            continue

        target_kind = prev_tile.find_border(border).get_opposite()
        next_tile.transform(border, target_kind)

        y, x = tiles_to_coords[prev_tile]
        if target_kind.is_vertical():
            if target_kind.is_higher():
                # dock via top border -> put under previous
                tiles_to_coords[next_tile] = y + 1, x
                coords_to_tiles[y + 1][x] = next_tile
            else:
                # dock via bottom border -> put above previous
                tiles_to_coords[next_tile] = y - 1, x
                coords_to_tiles[y - 1][x] = next_tile
        else:
            if target_kind.is_higher():
                # dock via right border -> put before previous
                tiles_to_coords[next_tile] = y, x - 1
                coords_to_tiles[y][x - 1] = next_tile
            else:
                # dock via right border -> put before previous
                tiles_to_coords[next_tile] = y, x + 1
                coords_to_tiles[y][x + 1] = next_tile

        for neighbor in neighbors[next_tile]:
            if neighbor.tile not in tiles_to_coords:
                frontier.append((next_tile, neighbor.tile, neighbor.border))

    return coords_to_tiles


def _build_image_grid(coords_to_tiles):
    image_data = []
    for row_no in sorted(coords_to_tiles):
        tiles_in_row = coords_to_tiles[row_no]
        tiles_data = []
        for col_no in sorted(tiles_in_row):
            tile_data = tiles_in_row[col_no].get_data_without_borders()
            tiles_data.append(tile_data)

        while all(tiles_data):
            image_row = []
            for tile_data in tiles_data:
                image_row += tile_data.pop(0)
            image_data.append(image_row)
    return image_data


def _main():
    for filename in ('test.txt', 'puzzle.txt'):
        print('\n', filename)

        tiles = _load_input_data(filename)
        grouped_neighbors = _find_tiles_neighbors(tiles)

        corners = []
        for tile, neighbors in grouped_neighbors.items():
            if len(neighbors) == 2:
                corners.append(tile)
        prod_of_corners_codes = functools.reduce(operator.mul, [x.code for x in corners])
        print('product of corners codes', prod_of_corners_codes)

        tiles_by_coords = _find_tiles_coords(grouped_neighbors, corners[0])
        image_data = _build_image_grid(tiles_by_coords)

        mask_data = [
            list('                  # '),
            list('#    ##    ##    ###'),
            list(' #  #  #  #  #  #   ')
        ]
        mask_info = _MaskInfo(mask_data)
        mask_info.process(image_data)

        roughness = 0
        for item in itertools.chain.from_iterable(image_data):
            if item == '#':
                roughness += 1
        print('habitat`s water roughness', roughness)


if __name__ == '__main__':
    _main()
