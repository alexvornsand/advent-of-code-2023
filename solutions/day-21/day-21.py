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