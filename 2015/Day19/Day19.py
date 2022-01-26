def parse(file):
    dict = {}
    with open(file, 'r') as f:
        line = f.readline().strip()
        while line != '':
            split = line.split('=>')
            key = split[0].strip()
            value = split[1].strip()
            if not key in dict:
                dict[key] = []
            dict[key].append(value)
            line = f.readline().strip()
        molecule = f.readline().strip()
    return molecule, dict

def replace_at(original_string, index, replacement, len = 1):
    return original_string[:index] + replacement + original_string[index+len:]

def get_distinct_molecules(molecule: str, dict):
    molecules = set()
    idx = 0
    while idx < len(molecule):
        inc = 1
        c = molecule[idx]
        if not c in dict and molecule[idx:idx+2] in dict:
            c = molecule[idx:idx+2]
            inc = 2
        if c in dict:
            possibilities = dict[c]
            for p in possibilities:
                m = replace_at(molecule, idx, p, len(c))
                molecules.add(m)
        idx += inc
    return len(molecules)

def get_steps(molecule: str, dict: dict):
    tmp = {}
    for k,v in dict.items():
        for i in v:
            tmp[i] = k
    dict = tmp
    steps = 0
    
    while molecule != 'e':
        original = molecule
        for k, v in dict.items():
            if v == 'e' and k == molecule:
                steps += 1
                molecule = 'e'
            elif v == 'e':
                continue
            if k in molecule:
                molecule = molecule.replace(k, v, 1)
                steps += 1
        if original == molecule:
            raise Exception()

    return steps

def main():
    assert replace_at("abc", 1, "dd") == "addc"
    assert replace_at("abcd", 1, "dd", 2) == "addd"
    
    molecule, dict = parse('test.txt')
    
    assert get_distinct_molecules(molecule, dict) == 4
    assert get_steps(molecule, dict) == 3
    
    molecule, dict = parse('test2.txt')
    
    assert get_distinct_molecules(molecule, dict) == 7
    assert get_steps(molecule, dict) == 6
    
    molecule, dict = parse('input.txt')
    
    print(f'Pt1: {get_distinct_molecules(molecule, dict)}')
    print(f'Pt2: {get_steps(molecule, dict)}')
    
if __name__ == '__main__':
    main()
