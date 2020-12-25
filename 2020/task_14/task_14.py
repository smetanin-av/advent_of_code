import itertools
import re
from typing import List

_RE_MASK_TPL = re.compile(r'mask = (?P<mask>[X01]+)')
_RE_COMMAND_TPL = re.compile(r'mem\[(?P<address>\d+)] = (?P<value>\d+)')

_MASK_LENGTH = 36


class _CommandInfo:
    def __init__(self, mask, address, value):
        self.mask = mask

        self.address = int(address)
        self.address_bits = f'{int(self.address):0{_MASK_LENGTH}b}'

        self.value = int(value)
        self.value_bits = f'{int(self.value):0{_MASK_LENGTH}b}'

    @staticmethod
    def _bits_to_int(bits: List[str]) -> int:
        return int(''.join(bits), base=2)

    def value_by_mask(self) -> int:
        masked_bits = [self._mask_value_bit(index) for index in range(_MASK_LENGTH)]
        return self._bits_to_int(masked_bits)

    def _mask_value_bit(self, index):
        return self.value_bits[index] if self.mask[index] == 'X' else self.mask[index]

    def addresses_by_mask(self) -> List[int]:
        holders_offsets = []
        address_bits = []
        for index, mask_digit in enumerate(self.mask):
            if mask_digit == '0':
                address_bits.append(self.address_bits[index])
            elif mask_digit == '1':
                address_bits.append('1')
            else:
                holders_offsets.append(index)
                address_bits.append('')

        count_of_holders = len(holders_offsets)
        results = []

        for holders_bits in itertools.product(('0', '1'), repeat=count_of_holders):
            address = address_bits.copy()
            results.append(address)
            for holder_no, bit_value in enumerate(holders_bits):
                holder_offset = holders_offsets[holder_no]
                address[holder_offset] = bit_value

        return [self._bits_to_int(x) for x in results]

    def _mask_address_bit(self, index):
        return self.address_bits[index] if self.mask[index] == '0' else self.mask[index]


def _load_input_data(filename) -> List[_CommandInfo]:
    with open(filename) as fp:
        text = fp.read()

    mask = ''.join(itertools.repeat('X', _MASK_LENGTH))
    commands = []

    for line in text.splitlines():
        match = _RE_MASK_TPL.fullmatch(line) or _RE_COMMAND_TPL.fullmatch(line)
        if match.re == _RE_MASK_TPL:
            mask = match.group('mask')
        else:
            command = _CommandInfo(mask, match.group('address'), match.group('value'))
            commands.append(command)
    return commands


def _main():
    for filename in ('test_0.txt', 'test_1.txt', 'puzzle.txt'):
        print('\n', filename)
        commands = _load_input_data(filename)

        if filename != 'test_1.txt':
            results = {cmd.address: cmd.value_by_mask() for cmd in commands}
            summa = sum(x for x in results.values())
            print('answer is', summa)

        if filename != 'test_0.txt':
            results = {address: cmd.value for cmd in commands for address in cmd.addresses_by_mask()}
            summa = sum(x for x in results.values())
            print('answer is', summa)


if __name__ == '__main__':
    _main()
