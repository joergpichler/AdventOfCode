import json

def parse(file):
    with open(file, 'r') as f:
        return f.readline().strip()

def get_json_sum(j, discardRed: bool):
    sum = 0
    if isinstance(j, dict):
        for _, v in j.items():
            if discardRed and v == "red":
                return 0
            else:
                sum += get_json_sum(v, discardRed)
    elif isinstance(j, list):
        for i in j:
            sum += get_json_sum(i, discardRed)
    elif isinstance(j, int):
        sum += j
    else:
        pass
        
    return sum

def sum_numbers(text: str, discardRed: bool = False):
    j = json.loads(text)
    return get_json_sum(j, discardRed)

def main():
    assert sum_numbers('[1,2,3]') == 6
    assert sum_numbers('{"a":2,"b":4}') == 6
    assert sum_numbers('[[[3]]]') == 3
    assert sum_numbers('{"a":{"b":4},"c":-1}') == 3
    assert sum_numbers('{"a":[-1,1]}') == 0
    assert sum_numbers('[-1,{"a":1}]') == 0
    assert sum_numbers('[]') == 0
    assert sum_numbers('{}') == 0
    
    json = parse('input.txt')
    
    print(f'Pt1: {sum_numbers(json)}')
    
    assert sum_numbers('[1,2,3]', True) == 6
    assert sum_numbers('[1,{"c":"red","b":2},3]', True) == 4
    assert sum_numbers('{"d":"red","e":[1,2,3,4],"f":5}', True) == 0
    assert sum_numbers('[1,"red",5]', True) == 6
    
    print(f'Pt2: {sum_numbers(json, True)}')

if __name__ == '__main__':
    main()
