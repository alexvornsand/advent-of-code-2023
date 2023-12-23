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