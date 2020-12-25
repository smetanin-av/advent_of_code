from typing import Dict, List, cast

_CUPS_LABELS = {
    'test': '389125467',
    'puzzle': '624397158'
}


class _CupInfo:
    def __init__(self, label: int):
        self.label = label
        self.next_cup = cast(_CupInfo, None)


class _CupsList:
    def __init__(self, labels: List[int]):
        self._data = self._build_data(labels)

    @staticmethod
    def _build_data(labels: List[int]) -> Dict[int, _CupInfo]:
        data = {}
        first = None
        last = None
        for label in labels:
            cup_info = _CupInfo(label)
            data[label] = cup_info
            if not first:
                first = cup_info
            else:
                cup_info.next_cup = first
            if not last:
                last = cup_info
            else:
                last.next_cup = cup_info
                last = cup_info
        return data

    def is_cup_exists(self, cup: int) -> bool:
        return cup in self._data

    def get_label_after(self, cup: int) -> int:
        return self._data[cup].next_cup.label

    def pick_cup_after(self, base_cup: int) -> int:
        base_cup_info = self._data[base_cup]
        next_cup_info = base_cup_info.next_cup
        base_cup_info.next_cup = next_cup_info.next_cup
        del self._data[next_cup_info.label]
        return next_cup_info.label

    def insert_cup_after(self, base_cup: int, new_cup: int) -> None:
        base_cup_info = self._data[base_cup]
        new_cup_info = _CupInfo(new_cup)
        self._data[new_cup] = new_cup_info
        new_cup_info.next_cup = base_cup_info.next_cup
        base_cup_info.next_cup = new_cup_info

    def get_labels_after(self, label: int, count: int) -> List[int]:
        cup_info = self._data[label].next_cup
        results = []
        while len(results) < count:
            results.append(cup_info.label)
            cup_info = cup_info.next_cup
        return results


class _CupsGame:
    def __init__(self, labels: List[int]):
        self.list_of_cups = _CupsList(labels)
        self.current = labels[0]
        self.minimum = min(labels)
        self.maximum = max(labels)

    def pick_up_3_after_current(self):
        labels = []
        while len(labels) < 3:
            label = self.list_of_cups.pick_cup_after(self.current)
            labels.append(label)
        return labels

    def find_destination(self):
        destination = self.current - 1
        while not self.list_of_cups.is_cup_exists(destination):
            destination -= 1
            if destination < self.minimum:
                destination = self.maximum
        return destination

    def do_round(self):
        picked_items = self.pick_up_3_after_current()
        destination = self.find_destination()

        for label in picked_items[::-1]:
            self.list_of_cups.insert_cup_after(destination, label)

        self.current = self.list_of_cups.get_label_after(self.current)

    def get_after(self, label: int, count: int) -> List[int]:
        return self.list_of_cups.get_labels_after(label, count)


def _main():
    for name, labels in _CUPS_LABELS.items():
        print('\n', name)

        initials = [int(label) for label in labels]
        game = _CupsGame(initials)
        for _ in range(100):
            game.do_round()

        answer = game.get_after(1, len(labels) - 1)
        print('100 moves answer is', ''.join(str(x) for x in answer))

        initials += range(10, 1000001)
        game = _CupsGame(initials)
        for _ in range(10000000):
            game.do_round()

        answer = game.get_after(1, 2)
        print('10000000 moves answer is', answer[0] * answer[1])


if __name__ == '__main__':
    _main()
