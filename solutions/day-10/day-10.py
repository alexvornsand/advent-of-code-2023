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

    def countInnerTiles(self):
        bridges = [tuple([(y + x) / 2 for y, x in zip(self.loop[i], self.loop[i + 1])]) for i in range(len(self.loop) - 1)]
        double_scale_loop = [tuple([c * 2 for c in coord]) for coord in self.loop + bridges]
        double_x_min = min([coord[0] for coord in double_scale_loop]) - 1
        double_x_max = max([coord[0] for coord in double_scale_loop]) + 1
        double_y_min = min([coord[1] for coord in double_scale_loop]) - 1
        double_y_max = max([coord[1] for coord in double_scale_loop]) + 1
        double_scale_exterior_tiles = []
        start = (double_x_min, double_y_min)
        x, y = start
        current_node = start
        queue = [
            neighbor 
            for neighbor 
            in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] 
            if 
                neighbor not in double_scale_exterior_tiles 
                    and neighbor not in double_scale_loop 
                    and neighbor[0] in range(double_x_min, double_x_max + 1) 
                    and neighbor[1] in range(double_y_min, double_y_max + 1)
        ]
        while len(queue) > 0:
            double_scale_exterior_tiles.append(current_node)
            current_node = queue[0]
            x, y = current_node
            queue.pop(0)
            queue += [
                neighbor 
                for neighbor 
                in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] 
                if 
                    neighbor not in double_scale_exterior_tiles 
                        and neighbor not in queue 
                        and neighbor not in double_scale_loop 
                        and neighbor[0] in range(double_x_min, double_x_max + 1) 
                        and neighbor[1] in range(double_y_min, double_y_max + 1)
            ]
        x_min = min([coord[0] for coord in self.loop])
        x_max = max([coord[0] for coord in self.loop])
        y_min = min([coord[1] for coord in self.loop])
        y_max = max([coord[1] for coord in self.loop])
        exterior_tiles = [
            (tile[0] / 2, tile[1] / 2) 
            for tile 
            in double_scale_exterior_tiles 
            if 
                tile[0] % 2 == 0 
                    and tile[1] % 2 == 0
                    and int(tile[0] / 2) in range(x_min, x_max + 1)
                    and int(tile[1] / 2) in range(y_min, y_max + 1)
        ]
        return (x_max - x_min + 1) * (y_max - y_min + 1) - len(exterior_tiles) - len(self.loop[:-1])

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
