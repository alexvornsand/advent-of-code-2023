# advent of code 2023
# day 2

file = 'input.txt'

class DiceGame:
    def __init__(self, lines):
        self.games = {int(game.split(':')[0].split(' ')[1]): [{cube.strip().split(' ')[1]: int(cube.strip().split(' ')[0]) for cube in draw.strip().split(',')} for draw in game.split(':')[1].strip().split(';')] for game in lines}
        self.max_draws = {game: {color: max([self.games[game][x][color] if color in self.games[game][x] else 0 for x in range(len(self.games[game]))]) for color in ['red', 'blue', 'green']} for game in self.games}

    def findQualifiedGames(self, targets):
        return [game for game in self.games if all([self.max_draws[game][color] <= targets[color] for color in targets])]
    
    def findCubePower(self):
        return [self.max_draws[game]['red'] * self.max_draws[game]['green'] * self.max_draws[game]['blue'] for game in self.games]
    
def part_1(diceGame):
    target = {'red': 12, 'green': 13, 'blue': 14}
    print('Part 1:', sum(diceGame.findQualifiedGames(target)))

def part_2(diceGame):
    print('Part 2:', sum(diceGame.findCubePower()))

def main():
    lines = open(file, 'r').read().splitlines()
    diceGame = DiceGame(lines)
    part_1(diceGame)
    part_2(diceGame)

if __name__ == '__main__':
    main()
