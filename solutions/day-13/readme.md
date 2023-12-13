### [--- Day 13: Point of Incidence ---](https://adventofcode.com/2023/day/13)

With your help, the hot springs team locates an appropriate spring which launches you neatly and precisely up to the edge of **Lava Island**.

There's just one problem: you don't see any **lava**.

You **do** see a lot of ash and igneous rock; there are even what look like gray mountains scattered around. After a while, you make your way to a nearby cluster of mountains only to discover that the valley between them is completely full of large **mirrors**. Most of the mirrors seem to be aligned in a consistent way; perhaps you should head in that direction?

As you move through the valley of mirrors, you find that several of them have fallen from the large metal frames keeping them in place. The mirrors are extremely flat and shiny, and many of the fallen mirrors have lodged into the ash at strange angles. Because the terrain is all one color, it's hard to tell where it's safe to walk or where you're about to run into a mirror.

You note down the patterns of ash (`.`) and rocks (`#`) that you see as you walk (your puzzle input); perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!

For example:

```
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
```

To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal line between two rows or across a vertical line between two columns.

In the first pattern, the reflection is across a vertical line between two columns; arrows on each of the two columns point at the line between the columns:


```123456789
    ><   
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><   
123456789
```

In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the vertical line is not perfectly in the middle of the pattern, part of the pattern (column 1) has nowhere to reflect onto and can be ignored; every other column has a reflected column within the pattern and must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.

The second pattern reflects across a horizontal line instead:

```
1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7
```

This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8, but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match: row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.

To **summarize** your pattern notes, add up the **number of columns** to the left of each vertical line of reflection; to that, also add **100 multiplied by the number of rows** above each horizontal line of reflection. In the above example, the first pattern's vertical line has `5` columns to its left and the second pattern's horizontal line has `4` rows above it, a total of **`405`**.

Find the line of reflection in each of the patterns in your notes. **What number do you get after summarizing all of your notes?**

### --- Part Two ---

You resume walking through the valley of mirrors and - **SMACK!** - run directly into one. Hopefully nobody was watching, because that must have been pretty embarrassing.

Upon closer inspection, you discover that every mirror has exactly one **smudge**: exactly one `.` or `#` should be the opposite type.

In each pattern, you'll need to locate and fix the smudge that causes a **different reflection line** to be valid. (The old reflection line won't necessarily continue being valid after the smudge is fixed.)

Here's the above example again:

```
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
```

The first pattern's smudge is in the top-left corner. If the top-left `#` were instead `.`, it would have a different, horizontal line of reflection:

```
1 ..##..##. 1
2 ..#.##.#. 2
3v##......#v3
4^##......#^4
5 ..#.##.#. 5
6 ..##..##. 6
7 #.#.##.#. 7
```

With the smudge in the top-left corner repaired, a new horizontal line of reflection between rows 3 and 4 now exists. Row 7 has no corresponding reflected row and can be ignored, but every other row matches exactly: row 1 matches row 6, row 2 matches row 5, and row 3 matches row 4.

In the second pattern, the smudge can be fixed by changing the fifth symbol on row 2 from `.` to `#`:

```
1v#...##..#v1
2^#...##..#^2
3 ..##..### 3
4 #####.##. 4
5 #####.##. 5
6 ..##..### 6
7 #....#..# 7
```

Now, the pattern has a different horizontal line of reflection between rows 1 and 2.

Summarize your notes as before, but instead use the new different reflection lines. In this example, the first pattern's new horizontal line has 3 rows above it and the second pattern's new horizontal line has 1 row above it, summarizing to the value **`400`**.

In each pattern, fix the smudge and find the different line of reflection. **What number do you get after summarizing the new reflection line in each pattern in your notes?**

### [--- Solution ---](day-13.py)

```Python
# advent of code 2023
# day 13

import numpy as np

file = 'input.txt'

class MirrorField:
    def __init__(self, maps):
        self.maps = maps

    def findMirror(self, map, smudges=0):
        for r in range(len(map) - 1):
            if r + 1 <= len(map) / 2:
                a = map[:r + 1, :]
                b = map[r + r + 1:r:-1, :]
            else:
                a = map[r + 1:, :]
                b = map[r:r + r + 1 - len(map):-1, :]
            if sum(sum(abs(a - b))) == smudges:
                return 100 * (r + 1)
        t_map = map.T
        for c in range(len(t_map) - 1):
            if c + 1 <= len(t_map) / 2:
                a = t_map[:c + 1, :]
                b = t_map[c + c + 1:c:-1, :]
            else:
                a = t_map[c + 1:, :]
                b = t_map[c:c + c + 1 - len(t_map):-1, :]
            if sum(sum(abs(a - b))) == smudges:
                return c + 1
            
    def findAllMirrors(self, smudges=0):
        return sum([self.findMirror(map, smudges) for map in self.maps])
    
def part_1(mirrorField):
    print('Part 1:', mirrorField.findAllMirrors())

def part_2(mirrorField):
    print('Part 2:', mirrorField.findAllMirrors(1))

def main():
    maps = [np.array([[1 if char == '#' else 0 for char in row] for row in map.splitlines()]) for map in open(file, 'r').read().split('\n\n')]
    mirrorField = MirrorField(maps)
    part_1(mirrorField)
    part_2(mirrorField)

if __name__ == '__main__':
    main()
```