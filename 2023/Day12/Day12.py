from functools import cache

def parse(file):
    with open(file, 'r') as f:
        for l in f:
            l = l.strip()
            split = l.split()
            yield (split[0], tuple(int(x) for x in split[1].split(',')))

@cache
def count(cfg, nums):
    if cfg == '':
        return 1 if nums == () else 0
    
    if nums == ():
        return 0 if '#' in cfg else 1
    
    total = 0

    if cfg[0] in '.?': # act as if ? is a dot
        total += count(cfg[1:], nums)
    if cfg[0] in '#?': # act as if ? is a spring
        if nums[0] <= len(cfg) and '.' not in cfg[:nums[0]] and (nums[0] == len(cfg) or cfg[nums[0]] != '#'):
            total += count(cfg[nums[0] + 1:], nums[1:]) 

    return total

def pt1(data):
    total = 0
    for cfg, nums in data:
        total += count(cfg, nums)
    return total

def pt2(data):
    total = 0
    for cfg, nums in data:
        cfg_new = '?'.join([cfg] * 5)
        nums_new = nums * 5
        total += count(cfg_new, nums_new)
    return total

def main():
    data = list(parse('test.txt'))
    assert pt1(data) == 21
    assert pt2(data) == 525152
    data = list(parse('input.txt'))
    print(pt1(data))
    print(pt2(data))

if __name__ == '__main__':
    main()
