# advent of code 2023
# day 17

from heapq import heappop, heappush

file = 'input.txt'

class LavaMaze:
    def __init__(self, maze):
        self.maze = maze

    def findMinimumPath(self, min_step=0, max_step=3):
        end = [len(self.maze[0]) - 1, len(self.maze) - 1]
        queue = [(0, 0, 0, 0, 1, 0), (0, 0, 0, 1, 0, 0)] 
        visited = set()
        while queue:
            d, x, y, dx, dy, s = heappop(queue)
            if x == end[0] and y == end[1]:
                if s >= min_step:
                    break
                continue
            if (x, y, dx, dy, s) in visited:
                continue    
            visited.add((x, y, dx, dy, s))
            if s < max_step:
                if 0 <= x + dx <= end[0] and 0 <= y + dy <= end[1]:
                    heappush(queue, (d + self.maze[y + dy][x + dx], x + dx, y + dy, dx, dy, s + 1))
            if s >= min_step:
                if 0 <= x + dy <= end[0] and 0 <= y + dx <= end[1]:
                    heappush(queue, (d + self.maze[y + dx][x + dy], x + dy, y + dx, dy, dx, 1))
                if 0 <= x - dy <= end[0] and 0 <= y - dx <= end[1]:
                    heappush(queue, (d + self.maze[y - dx][x - dy], x - dy, y - dx, -dy, -dx, 1))
        return d

def part_1(lavaMaze):
    print('Part 1:', lavaMaze.findMinimumPath())

def part_2(lavaMaze):
    print('Part 2:', lavaMaze.findMinimumPath(4, 10))

def main():
    maze = [[int(x) for x in row] for row in open(file, 'r').read().splitlines()]
    lavaMaze = LavaMaze(maze)
    part_1(lavaMaze)
    part_2(lavaMaze)
