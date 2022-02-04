class CompressedData:
    def __init__(self, data) -> None:
        self.data = data

    @property
    def length_v1(self):
        return self._calc_length(self.data, recursive=False)

    def _calc_length(self, data, multiplicator = 1, recursive = True):
        import re
        
        length = 0
        match = re.search(r"\((\d+)x(\d+)\)", data)
        while match is not None:
            no_of_characters = int(match.group(1))
            repetitions = int(match.group(2))
            start_idx = match.span()[0]
            end_idx = match.span()[1]

            length += start_idx

            sub_data = data[end_idx:end_idx+no_of_characters]

            if recursive:
                length += self._calc_length(sub_data, repetitions)
            else:
                length += repetitions * len(sub_data)

            data = data[end_idx+no_of_characters:]

            match = re.search(r"\((\d+)x(\d+)\)", data)
            
        length += len(data)
        return length * multiplicator

    @property
    def length_v2(self):
        return self._calc_length(self.data)

def test():
    assert CompressedData("ADVENT").length_v1 == 6
    assert CompressedData("A(1x5)BC").length_v1 == 7
    assert CompressedData("(3x3)XYZ") .length_v1== 9
    assert CompressedData("A(2x2)BCD(2x2)EFG").length_v1 == 11
    assert CompressedData("(6x1)(1x3)A").length_v1 == 6
    assert CompressedData("X(8x2)(3x3)ABCY").length_v1 == 18

    assert CompressedData("A(2x2)BCD(2x2)EFGA(2x2)BCD(2x2)EFG").length_v1 == 22

    assert CompressedData('(3x3)XYZ').length_v2 == 9
    assert CompressedData('X(8x2)(3x3)ABCY').length_v2 == 20
    assert CompressedData('(27x12)(20x12)(13x14)(7x10)(1x12)A').length_v2 == 241920
    assert CompressedData('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN').length_v2 == 445

def parse(file):
    with open(file, 'r') as f:
        return f.readline().strip()

def main():
    test()

    compressed_data = CompressedData(parse('input.txt'))

    print(f'Pt1: {compressed_data.length_v1}')
    print(f'Pt2: {compressed_data.length_v2}')

if __name__ == '__main__':
    main()