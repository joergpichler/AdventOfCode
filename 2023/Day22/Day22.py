import numpy as np
import regex as re

class Brick:
    def __init__(self, p1, p2) -> None:
        self.p1 = p1
        self.p2 = p2
        pass

    def __repr__(self) -> str:
        return f'{self.p1}~{self.p2}'
    
    @property
    def z_min(self):
        return min(self.p1[2], self.p2[2])
    
    def move_z(self, dz):
        if self.z_min + dz < 1:
            raise Exception
        self.p1 = (self.p1[0], self.p1[1], self.p1[2] + dz)
        self.p2 = (self.p2[0], self.p2[1], self.p2[2] + dz)

    def intersects(self, brick):
        return self._intersects((self.p1[2], self.p2[2]), (brick.p1[2], brick.p2[2])) and \
                self._intersects((self.p1[1], self.p2[1]), (brick.p1[1], brick.p2[1])) and \
                self._intersects((self.p1[0], self.p2[0]), (brick.p1[0], brick.p2[0]))
    
    def _intersects(self, a, b):
        a_min = min(a[0], a[1])
        a_max = max(a[0], a[1])
        b_min = min(b[0], b[1])
        b_max = max(b[0], b[1])
        return not (a_max < b_min or b_max < a_min)

def parse(file):
    def to_brick(l):
        r = re.findall(r'\d+', l)
        p1 = (int(r[0]), int(r[1]), int(r[2]))
        p2 = (int(r[3]), int(r[4]), int(r[5]))
        return Brick(p1, p2)
    with open(file, 'r') as f:
        return [to_brick(l.strip()) for l in f]
    
def can_fall(brick, bricks):
    if brick.z_min == 1:
        return False
    
    brick.move_z(-1)

    for other_brick in bricks:
        if brick is other_brick:
            continue
        if brick.intersects(other_brick):
            brick.move_z(1)
            return False
        
    brick.move_z(1)
    return True

def pt1(bricks):
    while True:
        brick_fell = False
        bricks.sort(key=lambda x: x.z_min)
        falling_bricks = 0
        for brick in bricks:
            if can_fall(brick, bricks):
                brick.move_z(-1)
                brick_fell = True           
                falling_bricks += 1
            while can_fall(brick, bricks):
                brick.move_z(-1)

        if not brick_fell:
            break

    total = 0
    for brick in bricks:
        other_bricks = [x for x in bricks if x is not brick]
        brick_fell = False
        for test_brick in other_bricks:
            if can_fall(test_brick, other_bricks):
                brick_fell = True
                break
        if not brick_fell:
            total += 1
    return total


def main():
    bricks = parse('test.txt')
    assert pt1(bricks) == 5
    bricks = parse('input.txt')
    print(pt1(bricks))

if __name__ == '__main__':
    main()
