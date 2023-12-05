import regex as re
from collections import namedtuple
import sys

Mapping = namedtuple('Mapping', 'source_range_start dest_range_start range_length')

class Map:
    def __init__(self, source, target) -> None:
        self.source = source
        self.target = target
        self._mappings = []

    def add_mapping(self, source_range_start, dest_range_start, range_length):
        self._mappings.append(Mapping(source_range_start, dest_range_start, range_length))

    def map(self, value):
        for mapping in self._mappings:
            offset = value - mapping.source_range_start
            if offset >= 0 and offset < mapping.range_length:
                return mapping.dest_range_start + offset
        return value
    
    def map_inverse(self, value):
        for mapping in self._mappings:
            offset = value - mapping.dest_range_start
            if offset >= 0 and offset < mapping.range_length:
                return mapping.source_range_start + offset
        return value
    
    def get_max_dest(self):
        result = max(map(lambda x: x.dest_range_start + x.range_length - 1 , self._mappings))
        return result + 1
    
    def __repr__(self) -> str:
        return f'{self.source}->{self.target}'

def parse(file):
    seeds = []
    maps = []
    current_map = None
    with open(file, 'r') as f:
        line = f.readline()
        while line:
            line = line.strip()
            if re.match(r'seeds: (\d+\s?)+', line):
                split = line.split(' ')
                for i in range(1, len(split)):
                    seeds.append(int(split[i]))
            match = re.match(r'(\w+)-to-(\w+) map:', line)
            if match:
                current_map = Map(match.groups()[0], match.groups()[1])
                maps.append(current_map)
            if current_map is not None:
                match = re.match(r'(\d+) (\d+) (\d+)', line)
                if match:
                    dest_range_start = int(match.groups()[0])
                    source_range_start = int(match.groups()[1])
                    range_length = int(match.groups()[2])
                    current_map.add_mapping(source_range_start, dest_range_start, range_length)
            line = f.readline()
    return seeds, maps

def find_location(seed, maps):
    source = 'seed'
    value = seed
    for map in maps:
        if not map.source == source:
            raise Exception
        value = map.map(value)
        source = map.target
    if not source == 'location':
        raise Exception
    
    return value

def find_seed(location, maps):
    source = 'location'
    value = location
    for map in maps:
        if not map.target == source:
            raise Exception
        value = map.map_inverse(value)
        source = map.source
    if not source == 'seed':
        raise Exception
    
    return value

def pt1(seeds, maps):
    min_value = sys.maxsize
    
    for seed in seeds:
        location = find_location(seed, maps)
        min_value = min(min_value, location)
    
    return min_value

def gen_seed_bounds(seeds):
    seed_bounds = []
    for i in range(0, len(seeds), 2):
        start = seeds[i]
        width = seeds[i + 1]
        seed_bounds.append((start, start + width - 1))
    return seed_bounds

def is_in_seed_bounds(seed, seed_bounds):
    for bound in seed_bounds:
        if seed >= bound[0] and seed <= bound[1]:
            return True
        
    return False

def pt2(seeds, maps):
    seed_bounds = gen_seed_bounds(seeds)
    end = max(map(lambda x: x.get_max_dest(), maps))
    maps.reverse()
    for i in range(0, end + 1):
        seed = find_seed(i, maps)
        if is_in_seed_bounds(seed, seed_bounds):
            return i
    raise Exception

def main():
    seeds, maps = parse('test.txt')
    assert pt1(seeds, maps) == 35
    assert pt2(seeds, maps) == 46

    seeds, maps = parse('input.txt')
    print(pt1(seeds, maps))
    print(pt2(seeds, maps))

if __name__ == '__main__':
    main()
