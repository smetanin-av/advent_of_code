from typing import Dict


class _SeatInfo:
    def __init__(self, ticket: str):
        self._data = ticket

    def get_row(self) -> int:
        value = self._data[:7].replace('B', '1').replace('F', '0')
        return int(value, 2)

    def get_col(self) -> int:
        value = self._data[7:].replace('R', '1').replace('L', '0')
        return int(value, 2)

    def get_seat_id(self) -> int:
        return self.get_row() * 8 + self.get_col()


def _load_input_data(filename) -> Dict[int, _SeatInfo]:
    with open(filename) as fp:
        tickets = fp.read().splitlines()
    seats_infos = {}
    for ticket in tickets:
        seat_info = _SeatInfo(ticket)
        seats_infos[seat_info.get_seat_id()] = seat_info
    return seats_infos


def _main():
    for filename in ('test.txt', 'input.txt'):
        print('\n', filename)
        seats_by_ids = _load_input_data(filename)

        min_seat_id = min(seats_by_ids.keys())
        print('min seat ID', min_seat_id)

        max_seat_id = max(seats_by_ids.keys())
        print('max seat ID', max_seat_id)

        for seat_id in range(min_seat_id, max_seat_id):
            if seat_id not in seats_by_ids and (seat_id - 1) in seats_by_ids and (seat_id + 1) in seats_by_ids:
                print('possible seat id', seat_id)


if __name__ == '__main__':
    _main()
