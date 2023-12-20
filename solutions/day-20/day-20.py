import re
import math

file = 'input.txt'

class Machine:
    def initialize(self):
        self.modules = {
            'button': {'type': 'button', 'destinations': ['broadcaster'], 'state': -1},
        }
        key = {'%': 'flip flop', '&': 'conjunction'}
        for instruction in self.instructions:
            module, destinations = instruction.split(' -> ')
            destinations = [dest.strip() for dest in destinations.split(',')]
            for destination in destinations:
                if destination not in self.modules:
                    self.modules[destination] = {'type': 'conjunction', 'destinations': [], 'state': {}}
            if re.match('\w+', module):
                module_type = module
                name = module
                state = -1
            else:
                module_type = key[module[0]]
                name = module[1:]
                if module_type == 'flip flop':
                    state = -1
                elif module_type == 'conjunction':
                    state = {}
            self.modules[name] = {'type': module_type, 'destinations': destinations, 'state': state}
        for module in self.modules:
            for destination in self.modules[module]['destinations']:
                if self.modules[destination]['type'] == 'conjunction':
                    self.modules[destination]['state'][module] = -1

    def __init__(self, instructions):
        self.island_of_interest = None
        self.instructions = instructions
        self.initialize()

    def processSignal(self, module, signal, debug=False):
        signal_map = {-1: 'low', 1: 'high'}
        next_queue = []
        for destination in self.modules[module]['destinations']:
            if debug:
                print('\t', module, ' -', signal_map[signal], '-> ', destination, sep='')
            if self.modules[destination]['type'] == 'flip flop' and signal == -1:
                self.modules[destination]['state'] *= -1
            elif self.modules[destination]['type'] == 'conjunction':
                self.modules[destination]['state'][module] = signal
        for destination in self.modules[module]['destinations']:
            if self.modules[destination]['type'] == 'flip flop' and signal == -1:
                next_queue.append([destination, self.modules[destination]['state']])
            elif self.modules[destination]['type'] == 'conjunction':
                next_queue.append([destination, 1 if -1 in list(self.modules[destination]['state'].values()) else -1])
            elif self.modules[destination]['type'] == 'broadcaster':
                next_queue.append([destination, signal])
        return next_queue
            
    def runProgram(self, n=1000):
        program_states = [[self.modules[module]['state'] for module in self.modules]]
        signals = {1: 0, -1: 0}
        i = 0
        while i < n:
            i += 1
            queue = [['button', -1]]
            while queue:
                module, signal = queue[0]
                queue.pop(0)
                signals[signal] += len(self.modules[module]['destinations'])
                next_queue = self.processSignal(module, signal)
                queue += next_queue
            program_state = [self.modules[module]['state'] for module in self.modules]
            if program_state in program_states:
                break
            program_states.append(program_state)
        return int((1000 / i * signals[-1]) * (1000 / i * signals[1])) 
    
    def runProgramForever(self):
        self.initialize()
        parent = list(self.modules['rx']['state'].keys())[0]
        ancestors = {ancestor: None for ancestor in list(self.modules[parent]['state'].keys())}
        unlooped_ancestors = list(ancestors.keys())
        i = 0
        while unlooped_ancestors:    
            i += 1
            queue = [['button', -1]]
            while queue:
                module, signal = queue[0]
                queue.pop(0)
                next_queue = self.processSignal(module, signal)
                if 1 in self.modules[parent]['state'].values():
                    for ancestor in ancestors:
                        if ancestors[ancestor] is None and self.modules[parent]['state'][ancestor] == 1:
                            ancestors[ancestor] = i
                            unlooped_ancestors.remove(ancestor)
                queue += next_queue
        return math.lcm(*ancestors.values())

def part_1(machine):
    print('Part 1:', machine.runProgram())

def part_2(machine):
    print('Part 2:', machine.runProgramForever())

def main():
    instructions = open(file, 'r').read().splitlines()
    machine = Machine(instructions)
    part_1(machine)
    part_2(machine)

if __name__ == '__main__':
    main()