from typing import NamedTuple


class _PublicKeys(NamedTuple):
    card: int
    door: int


_PUBLIC_KEYS_to_CHECK = {
    'test': _PublicKeys(card=5764801, door=17807724),
    'puzzle': _PublicKeys(card=11349501, door=5107328)
}


def _load_input_data(filename):
    with open(filename) as fp:
        text = fp.read()


def _main():
    for filename in ('test_0.txt', 'test_1.txt', 'puzzle.txt'):
        print('\n', filename)

        _ = _load_input_data(filename)
        for type_of_comparer in (_SimpleComparer, _SubGameComparer):
            print('compare is', type_of_comparer.__name__)
            deck_1 = deck_1_orig.get_copy(count_of_cards=len(deck_1_orig))
            deck_2 = deck_2_orig.get_copy(count_of_cards=len(deck_2_orig))

            game = _CardsGame(deck_1, deck_2, type_of_comparer)
            winner = game.play_to_end()

            print('winner is', winner.player_id, 'score', winner.get_score())
            print('deck #1', deck_1.get_all())
            print('deck #2', deck_2.get_all())


if __name__ == '__main__':
    _main()
