# advent of code 2023
# day 22

from collections import defaultdict

file = 'input.txt'

class Brick:
    def __init__(self, id, coords):
        self.id = id
        self.x_min, self.y_min, self.z_min, self.x_max, self.y_max, self.z_max = [int(x) for c in coords.split('~') for x in c.split(',')]
        self.resting_on = []
        self.supporting = []
        self.chained_dependency = 1

    def fall(self):
        self.z_min -= 1
        self.z_max -= 1
class Stack:
    def __init__(self, bricks):
        self.bricks = {i: Brick(i, bricks[i]) for i in range(len(bricks))}
        self.brick_order = sorted(list(self.bricks.keys()), key=lambda k: self.bricks[k].z_min)
        self.stack = defaultdict(lambda: None)

    def dropBrick(self, brick):
        while True:
            xs = range(self.bricks[brick].x_min, self.bricks[brick].x_max + 1)
            ys = range(self.bricks[brick].y_min, self.bricks[brick].y_max + 1)
            zs = range(self.bricks[brick].z_min, self.bricks[brick].z_max + 1)
            z = self.bricks[brick].z_min - 1
            resting_on = set([self.stack[(x, y, z)] for x in xs for y in ys if self.stack[x, y, z] is not None])
            if len(resting_on) > 0 or self.bricks[brick].z_min == 1:
                self.bricks[brick].resting_on = list(resting_on)
                for supporter in resting_on:
                    self.bricks[supporter].supporting.append(brick)
                for x in xs:
                    for y in ys:
                        for z in zs:
                            self.stack[(x, y, z)] = brick
                break
            else:
                self.bricks[brick].fall()

    def buildStack(self):
        for brick in self.brick_order:
            self.dropBrick(brick)

    def identifyLooseBricks(self):
        loose_bricks = []
        for brick in self.bricks:
            supported_bricks = self.bricks[brick].supporting
            if len(supported_bricks) == 0:
                loose_bricks.append(brick)
            elif all([len(self.bricks[supported_brick].resting_on) > 1 for supported_brick in supported_bricks]):
                loose_bricks.append(brick)
        return len(loose_bricks)
    
    def countChainedDependency(self, brick):
        fallen_bricks = set([brick])
        queue = [brick]
        while queue:
            falling_brick = queue.pop(0)
            dependent_bricks = [supported_brick for supported_brick in self.bricks[falling_brick].supporting if all([supporting_brick in fallen_bricks for supporting_brick in self.bricks[supported_brick].resting_on])]
            for dependent_brick in dependent_bricks:
                queue.append(dependent_brick)
                fallen_bricks.add(dependent_brick)
        self.bricks[brick].chained_dependency = len(fallen_bricks) - 1
        return self.bricks[brick].chained_dependency

    def totalChainedBricks(self):
        return sum(self.countChainedDependency(brick) for brick in self.bricks)

def part_1(stack):
    print('Part 1:', stack.identifyLooseBricks())

def part_2(stack):
    print('Part 2:', stack.totalChainedBricks())

def main():
    bricks = open(file, 'r').read().splitlines()
    stack = Stack(bricks)
    stack.buildStack()
    part_1(stack)
    part_2(stack)

if __name__ == '__main__':
    main()