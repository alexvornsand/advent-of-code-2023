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