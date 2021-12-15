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
    if len(argv) != 2:
        raise Exception
    day = int(argv[1])
    
    dir = 'Day' + str(day)
    os.mkdir(dir)
    open(fr'{dir}\input.txt', 'w').close()
    open(fr'{dir}\test.txt', 'w').close()
    with open(fr'{dir}\{dir}.py', 'w') as f:
        f.write(get_template())

if __name__ == '__main__':
    main(sys.argv)