from collections import defaultdict
import re

class Reactor:
    def __init__(self, min, max) -> None:
        self.min = min
        self.max = max
        self.state = defaultdict(bool)
        pass
    
    def toggle(self, ranges, state, ignore_min_max=False):
        x_min = ranges[0]
        x_max = ranges[1]
        y_min = ranges[2]
        y_max = ranges[3]
        z_min = ranges[4]
        z_max = ranges[5]
        
        if not ignore_min_max:
            if x_min < self.min and x_max < self.min:
                return
            if x_min > self.max and x_max > self.max:
                return
            
            if y_min < self.min and y_max < self.min:
                return
            if y_min > self.max and y_max > self.max:
                return
            
            if z_min < self.min and z_max < self.min:
                return
            if z_min > self.max and z_max > self.max:
                return
        
        #s_state = 'on' if state == 1 else 'off'
        #print(f'{s_state} x={x_min}..{x_max},y={y_min}..{y_max},z={z_min}..{z_max}')
        
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                for z in range(z_min, z_max + 1):
                    # if x < self.min or x > self.max or y < self.min or y > self.max or z < self.min or z > self.max:
                    #     continue
                    self.state[(x,y,z)] = state
    
    @property
    def on_count(self):
        return sum(v for k,v in self.state.items() if v)

def parse(file):
    instructions = []
    with open(file, 'r') as f:
        for line in f:
            m = re.match(r"^(.+)\sx=(.+?),y=(.+?),z=(.+?)\s*$", line)
            range = [0, 0, 0, 0, 0, 0]
            x = m.group(2).split("..")
            range[0] = int(x[0])
            range[1] = int(x[1])
            y = m.group(3).split("..")
            range[2] = int(y[0])
            range[3] = int(y[1])
            z = m.group(4).split("..")
            range[4] = int(z[0])
            range[5] = int(z[1])
            instructions.append((m.group(1), range))
    return instructions

def main():
    instructions = parse('input.txt')
    reactor = Reactor(-50, 50)
    for i in instructions:
        reactor.toggle(i[1], True if i[0] == 'on' else False, True)
    print(f'Pt1: {reactor.on_count}')

if __name__ == '__main__':
    main()
