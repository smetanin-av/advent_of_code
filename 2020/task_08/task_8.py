from typing import List


class _CommandInfo:
    def __init__(self, name: str, arg: str):
        self.name = name
        self.arg = int(arg)

    def swap_jmp_and_nop(self):
        self.name = {'nop': 'jmp', 'jmp': 'nop'}[self.name]


class _ContextInfo:
    def __init__(self):
        self.commands = []  # type: List[_CommandInfo]

    def add_command(self, text: str):
        name, arg = text.split(' ')
        self.commands.append(_CommandInfo(name, arg))

    def _try_execute(self):
        accumulator = 0
        index = 0
        visited = []

        while index < len(self.commands) and index not in visited:
            command = self.commands[index]
            visited.append(index)
            if command.name == 'nop':
                index += 1
            elif command.name == 'acc':
                accumulator += command.arg
                index += 1
            elif command.name == 'jmp':
                index += command.arg

        is_executed = index >= len(self.commands)
        if is_executed:
            print('executed successfully, accumulator is', accumulator)
        else:
            print('found cycle, accumulator is', accumulator)
        return is_executed

    def fix_and_execute(self):
        index = 0
        is_executed = False
        while not is_executed and index < len(self.commands):
            command = self.commands[index]
            if command.name != 'acc':
                command.swap_jmp_and_nop()
                print('changed command at', index + 1)
                is_executed = self._try_execute()
                command.swap_jmp_and_nop()
            index += 1


def _load_input_data(filename) -> _ContextInfo:
    with open(filename) as fp:
        data = fp.read()
    context = _ContextInfo()
    for line in data.splitlines():
        context.add_command(line)
    return context


def _main():
    for filename in ('test.txt', 'input.txt'):
        print('\n', filename)
        context = _load_input_data(filename)
        context.fix_and_execute()


if __name__ == '__main__':
    _main()
