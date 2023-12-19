### [--- Day 18: Lavaduct Lagoon ---](https://adventofcode.com/2023/day/18)

Thanks to your efforts, the machine parts factory is one of the first factories up and running since the lavafall came back. However, to catch up with the large backlog of parts requests, the factory will also need a **large supply of lava** for a while; the Elves have already started creating a large lagoon nearby for this purpose.

However, they aren't sure the lagoon will be big enough; they've asked you to take a look at the dig plan (your puzzle input). For example:

```
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
```

The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of meters **up** (`U`), **down** (`D`), **left** (`L`), or **right** (`R`), clearing full 1 meter cubes as they go. The directions are given as seen from above, so if "up" were north, then "right" would be east, and so on. Each trench is also listed with the **color that the edge of the trench should be painted** as an [RGB hexadecimal color code](https://en.wikipedia.org/wiki/RGB_color_model#Numeric_representations).

When viewed from above, the above example dig plan would result in the following loop of **trench** `(#)` having been dug out from otherwise **ground-level terrain** (`.`):

```
#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######
```

At this point, the trench could contain 38 cubic meters of lava. However, this is just the edge of the lagoon; the next step is to **dig out the interior** so that it is one meter deep as well:

```
#######
#######
#######
..#####
..#####
#######
#####..
#######
.######
.######
```

Now, the lagoon can contain a much more respectable **`62`** cubic meters of lava. While the interior is dug out, the edges are also painted according to the color codes in the dig plan.

The Elves are concerned the lagoon won't be large enough; if they follow their dig plan, **how many cubic meters of lava could it hold?**

### --- Part Two ---

The Elves were right to be concerned; the planned lagoon would be **much too small**.

After a few minutes, someone realizes what happened; someone **swapped the color and instruction parameters** when producing the dig plan. They don't have time to fix the bug; one of them asks if you can **extract the correct instructions** from the hexadecimal codes.

Each hexadecimal code is **six hexadecimal digits** long. The first five hexadecimal digits encode the **distance in meters** as a five-digit hexadecimal number. The last hexadecimal digit encodes the **direction to dig**: `0` means `R`, `1` means `D`, `2` means `L`, and `3` means `U`.

So, in the above example, the hexadecimal codes can be converted into the true instructions:

 - `#70c710` = `R 461937`
 - `#0dc571` = `D 56407`
 - `#5713f0` = `R 356671`
 - `#d2c081` = `D 863240`
 - `#59c680` = `R 367720`
 - `#411b91` = `D 266681`
 - `#8ceee2` = `L 577262`
 - `#caa173` = `U 829975`
 - `#1b58a2` = `L 112010`
 - `#caa171` = `D 829975`
 - `#7807d2` = `L 491645`
 - `#a77fa3` = `U 686074`
 - `#015232` = `L 5411`
 - `#7a21e3` = `U 500254`

Digging out this loop and its interior produces a lagoon that can hold an impressive **`952408144115`** cubic meters of lava.

Convert the hexadecimal color codes into the correct instructions; if the Elves follow this new dig plan, **how many cubic meters of lava could the lagoon hold?**

### [--- Solution ---](day-18.py)
```Python
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
```