# advent of code 2023
# day 13

import numpy as np

file = 'input.txt'

class MirrorField:
    def __init__(self, maps):
        self.maps = maps

    def findMirror(self, map, smudges=0):
        for r in range(len(map) - 1):
            if r + 1 <= len(map) / 2:
                a = map[:r + 1, :]
                b = map[r + r + 1:r:-1, :]
            else:
                a = map[r + 1:, :]
                b = map[r:r + r + 1 - len(map):-1, :]
            if sum(sum(abs(a - b))) == smudges:
                return 100 * (r + 1)
        t_map = map.T
        for c in range(len(t_map) - 1):
            if c + 1 <= len(t_map) / 2:
                a = t_map[:c + 1, :]
                b = t_map[c + c + 1:c:-1, :]
            else:
                a = t_map[c + 1:, :]
                b = t_map[c:c + c + 1 - len(t_map):-1, :]
            if sum(sum(abs(a - b))) == smudges:
                return c + 1
            
    def findAllMirrors(self, smudges=0):
        return sum([self.findMirror(map, smudges) for map in self.maps])
    
def part_1(mirrorField):
    print('Part 1:', mirrorField.findAllMirrors())

def part_2(mirrorField):
    print('Part 2:', mirrorField.findAllMirrors(1))

def main():
    maps = [np.array([[1 if char == '#' else 0 for char in row] for row in map.splitlines()]) for map in open(file, 'r').read().split('\n\n')]
    mirrorField = MirrorField(maps)
    part_1(mirrorField)
    part_2(mirrorField)

if __name__ == '__main__':
    main()