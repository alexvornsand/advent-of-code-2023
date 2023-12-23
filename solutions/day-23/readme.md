### [--- Day 23: A Long Walk ---](https://adventofcode.com/2023/day/23)

The Elves resume water filtering operations! Clean water starts flowing over the edge of Island Island.

They offer to help **you** go over the edge of Island Island, too! Just hold on tight to one end of this impossibly long rope and they'll lower you down a safe distance from the massive waterfall you just created.

As you finally reach Snow Island, you see that the water isn't really reaching the ground: it's being **absorbed by the air** itself. It looks like you'll finally have a little downtime while the moisture builds up to snow-producing levels. Snow Island is pretty scenic, even without any snow; why not take a walk?

There's a map of nearby hiking trails (your puzzle input) that indicates **paths** (`.`), **forest** (`#`), and steep **slopes** (`^`, `>`, `v`, and `<`).

For example:

```
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
```

You're currently on the single path tile in the top row; your goal is to reach the single path tile in the bottom row. Because of all the mist from the waterfall, the slopes are probably quite **icy**; if you step onto a slope tile, your next step must be **downhill** (in the direction the arrow is pointing). To make sure you have the most scenic hike possible, **never step onto the same tile twice**. What is the longest hike you can take?

In the example above, the longest hike you can take is marked with `O`, and your starting position is marked `S`:

```
#S#####################
#OOOOOOO#########...###
#######O#########.#.###
###OOOOO#OOO>.###.#.###
###O#####O#O#.###.#.###
###OOOOO#O#O#.....#...#
###v###O#O#O#########.#
###...#O#O#OOOOOOO#...#
#####.#O#O#######O#.###
#.....#O#O#OOOOOOO#...#
#.#####O#O#O#########v#
#.#...#OOO#OOO###OOOOO#
#.#.#v#######O###O###O#
#...#.>.#...>OOO#O###O#
#####v#.#.###v#O#O###O#
#.....#...#...#O#O#OOO#
#.#########.###O#O#O###
#...###...#...#OOO#O###
###.###.#.###v#####O###
#...#...#.#.>.>.#.>O###
#.###.###.#.###.#.#O###
#.....###...###...#OOO#
#####################O#
```

This hike contains **`94`** steps. (The other possible hikes you could have taken were `90`, `86`, `82`, `82`, and `74` steps long.)

Find the longest hike you can take through the hiking trails listed on your map. **How many steps long is the longest hike?**

### --- Part Two ---

As you reach the trailhead, you realize that the ground isn't as slippery as you expected; you'll have **no problem** climbing up the steep slopes.

Now, treat all **slopes** as if they were normal **paths** (`.`). You still want to make sure you have the most scenic hike possible, so continue to ensure that you **never step onto the same tile twice**. What is the longest hike you can take?

In the example above, this increases the longest hike to **`154`** steps:

```
#S#####################
#OOOOOOO#########OOO###
#######O#########O#O###
###OOOOO#.>OOO###O#O###
###O#####.#O#O###O#O###
###O>...#.#O#OOOOO#OOO#
###O###.#.#O#########O#
###OOO#.#.#OOOOOOO#OOO#
#####O#.#.#######O#O###
#OOOOO#.#.#OOOOOOO#OOO#
#O#####.#.#O#########O#
#O#OOO#...#OOO###...>O#
#O#O#O#######O###.###O#
#OOO#O>.#...>O>.#.###O#
#####O#.#.###O#.#.###O#
#OOOOO#...#OOO#.#.#OOO#
#O#########O###.#.#O###
#OOO###OOO#OOO#...#O###
###O###O#O###O#####O###
#OOO#OOO#O#OOO>.#.>O###
#O###O###O#O###.#.#O###
#OOOOO###OOO###...#OOO#
#####################O#
```

Find the longest hike you can take through the surprisingly dry hiking trails listed on your map. **How many steps long is the longest hike?**

