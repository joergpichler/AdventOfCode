import sys
import os

def get_template():
    return """import numpy as np

def parse(file):
    with open(file, 'r') as f:
        pass

def main():
    data = parse('test.txt')
    pass

if __name__ == '__main__':
    main()
"""

def main(argv):
    if len(argv) != 3:
        raise Exception
    year = int(argv[1])
    day = int(argv[2])
    
    day = 'Day' + str(day).zfill(2)
    
    os.mkdir(fr'{year}/{day}')
    open(fr'{year}/{day}\input.txt', 'w').close()
    open(fr'{year}/{day}\test.txt', 'w').close()
    with open(fr'{year}/{day}\{day}.py', 'w') as f:
        f.write(get_template())

if __name__ == '__main__':
    main(sys.argv)