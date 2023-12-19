### [--- Day 19: Aplenty ---](https://adventofcode.com/2023/day/19)

The Elves of Gear Island are thankful for your help and send you on your way. They even have a hang glider that someone [stole](https://adventofcode.com/2023/day/9) from Desert Island; since you're already going that direction, it would help them a lot if you would use it to get down there and return it to them.

As you reach the bottom of the **relentless avalanche of machine parts**, you discover that they're already forming a formidable heap. Don't worry, though - a group of Elves is already here organizing the parts, and they have a **system**.

To start, each part is rated in each of four categories:

 - `x`: E**x**tremely cool looking
 - `m: **M**usical (it makes a noise when you hit it)
 - `a`: **A**erodynamic
 - `s`: **S**hiny

Then, each part is sent through a series of **workflows** that will ultimately **accept** or **reject** the part. Each workflow has a name and contains a list of rules; each rule specifies a condition and where to send the part if the condition is true. The first rule that matches the part being considered is applied immediately, and the part moves on to the destination described by the rule. (The last rule in each workflow has no condition and always applies if reached.)

Consider the workflow `ex{x>10:one,m<20:two,a>30:R,A}`. This workflow is named `ex` and contains four rules. If workflow `ex` were considering a specific part, it would perform the following steps in order:

 - Rule "`x>10:one`": If the part's `x` is more than `10`, send the part to the workflow named `one`.
 - Rule "`m<20:two`": Otherwise, if the part's `m` is less than `20`, send the part to the workflow named `two`.
 - Rule "`a>30:R`": Otherwise, if the part's `a` is more than `30`, the part is immediately **rejected** (`R`).
 - Rule "`A`": Otherwise, because no other rules matched the part, the part is immediately **accepted** (`A`).

If a part is sent to another workflow, it immediately switches to the start of that workflow instead and never returns. If a part is accepted (sent to A) or rejected (sent to R), the part immediately stops any further processing.

The system works, but it's not keeping up with the torrent of weird metal shapes. The Elves ask if you can help sort a few parts and give you the list of workflows and some part ratings (your puzzle input). For example:

```
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
```

The workflows are listed first, followed by a blank line, then the ratings of the parts the Elves would like you to sort. All parts begin in the workflow named in. In this example, the five listed parts go through the following workflows:

 - `{x=787,m=2655,a=1222,s=2876}`: `in` -> `qqz` -> `qs` -> `lnx` -> **`A`**
 - `{x=1679,m=44,a=2067,s=496}`: `in` -> `px` -> `rfg` -> `gd` -> **`R`**
 - `{x=2036,m=264,a=79,s=2244}`: `in` -> `qqz` -> `hdj` -> `pv` -> **`A`**
 - `{x=2461,m=1339,a=466,s=291}`: `in` -> `px` -> `qkq` -> `crn` -> **`R`**
 - `{x=2127,m=1623,a=2188,s=1013}`: `in` -> `px` -> `rfg` -> **`A`**

Ultimately, three parts are **accepted**. Adding up the `x`, `m`, `a`, and `s` rating for each of the accepted parts gives `7540` for the part with `x=787`, `4623` for the part with `x=2036`, and `6951` for the part with `x=2127`. Adding all of the ratings for all of the accepted parts gives the sum total of **`19114`**.

Sort through all of the parts you've been given; what do you get if you add together all of the rating numbers for all of the parts that ultimately get accepted?

### --- Part Two ---

Even with your help, the sorting process **still** isn't fast enough.

One of the Elves comes up with a new plan: rather than sort parts individually through all of these workflows, maybe you can figure out in advance which combinations of ratings will be accepted or rejected.

Each of the four ratings (`x`, `m`, `a`, `s`) can have an integer value ranging from a minimum of `1` to a maximum of `4000`. Of all possible distinct combinations of ratings, your job is to figure out which ones will be accepted.

In the above example, there are **`167409079868000`** distinct combinations of ratings that will be accepted.

Consider only your list of workflows; the list of part ratings that the Elves wanted you to sort is no longer relevant. **How many distinct combinations of ratings will be accepted by the Elves' workflows?**

### [--- Solution ---](day-19.py)

```Python
# advent of code 2023
# day 19

import re
import math

file = 'input.txt'

class Rule:
    def __init__(self, id, instructions):
        self.id = id
        self.rules = [instruction.split(':')[0] if len(instruction.split(':')) > 1 else 'True' for instruction in instructions.split(',')]
        self.destinations = [instruction.split(':')[1] if len(instruction.split(':')) > 1 else instruction for instruction in instructions.split(',')]
    
    def evaluateRule(self, keys):
        x, m, a, s = keys
        i = 0
        while True:
            if eval(self.rules[i]):
                return self.destinations[i]
            i += 1

    def fracturePartRange(self, keys, i):
        if self.rules[i] == 'True':
            return [[keys, self.destinations[i], 0]]
        key, opr, threshold = re.search('(\w+)([<>])(\d+)', self.rules[i]).groups()
        if opr == '>':
            threshold = int(threshold) + 1
        else:
            threshold = int(threshold)
        key_low = {key: value for key, value in keys.items()}
        key_low[key] = []
        key_high = {key: value for key, value in keys.items()}
        key_high[key] = []
        for rng in keys[key]:
            if rng[1] < threshold:
                key_low[key].append(rng)
            elif rng[0] >= threshold:
                key_high[key].append(rng)
            else:
                key_low[key].append([rng[0], threshold - 1])
                key_high[key].append([threshold, rng[1]])
        if opr == '>':
            return [[key_high, self.destinations[i], 0], [{key: value for key, value in key_low.items()}, self.id, i + 1]]
        else:
            return [[key_low, self.destinations[i], 0], [{key: value for key, value in key_high.items()}, self.id, i + 1]]

class SortSystem:
    def __init__(self, parts, rules):
        self.parts = [[int(x) for x in list(re.findall('\d+', part))] for part in parts.splitlines()]
        self.rules = {name: Rule(name, instructions[:-1]) for name, instructions in [line.split('{') for line in rules.splitlines()]}
        self.destinations = {'A': [], 'R': []}

    def evaluatePart(self, part, rule='in'):
        result = self.rules[rule].evaluateRule(part)
        if result in self.destinations:
            self.destinations[result].append(sum(part))
        else:
            self.evaluatePart(part, result)

    def evaluateParts(self):
        for part in self.parts:
            self.evaluatePart(part)

    def findLegitCombinations(self):
        legit_combinations = []
        queue = [[{'x': [[1, 4000]], 'm': [[1, 4000]], 'a': [[1, 4000]], 's': [[1, 4000]]}, 'in', 0]]
        while queue:
            test = queue[0]
            queue.pop(0)
            keys, rule, index = test
            if rule == 'A':
                legit_combinations.append(math.prod([sum([rng[1] - rng[0] + 1 for rng in keys[key]]) for key in keys]))
            elif rule == 'R':
                continue
            else:
                additional_combinations = self.rules[rule].fracturePartRange(keys, index)
                for combination in additional_combinations:
                    queue.append(combination)
        return sum(legit_combinations)

def part_1(sortSystem):
    sortSystem.evaluateParts()
    print('Part 1:', sum(sortSystem.destinations['A']))

def part_2(sortSystem):
    print('Part 2:', sortSystem.findLegitCombinations())

def main():
    rules, parts = open(file, 'r').read().strip().split('\n\n')
    sortSystem = SortSystem(parts, rules)
    part_1(sortSystem)
    part_2(sortSystem)

if __name__ == '__main__':
    main()
```