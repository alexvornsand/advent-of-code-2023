# advent of code 2023
# day 11

import numpy as np

file = 'input.txt'

class Universe:
    def __init__(self, map):
        self.map = map
        self.galaxies = []
        self.expanded_galaxies = []

    def printMap(self):
        print('\n'.join([''.join(row) for row in self.map]))

    def findGalaxies(self):
        indices = np.where(self.map == '#')
        self.galaxies = [[x, y] for x, y in zip(list(indices[0]), list(indices[1]))]
        
    def expandUniverse(self, f=1):
        self.expanded_galaxies = [[coord for coord in galaxy] for galaxy in self.galaxies]
        empty_rows = [r for r in range(len(self.map)) if '#' not in self.map[r,:]]
        empty_columns = [c for c in range(len(self.map.T)) if '#' not in self.map[:,c]]
        for r in empty_rows:
            for galaxy in self.galaxies:
                if galaxy[0] > r:
                    self.expanded_galaxies[self.galaxies.index(galaxy)][0] += f - 1
        for c in empty_columns:
            for galaxy in self.galaxies:
                if galaxy[1] > c:
                    self.expanded_galaxies[self.galaxies.index(galaxy)][1] += f - 1

    def sumDistancesBetweenGalaxies(self):
        return int(sum([abs(i[0] - j[0]) + abs(i[1] - j[1]) for i in self.expanded_galaxies for j in self.expanded_galaxies if i != j]) / 2)

def part_1(universe):
    universe.expandUniverse(2)
    print('Part 1:', universe.sumDistancesBetweenGalaxies())

def part_2(universe):
    universe.expandUniverse(1000000)
    print('Part 2:', universe.sumDistancesBetweenGalaxies())

def main():
    map = np.array([[char for char in row] for row in open(file, 'r').read().splitlines()])
    universe = Universe(map)
    universe.findGalaxies()
    part_1(universe)
    part_2(universe)

if __name__ == '__main__':
    main()