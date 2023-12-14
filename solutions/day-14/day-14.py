# advent of code 2023
# day 14

file = 'input.txt'

class RockMap:
    def __init__(self, map, rocks):
        self.map = {coord: rocks.index(coord) if coord in rocks else map[coord] for coord in map}
        self.original_map = self.map.copy()
        self.rocks = rocks.copy()
        self.original_rocks = rocks.copy()
        self.history = []

    def neighbor(self, coord, dir):
        x, y = coord
        if dir == 'N':
            return (x, y - 1)
        if dir == 'E':
            return (x + 1, y)
        if dir == 'S':
            return (x, y + 1)
        if dir == 'W':
            return (x - 1, y)
        
    def printMap(self, anonymous=True):
        map = {key: 'O' if str(self.map[key]).isdigit() else self.map[key] for key in self.map} if anonymous else self.map
        max_lenght = max([len(str(val)) for val in map.values()])
        x_min = min([coord[0] for coord in self.map])
        x_max = max([coord[0] for coord in self.map])
        y_min = min([coord[1] for coord in self.map])
        y_max = max([coord[1] for coord in self.map])
        image = ''
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                if (x, y) in self.map:
                    image += str(map[(x, y)]).rjust(max_lenght, ' ')
                else:
                    image += ' '
            image += '\n'
        print(image)

    def calculateWeight(self, rocks):
        y_max = max([coord[1] for coord in self.map])
        return sum([y_max + 1 - rock[1] for rock in rocks])
    
    def summarizeMap(self):
        return [coord for coord in self.map if str(self.map[coord]).isdigit()]

    def tilt(self, dir):
        movable_rocks = [rock for rock in self.rocks if self.neighbor(rock, dir) in self.map and self.map[self.neighbor(rock, dir)] == '.']
        while len(movable_rocks) > 0:
            while len(movable_rocks) > 0:
                rock_coord = movable_rocks[0]
                movable_rocks.remove(rock_coord)
                rock_id = self.rocks.index(rock_coord)
                neighbor = self.neighbor(rock_coord, dir)
                self.map[rock_coord] = '.'
                while neighbor in self.map and self.map[neighbor] == '.':
                    current_rock = neighbor
                    neighbor = self.neighbor(current_rock, dir)
                self.map[current_rock] = rock_id
                self.rocks[rock_id] = current_rock
            movable_rocks = [rock for rock in self.rocks if self.neighbor(rock, dir) in self.map and self.map[self.neighbor(rock, dir)] == '.']

    def spin(self):
        self.tilt('N')
        self.tilt('W')
        self.tilt('S')
        self.tilt('E')

    def spinCycle(self):
        self.map = self.original_map.copy()
        self.rocks = self.original_rocks.copy()
        self.history.append(self.summarizeMap())
        i = 0
        while True:
            i += 1
            self.spin()
            state = self.summarizeMap()
            if state in self.history:
                break
            self.history.append(state.copy())
        cycle_start = self.history.index(state)
        cycle_end = i
        cycle_lenght = cycle_end - cycle_start
        return self.history[cycle_start + ((1000000000 - cycle_start) % cycle_lenght)]

def part_1(rockMap):
    rockMap.tilt('N')
    print('Part 1:', rockMap.calculateWeight(rockMap.rocks))

def part_2(rockMap):
    print('Part 2:', rockMap.calculateWeight(rockMap.spinCycle()))

def main():
    map_grid = [[char for char in row] for row in open(file, 'r').read().splitlines()]
    map = {(c, r): '#' if map_grid[r][c] == '#' else '.' for r in range(len(map_grid)) for c in range(len(map_grid[r]))}
    rocks = [(c, r) for r in range(len(map_grid)) for c in range(len(map_grid[r])) if map_grid[r][c] == 'O']
    rockMap = RockMap(map, rocks)
    part_1(rockMap)
    part_2(rockMap)

if __name__ == '__main__':
    main()