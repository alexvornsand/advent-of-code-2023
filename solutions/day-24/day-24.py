# advent of code 2023
# day 24

from sympy import *

file = 'input.txt'

class HailStone:
    def __init__(self, coords):
        self.x, self.y, self.z, self.dx, self.dy, self.dz = coords
        self.m = self.dy / self.dx
        self.b = self.y - self.x * self.m
class Sky:
    def __init__(self, stones):
        self.stones = {i: HailStone(stones[i]) for i in range(len(stones))}

    def findIntersection(self, A, B):
        if A.m == B.m:
            return None
        else:
            x = (B.b - A.b) / (A.m - B.m)
            y = A.m * x + A.b
            if (x - A.x) / A.dx >= 0 and (x - B.x) / B.dx >= 0:
                return (x, y)
            else:
                return None
        
    def findAllIntersections(self, r_min=200000000000000, r_max=400000000000000):
        valid_intersections = 0
        for i in range(len(self.stones) - 1):
            for j in range(i + 1, len(self.stones)):
                intersection = self.findIntersection(self.stones[i], self.stones[j])
                if intersection:
                    x, y = intersection
                    if r_min <= x <= r_max and r_min <= y <= r_max:
                        valid_intersections += 1
        return valid_intersections
    
    def findThroughLine(self):
        x, y, z, dx, dy, dz, t0, t1, t2 = symbols('x, y, z, dx, dy, dz, t0, t1, t2')
        eq1 = Eq((self.stones[0].x-x)-(dx-self.stones[0].dx)*t0, 0)
        eq2 = Eq((self.stones[0].y-y)-(dy-self.stones[0].dy)*t0, 0)
        eq3 = Eq((self.stones[0].z-z)-(dz-self.stones[0].dz)*t0, 0)
        eq4 = Eq((self.stones[1].x-x)-(dx-self.stones[1].dx)*t1, 0)
        eq5 = Eq((self.stones[1].y-y)-(dy-self.stones[1].dy)*t1, 0)
        eq6 = Eq((self.stones[1].z-z)-(dz-self.stones[1].dz)*t1, 0)
        eq7 = Eq((self.stones[2].x-x)-(dx-self.stones[2].dx)*t2, 0)
        eq8 = Eq((self.stones[2].y-y)-(dy-self.stones[2].dy)*t2, 0)
        eq9 = Eq((self.stones[2].z-z)-(dz-self.stones[2].dz)*t2, 0)
        sol = solve([eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9], [x, y, z, dx, dy, dz, t0, t1, t2])
        return sum(sol[0][:3])

def part_1(sky):
    print('Part 1:', sky.findAllIntersections())

def part_2(sky):
    print('Part 2:', sky.findThroughLine())

def main():
    stones = [[int(x.strip()) for triplet in line.split('@') for x in triplet.strip().split(',')] for line in open(file, 'r').read().splitlines()]
    sky = Sky(stones)
    part_1(sky)
    part_2(sky)

if __name__ == '__main__':
    main()