### [--- Solution ---](day-23.py)
```Python
# advent of code 2023
# day 23

from collections import defaultdict

file = 'input.txt'

class Maze:
    def __init__(self, maze):
        self.maze = maze
        self.starting_position = [(c, 0) for c in range(len(self.maze[0])) if self.maze[0][c] == '.'][0]
        self.ending_position = [(c, len(self.maze) - 1) for c in range(len(self.maze[0])) if self.maze[len(self.maze) - 1][c] == '.'][0]

    def navigateMaze(self, start, distance=0):
        m, n = (len(self.maze[0]), len(self.maze))
        x, y = start
        visited_nodes = set()
        while True:
            next_queue = []
            if 0 <= x + 1 < m and 0 <= y < n and self.maze[y][x + 1] == '.' and (x + 1, y) not in visited_nodes:
                next_queue.append(((x + 1, y), distance + 1))
            elif 0 <= x + 1 < m and 0 <= y < n and self.maze[y][x + 1] == '>' and (x + 1, y) not in visited_nodes:
                next_queue.append(((x + 2, y), distance + 2))
            if 0 <= x - 1 < m and 0 <= y < n and self.maze[y][x - 1] == '.' and (x - 1, y) not in visited_nodes:
                next_queue.append(((x - 1, y), distance + 1))
            elif 0 <= x - 1 < m and 0 <= y < n and self.maze[y][x - 1] == '<' and (x - 1, y) not in visited_nodes:
                next_queue.append(((x - 2, y), distance + 2))
            if 0 <= x < m and 0 <= y + 1 < n and self.maze[y + 1][x] == '.' and (x, y + 1) not in visited_nodes:
                next_queue.append(((x, y + 1), distance + 1))
            elif 0 <= x < m and 0 <= y + 1 < n and self.maze[y + 1][x] == 'v' and (x, y + 1) not in visited_nodes:
                next_queue.append(((x, y + 2), distance + 2))
            if 0 <= x < m and 0 <= y - 1 < n and self.maze[y - 1][x] == '.' and (x, y - 1) not in visited_nodes:
                next_queue.append(((x, y - 1), distance + 1))
            elif 0 <= x < m and 0 <= y - 1 < n and self.maze[y - 1][x] == '^' and (x, y - 1) not in visited_nodes:
                next_queue.append(((x, y - 2), distance + 2))
            visited_nodes.add((x, y))
            if (x, y) == self.ending_position:
                return distance
            if len(next_queue) == 0:
                return 0
            elif len(next_queue) == 1:
                (x, y), distance = next_queue.pop(0)
            else:
                return max([self.navigateMaze(*branch) for branch in next_queue])
            
    def buildGraph(self, debug=False):
        m, n = (len(self.maze[0]), len(self.maze))
        x, y = self.starting_position
        graph = defaultdict(lambda: defaultdict(lambda: 0))
        visited_nodes = set()
        node_queue = [self.starting_position]
        while node_queue:
            xi, yi = node_queue.pop()
            if debug: print('initital node:', (xi, yi))
            visited_nodes.add((xi, yi))
            for dxi, dyi in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if 0 <= xi + dxi < m and 0 <= yi + dyi < n and self.maze[yi + dyi][xi + dxi] != '#':
                    if debug: print('\tgoing through:', (xi + dxi, yi + dyi))
                    visited_tiles = set()
                    visited_tiles.add((xi, yi))
                    tile_queue = [((xi + dxi, yi + dyi), 1)]
                    distance = 0
                    while tile_queue:
                        (x, y), distance = tile_queue.pop(0)
                        if debug: print('\t\tat:', (x, y))
                        next_queue = []
                        visited_tiles.add((x, y))
                        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                            if 0 <= x + dx < m and 0 <= y + dy < n and self.maze[y + dy][x + dx] != '#' and (x + dx, y + dy) not in visited_tiles:
                                next_queue.append(((x + dx, y + dy), distance + 1))
                        if debug: print('\t\t\tneighbors:', next_queue)
                        if len(next_queue) == 1:
                            tile_queue = next_queue.copy()
                        else:
                            if debug: print('\tterminal node:', (x, y))
                            graph[(xi, yi)][(x, y)] = max(graph[(xi, yi)][(x, y)], distance)
                            if (x, y) not in node_queue and (x, y) not in visited_nodes:
                                node_queue.append((x, y))
        self.graph = graph
    
    def navigateSteepMaze(self, start, distance=0, visited_nodes = set()):
        queue = [(start, distance)]
        while queue:
            current_node, d = queue.pop()
            visited_nodes.add(current_node)
            if current_node == self.ending_position:
                return d
            else:
                neighbors = [key for key in self.graph[current_node] if key not in visited_nodes]
                if len(neighbors) > 0:
                    return max([self.navigateSteepMaze(neighbor, d + self.graph[current_node][neighbor], set([node for node in visited_nodes] + [neighbor])) for neighbor in neighbors])
                else:
                    return 0
def part_1(maze):
    print('Part 1:', maze.navigateMaze(maze.starting_position))

def part_2(maze):
    print('Part 2:', maze.navigateSteepMaze(maze.starting_position))

def main():
    grid = [[x for x in row] for row in open(file, 'r').read().splitlines()]
    maze = Maze(grid)
    maze.buildGraph()
    part_1(maze)
    part_2(maze)

if __name__ == '__main__':
    main()
```