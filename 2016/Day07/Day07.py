class IpAddress:
    def __init__(self, str) -> None:
        self.str = str

    def _contains_abba(s):
        for i in range(0, len(s) - 3):
                first_char = s[i]
                second_char = s[i + 1]
                if second_char == first_char:
                    continue
                if s[i + 2] == second_char and s[i + 3] == first_char:
                    return True
        return False

    def _get_abas(s):
        for i in range(0, len(s) - 2):
                first_char = s[i]
                second_char = s[i + 1]
                if second_char == first_char:
                    continue
                if s[i + 2] == first_char:
                    yield s[i:i + 3]

    def _aba_to_bab(aba):
        return f'{aba[1]}{aba[0]}{aba[1]}'

    def _get_supernet_sequences(self):
        import re
        # replace all hypernet sequences and return the remaining elements
        return re.sub("\[.+?\]", " ", self.str).split(" ")

    def _get_hypernet_sequences(self):
        import re
        return re.findall("\[(.+?)\]", self.str)

    def supports_tls(self):
        abba_in_supernet = False

        for supernet_sequence in self._get_supernet_sequences():
            if IpAddress._contains_abba(supernet_sequence):
                abba_in_supernet = True
                break

        if not abba_in_supernet:
            return False
        
        abba_in_hypernet = False

        for hypernet_sequence in self._get_hypernet_sequences():
            if IpAddress._contains_abba(hypernet_sequence):
                abba_in_hypernet = True
                break

        return not abba_in_hypernet

    def supports_ssl(self):
        abas = []

        for supernet_seqeuence in self._get_supernet_sequences():
            for aba in IpAddress._get_abas(supernet_seqeuence):
                abas.append(aba)
        
        if len(abas) == 0:
            return False

        for hypernet_sequence in self._get_hypernet_sequences():
            for bab in (IpAddress._aba_to_bab(aba) for aba in abas):
                if bab in hypernet_sequence:
                    return True 

        return False

def parse(file):
    with open(file, 'r') as f:
        return [IpAddress(l.strip()) for l in f]

def test():
    data = parse('test.txt')
    count = sum((i.supports_tls() for i in data))
    assert count == 2
    data = parse('test2.txt')
    count = sum((i.supports_ssl() for i in data))
    assert count == 3

def main():
    test()
    
    data = parse('input.txt')
    count = sum((i.supports_tls() for i in data))
    print(f'Pt1: {count}')
    count = sum((i.supports_ssl() for i in data))
    print(f'Pt2: {count}')

if __name__ == '__main__':
    main()
