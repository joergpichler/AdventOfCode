from typing import List

def flipBits(bits: List[str]):
    result = []
    
    for i in range(0, len(bits)):
        if bits[i] == '1':
            result.append('0')
        elif bits[i] == '0':
            result.append('1')
        else:
            raise Exception
    
    return result

def getMostCommonBitAtPos(binaries: List[str], pos: int):
    zeroes = 0
    ones = 0
    
    for binary in binaries:
        bit = binary[pos]
        if bit == '0':
            zeroes += 1
        elif bit == '1':
            ones += 1
        else:
            raise Exception
        
    if zeroes > ones:
        return '0'
    elif ones > zeroes:
        return '1'
    else:
        return '-1'

def getEntriesWithBitAtPos(binaries: List[str], bit: str, pos: int):
    filtered = filter(lambda x: x[pos] == bit, binaries)
    return list(filtered)

def getGammaAndEpsilonRate(binaries: List[str]):
    length = len(binaries[0])
    
    mostCommonBits = [0 for x in range(length)]
    
    for i in range(0, length):
        mostCommonBits[i] = getMostCommonBitAtPos(binaries, i)
    
    gamma = ''.join(map(str, mostCommonBits))
    epsilon = ''.join(map(str, flipBits(mostCommonBits)))
    
    return [gamma, epsilon]

def getOxygenRating(binaries: List[str]):
    for i in range(len(binaries[0])):
        if len(binaries) == 1:
            break
        mostCommonBit = getMostCommonBitAtPos(binaries, i)
        if(mostCommonBit == '-1'):
            mostCommonBit = '1'
        binaries = getEntriesWithBitAtPos(binaries, mostCommonBit, i)
    
    if len(binaries) != 1:
        raise Exception
    
    return binaries[0]

def getCO2Rating(binaries: List[str]):
    for i in range(len(binaries[0])):
        if len(binaries) == 1:
            break
        mostCommonBit = getMostCommonBitAtPos(binaries, i)
        if(mostCommonBit == '1'):
            mostCommonBit = '0'
        elif(mostCommonBit == '0'):
            mostCommonBit = '1'
        elif(mostCommonBit == '-1'):
            mostCommonBit = '0'
        binaries = getEntriesWithBitAtPos(binaries, mostCommonBit, i)
    
    if len(binaries) != 1:
        raise Exception
    
    return binaries[0]

def getOxygenAndCO2Rating(binaries: List[str]):
    return [getOxygenRating(binaries), getCO2Rating(binaries)]
        
def main():
    with open('input.txt', 'r') as f:
        binaries = list(map(lambda x: x.strip(), f.readlines()))
        
    gamma, epsilon = list(map(lambda x: int(x,2), getGammaAndEpsilonRate(binaries)))
    
    print(f"Gamma {gamma} Epsilon {epsilon} Product {gamma * epsilon}")
    
    oxygen, co2 = list(map(lambda x: int(x,2), getOxygenAndCO2Rating(binaries)))
    
    print(f"Oxygen {oxygen} CO2 {co2} Product {oxygen * co2}")

if __name__ == "__main__":
    main()