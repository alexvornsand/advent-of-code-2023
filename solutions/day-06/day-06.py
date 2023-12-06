# advent of code 2023
# day 6

import re
import math

file = 'input.txt'

class BoatRaces:
    def __init__(self, races):
        self.races = races
        self.big_race = (int(''.join([str(n[0]) for n in self.races])), int(''.join([str(n[1]) for n in self.races])))

    def runRace(self, race):
        t, d = race
        a = (t - (t**2 - 4 * d)**(1 / 2)) / 2
        b = (t + (t**2 - 4 * d)**(1 / 2)) / 2
        if a > b:            
            return abs(math.ceil(a) - math.floor(b)) - 1
        else:
            return abs(math.floor(a) - math.ceil(b)) - 1
    
    def runAllRaces(self):
        return [self.runRace(race) for race in self.races]
    
def part_1(boatRaces):
    print('Part 1:', math.prod(boatRaces.runAllRaces()))

def part_2(boatRaces):
    print('Part 2:', boatRaces.runRace(boatRaces.big_race))

def main():
    lines = [[int(x) for x in list(re.findall('\d+', line.split(':')[1]))] for line in open(file, 'r').read().splitlines()]
    races = [(time, distance) for time, distance in zip(lines[0], lines[1])]
    boatRaces = BoatRaces(races)
    part_1(boatRaces)
    part_2(boatRaces)

if __name__ == '__main__':
    main()