# advent of code 2023
# day 18

from collections import defaultdict

file = 'input.txt'

class Lagoon:
    def __init__(self, instructions):
        self.instructions = instructions

    def translateHex(self, hex):
        directions = ['R','D','L','U']
        dir = hex[-1]
        dist = int(hex[:-1], 16)
        return directions[int(dir)], dist

    def digHole(self, colorSwap=False):
        self.edges = []
        self.corners = defaultdict(lambda: ' ')
        self.asymptotes = {'x': set(), 'y': set()}
        directions = {'U': (0, -1, '|'), 'D': (0, 1, '|'), 'L': (-1, 0, '-'), 'R': (1, 0, '-')}
        corners = {
            ('U', 'R'): 'F',
            ('U', 'L'): '7',
            ('R', 'U'): 'J',
            ('R', 'D'): '7',
            ('D', 'R'): 'L',
            ('D', 'L'): 'J',
            ('L', 'U'): 'L',
            ('L', 'D'): 'F',
            ('S', 'U'): 'S',
            ('S', 'D'): 'S',
            ('S', 'L'): 'S',
            ('S', 'R'): 'S',
        }
        cursor = (0, 0)
        dir = 'S'
        for instruction in self.instructions:
            old_dir = dir
            dir, dist, color = instruction
            if colorSwap:
                dir, dist = self.translateHex(color)
            self.corners[cursor] = corners[(old_dir, dir)]
            x, y = cursor
            self.asymptotes['x'].add(x)
            self.asymptotes['y'].add(y)
            dx, dy, mark = directions[dir]
            new_cursor = (x + (dx * dist), y + (dy * dist))
            self.corners[new_cursor] = mark
            if dir in ['U', 'D']:
                self.edges.append(sorted((cursor, new_cursor), key=lambda e: e[1]))
            cursor = new_cursor
        old_dir = dir
        dir, dist, color = self.instructions[0]
        self.corners[cursor] = corners[(old_dir, dir)]
    
    def checkInterior(self, coord):
        x, y = coord
        return sum([m[1] < y < n[1] and x < m[0] for m, n in self.edges]) % 2 == 1

    def countInterior(self):
        asymptotes = {}
        asymptotes['x'] = sorted(list(self.asymptotes['x']))
        asymptotes['y'] = sorted(list(self.asymptotes['y']))
        interior = 0
        for j in range(len(self.asymptotes['y']) - 1):
            for i in range(len(self.asymptotes['x']) - 1):
                x = asymptotes['x'][i]
                y = asymptotes['y'][j]
                if self.checkInterior((x + .5, y + .5)):
                    x_adjust = 0 if self.checkInterior((x - .5, y + .5)) else 1
                    y_adjust = 0 if self.checkInterior((x + .5, y - .5)) else 1
                    ne_adjust = y_adjust if self.checkInterior((asymptotes['x'][i + 1] + .5, y - .5)) else 0
                    nw_adjust = 1 if self.checkInterior((x - .5, y - .5)) and x_adjust + y_adjust == 2 else 0
                    interior += (asymptotes['x'][i + 1] - x + x_adjust) * (asymptotes['y'][j + 1] - y + y_adjust) - ne_adjust - nw_adjust
        return interior

    def printMap(self, asymptotes=False):
        x_min = min([key[0] for key in self.corners])
        x_max = max([key[0] for key in self.corners])
        y_min = min([key[1] for key in self.corners])
        y_max = max([key[1] for key in self.corners])
        image = ''
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                if asymptotes:
                    if (x, y) in self.corners:
                        image += self.corners[(x, y)]
                    elif x in self.asymptotes['x'] and y in self.asymptotes['y']:
                        image += '+'
                    elif x in self.asymptotes['x']:
                        image += '|'
                    elif y in self.asymptotes['y']:
                        image += '-'
                    else:
                        image += ' '
                else:
                    image += self.corners[(x, y)]
            image += '\n'
        print(image)

def part_1(lagoon):
    lagoon.digHole()
    print('Part 1:', lagoon.countInterior())

def part_2(lagoon):
    lagoon.digHole(True)
    print('Part 2:', lagoon.countInterior())

def main():
    instructions = [[dir, int(dist), color[2:-1]] for dir, dist, color in [instruction.split(' ') for instruction in open(file, 'r').read().splitlines()]]
    lagoon = Lagoon(instructions)
    part_1(lagoon)
    part_2(lagoon)

if __name__ == '__main__':
    main()