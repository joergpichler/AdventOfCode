import regex as re

class Workflow:
    def __init__(self, line) -> None:
        match = re.match(r'(.+){(.+)}', line)
        self.id = match.groups()[0]
        self.rules = match.groups()[1].split(',')
        self.enter_rules = []

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

def enter_workflow(workflow, workflows, enter_rules, result):
    for rule in enter_rules:
        workflow.enter_rules.append(rule)

    for i in range(len(workflow.rules)):
        rule = workflow.rules[i]
        # todo add inverse rules of previous rules
        enter_rules = [x for x in workflow.enter_rules]
        for prev_rule in workflow.rules[:i]:
            match = re.match(r'([xmas])([<>])(\d+):\w+', prev_rule)
            if not match:
                raise Exception
            num = int(match.groups()[2])
            if match.groups()[1] == '<':
                sign = '>'
                num -= 1
            elif match.groups()[1] == '>':
                sign = '<'
                num += 1
            inverted_rule = f'{match.groups()[0]}{sign}{num}'
            enter_rules.append(inverted_rule)
        match = re.match(r'([xmas][<>]\d+):(\w+)', rule)
        if match:
            enter_rules.append(match.groups()[0])
            next_workflow_id = match.groups()[1]
        else:
            next_workflow_id = rule

        if next_workflow_id == 'A':
            result.append(enter_rules)
            continue
        elif next_workflow_id == 'R':
            continue
        else:
            next_workflow = workflows[next_workflow_id]
            enter_workflow(next_workflow, workflows, enter_rules, result)

def calc_result(results):
    total = 0

    for rules in results:
        x = [True] * 4000
        m = [True] * 4000
        a = [True] * 4000
        s = [True] * 4000

        for rule in rules:
            if rule[0] == 'x':
                l = x
            elif rule[0] == 'm':
                l = m
            elif rule[0] == 'a':
                l = a
            elif rule[0] == 's':
                l = s
            else:
                raise Exception
            
            match = re.match(r'\w([<>])(\d+)', rule)
            num = int(match.groups()[1])
            if match.groups()[0] == '<':
                for i in range(num - 1, len(l)):
                    l[i] = False
            elif match.groups()[0] == '>':
                for i in range(num):
                    l[i] = False
                pass
            else:
                raise Exception
            pass

        t_x = len([1 for y in x if y])
        t_m = len([1 for x in m if x])
        t_a = len([1 for x in a if x])
        t_s = len([1 for x in s if x])
        total +=  t_x * t_m  * t_a * t_s 
    
    return total

def pt2(workflows):
    workflow = workflows['in']
    result = []
    enter_workflow(workflow, workflows, [], result)
    return calc_result(result)

def main():
    parts, workflows = parse('test.txt')
    assert pt1(parts, workflows) == 19114
    assert pt2(workflows) == 167409079868000
    parts, workflows = parse('input.txt')
    print(pt1(parts, workflows))
    print(pt2(workflows))

if __name__ == '__main__':
    main()