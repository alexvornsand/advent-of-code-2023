### [--- Day 16: The Floor Will Be Lava ---](https://adventofcode.com/2023/day/16)

With the beam of light completely focused **somewhere**, the reindeer leads you deeper still into the Lava Production Facility. At some point, you realize that the steel facility walls have been replaced with cave, and the doorways are just cave, and the floor is cave, and you're pretty sure this is actually just a giant cave.

Finally, as you approach what must be the heart of the mountain, you see a bright light in a cavern up ahead. There, you discover that the beam of light you so carefully focused is emerging from the cavern wall closest to the facility and pouring all of its energy into a contraption on the opposite side.

Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing **empty space** (`.`), **mirrors** (`/` and `\`), and **splitters** (`|` and `-`).

The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of the beam's light into **heat** to melt the rock in the cavern.

You note the layout of the contraption (your puzzle input). For example:

```
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
```

The beam enters in the top-left corner from the left and heading to the **right**. Then, its behavior depends on what it encounters as it moves:

 - If the beam encounters **empty space** (`.`), it continues in the same direction.
 - If the beam encounters a **mirror** (`/` or `\`), the beam is reflected 90 degrees depending on the angle of the mirror. For instance, a rightward-moving beam that encounters a `/` mirror would continue **upward** in the mirror's column, while a rightward-moving beam that encounters a `\` mirror would continue **downward** from the mirror's column.
 - If the beam encounters the **pointy end of a splitter** (`|` or `-`), the beam passes through the splitter as if the splitter were **empty space**. For instance, a rightward-moving beam that encounters a `-` splitter would continue in the same direction.
 - If the beam encounters the **flat side of a splitter** (`|` or `-`), the beam is **split into two beams** going in each of the two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a `|` splitter would split into two beams: one that continues **upward** from the splitter's column and one that continues **downward** from the splitter's column.

Beams do not interact with other beams; a tile can have many beams passing through it at the same time. A tile is **energized** if that tile has at least one beam pass through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the contraption:

```
>|<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..
```

Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead. Here is the same diagram but instead only showing whether a tile is **energized** (`#`) or not (`.`):

```
######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..
```

Ultimately, in this example, **`46`** tiles become **energized**.

The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the current situation. With the beam starting in the top-left heading right, **how many tiles end up being energized?**

### --- Part Two ---

As you try to work out what might be wrong, the reindeer tugs on your shirt and leads you to a nearby control panel. There, a collection of buttons lets you align the contraption so that the beam enters from **any edge tile** and heading away from that edge. (You can choose either of two directions for the beam if it starts on a corner; for instance, if the beam starts in the bottom-right corner, it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), any tile in the bottom row (heading upward), any tile in the leftmost column (heading right), or any tile in the rightmost column (heading left). To produce lava, you need to find the configuration that **energizes as many tiles as possible**.

In the above example, this can be achieved by starting the beam in the fourth tile from the left in the top row:

```
.|<2<\....
|v-v\^....
.v.v.|->>>
.v.v.v^.|.
.v.v.v^...
.v.v.v^..\
.v.v/2\\..
<-2-/vv|..
.|<<<2-|.\
.v//.|.v..
```

Using this configuration, **`51`** tiles are energized:

```
.#####....
.#.#.#....
.#.#.#####
.#.#.##...
.#.#.##...
.#.#.##...
.#.#####..
########..
.#######..
.#...#.#..
```

Find the initial beam configuration that energizes the largest number of tiles; **how many tiles are energized in that configuration?**

### [--- Solution --- ](day-16.py)
```Python
# advent of code 2023
# day 16

file = 'input.txt'

class LaserGame:
    def __init__(self, map):
        self.map = map
        self.energized_positions = set()
        self.cache = []

    def neighbor(self, position, direction):
        x, y = position
        if direction == 'N':
            return (x, y - 1)
        elif direction == 'E':
            return (x + 1, y)
        elif direction == 'S':
            return (x, y + 1)
        else:
            return (x - 1, y)

    def printMap(self):
        x_min = min([key[0] for key in self.map])
        x_max = max([key[0] for key in self.map])
        y_min = min([key[1] for key in self.map])
        y_max = max([key[1] for key in self.map])
        image = ''
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                if (x, y) in self.energized_positions:
                    image += '#'
                else:
                    image += self.map[(x, y)]
            image += '\n'
        print(image)

    def laserMovement(self, position, direction):
        if (position, direction) in self.cache:
            return []
        else:
            self.cache.append((position, direction))
        neighbor = self.neighbor(position, direction)
        next_positions = []
        if neighbor in self.map:
            self.energized_positions.add(neighbor)
            if self.map[neighbor] == '.':
                next_positions.append([neighbor, direction])
            elif direction == 'E':
                if self.map[neighbor] == '-':
                    next_positions.append([neighbor, direction])
                elif self.map[neighbor] == '/':
                    next_positions.append([neighbor, 'N'])
                elif self.map[neighbor] == '\\':
                    next_positions.append([neighbor, 'S'])
                elif self.map[neighbor] == '|':
                    next_positions.append([neighbor, 'N'])
                    next_positions.append([neighbor, 'S'])
            elif direction == 'S':
                if self.map[neighbor] == '|':
                    next_positions.append([neighbor, direction])
                elif self.map[neighbor] == '/':
                    next_positions.append([neighbor, 'W'])
                elif self.map[neighbor] == '\\':
                    next_positions.append([neighbor, 'E'])
                elif self.map[neighbor] == '-':
                    next_positions.append([neighbor, 'W'])
                    next_positions.append([neighbor, 'E'])
            elif direction == 'W':
                if self.map[neighbor] == '-':
                    next_positions.append([neighbor, direction])
                elif self.map[neighbor] == '/':
                    next_positions.append([neighbor, 'S'])
                elif self.map[neighbor] == '\\':
                    next_positions.append([neighbor, 'N'])
                elif self.map[neighbor] == '|':
                    next_positions.append([neighbor, 'N'])
                    next_positions.append([neighbor, 'S'])
            else:
                if self.map[neighbor] == '|':
                    next_positions.append([neighbor, direction])
                elif self.map[neighbor] == '/':
                    next_positions.append([neighbor, 'E'])
                elif self.map[neighbor] == '\\':
                    next_positions.append([neighbor, 'W'])
                elif self.map[neighbor] == '-':
                    next_positions.append([neighbor, 'E'])
                    next_positions.append([neighbor, 'W'])
        return [p  for pos in next_positions for p in self.laserMovement(pos[0], pos[1])]
    
    def shootLaser(self, start, direction):
        self.cache = []
        self.energized_positions = set()
        self.laserMovement(start, direction)
        return len(self.energized_positions)
    
    def optimizeLaser(self):
        x_min = min([key[0] for key in self.map])
        x_max = max([key[0] for key in self.map])
        y_min = min([key[1] for key in self.map])
        y_max = max([key[1] for key in self.map])
        max_along_x = max([self.shootLaser((x, -1), 'S') for x in range(x_min, x_max + 1)])
        max_along_y = max([self.shootLaser((-1, y), 'E') for y in range(y_min, y_max + 1)])
        return max(max_along_x, max_along_y)

def part_1(laserGame):
    print('Part 1:', laserGame.shootLaser((-1, 0), 'E'))
    
def part_2(laserGame):
    print('Part 2:', laserGame.optimizeLaser())
    
def main():
    map_grid = [[char for char in line] for line in open(file, 'r').read().splitlines()]
    map = {(c, r): map_grid[r][c] for r in range(len(map_grid)) for c in range(len(map_grid[r]))}
    laserGame = LaserGame(map)
    part_1(laserGame)
    part_2(laserGame)
    
if __name__ == '__main__':
    main()
```