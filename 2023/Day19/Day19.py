import regex as re

class Workflow:
    def __init__(self, line) -> None:
        match = re.match(r'(.+){(.+)}', line)
        self.id = match.groups()[0]
        self.rules = match.groups()[1].split(',')

    def __repr__(self) -> str:
        return self.id
    
    def run(self, part):
        for rule in self.rules:
            match = re.match(r'([xmas])([<>])(\d+):(\w+)', rule)
            if match:
                part_value = part.dict[match.groups()[0]]
                comparison = match.groups()[1]
                comparison_value = int(match.groups()[2])
                next_workflow = match.groups()[3]
                if comparison == '<':
                    if part_value < comparison_value:
                        return next_workflow
                elif comparison == '>':
                    if part_value > comparison_value:
                        return next_workflow
            else:
                return rule

class Part:
    def __init__(self, line) -> None:
        self.dict = {}
        matches = re.findall(r'[xmas]=\d+', line)
        for match in matches:
            split = match.split('=')
            self.dict[split[0]] = int(split[1])
    
    def __repr__(self) -> str:
        return self.dict.__repr__()
    
    @property
    def rating(self):
        return sum(self.dict.values())

def parse(file):
    workflows = {}
    parts = []
    with open(file, 'r') as f:
        line = f.readline().strip()
        while line:
            workflow = Workflow(line)
            workflows[workflow.id] = workflow
            line = f.readline().strip()

        line = f.readline().strip()
        while line:
            parts.append(Part(line))
            line = f.readline().strip()
    return parts, workflows

def runWorkflow(part, workflows):
    def _runWorkflow(part, workflow_name, workflows):
        workflow = workflows[workflow_name]
        return workflow.run(part)

    next_workflow = _runWorkflow(part, 'in', workflows)
    while next_workflow != 'A' and next_workflow != 'R':
        next_workflow = _runWorkflow(part, next_workflow, workflows)
    return next_workflow

def pt1(parts, workflows):
    total = 0
    for part in parts:
        result = runWorkflow(part, workflows)
        if result == 'A':
            total += part.rating
    return total

def main():
    parts, workflows = parse('test.txt')
    assert pt1(parts, workflows) == 19114
    parts, workflows = parse('input.txt')
    print(pt1(parts, workflows))

if __name__ == '__main__':
    main()
