# advent of code 2023
# day 01

import regex as re

file = 'input.txt'

class Calibration:
    def __init__(self, instructions):
        self.instructions = instructions
        self.number_codes = {
            'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 
            'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 
            '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', 
            '6': '6', '7': '7', '8': '8', '9': '9'
        }

    def sumCalibrationValues(self, string):
        return sum([int(self.number_codes[re.findall(string, line, overlapped = True)[0]] + self.number_codes[re.findall(string, line, overlapped = True)[-1]]) for line in self.instructions])
    
def part_1(calibration):
    print('Part 1:', calibration.sumCalibrationValues('\d'))

def part_2(calibration):
    print('Part 2:', calibration.sumCalibrationValues('(?:\d|(?:one|two)|three|four|five|six|seven|eight|nine)'))

def main():
    instructions = open(file, 'r').read().splitlines()
    calibration = Calibration(instructions)
    part_1(calibration)
    part_2(calibration)

if __name__ == '__main__':
    main()


