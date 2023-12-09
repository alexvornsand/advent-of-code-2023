# advent of code 2023
# day 9

file = 'input.txt'

class OASIS:
    def __init__(self, histories):
        self.histories = {i: {0: histories[i]} for i in range(len(histories))}

    def extendHistory(self, history):
        i = 0
        while not all([x == 0 for x in self.histories[history][i]]):
            self.histories[history][i + 1] = [self.histories[history][i][j] - self.histories[history][i][j - 1] for j in range(1, len(self.histories[history][i]))]
            i += 1
        i -= 1
        while i > 0:
            self.histories[history][i - 1].append(self.histories[history][i - 1][-1] + self.histories[history][i][-1])
            self.histories[history][i - 1].insert(0, self.histories[history][i - 1][0] - self.histories[history][i][0])
            i -= 1

    def extendHistories(self):
        for history in self.histories:
            self.extendHistory(history)

    def sumOfFirst(self):
        return sum([self.histories[history][0][0] for history in self.histories])
    
    def sumOfLast(self):
        return sum([self.histories[history][0][-1] for history in self.histories])
    
def part_1(oasis):
    print('Part 1:', oasis.sumOfLast())

def part_2(oasis):
    print('Part 2:', oasis.sumOfFirst())

def main():
    histories = [[int(x) for x in line.split(' ')] for line in open(file, 'r').read().splitlines()]
    oasis = OASIS(histories)
    oasis.extendHistories()
    part_1(oasis)
    part_2(oasis)

if __name__ == '__main__':
    main()