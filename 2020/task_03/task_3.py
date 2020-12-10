class _RowInfo:
    def __init__(self, line: str):
        self._line = line

    def get_item(self, col):
        return self._line[col % len(self._line)]


class _MapInfo:
    def __init__(self, lines):
        self._rows = [_RowInfo(x) for x in lines]

    def count_or_rows(self):
        return len(self._rows)

    def get_item(self, row: int, col: int):
        return self._rows[row].get_item(col)


def _load_input_data(filename) -> _MapInfo:
    with open(filename) as fp:
        lines = fp.read().splitlines()
        return _MapInfo(lines)


def _count_of_trees(map_info: _MapInfo, down: int, right: int):
    row = 0
    col = 0
    count = 0

    while row < map_info.count_or_rows():
        item = map_info.get_item(row, col)
        if item == '#':
            count += 1
        row += down
        col += right

    return count


def _main():
    for filename in ('test.txt', 'input.txt'):
        map_info = _load_input_data(filename)
        answer = 1

        print('\n', filename)
        for right, down in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
            count = _count_of_trees(map_info, down, right)
            answer *= count
            print('right', right, 'down', down, 'count of trees', count)
        print('answer', answer)


if __name__ == '__main__':
    _main()
