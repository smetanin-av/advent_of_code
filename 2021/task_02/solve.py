from typing import List, Tuple


def _load_input_data(filename: str) -> List[str]:
    with open(filename) as fp:
        return [x for x in fp.readlines() if x]


def _parse_command(command: str) -> Tuple[str, int]:
    name, value = command.split()
    return name, int(value)


def _main():
    for filename in ('test.txt', 'puzzle.txt'):
        print('loading', filename)
        commands = _load_input_data(filename)

        h_pos = 0
        depth = 0
        aim = 0

        for name, value in map(_parse_command, commands):
            if name == 'forward':
                h_pos += value
                depth += aim * value
            elif name == 'down':
                aim += value
            elif name == 'up':
                aim -= value

        print('position is', h_pos * depth)


if __name__ == '__main__':
    _main()
