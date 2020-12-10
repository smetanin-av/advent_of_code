import re
from collections import defaultdict
from typing import Dict, List, Tuple

_RE_RULE_DEF_TMPL = re.compile(r'(?P<color>.*) bags contain (?P<content>.*)')
_RE_INNER_BAGS_COLORS = re.compile(r'(?P<count>\d+) (?P<color>[a-z ]+) bag')


class _RulesInfo:
    def __init__(self):
        self.outer_bags = defaultdict(list)  # type: Dict[str, List[str]]
        self.inner_bags = defaultdict(list)  # type: Dict[str, List[Tuple[int, str]]]

    @staticmethod
    def _parse_rule_def(text: str) -> Tuple[str, str]:
        match = _RE_RULE_DEF_TMPL.fullmatch(text)
        return match.group('color'), match.group('content')

    def add_rule(self, text: str):
        outer_color, content_info = self._parse_rule_def(text)
        inner_colors = _RE_INNER_BAGS_COLORS.findall(content_info)
        for count_of_bags, inner_color in inner_colors:
            self.outer_bags[inner_color].append(outer_color)
            self.inner_bags[outer_color].append((int(count_of_bags), inner_color))

    def possible_outer_bags(self, breadcrumbs: List[str]) -> List[List[str]]:
        variants = []
        for holder_color in self.outer_bags.get(breadcrumbs[0], []):
            if holder_color in breadcrumbs:
                print('found cycle', breadcrumbs, holder_color)
            variant = [holder_color, *breadcrumbs]
            variants.append(variant)
            variants.extend(self.possible_outer_bags(variant))
        return variants

    def count_of_inner_bags(self, color: str) -> int:
        count = 0
        for count_of_bags, inner_color in self.inner_bags[color]:
            count += (self.count_of_inner_bags(inner_color) + 1) * count_of_bags
        return count


def _load_input_data(filename) -> _RulesInfo:
    with open(filename) as fp:
        data = fp.read()
    rules_info = _RulesInfo()
    for line in data.splitlines():
        rules_info.add_rule(line)
    return rules_info


def _main():
    for filename in ('test_0.txt', 'test_1.txt', 'input.txt'):
        print('\n', filename)
        rules_info = _load_input_data(filename)

        variants = rules_info.possible_outer_bags(['shiny gold'])
        print('found', len(variants), 'variants')

        top_bag_colors = set(bag_colors[0] for bag_colors in variants)
        print('answer is', len(top_bag_colors))

        count_of_inner_bags = rules_info.count_of_inner_bags('shiny gold')
        print('count of inner bags', count_of_inner_bags)


if __name__ == '__main__':
    _main()
