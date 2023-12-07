# advent of code 2023
# day 7

file = 'input.txt'

class CamelCards:
    def __init__(self, deals):
        self.deals = []
        for deal in deals:
            hand, wager = deal
            hand = [x for x in hand]
            self.deals.append([hand, int(wager)])

    def valueHand(self, deal, jokers=False):
        hand, wager = deal
        if jokers:
            tie_breaker_hand = [int(x) if x.isdigit() else {'A': 14, 'K': 13, 'Q': 12, 'J': 0, 'T': 10}[x] for x in hand]
            joker_replacement = max([x for x in tie_breaker_hand if x != 0], key=lambda d: tie_breaker_hand.count(d)) if tie_breaker_hand != [0, 0, 0, 0, 0] else 14
            hand_value_hand = [joker_replacement if x == 0 else x for x in tie_breaker_hand]
        else:
            hand_value_hand = [int(x) if x.isdigit() else {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}[x] for x in hand]
            tie_breaker_hand = hand_value_hand
        if len(set(hand_value_hand)) == 1:
            hand_value = 7
        elif len(set(hand_value_hand)) == 2:
            if hand_value_hand.count(hand_value_hand[0]) in [1, 4]:
                hand_value = 6
            else:
                hand_value = 5
        elif len(set(hand_value_hand)) == 3:
            if any([hand_value_hand.count(hand_value_hand[i]) == 3 for i in range(len(hand_value_hand))]):
                hand_value = 4
            else:
                hand_value = 3
        elif len(set(hand_value_hand)) == 4:
            hand_value = 2
        else:
            hand_value = 1
        tie_breaker = sum([tie_breaker_hand[i] * 0.01 ** (i + 1) for i in range(len(tie_breaker_hand))])
        return hand_value + tie_breaker
    
    def countWinnings(self, jokers=False):
        sorted_hands = sorted(self.deals, key=lambda d: self.valueHand(d, jokers))
        return sum([sorted_hands[i][1] * (i + 1) for i in range(len(sorted_hands))])
    
def part_1(camelCards):
    print('Part 1:', camelCards.countWinnings())

def part_2(camelCards):
    print('Part 2:', camelCards.countWinnings(True))

def main():
    deals = [deal.split(' ') for deal in open(file, 'r').read().splitlines()]
    camelCards = CamelCards(deals)
    part_1(camelCards)
    part_2(camelCards)

if __name__ == '__main__':
    main()
