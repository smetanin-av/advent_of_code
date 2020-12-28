from typing import NamedTuple


class _PublicKeys(NamedTuple):
    card: int
    door: int


_SUBJECT_NUMBER = 7
_VALUES_HIGH_BOUND = 20201227

_PUBLIC_KEYS_to_CHECK = {
    'test': _PublicKeys(card=5764801, door=17807724),
    'puzzle': _PublicKeys(card=11349501, door=5107328)
}


def _do_transform_step(value: int, subject: int) -> int:
    return (value * subject) % _VALUES_HIGH_BOUND


def _do_transform_loop(subject: int, loop_size: int) -> int:
    value = 1
    for _ in range(loop_size):
        value = _do_transform_step(value, subject)
    return value


def _main():
    for name, publick_key in _PUBLIC_KEYS_to_CHECK.items():
        print('\n', name)

        card_loop_size = None
        door_loop_size = None

        value = 1
        index = 0

        while not card_loop_size or not door_loop_size:
            value = _do_transform_step(value, _SUBJECT_NUMBER)
            index += 1
            if value == publick_key.card:
                card_loop_size = index
            if value == publick_key.door:
                door_loop_size = index

        print('card loop size', card_loop_size)
        print('encryption key', _do_transform_loop(publick_key.door, card_loop_size))

        print('door loop size', door_loop_size)
        print('encryption key', _do_transform_loop(publick_key.card, door_loop_size))


if __name__ == '__main__':
    _main()
