class Node:
    def __init__(self, name) -> None:
        self.name = name
        self.kind = Node._getKind(name)
        self.paths = []
        
    @staticmethod
    def _getKind(name):
        import re
        if name == 'start':
            return 'start'
        if name == 'end':
            return 'end'
        if re.match("[A-Z]+", name):
            return 'big'
        if re.match("[a-z]+", name):
            return 'small'
        
    def addPath(self, node):
        if not node in self.paths:
            self.paths.append(node)
            
    def __repr__(self) -> str:
        return self.name
    
    def __eq__(self, __o: object) -> bool:
        return self.name == __o.name
        
def parse(file):
    nodes = {}
    
    with open(file, 'r') as f:
        for line in f:
            strip = line.strip().split('-')
            for node in strip:
                if not node in nodes:
                    nodes[node] = Node(node)
            
            nodeA = nodes[strip[0]]
            nodeB = nodes[strip[1]]
            nodeA.addPath(nodeB)
            nodeB.addPath(nodeA)
    
    return nodes

def part1(nodes):
    startNode = nodes['start']
    result = []
    visitNodes(startNode, result)
    print(f'Pt1: {len(result)} paths')

def visitNodes(node: Node, result, visitedNodes = [], pt2Rules = False):
    visitedNodes.append(node)
    if node.kind == 'end':
        result.append(visitedNodes)
    else:
        for nextNode in node.paths:
            if nextNode.kind == 'start':
                continue
            if not pt2Rules and nextNode.kind == 'small' and nextNode in visitedNodes:
                continue
            if pt2Rules and nextNode.kind == 'small' and not canBeNextSmallNodePt2Rules(nextNode, visitedNodes):
                continue
            visitNodes(nextNode, result, visitedNodes.copy(), pt2Rules=pt2Rules)

def canBeNextSmallNodePt2Rules(nextNode, nodes):
    if nextNode.kind != 'small':
        raise Exception
    
    isAlreadyVisited = nextNode in nodes
    singleSmallNodeAppearsMultipleTimes = False
    
    smallNodes = list(filter(lambda n: n.kind == 'small', nodes))
    for smallNode in smallNodes:
        if len(list(filter(lambda n: n.name == smallNode.name, smallNodes))) > 1:
            singleSmallNodeAppearsMultipleTimes = True
            break
    
    return not (isAlreadyVisited and singleSmallNodeAppearsMultipleTimes)

def part2(nodes):
    startNode = nodes['start']
    result = []
    visitNodes(startNode, result, pt2Rules=True)
    print(f'Pt2: {len(result)} paths')

def main():
    nodes = parse('input.txt')
    
    part1(nodes)
    
    part2(nodes)

if __name__ == '__main__':
    main()