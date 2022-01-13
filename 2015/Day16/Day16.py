class Sue:
    def __init__(self, str) -> None:
        import re
        
        spl = str.split(':')
        self.nr = int(spl[0].split(' ')[1])
        
        self.props = {}
        for p in str[len(spl[0])+1:].split(','):
            match = re.match(r'(.+?):\s(\d+)', p.strip())
            self.props[match.group(1)] = int(match.group(2))
        
        pass
        
    def __repr__(self) -> str:
        return f'{self.nr} {self.props}'

def parse(file):
    with open(file, 'r') as f:
        return [Sue(l) for l in f]

def main():
    scan = {'children': 3, 'cats': 7, 'samoyeds': 2, 'pomeranians': 3, 'akitas': 0, 'vizslas': 0, 'goldfish': 5, 'trees' : 3, 'cars': 2, 'perfumes' : 1}
    
    sues = parse('input.txt')
    
    for sue in sues:
        matches = True
        for p,v in scan.items():
            if p in sue.props and sue.props[p] != v:
                matches = False
        if matches:
            break
    
    print(f'Pt1: {sue.nr}')
    
    for sue in sues:
        matches = True
        for p,v in scan.items():
            if p in ['cats', 'trees'] and p in sue.props:
                if sue.props[p] <= v:
                    matches = False
            elif p in ['pomeranians', 'goldfish'] and p in sue.props:
                if sue.props[p] >= v:
                    matches = False
            elif p in sue.props and sue.props[p] != v:
                matches = False
        if matches:
            break
        
    print(f'Pt2: {sue.nr}')

if __name__ == '__main__':
    main()
