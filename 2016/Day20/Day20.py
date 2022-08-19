import re

def parse(file):
    
    def line_to_tuple(l):
        match = re.findall('\d+', l)
        return (int(match[0]), int(match[1]))

    with open(file, 'r') as f:
        lines = [line_to_tuple(l) for l in f]
    
    return sorted(lines, key=lambda x:x[0])


def determine_lowest_ip(ips):
    for i in range(len(ips)):
        item = ips[i]
        lowest = item[1] + 1

        for j in range(len(ips)):
            inner_item = ips[j]
            if lowest < inner_item[0]:
                return lowest
            if inner_item[0] <= lowest and inner_item[1] >= lowest:
                break
    
    raise Exception


def determine_allowed_ip_count(ips, max = 4294967295):
    allowed_ranges = [(0, max)]

    for r in ips:
        
        r_including_lower = next(filter(lambda x: x[0] <= r[0] and x[1] >= r[0],  allowed_ranges), None)
        r_including_upper = next(filter(lambda x: x[0] <= r[1] and x[1] >= r[1],  allowed_ranges), None)
        
        l = r[0]
        h = r[1]

        if r_including_lower == None and not r_including_upper == None:
            idx = allowed_ranges.index(r_including_upper)
            if h == r_including_upper[1]:
                allowed_ranges.pop(idx)
            else:
                new_range = (h + 1, r_including_upper[1])
                allowed_ranges.pop(idx)
                allowed_ranges.insert(idx, new_range)
        elif r_including_upper == None and not r_including_lower == None:
            idx = allowed_ranges.index(r_including_lower)
            raise Exception
        elif r_including_lower == None and r_including_upper == None:
            pass # can be ignored since range is not allowed anymore
        elif r_including_lower == r_including_upper:
            idx = allowed_ranges.index(r_including_lower)
            if r_including_lower[0] == l and r_including_lower[1] == h: # both edges are the same
                allowed_ranges.pop(idx)
            elif r_including_lower[0] == l: # only low is the same -> new range is defined by upper limits
                new_range = (h + 1, r_including_lower[1])
                allowed_ranges.pop(idx)
                allowed_ranges.insert(idx, new_range)
            elif r_including_lower[1] == h: # only high is the same
                new_range = (r_including_lower[0], l - 1)
                allowed_ranges.pop(idx)
                allowed_ranges.insert(idx, new_range)
            else:
                new_range_1 = (r_including_lower[0], l - 1)
                new_range_2 = (h + 1, r_including_lower[1])
                allowed_ranges.pop(idx)
                allowed_ranges.insert(idx, new_range_2)
                allowed_ranges.insert(idx, new_range_1)
        else:
            raise Exception

    return sum(map(lambda x: x[1]-x[0]+1, allowed_ranges))

def main():
    ips = parse('test.txt')
    lowest_ip = determine_lowest_ip(ips)
    assert lowest_ip == 3
    allowed = determine_allowed_ip_count(ips, 10)
    assert allowed == 3

    ips = parse('input.txt')
    lowest_ip = determine_lowest_ip(ips)
    print(f'Pt1: {lowest_ip}')

    allowed = determine_allowed_ip_count(ips)
    print(f'Pt2: {allowed}')

if __name__ == '__main__':
    main()
