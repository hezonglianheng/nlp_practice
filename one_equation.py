class Edge:
    """有向边"""

    def __init__(self, start: int, end: int, word: str,
                 weight: float, types: set = None):
        self.word = word
        self.types = types
        self.start = start
        self.end = end
        self.weight = weight

    def get_types(self) -> set:
        return self.types

    def __str__(self):
        line = 'text:' + self.word + ' start:' + \
                str(self.start) + ' end:' + str(self.end) + \
                ' types:' + str(self.types)
        return line


class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:
    """单链表"""

    def __init__(self):
        self.head = None

    def put(self,item):
        self.head = Node(item, self.head)

    def __str__(self):
        temp = self.head
        result = ''
        while temp is not None:
            result += str(temp.data)
            temp = temp.next
        return result

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next


class AdjList:
    """正向邻接链表表示的切分词图"""

    def __init__(self, vertices_num:int):
        self.vertices_num = vertices_num
        self.list = [LinkedList() for i in range(vertices_num)]

    def add_edge(self, new_edge):
        self.list[new_edge.start].put(new_edge)

    def get_edge(self,position:int) -> LinkedList:
        return self.list[position]

    def __str__(self):
        tmp = []
        for r in range(self.vertices_num):
            if not self.list[r]:
                continue
            tmp.append('node:')
            tmp.append(str(r))
            tmp.append(': ')
            tmp.append(str(self.list[r]))
            tmp.append('\n')
        return ' '.join(tmp)


if __name__ == '__main__':
    word1 = Edge(2, 3, '见', 2.0)
    word2 = Edge(1, 3, "意见", 3.0)
    word_list = LinkedList()
    word_list.put(word1)
    word_list.put(word2)
    for i in word_list:
        print(i)

