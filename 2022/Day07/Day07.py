class Directory:
    def __init__(self, name: str, parent) -> None:
        self.name = name
        self.parent = parent
        self.files = []
        self.directories = []

    def getdir(self, name):
        if name == '..':
            return self.parent
    
        dir = next((d for d in self.directories if d.name == name), None)

        return dir

    def mkdir(self, name):
        dir = self.getdir(name)
        if dir is not None:
            raise Exception
        self.directories.append(Directory(name, self))

    def touch(self, name, size):
        file = next((f for f in self.files if f.name == name), None)
        if file is not None:
            raise Exception
        self.files.append(File(name, size, self))

    def __repr__(self) -> str:
        return self.name

    def get_size(self):
        return sum(map(lambda x: x.size, self.files)) + sum(map(lambda x: x.get_size(), self.directories))
    
class File:
    def __init__(self, name, size, parent) -> None:
        self.name = name
        self.size = size
        self.parent = parent

    def __repr__(self) -> str:
        return self.name

def parse(file):
    root = Directory('root', None)
    cd = None
    ls = False

    with open(file, 'r') as f:
        for l in f:
            l = l.strip()
            if l[0] == '$':
                ls = False
                cmd = l.split(' ')
                if cmd[1] == 'cd':
                    if cmd[2] == '/':
                        cd = root
                    else:
                        cd = cd.getdir(cmd[2])
                elif cmd[1] == 'ls':
                    ls = True
                    continue
            else:
                if not ls:
                    raise Exception
                e = l.split(' ')
                if e[0] == 'dir':
                    cd.mkdir(e[1])
                else:
                    cd.touch(e[1], int(e[0]))
                
    return root

def walk_dirs(directory, func):
    func(directory)
    for subdir in directory.directories:
        walk_dirs(subdir, func)

def pt1(directory):
    total_size = 0
    def func(d):
        size = d.get_size()
        if size <= 100000:
            nonlocal total_size
            total_size += size
    walk_dirs(directory, func)
    return total_size

def pt2(directory):
    total_disk_space = 70000000
    needed_disk_space = 30000000

    free_disk_space = total_disk_space - directory.get_size()
    size_to_delete = needed_disk_space - free_disk_space

    if size_to_delete < 0:
        raise Exception

    candidates = []

    def func(d):
        nonlocal size_to_delete
        if d.get_size() >= size_to_delete:
            candidates.append(d)

    walk_dirs(directory, func)

    return sorted(candidates, key=lambda d: d.get_size())[0].get_size()

def main():
    root = parse('test.txt')
    assert pt1(root) == 95437
    assert pt2(root) == 24933642
    
    root = parse('input.txt')
    print(f'{pt1(root)}')
    print(f'{pt2(root)}')
    pass

if __name__ == '__main__':
    main()
