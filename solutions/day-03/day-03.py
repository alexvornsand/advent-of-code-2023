# advent of code 2023
# day 3

file = 'input.txt'

class Engine:
    def __init__(self, engine_map):
        self.map = engine_map
        self.numbers = []
        self.gear_ratios = []

    def evaluateEngine(self):
        r = 0
        gears = {}
        while r < len(self.map):
            current_number = []
            current_gears = []
            valid_number = False
            c = 0
            while c < len(self.map[r]):
                if self.map[r][c].isdigit():
                    current_number.append(self.map[r][c])
                    for neighbor in [(r + 1, c + 1), (r + 1, c), (r + 1, c - 1), (r, c + 1), (r, c), (r, c - 1), (r - 1, c + 1), (r - 1, c), (r - 1, c - 1)]:
                        y, x = neighbor
                        if y in list(range(len(self.map))) and x in list(range(len(self.map[0]))) and self.map[y][x] != '.' and not self.map[y][x].isdigit():
                            valid_number = True
                            if self.map[y][x] == '*':
                                current_gears.append(neighbor)
                else:
                    if len(current_number) > 0 and valid_number:
                        self.numbers.append(int(''.join(current_number)))
                        for gear in list(set(current_gears)):
                            if gear in gears:
                                gears[gear].append(int(''.join(current_number)))
                            else:
                                gears[gear] = [int(''.join(current_number))]
                    valid_number = False
                    current_number = []
                    current_gears = []
                c += 1
            if len(current_number) > 0 and valid_number:
                self.numbers.append(int(''.join(current_number)))
                for gear in list(set(current_gears)):
                    if gear in gears:
                        gears[gear].append(int(''.join(current_number)))
                    else:
                        gears[gear] = [int(''.join(current_number))]
            valid_number = False
            current_number = []
            current_gears = []
            r += 1
        for gear in gears:
            if len(gears[gear]) == 2:
                self.gear_ratios.append(gears[gear][0] * gears[gear][1])

def part_1(engine):
    print('Part 1:', sum(engine.numbers))

def part_2(engine):
    print('Part 2:', sum(engine.gear_ratios))

def main():
    engine_map = [[chr for chr in line] for line in open(file, 'r').read().splitlines()]
    engine = Engine(engine_map)
    engine.evaluateEngine()
    part_1(engine)
    part_2(engine)

if __name__ == '__main__':
    main()