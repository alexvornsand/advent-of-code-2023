### --- Day 14: Parabolic Reflector Dish ---

You reach the place where all of the mirrors were pointing: a massive [parabolic reflector dish](https://en.wikipedia.org/wiki/Parabolic_reflector) attached to the side of another large mountain.

The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the dish is meant to focus light, all it's doing right now is sending it in a vague direction.

This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go where it's pointing and use the light to fix the lava production.

Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. Depending on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes move and ultimately the focus of the dish.

In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets you **tilt** it in one of four directions! The rounded rocks (`O`) will roll when the platform is tilted, while the cube-shaped rocks (`#`) will stay in place. You note the positions of all of the empty spaces (`.`) and rocks (your puzzle input). For example:

```
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
```

Start by tilting the lever so all of the rocks will slide **north** as far as they will go:

```
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
```

You notice that the support beams along the north side of the platform are **damaged**; to ensure the platform doesn't collapse, you should calculate the **total load** on the north support beams.

The amount of load caused by a single rounded rock (`O`) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (`#`) don't contribute to load.) So, the amount of load caused by each rock in each row is as follows:

```
OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1
```

The total load is the sum of the load caused by all of the **rounded rocks**. In this example, the total load is **`136`**.

Tilt the platform so that the rounded rocks all roll north. Afterward, **what is the total load on the north support beams?**

### --- Part Two ---

The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, you'll need to move the rocks to the edges of the platform. Fortunately, a button on the side of the control panel labeled "spin cycle" attempts to do just that!

Each cycle tilts the platform four times so that the rounded rocks roll **north**, then **west**, then **south**, then **east**. After each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction. After one cycle, the platform will have finished rolling the rounded rocks in those four directions in that order.

Here's what happens in the example above after each of the first few cycles:

```
After 1 cycle:
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

After 2 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

After 3 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
```

This process should work if you leave it running long enough, but you're still worried about the north support beams. To make sure they'll survive for a while, you need to calculate the **total load** on the north support beams after `1000000000` cycles.

In the above example, after `1000000000` cycles, the total load on the north support beams is **`64`**.

Run the spin cycle for `1000000000` cycles. Afterward, **what is the total load on the north support beams?**

### [--- Solution ---](day-14.py)

```Python
# advent of code 2023
# day 14

file = 'input.txt'

class RockMap:
    def __init__(self, map, rocks):
        self.map = {coord: rocks.index(coord) if coord in rocks else map[coord] for coord in map}
        self.original_map = self.map.copy()
        self.rocks = rocks.copy()
        self.original_rocks = rocks.copy()
        self.history = []

    def neighbor(self, coord, dir):
        x, y = coord
        if dir == 'N':
            return (x, y - 1)
        if dir == 'E':
            return (x + 1, y)
        if dir == 'S':
            return (x, y + 1)
        if dir == 'W':
            return (x - 1, y)
        
    def printMap(self, anonymous=True):
        map = {key: 'O' if str(self.map[key]).isdigit() else self.map[key] for key in self.map} if anonymous else self.map
        max_lenght = max([len(str(val)) for val in map.values()])
        x_min = min([coord[0] for coord in self.map])
        x_max = max([coord[0] for coord in self.map])
        y_min = min([coord[1] for coord in self.map])
        y_max = max([coord[1] for coord in self.map])
        image = ''
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                if (x, y) in self.map:
                    image += str(map[(x, y)]).rjust(max_lenght, ' ')
                else:
                    image += ' '
            image += '\n'
        print(image)

    def calculateWeight(self, rocks):
        y_max = max([coord[1] for coord in self.map])
        return sum([y_max + 1 - rock[1] for rock in rocks])
    
    def summarizeMap(self):
        return [coord for coord in self.map if str(self.map[coord]).isdigit()]

    def tilt(self, dir):
        movable_rocks = [rock for rock in self.rocks if self.neighbor(rock, dir) in self.map and self.map[self.neighbor(rock, dir)] == '.']
        while len(movable_rocks) > 0:
            while len(movable_rocks) > 0:
                rock_coord = movable_rocks[0]
                movable_rocks.remove(rock_coord)
                rock_id = self.rocks.index(rock_coord)
                neighbor = self.neighbor(rock_coord, dir)
                self.map[rock_coord] = '.'
                while neighbor in self.map and self.map[neighbor] == '.':
                    current_rock = neighbor
                    neighbor = self.neighbor(current_rock, dir)
                self.map[current_rock] = rock_id
                self.rocks[rock_id] = current_rock
            movable_rocks = [rock for rock in self.rocks if self.neighbor(rock, dir) in self.map and self.map[self.neighbor(rock, dir)] == '.']

    def spin(self):
        self.tilt('N')
        self.tilt('W')
        self.tilt('S')
        self.tilt('E')

    def spinCycle(self):
        self.map = self.original_map.copy()
        self.rocks = self.original_rocks.copy()
        self.history.append(self.summarizeMap())
        i = 0
        while True:
            i += 1
            self.spin()
            state = self.summarizeMap()
            if state in self.history:
                break
            self.history.append(state.copy())
        cycle_start = self.history.index(state)
        cycle_end = i
        cycle_lenght = cycle_end - cycle_start
        return self.history[cycle_start + ((1000000000 - cycle_start) % cycle_lenght)]

def part_1(rockMap):
    rockMap.tilt('N')
    print('Part 1:', rockMap.calculateWeight(rockMap.rocks))

def part_2(rockMap):
    print('Part 2:', rockMap.calculateWeight(rockMap.spinCycle()))

def main():
    map_grid = [[char for char in row] for row in open(file, 'r').read().splitlines()]
    map = {(c, r): '#' if map_grid[r][c] == '#' else '.' for r in range(len(map_grid)) for c in range(len(map_grid[r]))}
    rocks = [(c, r) for r in range(len(map_grid)) for c in range(len(map_grid[r])) if map_grid[r][c] == 'O']
    rockMap = RockMap(map, rocks)
    part_1(rockMap)
    part_2(rockMap)

if __name__ == '__main__':
    main()
```