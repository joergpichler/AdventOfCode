import numpy as np
import re

class Area:
    def __init__(self, x_min, x_max, y_min, y_max) -> None:
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

def parse(file):
    with open(file, 'r') as f:
        match = re.match(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)', f.readline())
        x_bound_1 = int(match.group(1))
        x_bound_2 = int(match.group(2))
        y_bound_1 = int(match.group(3))
        y_bound_2 = int(match.group(4))
        
        return Area(min(x_bound_1, x_bound_2), max(x_bound_1, x_bound_2), min(y_bound_1, y_bound_2), max(y_bound_1, y_bound_2))

def gaussian_sum(n):
    return int((n ** 2 + n) / 2)

def hits_target_area(velocity, area):
    point = [0, 0]
    while True:
        point[0] += velocity[0]
        point[1] += velocity[1]
        
        if point[1] < area.y_min or point[0] > area.x_max:
            return False
        
        if point[0] >= area.x_min and point[0] <= area.x_max and \
            point[1] >= area.y_min and point[1] <= area.y_max:
                return True
        
        velocity = [velocity[0] - 1 if velocity[0] > 0 else 0, velocity[1] - 1]

def main():
    file = 'input.txt'
    area = parse(file)
    
    if file == 'test.txt':
        assert hits_target_area((7, 2), area) == True
        assert hits_target_area((6, 3), area) == True
        assert hits_target_area((9, 0), area) == True
        assert hits_target_area((17, -4), area) == False
        assert hits_target_area((6, 9), area) == True
    
    y_max = 0
    found_velocity = None
    velocities = []
    
    for x in range(1, 1000):
        for y in range(-1000, 1000):
            velocity = (x, y)
            if hits_target_area(velocity, area):
                velocities.append(velocity)
                y = gaussian_sum(y)
                if y > y_max:
                    y_max = y
                    found_velocity = velocity
    
    print(f'Pt1: {y_max}')
    print(f'Pt2: {len(velocities)}')

if __name__ == '__main__':
    main()
