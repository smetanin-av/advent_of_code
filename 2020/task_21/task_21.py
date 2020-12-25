import re
from collections import defaultdict
from typing import Iterable, List, Set, Tuple

_RE_FOOD_INFO = re.compile(r'(?P<ingredients>[a-z ]+) \(contains (?P<allergens>[a-z, ]+)\)')


class _FoodInfo:
    def __init__(self, text: str):
        match = _RE_FOOD_INFO.fullmatch(text)
        self.ingredients = match.group('ingredients').split(' ')
        self.allergens = match.group('allergens').split(', ')


class _ListOfFoods:
    def __init__(self):
        self._foods_all = []
        self._by_ingredients = defaultdict(list)
        self.allergens_info = {}

    def add_food(self, text: str):
        food = _FoodInfo(text)
        self._foods_all.append(food)

        for ingredient in food.ingredients:
            self._by_ingredients[ingredient].append(food)

        for allergen in food.allergens:
            ingredients = self.allergens_info.get(allergen)
            if ingredients:
                if isinstance(ingredients, set):
                    ingredients.intersection_update(food.ingredients)
                    if len(ingredients) == 1:
                        self.allergens_info[allergen] = ingredients.pop()
                elif ingredients not in food.ingredients:
                    raise Exception('Wrong match!')
            else:
                self.allergens_info[allergen] = set(food.ingredients)
        self.update_allergens_info()

    def get_possible_allergens(self) -> Iterable[str]:
        for ingredients in self.allergens_info.values():
            if isinstance(ingredients, str):
                yield ingredients
            elif isinstance(ingredients, set):
                for ingredient in ingredients:
                    yield ingredient

    def is_possible_allergen(self, ingredient) -> bool:
        return ingredient in self.get_possible_allergens()

    def get_foods_with_safe_ingredients(self) -> Iterable[Tuple[str, List[_FoodInfo]]]:
        for ingredient, foods in self._by_ingredients.items():
            if not self.is_possible_allergen(ingredient):
                yield ingredient, foods

    def get_matched_allergens(self) -> Iterable[Tuple[str, str]]:
        for allergen, ingredients in self.allergens_info.items():
            if isinstance(ingredients, str):
                yield allergen, ingredients

    def get_unmatched_allergens(self) -> Iterable[Tuple[str, Set]]:
        for allergen, ingredients in self.allergens_info.items():
            if isinstance(ingredients, set):
                yield allergen, ingredients

    def get_allergens_to_update(self) -> Iterable[Tuple[str, Set]]:
        for _, ingredient in self.get_matched_allergens():
            for allergen, ingredients in self.get_unmatched_allergens():
                if ingredient in ingredients:
                    yield allergen, ingredients - {ingredient}

    def update_allergens_info(self) -> None:
        for allergen, ingredients in self.get_allergens_to_update():
            if len(ingredients) == 1:
                self.allergens_info[allergen] = ingredients.pop()
            else:
                self.allergens_info[allergen] = ingredients


def _load_input_data(filename) -> _ListOfFoods:
    with open(filename) as fp:
        text = fp.read()

    list_of_foods = _ListOfFoods()
    for line in text.splitlines():
        list_of_foods.add_food(line)

    return list_of_foods


def _main():
    for filename in ('test.txt', 'puzzle.txt'):
        print('\n', filename)

        list_of_foods = _load_input_data(filename)

        count = 0
        for ingredient, foods in list_of_foods.get_foods_with_safe_ingredients():
            count += len(foods)
        print('usage of safe ingredients is', count)

        while any(list_of_foods.get_allergens_to_update()):
            list_of_foods.update_allergens_info()

        dangerous = []
        for allergen in sorted(list_of_foods.allergens_info):
            ingredient = list_of_foods.allergens_info[allergen]
            dangerous.append(ingredient)
        print('dangerous are', ','.join(dangerous))


if __name__ == '__main__':
    _main()
