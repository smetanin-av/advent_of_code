from typing import Tuple, List, NamedTuple, Optional


class _BusInfo(NamedTuple):
    bus_id: int
    offset: int


def _load_input_data(filename) -> Tuple[int, List[_BusInfo]]:
    with open(filename) as fp:
        text = fp.read()
    depart_time, buses_ids = text.splitlines()
    buses_infos = []
    for index, bus_id in enumerate(buses_ids.split(',')):
        if bus_id == 'x':
            continue
        bus_info = _BusInfo(bus_id=int(bus_id), offset=int(bus_id) - index)
        buses_infos.append(bus_info)
    return int(depart_time), buses_infos


class _WaintingInfo(NamedTuple):
    bus_id: Optional[int]
    time: Optional[int]


def _get_waiting_info(depart_time: int, buses_infos: List[_BusInfo]) -> _WaintingInfo:
    result = _WaintingInfo(bus_id=None, time=None)
    for bus_info in buses_infos:
        time = bus_info.bus_id - (depart_time % bus_info.bus_id)
        if not result.time or result.time > time:
            result = _WaintingInfo(bus_id=bus_info.bus_id, time=time)
    return result


# used https://en.wikipedia.org/wiki/Chinese_remainder_theorem
def _find_subsequent_time(buses_infos: List[_BusInfo]) -> int:
    all_buses_time = 1
    for bus_info in buses_infos:
        all_buses_time *= bus_info.bus_id
    summa = 0
    for bus_info in buses_infos:
        others_buses_time = all_buses_time // bus_info.bus_id
        summa += bus_info.offset * _multiplicative_inverse(others_buses_time, bus_info.bus_id) * others_buses_time
    return summa % all_buses_time


def _multiplicative_inverse(product, number):
    if number == 1:
        return 1
    remainder = number
    val_old, val_new = 0, 1
    while product > 1:
        quotient = product // remainder
        product, remainder = remainder, product % remainder
        val_old, val_new = val_new - quotient * val_old, val_old
    if val_new < 0:
        val_new += number
    return val_new


def _main():
    for filename in ('test.txt', 'input.txt'):
        print('\n', filename)
        depart_time, buses_infos = _load_input_data(filename)

        waiting = _get_waiting_info(depart_time, buses_infos)
        print('bus id', waiting.bus_id, 'wait time', waiting.time,
              'answer is', waiting.bus_id * waiting.time)

        time = _find_subsequent_time(buses_infos)
        print('subsequent time is', time)


if __name__ == '__main__':
    _main()
