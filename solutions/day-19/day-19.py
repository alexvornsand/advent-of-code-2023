# advent of code 2023
# day 19

import re
import math

file = 'input.txt'

class Rule:
    def __init__(self, id, instructions):
        self.id = id
        self.rules = [instruction.split(':')[0] if len(instruction.split(':')) > 1 else 'True' for instruction in instructions.split(',')]
        self.destinations = [instruction.split(':')[1] if len(instruction.split(':')) > 1 else instruction for instruction in instructions.split(',')]
    
    def evaluateRule(self, keys):
        x, m, a, s = keys
        i = 0
        while True:
            if eval(self.rules[i]):
                return self.destinations[i]
            i += 1

    def fracturePartRange(self, keys, i):
        if self.rules[i] == 'True':
            return [[keys, self.destinations[i], 0]]
        key, opr, threshold = re.search('(\w+)([<>])(\d+)', self.rules[i]).groups()
        if opr == '>':
            threshold = int(threshold) + 1
        else:
            threshold = int(threshold)
        key_low = {key: value for key, value in keys.items()}
        key_low[key] = []
        key_high = {key: value for key, value in keys.items()}
        key_high[key] = []
        for rng in keys[key]:
            if rng[1] < threshold:
                key_low[key].append(rng)
            elif rng[0] >= threshold:
                key_high[key].append(rng)
            else:
                key_low[key].append([rng[0], threshold - 1])
                key_high[key].append([threshold, rng[1]])
        if opr == '>':
            return [[key_high, self.destinations[i], 0], [{key: value for key, value in key_low.items()}, self.id, i + 1]]
        else:
            return [[key_low, self.destinations[i], 0], [{key: value for key, value in key_high.items()}, self.id, i + 1]]

class SortSystem:
    def __init__(self, parts, rules):
        self.parts = [[int(x) for x in list(re.findall('\d+', part))] for part in parts.splitlines()]
        self.rules = {name: Rule(name, instructions[:-1]) for name, instructions in [line.split('{') for line in rules.splitlines()]}
        self.destinations = {'A': [], 'R': []}

    def evaluatePart(self, part, rule='in'):
        result = self.rules[rule].evaluateRule(part)
        if result in self.destinations:
            self.destinations[result].append(sum(part))
        else:
            self.evaluatePart(part, result)

    def evaluateParts(self):
        for part in self.parts:
            self.evaluatePart(part)

    def findLegitCombinations(self):
        legit_combinations = []
        queue = [[{'x': [[1, 4000]], 'm': [[1, 4000]], 'a': [[1, 4000]], 's': [[1, 4000]]}, 'in', 0]]
        while queue:
            test = queue[0]
            queue.pop(0)
            keys, rule, index = test
            if rule == 'A':
                legit_combinations.append(math.prod([sum([rng[1] - rng[0] + 1 for rng in keys[key]]) for key in keys]))
            elif rule == 'R':
                continue
            else:
                additional_combinations = self.rules[rule].fracturePartRange(keys, index)
                for combination in additional_combinations:
                    queue.append(combination)
        return sum(legit_combinations)

def part_1(sortSystem):
    sortSystem.evaluateParts()
    print('Part 1:', sum(sortSystem.destinations['A']))

def part_2(sortSystem):
    print('Part 2:', sortSystem.findLegitCombinations())

def main():
    rules, parts = open(file, 'r').read().strip().split('\n\n')
    sortSystem = SortSystem(parts, rules)
    part_1(sortSystem)
    part_2(sortSystem)

if __name__ == '__main__':
    main()