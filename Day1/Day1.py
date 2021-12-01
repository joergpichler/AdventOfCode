def CalcNoOfIncreases(list):
    # use zip to create two shifted lists and calc diff between each element
    diff = [j - i for i, j in zip(list[:-1], list[1:])]
    # generator generates 1 for positive elements, so sum equals no of positive elements
    return sum([i > 0 for i in diff])

testFile = open('input.txt', 'r')
depths = list(map(int, testFile.readlines())) # map strings to int

print(f"Part 1: {CalcNoOfIncreases(depths)} increases")

windowSize = 3
windowSums = []

# use range and slice array into windowSize chunks
for i in range(len(depths) - windowSize + 1):
    windowSums.append(sum(depths[i:i + windowSize]))
    
print(f"Part 2: {CalcNoOfIncreases(windowSums)} increases")