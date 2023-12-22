### [--- Day 21: Step Counter ---](https://adventofcode.com/2023/day/21)

You manage to catch the [airship](https://adventofcode.com/2023/day/7) right as it's dropping someone else off on their all-expenses-paid trip to Desert Island! It even helpfully drops you off near the [gardener](https://adventofcode.com/2023/day/5) and his massive farm.

"You got the sand flowing again! Great work! Now we just need to wait until we have enough sand to filter the water for Snow Island and we'll have snow again in no time."

While you wait, one of the Elves that works with the gardener heard how good you are at solving problems and would like your help. He needs to get his [steps](https://en.wikipedia.org/wiki/Pedometer) in for the day, and so he'd like to know which garden plots he can reach with exactly his remaining 64 steps.

He gives you an up-to-date map (your puzzle input) of his starting position (`S`), garden plots (`.`), and rocks (`#`). For example:

```
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
```

The Elf starts at the starting position (`S`) which also counts as a garden plot. Then, he can take one step north, south, east, or west, but only onto tiles that are garden plots. This would allow him to reach any of the tiles marked `O`:

```
...........
.....###.#.
.###.##..#.
..#.#...#..
....#O#....
.##.OS####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
```

Then, he takes a second step. Since at this point he could be at **either** tile marked `O`, his second step would allow him to reach any garden plot that is one step north, south, east, or west of **any** tile that he could have reached after the first step:

```
...........
.....###.#.
.###.##..#.
..#.#O..#..
....#.#....
.##O.O####.
.##.O#...#.
.......##..
.##.#.####.
.##..##.##.
...........
```

After two steps, he could be at any of the tiles marked `O` above, including the starting position (either by going north-then-south or by going west-then-east).

A single third step leads to even more possibilities:

```
...........
.....###.#.
.###.##..#.
..#.#.O.#..
...O#O#....
.##.OS####.
.##O.#...#.
....O..##..
.##.#.####.
.##..##.##.
...........
```

He will continue like this until his steps for the day have been exhausted. After a total of `6` steps, he could reach any of the garden plots marked `O`:

```
...........
.....###.#.
.###.##.O#.
.O#O#O.O#..
O.O.#.#.O..
.##O.O####.
.##.O#O..#.
.O.O.O.##..
.##.#.####.
.##O.##.##.
...........
```

In this example, if the Elf's goal was to get exactly `6` more steps today, he could use them to reach any of **`16`** garden plots.

However, the Elf **actually needs to get 64 steps today**, and the map he's handed you is much larger than the example map.

Starting from the garden plot marked `S` on your map, **how many garden plots could the Elf reach in exactly `64` steps?**

### --- Part Two ---

The Elf seems confused by your answer until he realizes his mistake: he was reading from a list of his favorite numbers that are both perfect squares and perfect cubes, not his step counter.

The **actual** number of steps he needs to get today is exactly **`26501365`**.

He also points out that the garden plots and rocks are set up so that the map **repeats infinitely** in every direction.

So, if you were to look one additional map-width or map-height out from the edge of the example map above, you would find that it keeps repeating:

```
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##..S####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
```

This is just a tiny three-map-by-three-map slice of the inexplicably-infinite farm layout; garden plots and rocks repeat as far as you can see. The Elf still starts on the one middle tile marked `S`, though - every other repeated `S` is replaced with a normal garden plot (`.`).

Here are the number of reachable garden plots in this new infinite version of the example map for different numbers of steps:

 - In exactly `6` steps, he can still reach **`16`** garden plots.
 - In exactly `10` steps, he can reach any of **`50`** garden plots.
 - In exactly `50` steps, he can reach **`1594`** garden plots.
 - In exactly `100` steps, he can reach **`6536`** garden plots.
 - In exactly `500` steps, he can reach **`167004`** garden plots.
 - In exactly `1000` steps, he can reach **`668697`** garden plots.
 - In exactly `5000` steps, he can reach **`16733044`** garden plots.

However, the step count the Elf needs is much larger! Starting from the garden plot marked S on your infinite map, **how many garden plots could the Elf reach in exactly `26501365` steps?**

### [--- Solution ---](day-21.py)
```Python
# advent of code 2023
# day 21

from collections import defaultdict

file = 'input.txt'

class GardenMaze:
    def __init__(self, maze):
        self.maze = maze
        self.starting_position = [(x, y) for y in range(len(self.maze)) for x in range(len(self.maze[y])) if self.maze[y][x] == 'S'][0]
        self.maze[self.starting_position[1]][self.starting_position[0]] = '.'

    def navigateSmallMaze(self, start, s=64):
        neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        end = (len(self.maze[0]), len(self.maze))
        queue = [start]
        visited_nodes = set()
        distances = defaultdict(lambda: 999999)
        distances[start] = 0
        while queue:
            x, y = queue.pop(0)      
            for dx, dy in neighbors:
                if 0 <= x + dx < end[0] and 0 <= y + dy < end[1]:
                    if self.maze[y + dy][x + dx] != '#' and (x + dx, y + dy) not in visited_nodes:
                        distances[(x + dx, y + dy)] = min(distances[(x + dx, y + dy)], distances[(x, y)] + 1)
                        if (x + dx, y + dy) not in queue:
                            queue.append((x + dx, y + dy))
            visited_nodes.add((x, y))
        return sum([distances[key] <= s and (distances[key] % 2) == (s % 2) for key in distances])
    
    def navigateMaze(self, s=64):
        w, h = (len(self.maze[0]), len(self.maze))
        c = self.starting_position[0]
        n = (s - c) / w
        odds = self.navigateSmallMaze(self.starting_position, 2 * w + 1)
        evens = self.navigateSmallMaze(self.starting_position, 2 * w)
        inner_diagonals = (
            self.navigateSmallMaze((0, 0), w + c - 1),
            self.navigateSmallMaze((0, h - 1), w + c - 1),
            self.navigateSmallMaze((w - 1, 0), w + c - 1),
            self.navigateSmallMaze((w - 1, h - 1), w + c - 1)
        )
        outer_diagonals = (
            self.navigateSmallMaze((0, 0), c - 1),
            self.navigateSmallMaze((0, h - 1), c - 1),
            self.navigateSmallMaze((w - 1, 0), c - 1),
            self.navigateSmallMaze((w - 1, h - 1), c - 1)
        )
        caps = (
            self.navigateSmallMaze((c, h - 1), w - 1),
            self.navigateSmallMaze((0, c), w - 1),
            self.navigateSmallMaze((c, 0), w - 1),
            self.navigateSmallMaze((w - 1, c), w - 1)
        )
        return int((((n - 1) ** 2) * odds) + ((n ** 2) * evens) + ((n - 1) * sum(inner_diagonals)) + (n * sum(outer_diagonals)) + sum(caps))

def part_1(gardenMaze):
    print('Part 1:', gardenMaze.navigateSmallMaze(gardenMaze.starting_position))

def part_2(gardenMaze):
    print('Part 2:', gardenMaze.navigateMaze(26501365))

def main():
    maze = [[x for x in line] for line in open(file, 'r').read().splitlines()]
    gardenMaze = GardenMaze(maze)
    part_1(gardenMaze)
    part_2(gardenMaze)

if __name__ == '__main__':
    main()
```