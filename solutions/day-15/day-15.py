# advent of code 2023
# day 15

from collections import OrderedDict

file = 'input.txt'

class Lenses:
    def __init__(self, codes):
        self.codes = codes
        self.lenses = {lens: 0 for lens in set(codes)}
        self.boxes = {i: OrderedDict() for i in range(256)}

    def hash(self, lens):
        return sum([ord(lens[i]) * 17 ** (len(lens) - i) % 256 for i in range(len(lens))]) % 256
    
    def findHashes(self):
        for lens in self.lenses:
            self.lenses[lens] = self.hash(lens)

    def getAllHashes(self):
        return sum([self.lenses[lens] for lens in self.codes])
    
    def processLens(self, lens):
        if lens[-1] == '-':
            id, length = lens.split('-')
            try:
                del self.boxes[self.hash(id)][id]
            except:
                pass
        else:
            id, length = lens.split('=')
            self.boxes[self.hash(id)][id] = int(length)
    
    def processLenses(self):
        for lens in self.codes:
            self.processLens(lens)
        
    def getLensPower(self, box):
        power =  sum([(box + 1) * (i + 1) * (self.boxes[box][list(self.boxes[box].keys())[i]]) for i in range(len(self.boxes[box]))])
        return power
    
    def getTotalLensPower(self):
        return sum([self.getLensPower(box) for box in self.boxes])

def part_1(lenses):
    print('Part 1:', lenses.getAllHashes())

def part_2(lenses):
    print('Part 2:', lenses.getTotalLensPower())

def main():
    codes = open(file, 'r').read().strip().split(',')
    lenses = Lenses(codes)
    lenses.findHashes()
    lenses.processLenses()
    part_1(lenses)
    part_2(lenses)

if __name__ == '__main__':
    main()