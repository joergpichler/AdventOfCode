import re
from typing import Callable, List, Tuple

class City:
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id
    
    def __repr__(self) -> str:
        return f'[{self.id}] {self.name}'

class Map:
    def __init__(self, distances):
        self.distances = {}
        self.cities = {}
        
        cities_to_num = {}
        ctr = 0
        for dist in distances:
            if not dist[0] in cities_to_num:
                idA = ctr
                cities_to_num[dist[0]] = idA
                ctr += 1
            else:
                idA = cities_to_num[dist[0]]
            if not dist[1] in cities_to_num:
                idB = ctr
                cities_to_num[dist[1]] = idB
                ctr += 1
            else:
                idB = cities_to_num[dist[1]]
            self.distances[(idA, idB)] = dist[2]
                
        for k,v in cities_to_num.items():
            self.cities[v] = City(k, v)
            
    def get_next_cities(self, city: City):
        for k,v in self.distances.items():
            if k[0] == city.id:
                yield self.cities[k[1]]
            elif k[1] == city.id:
                yield self.cities[k[0]]
                
    def get_distance(self, cityA: City, cityB: City):
        if (cityA.id, cityB.id) in self.distances:
            distance = self.distances[(cityA.id, cityB.id)]
        else:
            distance = self.distances[(cityB.id, cityA.id)]
        return distance

def parse_line(line):
    match = re.match(r'^(.+?)\sto\s(.+?)\s=\s(\d+)$', line)
    if not match:
        raise Exception()
    return (match.group(1), match.group(2), int(match.group(3)))

def parse(file) -> Map:
    with open(file, 'r') as f:
        return Map([parse_line(l.strip()) for l in f])

class CityNode:
    def __init__(self, city: City) -> None:
        self.previous_node = None
        self.city = city
        self.next_nodes = []
        
    def __repr__(self) -> str:
        return self.city.__repr__()

def buildNode(node: CityNode, map: Map, visitedCities: List[City] = []):
    nextCities = list(map.get_next_cities(node.city))
    node.next_nodes = [CityNode(c) for c in nextCities if not c in visitedCities]
    for next_node in node.next_nodes:
        visited = visitedCities.copy()
        visited.append(node.city)
        next_node.previous_node = node
        buildNode(next_node, map, visited)

def visit_node(node: CityNode, targetDepth: int, map: Map, distances: List[Tuple], currentDepth = 1):
    for next_node in node.next_nodes:
        visit_node(next_node, targetDepth, map, distances, currentDepth + 1)
    
    if currentDepth == targetDepth and len(node.next_nodes) == 0:
        dist = 0
        node_walk = node
        while node_walk.previous_node is not None:
            dist += map.get_distance(node_walk.city, node_walk.previous_node.city)
            node_walk = node_walk.previous_node
        distances.append((node, dist))

def walk_tree(node: CityNode, targetDepth: int, map: Map, func: Callable[[int, int], bool]):
    distances = []
    visit_node(node, targetDepth, map, distances)
    min = distances[0]
    for i in range(1, len(distances)):
        if func(distances[i][1], min[1]):
            min = distances[i]
    return min

def get_roundtrip_from(startingCity: City, map: Map, func: Callable[[int, int], bool]):
    node = CityNode(startingCity)
    buildNode(node, map)
    return walk_tree(node, len(map.cities), map, func)

def get_roundtrip(map: Map, func: Callable[[int, int], bool]):
    trips = []
    for _, city in map.cities.items():
        trips.append(get_roundtrip_from(city, map, func))
    trip = trips[0]
    for i in range(1, len(trips)):
        if func(trips[i][1], trip[1]):
            trip = trips[i]
    return trip[1]

def main():
    map = parse('input.txt')
    
    print(f'Pt1: {get_roundtrip(map, lambda a, b: a < b)}') 
    
    print(f'Pt2: {get_roundtrip(map, lambda a, b: a > b)}') 

if __name__ == '__main__':
    main()
