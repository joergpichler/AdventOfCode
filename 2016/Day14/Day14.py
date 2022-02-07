from typing import Callable


def calculate_hash(text: str):
    import hashlib
    hash = hashlib.md5(text.encode())
    return hash.hexdigest()


def calculate_hash_2016(text: str):
    for _ in range(2017):
        text = calculate_hash(text)
    return text


def parse(file):
    with open(file, 'r') as f:
        pass


def get_triple(text:str):
    import re
    pattern = re.compile(r"([0-9a-f])\1{2}")
    matches = pattern.findall(text)
    if matches:
        return matches[0]
    return ''


def calc_keys(salt: str, count: int, hashfunc: Callable):
    keys = []

    counter = 0
    candidates = []
    collect_candidates = True
    
    while len(keys) < count or len(candidates) > 0:
        to_remove = set()

        hash = hashfunc(f'{salt}{counter}')
        triple_char = get_triple(hash)

        for i, candidate in enumerate(candidates):
            if counter > candidate[0] + 1000:
                to_remove.add(i)
            elif candidate[1] * 5 in hash:
                keys.append(candidate[0])
                to_remove.add(i)

        if triple_char and collect_candidates:
            candidates.append((counter, triple_char))

        for i in sorted(to_remove, reverse=True):
            del candidates[i]

        if len(keys) >= count:
            collect_candidates = False

        counter += 1

    return list(sorted(keys))[:64]


def test():
    assert calc_keys('abc', 64, calculate_hash)[63] == 22728

    assert calculate_hash_2016('abc0') == 'a107ff634856bb300138cac6568c0f24'
    assert calc_keys('abc', 64, calculate_hash_2016)[63] == 22551


def main():
    test()
    index = calc_keys('cuanljph', 64, calculate_hash)[63]
    print(f'Pt1: {index}')
    index = calc_keys('cuanljph', 64, calculate_hash_2016)[63]
    print(f'Pt2: {index}')


if __name__ == '__main__':
    main()
