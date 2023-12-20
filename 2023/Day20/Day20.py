import regex as re
import math

class Button:
    def __init__(self) -> None:
        self.id = 'button'
        self.targets = ['broadcaster']

    def __repr__(self) -> str:
        return f'Button -> broadcaster'
    
    def trigger(self, source, pulse):
        yield 0

class Broadcaster:
    def __init__(self, targets) -> None:
        self.id = 'broadcaster'
        self.targets = targets
    
    def __repr__(self) -> str:
        return f'Broadcaster -> {self.targets}'
    
    def trigger(self, source, pulse):
        yield pulse
    
class FlipFlop:
    def __init__(self, id, targets) -> None:
        self.id = id
        self.targets = targets
        self.state = 0
    
    def __repr__(self) -> str:
        return f'FlipFlop {self.id} -> {self.targets}'
    
    def trigger(self, source, pulse):
        if pulse == 1:
            return
        if self.state == 0:
            self.state = 1
            yield 1
        elif self.state == 1:
            self.state = 0
            yield 0
    
class Conjunction:
    def __init__(self, id, targets) -> None:
        self.id = id
        self.targets = targets
        self._inputs = {}

    def __repr__(self) -> str:
        return f'Conjunction {self.id} -> {self.targets} [{self._inputs}]'
    
    def add_input(self, id):
        self._inputs[id] = 0

    def trigger(self, source, pulse):
        if not source in self._inputs:
            raise Exception
        self._inputs[source] = pulse
        if sum((1 for x in self._inputs.values() if x)) == len(self._inputs):
            yield 0
        else:
            yield 1

class ObservingConjunction(Conjunction):
    def __init__(self, conjunction, callback) -> None:
        super().__init__(conjunction.id, conjunction.targets)
        self._inputs = conjunction._inputs
        self._callback = callback        

    def trigger(self, source, pulse):
        if not source in self._inputs:
            raise Exception
        self._callback(source, pulse)
        self._inputs[source] = pulse
        if sum((1 for x in self._inputs.values() if x)) == len(self._inputs):
            yield 0
        else:
            yield 1

class PulseQueue:
    def __init__(self) -> None:
        self.queue = []
        self.low_pulses = 0
        self.high_pulses = 0

    def addPulse(self, module, pulse_value):
        if pulse_value == 0:
            self.low_pulses += len(module.targets)
        elif pulse_value == 1:
            self.high_pulses += len(module.targets)
        else:
            raise Exception
        
        self.queue.append((module.id, module.targets, pulse_value))

    def hasPulses(self):
        return len(self.queue) > 0
    
    def getPulse(self):
        pulse = self.queue.pop(0)        
        return pulse

class System:
    def __init__(self, modules) -> None:
        self.modules = {x.id: x for x in modules}
        self.modules['button'] = Button()

        for conjunction in (x for x in modules if isinstance(x, Conjunction)):
            for module in (y for y in self.modules.values() if conjunction.id in y.targets):
                conjunction.add_input(module.id)

    def run(self, part2 = False):
        if part2:
            cycles = {}
            def callback(source, pulse):
                nonlocal cycles
                nonlocal i
                if pulse and cycles[source] == 0:
                    #print(f'{source}: {i}')
                    cycles[source] = i + 1
                if all(x != 0 for x in cycles.values()):
                    print(f'{math.lcm(*cycles.values())}')
                    raise Exception

            prev_rx_module = next(x for x in self.modules.values() if 'rx' in x.targets)
            replacement = ObservingConjunction(prev_rx_module, callback)
            self.modules[replacement.id] = replacement
            cycles = { x:0 for x in replacement._inputs }

        queue = PulseQueue()
        iterations = 1000 if not part2 else 10000000000000
        for i in range(iterations):            
            queue.addPulse(self.modules['button'], next(self.modules['button'].trigger(None, None)))
            while queue.hasPulses():
                source, targets, pulse_value = queue.getPulse()
                for target in targets:
                    if target not in self.modules:
                        #print(f'{source} {pulse_value} -> {target}')
                        continue
                    module = self.modules[target]
                    #print(f'{source} {pulse_value} -> {module.id}')
                    pulses = list(module.trigger(source, pulse_value))
                    for pulse in pulses:
                        queue.addPulse(module, pulse)
            #print()
            pass
        return queue.low_pulses * queue.high_pulses

def module_factory(line):
    match = re.match(r'(.+)\s->\s(.+)', line)
    if not match:
        raise Exception
    id = match.groups()[0]        
    targets = [x.strip() for x in match.groups()[1].split(',')]
    if id == 'broadcaster':
        return Broadcaster(targets)
    elif id[0] == '%':
        return FlipFlop(id[1:], targets)
    elif id[0] == '&':
        return Conjunction(id[1:], targets)
    else:
        raise Exception

def parse(file):
    with open(file, 'r') as f:
        return [module_factory(l.strip()) for l in f]

def main():
    modules = parse('test.txt')
    assert System(modules).run() == 32000000
    modules = parse('test2.txt')
    assert System(modules).run() == 11687500
    modules = parse('input.txt')
    print(System(modules).run())
    try:
        modules = parse('input.txt')
        System(modules).run(True)
    except:
        pass
if __name__ == '__main__':
    main()
