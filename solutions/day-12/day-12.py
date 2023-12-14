# advent of code 2023
# day 12

import re
from functools import cache

file = 'input.txt'

class Nonograms:
    def __init__(self, maps):
        self.maps = maps
        self.quintuple_maps = [['?'.join([map[0] for i in range(5)]), map[1] * 5] for map in self.maps]
        
    @cache
    def findStringCombinations(self, remaining_string, remaining_parts):
        if len(remaining_parts) == 0:
            if '#' in remaining_string:
                return 0
            else:
                return 1
        else:
            remaining_string = re.sub('^\.*', '', remaining_string)
            next_part = remaining_parts[0]
            match = re.search(f'^((#+)\?*)(?:\.|$)', remaining_string)
            if match:
                if len(match.groups()[1]) < next_part:
                    if len(match.groups()[0]) >= next_part:
                        remaining_string = remaining_string.replace(match.groups()[0][:next_part], '', 1)
                        remaining_string = '' if len(remaining_string) == 0 else remaining_string[1:]
                        next_remaining_parts = remaining_parts[1:]
                        return self.findStringCombinations(remaining_string, next_remaining_parts)
                    else:
                        return 0
                elif len(match.groups()[1]) == next_part:
                    remaining_string = remaining_string.replace(match.groups()[0][:next_part], '', 1)
                    remaining_string = '' if len(remaining_string) == 0 else remaining_string[1:]
                    next_remaining_parts = remaining_parts[1:]
                    return self.findStringCombinations(remaining_string, next_remaining_parts)
                elif len(match.groups()[1]) > next_part:
                    return 0
            else:
                if remaining_string.count('?') == 0:
                    return 0
                else:
                    try_open = remaining_string.replace('?', '.', 1)
                    try_closed = remaining_string.replace('?', '#', 1)
                    return self.findStringCombinations(try_open, remaining_parts) + self.findStringCombinations(try_closed, remaining_parts)

def part_1(nonograms):
    print('Part 1:', sum([nonograms.findStringCombinations(map[0], map[1]) for map in nonograms.maps]))

def part_2(nonograms):
    print('Part 2:', sum([nonograms.findStringCombinations(map[0], map[1]) for map in nonograms.quintuple_maps]))

def main():
    damaged_maps = open(file, 'r').read().splitlines()
    maps = [[map.split(' ')[0], tuple(eval('[' + map.split(' ')[1] + ']'))] for map in damaged_maps]
    nonograms = Nonograms(maps)
    part_1(nonograms)
    part_2(nonograms)

if __name__ == '__main__':
    main()