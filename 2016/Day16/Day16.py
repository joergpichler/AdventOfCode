def fill(input: str, target_length):
    result = input
    while(len(result) < target_length):
        a = [c for c in result]
        b = a.copy()
        b.reverse()
        for (idx, element) in enumerate(b):
            b[idx] = "0" if element == "1" else "1"
        result = "".join(a) + "0" + "".join(b)
    return result

def calc_checksum(input: str):
    if len(input) % 2 != 0:
        raise Exception("input length not dividable by 2")

    while(len(input) % 2 == 0):
        pairs = []
        for i in range(0, len(input), 2):
            pairs.append(input[i:i+2])
        input = ""
        for p in pairs:
            if(p[0] == p[1]):
                input += "1"
            else:
                input += "0"
    return input

def fill_and_calc_checksum(input: str, target_length):
    filled = fill(input, target_length)
    if(len(filled) > target_length):
        filled = filled[:target_length]
    checksum = calc_checksum(filled)
    return checksum

def test():
    assert fill("1", 3) == "100"
    assert fill("0", 3) == "001"
    assert fill("11111", len("11111000000")) == "11111000000"
    assert fill("111100001010", len("1111000010100101011110000")) == "1111000010100101011110000"

    assert calc_checksum("110010110100") == "100"

    assert fill_and_calc_checksum("10000", 20) == "01100"

def main():
    # test()

    result = fill_and_calc_checksum("11110010111001001", 272)
    print(f'Pt1: {result}')
    result = fill_and_calc_checksum("11110010111001001", 35651584)
    print(f'Pt2: {result}')

if __name__ == '__main__':
    main()
