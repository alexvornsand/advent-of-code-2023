### [--- Day 3: Gear Ratios ---](https://adventofcode.com/2023/day/3)

You and the Elf eventually reach a [gondola lift](https://en.wikipedia.org/wiki/Gondola_lift) station; he says the gondola lift will take you up to the **water source**, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can **add up all the part numbers** in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently **any number adjacent to a symbol**, even diagonally, is a "part number" and should be included in your sum. (Periods (`.`) do not count as a symbol.)

Here is an example engine schematic:

```
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
```

In this schematic, two numbers are **not** part numbers because they are not adjacent to a symbol: `114` (top right) and `58` (middle right). Every other number is adjacent to a symbol and so **is** a part number; their sum is **`4361`**.

Of course, the actual engine schematic is much larger. **What is the sum of all of the part numbers in the engine schematic?**

### --- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A **gear** is any `*` symbol that is adjacent to **exactly two part numbers**. Its **gear ratio** is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

```
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
```

In this schematic, there are **two** gears. The first is in the top left; it has part numbers `467` and `35`, so its gear ratio is `16345`. The second gear is in the lower right; its gear ratio is `451490`. (The `*` adjacent to `617` is **not** a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces **`467835`**.

**What is the sum of all of the gear ratios in your engine schematic?**

### [--- Solution ---](day-03.py)
```Python
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
    ```