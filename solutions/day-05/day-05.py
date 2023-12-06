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