import abc
import re
from collections import deque
from typing import Tuple, Type, Union

_RE_PLAYER_TITLE = re.compile(r'Player (?P<id>\d+):')


class _IComparer(abc.ABC):
    def __init__(self, game: '_CardsGame'):
        self.game = game

    @property
    def deck_1(self):
        return self.game.deck_1

    @property
    def deck_2(self):
        return self.game.deck_2

    @abc.abstractmethod
    def is_first_wins(self, card_1: int, card_2: int) -> bool:
        pass


class _SimpleComparer(_IComparer):
    def is_first_wins(self, card_1: int, card_2: int) -> bool:
        return card_1 > card_2


class _SubGameComparer(_SimpleComparer):
    def is_first_wins(self, card_1: int, card_2: int) -> bool:
        if self.is_sub_game_possible(card_1, card_2):
            copy_1 = self.deck_1.get_copy(card_1)
            copy_2 = self.deck_2.get_copy(card_2)
            sub_game = _CardsGame(copy_1, copy_2, _SubGameComparer)
            player_1 = self.deck_1.player_id
            return sub_game.play_to_end().player_id == player_1
        else:
            return super().is_first_wins(card_1, card_2)

    def is_sub_game_possible(self, card_1: int, card_2: int) -> bool:
        return len(self.deck_1) >= card_1 and len(self.deck_2) >= card_2


class _DeckInfo:
    def __init__(self, player_id: str):
        self.player_id = player_id
        self._cards = deque()

    @staticmethod
    def build(text: str) -> '_DeckInfo':
        player_id = _RE_PLAYER_TITLE.fullmatch(text).group('id')
        return _DeckInfo(player_id)

    def add_card(self, card: Union[str, int]) -> None:
        if isinstance(card, str):
            card = int(card)
        self._cards.append(card)

    def pop_card(self) -> int:
        return self._cards.popleft()

    def get_score(self):
        score = 0
        cards_count = len(self._cards)
        for index, card in enumerate(self._cards):
            score += (cards_count - index) * card
        return score

    def get_all(self) -> Tuple:
        return tuple(self._cards)

    def get_copy(self, count_of_cards: int) -> '_DeckInfo':
        copy = _DeckInfo(self.player_id)
        for index in range(count_of_cards):
            card = self._cards[index]
            copy._cards.append(card)
        return copy

    def __bool__(self):
        return bool(self._cards)

    def __len__(self):
        return len(self._cards)


class _CardsGame:
    def __init__(self, deck_1: _DeckInfo, deck_2: _DeckInfo, type_of_comparer: Type[_IComparer]):
        self.deck_1 = deck_1
        self.deck_2 = deck_2
        self._history = set()
        self._comparer = type_of_comparer(self)

    def _play_round(self):
        card_1 = self.deck_1.pop_card()
        card_2 = self.deck_2.pop_card()

        if self._comparer.is_first_wins(card_1, card_2):
            self.deck_1.add_card(card_1)
            self.deck_1.add_card(card_2)
        else:
            self.deck_2.add_card(card_2)
            self.deck_2.add_card(card_1)

    def _get_state(self):
        return self.deck_1.get_all(), self.deck_2.get_all()

    def play_to_end(self) -> _DeckInfo:
        while self.deck_1 and self.deck_2:
            state = self._get_state()
            if state in self._history:
                return self.deck_1
            else:
                self._play_round()
                self._history.add(state)
        return self.deck_1 or self.deck_2


def _load_input_data(filename) -> Tuple[_DeckInfo, _DeckInfo]:
    with open(filename) as fp:
        text = fp.read()

    decks = []
    deck = None

    for line in text.splitlines():
        if not line:
            deck = None
        elif deck is not None:
            deck.add_card(line)
        else:
            deck = _DeckInfo.build(line)
            decks.append(deck)

    return decks[0], decks[1]


def _main():
    for filename in ('test_0.txt', 'test_1.txt', 'input.txt'):
        print('\n', filename)

        deck_1_orig, deck_2_orig = _load_input_data(filename)
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
