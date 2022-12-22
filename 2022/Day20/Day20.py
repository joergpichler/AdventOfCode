class LinkedListItem:
    def __init__(self, item) -> None:
        self.item = item
        self.next = None
        self.previous = None

    def __repr__(self) -> str:
        return str(self.item)

class LinkedList:
    def __init__(self) -> None:
        self.first_item = None
        self._length = 0

    def add(self, item):
        new_item = LinkedListItem(item)
        if self.first_item is None:
            self.first_item = new_item
        elif self.first_item.next is None and self.first_item.previous is None:
            self.first_item.next = new_item
            self.first_item.previous = new_item
            new_item.previous = self.first_item
            new_item.next = self.first_item
        else:
            last_item = self.first_item.previous
            new_item.previous = last_item
            new_item.next = self.first_item
            last_item.next = new_item
            self.first_item.previous = new_item
        self._length += 1

    def __iter__(self):
        return LinkedListIterator(self)

    def move_item(self, item, offset):
        # check if item is part of the list
        passed = False
        for elem in self:
            if elem is item:
                passed = True
                break
        if not passed:
            raise Exception
        if offset == 0:
            return
        
        if abs(offset) >= self._length:
            if offset > 0:
                minimized_offset = offset % (self._length - 1)
                pass
            elif offset < 0:
                minimized_offset = (abs(offset) % (self._length - 1)) * -1
            else:
                raise Exception
        else:
            minimized_offset = offset

        if minimized_offset > 0:
            for _ in range(minimized_offset):
                self._move_forward(item)
        elif minimized_offset < 0:
            for _ in range(int(abs(minimized_offset))):
                self._move_backward(item)

    def _move_forward(self, item: LinkedListItem):    
        item.previous.next = item.next
        item.next.previous = item.previous
        item.previous = item.next
        item.next = item.next.next
        item.previous.next = item
        item.next.previous = item

    def _move_backward(self, item: LinkedListItem):
        item.previous.next = item.next
        item.next.previous = item.previous
        item.next = item.previous
        item.previous = item.previous.previous
        item.previous.next = item
        item.next.previous = item

class LinkedListIterator:
    def __init__(self, linked_list: LinkedList) -> None:
        self._linked_list = linked_list
        self._current_item = self._linked_list.first_item
        self._iteration_started = False

    def __next__(self) -> LinkedListItem:
        if self._current_item is None:
            raise StopIteration

        if self._iteration_started and self._current_item is self._linked_list.first_item:
            raise StopIteration

        self._iteration_started = True

        item = self._current_item

        self._current_item = item.next
        
        return item

def parse(file):
    linked_list = LinkedList()
    with open(file, 'r') as f:
        for l in f:
            number = int(l.strip())
            linked_list.add(number)
    return linked_list

def calc_coords(linked_list: LinkedList):
    item = None
    for elem in linked_list:
        if elem.item == 0:
            item = elem
            break
    if item is None:
        raise Exception
    results = []
    for _ in range(3):
        for _ in range(1000):
            item = item.next
        results.append(item.item)
    return sum(results)

def mix(linked_list: LinkedList, times = 1):
    original_list = list(linked_list)
    for _ in range(times):
        for item in original_list:
            linked_list.move_item(item, item.item)
    return calc_coords(linked_list)

def decrypt(linked_list: LinkedList):
    for item in linked_list:
        item.item *= 811589153

def main():
    linked_list = parse('test.txt')
    assert mix(linked_list) == 3
    linked_list = parse('test.txt')
    decrypt(linked_list)
    assert mix(linked_list, 10) == 1623178306

    linked_list = parse('input.txt')
    assert mix(linked_list) == 19559
    linked_list = parse('input.txt')
    decrypt(linked_list)
    print(f'{mix(linked_list, 10)}')

if __name__ == '__main__':
    main()
