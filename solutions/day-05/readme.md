### [--- Day 5: If You Give A Seed A Fertilizer ---](https://adventofcode.com/2023/day/5)

You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we **ran out of sand** to [filter](https://en.wikipedia.org/wiki/Sand_filter) it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our **food production problem**. The latest Island Island [Almanac](https://en.wikipedia.org/wiki/Almanac) just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil `123` and fertilizer `123` aren't necessarily related to each other.

For example:

```
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
```

The almanac starts by listing which seeds need to be planted: seeds `79`, `14`, `55`, and `13`.

The rest of the almanac contains a list of **maps** which describe how to convert numbers from a **source category** into numbers in a **destination category**. That is, the section that starts with seed-to-soil map: describes how to convert a **seed number** (the source) to a **soil number** (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire **ranges** of numbers that can be converted. Each line within a map contains three numbers: the **destination range start**, the **source range start**, and the **range length**.

Consider again the example `seed-to-soil map`:

```
50 98 2
52 50 48
```

The first line has a **destination range start** of `50`, a **source range start** of `98`, and a **range length** of `2`. This line means that the source range starts at `98` and contains two values: `98` and `99`. The destination range is the same length, but it starts at `50`, so its two values are `50` and `51`. With this information, you know that seed number `98` corresponds to soil number `50` and that seed number `99` corresponds to soil number `51`.

The second line means that the source range starts at `50` and contains `48` values: `50`, `51`, ..., `96`, `97`. This corresponds to a destination range starting at `52` and also containing `48` values: `52`, `53`, ..., `98`, `99`. So, seed number `53` corresponds to soil number `55`.

Any source numbers that **aren't mapped** correspond to the **same** destination number. So, seed number `10` corresponds to soil number `10`.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

```
seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
```

With this map, you can look up the soil number required for each initial seed number:

 - Seed number `79` corresponds to soil number `81`.
 - Seed number `14` corresponds to soil number `14`.
 - Seed number `55` corresponds to soil number `57`.
 - Seed number `13` corresponds to soil number `13`.

The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the **lowest location number that corresponds to any of the initial seeds**. To do this, you'll need to convert each seed number through other categories until you can find its corresponding **location number**. In this example, the corresponding types are:

 - Seed `79`, soil `81`, fertilizer `81`, water `81`, light `74`, temperature `78`, humidity `78`, **location `82`**.
 - Seed `14`, soil `14`, fertilizer `53`, water `49`, light `42`, temperature `42`, humidity `43`, **location `43`**.
 - Seed `55`, soil `57`, fertilizer `57`, water `53`, light `46`, temperature `82`, humidity `82`, **location `86`**.
 - Seed `13`, soil `13`, fertilizer `52`, water `41`, light `34`, temperature `34`, humidity `35`, **location `35`**.

So, the lowest location number in this example is **`35`**.

**What is the lowest location number that corresponds to any of the initial seed numbers?**

### --- Part 2 ---

Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the `seeds:` line actually describes **ranges of seed numbers**.

The values on the initial `seeds:` line come in pairs. Within each pair, the first value is the **start** of the range and the second value is the **length** of the range. So, in the first line of the example above:

```
seeds: 79 14 55 13
```

This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number `79` and contains `14` values: `79`, `80`, ..., `91`, `92`. The second range starts with seed number `55` and contains `13` values: `55`, `56`, ..., `66`, `67`.

Now, rather than considering four seed numbers, you need to consider a total of **`27`** seed numbers.

In the above example, the lowest location number can be obtained from seed number `82`, which corresponds to soil `84`, fertilizer `84`, water `84`, light `77`, temperature `45`, humidity `46`, and **location `46`**. So, the lowest location number is **`46`**.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. **What is the lowest location number that corresponds to any of the initial seed numbers?**

### [--- Solution ---](day-05.py)

```Python
# advent of code 2023
# day 5

import math

file = 'input.txt'

class Almanac:
    def __init__(self, file):
        sections = [section.split(':') for section in open(file, 'r').read().split('\n\n')]
        self.seeds = [int(seed) for seed in sections[0][1].strip().split(' ')]
        self.ranges = [(self.seeds[2 * i], self.seeds[2 * i] + self.seeds[2 * i + 1] - 1) for i in range(int(len(self.seeds) / 2))]
        self.maps = {}
        self.map_values = {}
        map_sections = sections[1:]
        for map_section in map_sections:
            frm, x, to = map_section[0].replace('map', '').strip().split('-')
            self.maps[frm] = to
            self.map_values[frm] = [{
                'source start': int(mapping.split(' ')[1].strip()),
                'source end': int(mapping.split(' ')[1].strip())  + int(mapping.split(' ')[2].strip()) - 1,
                'destination start': int(mapping.split(' ')[0].strip()),
                'destination end': int(mapping.split(' ')[0].strip()) + int(mapping.split(' ')[2].strip()) - 1,
                'shift': int(mapping.split(' ')[0].strip()) - int(mapping.split(' ')[1].strip())
            } for mapping in map_section[1].strip().split('\n')]
        self.critical_points = []

    def identifyCriticalPoints(self, section):
        critical_points = [{
            'source start': -math.inf, 
            'source end': math.inf,
            'destination start': -math.inf, 
            'destination end': math.inf, 
            'shift': 0
        }]
        for segment in self.map_values[section]:
            for i in range(len(critical_points)):
                if segment['source start'] >= critical_points[i]['source start'] and segment['source end'] <= critical_points[i]['source end']:
                    if segment['source end'] < critical_points[i]['source end']:
                        i_tail = critical_points[i].copy()
                        i_tail['source start'] = segment['source end'] + 1
                        i_tail['destination start'] = i_tail['source start'] + i_tail['shift']
                        critical_points.append(i_tail.copy())
                    if segment['source start'] > critical_points[i]['source start']:
                        critical_points[i]['source end'] = segment['source start'] - 1
                        critical_points[i]['destination end'] = critical_points[i]['source end'] + critical_points[i]['shift']
                    else:
                        critical_points.pop(i)
                    critical_points.append(segment)
                    critical_points = sorted(critical_points, key=lambda p: p['source start'])
                    break
        return critical_points
    
    def mergePoints(self, start, end):
        start_points = [point['destination start'] for point in start]
        end_points = [point['source start'] for point in end]
        set_of_points = sorted(list(set(start_points).union(set(end_points))))
        new_points = []
        for i in range(len(set_of_points)):
            new_point = {}
            stage_two_start = set_of_points[i]
            stage_two_end = set_of_points[i + 1] - 1 if i + 1 < len(set_of_points) else math.inf
            for point in start:
                if stage_two_start >= point['destination start'] and stage_two_end <= point['destination end']:
                    s_shift = point['shift']
            for point in end:
                if stage_two_start >= point['source start'] and stage_two_end <= point['source end']:
                    e_shift = point['shift']
            new_point['source start'] = stage_two_start - s_shift
            new_point['source end'] = stage_two_end - s_shift
            new_point['shift'] = s_shift + e_shift
            new_point['destination start'] = new_point['source start'] + new_point['shift']
            new_point['destination end'] = new_point['source end'] + new_point['shift']
            new_points.append(new_point)
        return sorted(new_points, key=lambda p:p['source start'])
    
    def identifyAllCriticalPoints(self):
        self.critical_points = self.identifyCriticalPoints('seed')        
        for map in list(self.maps.keys())[1:]:
            self.critical_points = self.mergePoints(self.critical_points, self.identifyCriticalPoints(map))

    def findMinAmongPoints(self):
        return(min([seed + point['shift'] for seed in self.seeds for point in self.critical_points if seed >= point['source start'] and seed <= point['source end']]))            
            
    def findMinAmongRanges(self):
        values = []
        for range in self.ranges:
            start, end = range
            if start <= self.critical_points[0]['source end']:
                values.append(start + self.critical_points[0]['shift'])
            if end >= self.critical_points[-1]['source start']:
                values.append(start + self.critical_points[-1]['shift'])
            for point in self.critical_points:
                if point['source start'] >= start and point['source start'] <= end:
                    values.append(point['destination start'])
                if point['source end'] >= start and point['source end'] <= end:
                    values.append(point['destination end'])
        return min(values)

def part_1(almanac):
    print('Part 1:', almanac.findMinAmongPoints())

def part_2(almanac):
    print('Part 2:', almanac.findMinAmongRanges())

def main():
    almanac = Almanac(file)
    almanac.identifyAllCriticalPoints()
    part_1(almanac)
    part_2(almanac)

if __name__ == '__main__':
    main()
```