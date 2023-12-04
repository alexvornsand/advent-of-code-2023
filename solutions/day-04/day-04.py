# advent of code 2023
# day 4

import re

file = 'input.txt'

class ScratchCards:
    def __init__(self, cards):
        self.cards = cards
        self.scores = []
        self.card_counts = [1 for card in self.cards]
        for card in self.cards:
            numbers = card[0]
            winners = card[1]
            self.scores.append(sum([number in winners for number in numbers]))
        
    def valueCards(self, score):
        if score == 0:
            return 0
        else:
            return 2 ** (score - 1)
        
    def naivePoints(self):
        return sum([self.valueCards(card) for card in self.scores])
    
    def accumulateCards(self):
        for i in range(len(self.cards)):
            for x in range(self.scores[i]):
                if i + x + 1 < len(self.card_counts):
                    self.card_counts[i + x + 1] += self.card_counts[i]
        return(sum(self.card_counts))

def part_1(scratchCards):
    print('Part 1:', scratchCards.naivePoints())

def part_2(scratchCards):
    print('Part 2:', scratchCards.accumulateCards())

def main():
    cards = [[[int(num) for num in list(re.findall('\d+', set))] for set in card.split(':')[1].strip().split('|')] for card in open(file, 'r').read().splitlines()]
    scratchCards = ScratchCards(cards)
    part_1(scratchCards)
    part_2(scratchCards)

if __name__ == '__main__':
    main()