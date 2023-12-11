### [--- Day 11: Cosmic Expansion ---](https://adventofcode.com/2023/day/11)

You continue following signs for "Hot Springs" and eventually come across an [observatory](https://en.wikipedia.org/wiki/Observatory). The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.

Maybe you can help him with the analysis to speed things up?

The researcher has collected a bunch of data and compiled the data into a single giant **image** (your puzzle input). The image includes **empty space** (`.`) and **galaxies** `(#).` For example:

```
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
```

The researcher is trying to figure out the sum of the lengths of the **shortest path between every pair of galaxies**. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact, the result is that **any rows or columns that contain no galaxies** should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

```
   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^
```

These rows and columns need to be **twice as big**; the result of cosmic expansion therefore looks like this:

```
....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
```

Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

```
....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......
```

In these 9 galaxies, there are **36 pairs**. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one `.` or `#` at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies `5` and `9`:

```
....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......
```

This path has length **`9`** because it takes a minimum of **nine steps** to get from galaxy `5` to galaxy `9` (the eight locations marked #`plus the step onto galaxy `9` itself). Here are some other example shortest path lengths:

 - Between galaxy `1` and galaxy `7`: `15`
 - Between galaxy `3` and galaxy `6`: `17`
 - Between galaxy `8` and galaxy `9`: `5`

In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is **`374`**.

Expand the universe, then find the length of the shortest path between every pair of galaxies. **What is the sum of these lengths?**

### --- Part Two ---

The galaxies are much **older** (and thus much **farther apart**) than the researcher initially estimated.

Now, instead of the expansion you did before, make each empty row or column **one million times** larger. That is, each empty row should be replaced with `1000000` empty rows, and each empty column should be replaced with `1000000` empty columns.

(In the example above, if each empty row or column were merely `10` times larger, the sum of the shortest paths between every pair of galaxies would be **`1030`**. If each empty row or column were merely `100` times larger, the sum of the shortest paths between every pair of galaxies would be **`8410`**. However, your universe will need to expand far beyond these values.)

Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. *What is the sum of these lengths?*

### [--- Solution ---](day-11.py)

```Python
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
```