# advent of code 2023
# day 8

import math

file = 'input.txt'

class Desert:
    def __init__(self, instructions, maps):
        self.instructions = [{'L': 0, 'R': 1}[instr] for instr in instructions[0]]
        self.map = {}
        for map in maps:
            key, value = [string.strip() for string in map.split('=')]
            self.map[key] = [neighbor.strip() for neighbor in value[1:-1].split(',')]

    def navigateMap(self):
        i = 0
        loc = 'AAA'
        while True:
            if loc == 'ZZZ':
                return i
            else:
                loc = self.map[loc][self.instructions[i % len(self.instructions)]]
                i += 1

    def navigateMultiMaps(self):
        cycles = []
        for start in [loc for loc in list(self.map.keys()) if loc[2] == 'A']:
            loc = start
            i = 0
            while True:
                if loc[2]  == 'Z':
                    cycles.append(i)
                    break
                else:
                    loc = self.map[loc][self.instructions[i % len(self.instructions)]]
                    i += 1
        return math.lcm(*cycles)

def part_1(desert):
    print('Part 1:', desert.navigateMap())

def part_2(desert):
    print('Part 2:', desert.navigateMultiMaps())

def main():
    instructions, maps = [section.splitlines() for section in open(file, 'r').read().split('\n\n')]
    desert = Desert(instructions, maps)
    part_1(desert)
    part_2(desert)

if __name__ == '__main__':
    main()