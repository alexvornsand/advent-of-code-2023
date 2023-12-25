# advent of code 2023
# day 25

import networkx as nx
import math

file = 'input.txt'

class Network:
    def __init__(self, connections):
        dict = {}
        for connection in connections:
            parent, children = connection.split(':')
            children = children.strip().split(' ')
            dict[parent] = {child: {'weight': 1} for child in children}
        self.G = nx.Graph(dict)
        
    def findSplit(self):
        self.G.remove_edges_from(nx.minimum_edge_cut(self.G))
        return math.prod([len(x) for x in nx.connected_components(self.G)])

def part_1(network):
    print('Part 1:', network.findSplit())

def main():
    connections = open(file, 'r').read().splitlines()
    network = Network(connections)
    part_1(network)

if __name__ == '__main__':
    main()