### [--- Day 24: Never Tell Me The Odds ---](https://adventofcode.com/2023/day/24)

It seems like something is going wrong with the snow-making process. Instead of forming snow, the water that's been absorbed into the air seems to be forming [hail](https://en.wikipedia.org/wiki/Hail)!

Maybe there's something you can do to break up the hailstones?

Due to strong, probably-magical winds, the hailstones are all flying through the air in perfectly linear trajectories. You make a note of each hailstone's **position** and **velocity** (your puzzle input). For example:

```
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
```

Each line of text corresponds to the position and velocity of a single hailstone. The positions indicate where the hailstones are **right now** (at time `0`). The velocities are constant and indicate exactly how far each hailstone will move in **one nanosecond**.

Each line of text uses the format `px py pz @ vx vy vz`. For instance, the hailstone specified by `20, 19, 15 @ 1, -5, -3` has initial X position `20`, Y position `19`, Z position `15`, X velocity `1`, Y velocity `-5`, and Z velocity `-3`. After one nanosecond, the hailstone would be at `21, 14, 12`.

Perhaps you won't have to do anything. How likely are the hailstones to collide with each other and smash into tiny ice crystals?

To estimate this, consider only the X and Y axes; **ignore the Z axis**. Looking **forward in time**, how many of the hailstones' **paths** will intersect within a test area? (The hailstones themselves don't have to collide, just test for intersections between the paths they will trace.)

In this example, look for intersections that happen with an X and Y position each at least `7` and at most `27`; in your actual data, you'll need to check a much larger test area. Comparing all pairs of hailstones' future paths produces the following results:

```
Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 18, 19, 22 @ -1, -1, -2
Hailstones' paths will cross inside the test area (at x=14.333, y=15.333).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths will cross inside the test area (at x=11.667, y=16.667).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=6.2, y=19.4).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone A.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths are parallel; they never intersect.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-6, y=-5).

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-2, y=3).

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone B.

Hailstone A: 12, 31, 28 @ -1, -2, -1
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.
```

So, in this example, **`2`** hailstones' future paths cross inside the boundaries of the test area.

However, you'll need to search a much larger test area if you want to see if any hailstones might collide. Look for intersections that happen with an X and Y position each at least `200000000000000` and at most `400000000000000`. Disregard the Z axis entirely.

Considering only the X and Y axes, check all pairs of hailstones' future paths for intersections. **How many of these intersections occur within the test area?**

### --- Part Two ---

Upon further analysis, it doesn't seem like **any** hailstones will naturally collide. It's up to you to fix that!

You find a rock on the ground nearby. While it seems extremely unlikely, if you throw it just right, you should be able to **hit every hailstone in a single throw**!

You can use the probably-magical winds to reach **any integer position** you like and to propel the rock at **any integer velocity**. Now **including the Z axis** in your calculations, if you throw the rock at time `0`, where do you need to be so that the rock **perfectly collides with every hailstone**? Due to probably-magical inertia, the rock won't slow down or change direction when it collides with a hailstone.

In the example above, you can achieve this by moving to position `24, 13, 10` and throwing the rock at velocity `-3, 1, 2.` If you do this, you will hit every hailstone as follows:

```
Hailstone: 19, 13, 30 @ -2, 1, -2
Collision time: 5
Collision position: 9, 18, 20

Hailstone: 18, 19, 22 @ -1, -1, -2
Collision time: 3
Collision position: 15, 16, 16

Hailstone: 20, 25, 34 @ -2, -2, -4
Collision time: 4
Collision position: 12, 17, 18

Hailstone: 12, 31, 28 @ -1, -2, -1
Collision time: 6
Collision position: 6, 19, 22

Hailstone: 20, 19, 15 @ 1, -5, -3
Collision time: 1
Collision position: 21, 14, 12
```

Above, each hailstone is identified by its initial position and its velocity. Then, the time and position of that hailstone's collision with your rock are given.

After 1 nanosecond, the rock has **exactly the same position** as one of the hailstones, obliterating it into ice dust! Another hailstone is smashed to bits two nanoseconds after that. After a total of 6 nanoseconds, all of the hailstones have been destroyed.

So, at time `0`, the rock needs to be at X position `24`, Y position `13`, and Z position `10`. Adding these three coordinates together produces **`47`**. (Don't add any coordinates from the rock's velocity.)

Determine the exact position and velocity the rock needs to have at time `0` so that it perfectly collides with every hailstone. **What do you get if you add up the X, Y, and Z coordinates of that initial position?**

### [--- Solution ---](day-24.py)
```Python
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
```