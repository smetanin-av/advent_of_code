import re
from typing import List, Dict, Optional

_RE_DELIMITER = re.compile(r'\s+')
_RE_HGT_TMPL = re.compile(r'(?P<height>\d{2,3})(?P<units>\w{2})')
_RE_HCL_TMPL = re.compile(r'#[0-9a-f]{6}')
_RE_PID_TMPL = re.compile(r'\d{9}')

_MANDATORY_FIELDS = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')
_HEIGHT_RANGES = {'cm': (150, 193), 'in': (59, 76)}


class _PassportInfo:
    def __init__(self, text: str):
        self.fields = {}  # type: Dict[str, str]
        for field_info in _RE_DELIMITER.split(text):
            name, value = field_info.split(':')
            self.fields[name] = value

    @staticmethod
    def _is_value_in_range(value: Optional[str], low: int, high: int) -> bool:
        return value and value.isdigit() and (low <= int(value) <= high)

    def _get_value(self, name: str) -> Optional[str]:
        return self.fields.get(name)

    def _is_field_in_range(self, name: str, low: int, high: int) -> bool:
        return self._is_value_in_range(self._get_value(name), low, high)

    def _is_field_match_pattern(self, name: str, pattern: re.Pattern):
        value = self._get_value(name)
        return value and pattern.fullmatch(value)

    def is_byr_valid(self):
        return self._is_field_in_range('byr', 1920, 2002)

    def is_iyr_valid(self):
        return self._is_field_in_range('iyr', 2010, 2020)

    def is_eyr_valid(self):
        return self._is_field_in_range('eyr', 2020, 2030)

    def is_hgt_valid(self):
        value = self._get_value('hgt')
        if not value:
            return False

        match = _RE_HGT_TMPL.fullmatch(value)
        if not match:
            return False

        units = match.group('units')
        if units not in _HEIGHT_RANGES:
            return False

        height = match.group('height')
        low, high = _HEIGHT_RANGES.get(units)
        return self._is_value_in_range(height, low, high)

    def is_hcl_valid(self):
        return self._is_field_match_pattern('hcl', _RE_HCL_TMPL)

    def is_ecl_valid(self):
        return self._get_value('ecl') in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')

    def is_pid_valid(self):
        return self._is_field_match_pattern('pid', _RE_PID_TMPL)

    def is_valid(self):
        return (self.is_byr_valid() and self.is_iyr_valid() and self.is_eyr_valid() and self.is_hgt_valid() and
                self.is_hcl_valid() and self.is_ecl_valid() and self.is_pid_valid())


def _load_input_data(filename) -> List[_PassportInfo]:
    with open(filename) as fp:
        texts = fp.read().split('\n\n')
        return [_PassportInfo(text) for text in texts]


def _main():
    for filename in ('test.txt', 'puzzle.txt'):
        print('\n', filename)
        passports = _load_input_data(filename)
        valid = list(filter(_PassportInfo.is_valid, passports))
        print('count of valid', len(valid))


if __name__ == '__main__':
    _main()
