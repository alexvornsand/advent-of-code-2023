# advent of code 2023
# day 10

file = 'input.txt'

class Labyrinth:
    def __init__(self, grid):
        self.map = {(c, r): grid[r][c] for r in range(len(grid)) for c in range(len(grid[r]))}
        self.start = [(c, r) for r in range(len(grid)) for c in range(len(grid[r])) if grid[r][c] == 'S'][0]
        self.loop = []

    def findNeighbors(self, coord):
        x, y = coord
        shape = self.map[coord]
        neighbors = []
        if (x + 1, y) in self.map and self.map[(x + 1, y)] in ('7', 'J', '-', 'S') and shape in ('L', 'F', '-', 'S'):
            neighbors.append((x + 1, y))
        if (x - 1, y) in self.map and self.map[(x - 1, y)] in ('L', 'F', '-', 'S') and shape in ('7', 'J', '-', 'S'):
            neighbors.append((x - 1, y))
        if (x, y + 1) in self.map and self.map[(x, y + 1)] in ('L', 'J', '|', 'S') and shape in ('7', 'F', '|', 'S'):
            neighbors.append((x, y + 1))
        if (x, y - 1) in self.map and self.map[(x, y - 1)] in ('7', 'F', '|', 'S') and shape in ('L', 'J', '|', 'S'):
            neighbors.append((x, y - 1))
        return neighbors
    
    def printMap(self, loop):
        x_min = min([coord[0] for coord in loop])
        x_max = max([coord[0] for coord in loop])
        y_min = min([coord[1] for coord in loop])
        y_max = max([coord[1] for coord in loop])
        image = ''
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                if (x, y) in loop:
                    image += self.map[(x, y)]
                else:
                    image += ' '
            image += '\n'
        print(image)

    def checkInterior(self, coord):
        x, y = coord
        right_neighbors = ''.join([self.map[(c, y)] for c in range(x, max([coord[0] for coord in self.map]) + 1) if self.map[(c, y)] in ['F', 'J', 'L', '7', '|']])
        right_neighbors = right_neighbors.replace('F7', '').replace('LJ', '')
        return (right_neighbors.count('|') + right_neighbors.count('7') + right_neighbors.count('J')) % 2 == 1

    def countInnerTiles(self):
        empty_tiles = [coord for coord in self.map if self.map[coord] == '.']
        return sum([self.checkInterior(tile) for tile in empty_tiles])

    def findLoop(self):
        for loop_direction in self.findNeighbors(self.start):
            loop = [self.start, loop_direction]
            current_node = loop_direction
            previous_node = self.start
            while current_node != self.start:
                neighbors = [neighbor for neighbor in self.findNeighbors(current_node) if neighbor != previous_node]
                if len(neighbors) == 0:
                    break
                else:
                    neighbor = neighbors[0]
                    loop.append(neighbor)
                    previous_node = current_node
                    current_node = neighbor
            self.loop = loop
            self.map = {key: self.map[key] if key in self.loop else '.' for key in self.map}
            last = tuple(x - y for x, y in zip(self.loop[0], self.loop[-2]))
            first = tuple(x - y for x, y in zip(self.loop[0], self.loop[1]))
            if (first, last) in [((1, 0), (0, -1)), ((0, -1), (-1, 0))]:
                self.map[self.start] = '7'
            elif (first, last) in [((1, 0), (-1, 0)), ((-1, 0), (1, 0))]:
                self.map[self.start] = '-'
            elif (first, last) in [((1, 0), (0, 1)), ((0, 1), (1, 0))]:
                self.map[self.start] = 'J'
            elif (first, last) in [((-1, 0), (0, -1)), ((0, -1), (-1, 0))]:
                self.map[self.start] = 'F'
            elif (first, last) in [((-1, 0), (0, 1)), ((0, 1), (-1, 0))]:
                self.map[self.start] = 'L'
            elif (first, last) in [((0, -1), (0, 1)), ((0, 1), (0, -1))]:
                self.map[self.start] = '|'
            break

def part_1(labyrinth):
    print('Part 1:', len(labyrinth.loop) // 2)

def part_2(labyrinth):
    print('Part 2:', labyrinth.countInnerTiles())

def main():
    grid = [[x for x in line] for line in open(file, 'r').read().splitlines()]
    labyrinth = Labyrinth(grid)
    labyrinth.findLoop()
    part_1(labyrinth)
    part_2(labyrinth)

if __name__ == '__main__':
    main()
