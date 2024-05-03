from typing import Dict, List, Set

from parser_constants import *


class FirstFollowCalculator:
    def __init__(self, rules: List[GRAMMAR_RULE]):
        self.rules = rules
        self.first_sets: Dict[NonTerminal, Set[Terminal]] = {non_terminal: set() for non_terminal, _ in rules}
        self.follow_sets: Dict[NonTerminal, Set[Terminal]] = {non_terminal: set() for non_terminal, _ in rules}
        self.predict_sets = {}

    def collect_set(self, initial_set: Set[Terminal], items: GRAMMAR_RHS, additional_set: Set[Terminal]) -> Set[Terminal]:
        result = initial_set
        eps = False

        for index, item in enumerate(items):
            if isinstance(item, NonTerminal):
                filtered = self.first_sets[item] - {EPSILON}
                result = result.union(filtered)

                if EPSILON in self.first_sets[item]:
                    if index + 1 < len(items):
                        continue
                    eps = True
            else:
                result = result.union({item})

            break

        return result.union(additional_set) if eps else result

    def calculate_first_sets(self):
        changed = True

        while changed:
            changed = False

            for left, right in self.rules:
                current_set = self.first_sets[left]
                new_set = current_set.union(self.collect_set(current_set, right, {EPSILON}))

                if len(self.first_sets[left]) != len(new_set):
                    self.first_sets[left] = new_set
                    changed = True

    def calculate_follow_sets(self):
        self.follow_sets[self.rules[0][0]].add(EOF)

        changed = True

        while changed:
            changed = False

            for left, right in self.rules:
                for index, item in enumerate(right):
                    if not isinstance(item, NonTerminal):
                        continue

                    set_accum = self.follow_sets[item]
                    if index + 1 < len(right):
                        next_set = self.collect_set(set_accum, right[index + 1:], self.follow_sets[left])
                    else:
                        next_set = self.follow_sets[left]

                    updated_set = set_accum.union(next_set)
                    if len(self.follow_sets[item]) != len(updated_set):
                        self.follow_sets[item] = updated_set
                        changed = True

    def calculate_predict_sets(self):
        for rule_index, (left, right) in enumerate(self.rules):
            set_accum = set()

            if isinstance(right[0], NonTerminal):
                set_accum = set_accum.union(self.collect_set(set_accum, right, self.follow_sets[left]))
            elif right[0] == EPSILON:
                set_accum = self.follow_sets[left]
            else:
                set_accum.add(right[0])

            self.predict_sets[rule_index + 1] = set_accum



if __name__ == '__main__':
    calculator = FirstFollowCalculator(grammar_rules)
    calculator.calculate_first_sets()
    calculator.calculate_follow_sets()
    calculator.calculate_predict_sets()

    from pprint import pprint
    pprint(calculator.first_sets)
    pprint(calculator.follow_sets)
    pprint(calculator.predict_sets)