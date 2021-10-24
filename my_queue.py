import random


class Node:
    def __init__(self, item):
        self.item = item
        self.next = None


class Queue:
    def __init__(self):
        self.head = None
        self.rear = None

    @property
    def is_empty(self):
        return self.head is None

    def enqueue(self, item):
        node = Node(item)
        if self.head is None:
            self.head = node
        else:
            self.rear.next = node
        self.rear = node

    def dequeue(self):
        if self.is_empty:
            raise Exception('Queue empty error!')
        else:
            new_head = self.head.next
            dequeue_item = self.head.item
            self.head = new_head
            return dequeue_item

    def length(self):
        length = 0
        if not self.is_empty:
            current = self.head
            length += 1
            while current.next is not None:
                current = current.next
                length += 1
        return length


if __name__ == '__main__':
    q = Queue()
    for i in range(100):
        num = random.randint(1, 101)
        q.enqueue(num)
    print(q.length())
    while not q.is_empty:
        q.dequeue()
