# encoding:utf8
import pickle

start_word = "始？？始"
end_word = '末？？末'


class RelationInfo:
    """表示每一条二元关系的类"""

    def __init__(self, pre_word: str, next_word: str,
                 freq: int = 0):
        self.pre = pre_word
        self.next = next_word
        self.freq = freq


class WordInfo:
    """表示每个词的类"""

    def __init__(self, word: str, freq: int = 0,
                 types: set = None):
        self.word = word
        self.freq = freq
        self.types = types
        self._connections = []  # 存放代表后继的RelationInfo类

    def add_connection(self, connection: RelationInfo):
        self._connections.append(connection)

    def get_connection(self) -> list:
        return self._connections


class Node:
    """表示词典中节点的类"""

    def __init__(self, char_num: int):
        self.char_num = char_num
        self.left = None
        self.mid = None
        self.right = None
        self.data = None  # 保存WordInfo类数据


class Dictionary:
    """表示词语关系的字典"""

    def __init__(self):
        try:
            file = open('dictionary.dat', 'rb+')
        except FileNotFoundError:
            file = open('dictionary.dat', 'wb+')
            self.root = None
            self.word_create(start_word)  # 创建起始词节点
            self.basic_create('word_frequency.txt')
            self.relation_create('relation_frequency.txt')
            pickle.dump(self, file)
            file.close()
        else:
            saved_dic = pickle.load(file)
            # save_dic 是另一个Dictionary对象
            self.root = saved_dic.root
            file.close()

    def basic_create(self, file: str):
        file = open(file, 'r', encoding='utf8')
        word_list = file.readlines()
        file.close()
        for item in word_list:
            item_str = item[:-1]
            lst1 = item_str.split(':')
            freq = int(lst1[-1])
            lst2 = lst1[0].split('/')
            word = lst2[0]
            types = set(lst2[-1])
            self.word_create(word, freq, types)

    def word_create(self, word: str, freq: int = 0,
                    types: set = None):
        char_index = 0
        if len(word) > char_index:
            current_ch_num = ord(word[char_index])
        else:
            return None
        if self.root is None:
            self.root = Node(current_ch_num)
            self.root.data = WordInfo(word[char_index])
        current_node = self.root
        while True:
            compare = current_ch_num - current_node.char_num
            if compare == 0:
                char_index += 1
                if char_index == len(word):
                    current_node.data = WordInfo(word, freq,
                                                 types)
                    break
                else:
                    current_ch_num = ord(word[char_index])
                    if current_node.mid is None:
                        current_node.mid = Node(current_ch_num)
                    current_node = current_node.mid
            elif compare > 0:
                if current_node.right is None:
                    current_node.right = Node(current_ch_num)
                current_node = current_node.right
            else:
                if current_node.left is None:
                    current_node.left = Node(current_ch_num)
                current_node = current_node.left

    def search(self, text: str):
        if self.root is None:
            return None
        current_node = self.root
        char_index = 0
        if len(text) > char_index:
            current_ch_num = ord(text[char_index])
        else:
            return None
        while True:
            compare = current_ch_num - current_node.char_num
            if compare == 0:
                char_index += 1
                if char_index == len(text):
                    return current_node
                current_ch_num = ord(text[char_index])
                if current_node.mid is None:
                    raise ValueError('输入的词不存在！')
                current_node = current_node.mid
            elif compare > 0:
                if current_node.right is None:
                    raise ValueError('输入的词不存在！')
                current_node = current_node.right
            else:
                if current_node.left is None:
                    raise ValueError('输入的词不存在！')
                current_node = current_node.left

    def relation_create(self, file: str):
        file = open(file, 'r', encoding='utf8')
        relation_list = file.readlines()
        file.close()
        for n in relation_list:
            item = n[:-1]
            lst1 = item.split(':')
            freq = int(lst1[-1])
            lst2 = lst1[0].split("@")
            pre_list = lst2[0].split('/')
            next_list = lst2[-1].split('/')
            pre_word = pre_list[0]
            next_word = next_list[0]
            relation = RelationInfo(pre_word, next_word, freq)
            node = self.search(pre_word)
            if node is not None:
                if node.data is not None:
                    node.data.add_connection(relation)

    def match_all(self, text: str, start: int = 0) -> list:
        result = []  # 存放WordInfo类的数据
        if self.root is None or text is None:
            return result
        current_node = self.root
        char_index = start
        current_ch_num = ord(text[char_index])
        while True:
            compare = current_ch_num - current_node.char_num
            if compare == 0:
                char_index += 1
                if current_node.data is not None:
                    result.append(current_node.data)
                if char_index == len(text):
                    return result
                current_ch_num = ord(text[char_index])
                if current_node.mid is None:
                    if len(result) == 0:
                        raise ValueError('没有这个词！')
                    else:
                        return result
                else:
                    current_node = current_node.mid
            elif compare > 0:
                if current_node.right is None:
                    if len(result) == 0:
                        raise ValueError('没有这个词！')
                    else:
                        return result
                else:
                    current_node = current_node.right
            else:
                if current_node.left is None:
                    if len(result) == 0:
                        raise ValueError('没有这个词！')
                    else:
                        return result
                else:
                    current_node = current_node.left


class Vertices:
    """切词图中用的图上节点类"""

    def __init__(self, start: int, end: int, info: WordInfo):
        self.start = start
        self.end = end
        self.info = info


class Graph:
    """中文的字符串生成图"""

    def __init__(self, text: str, base: Dictionary,
                 word_weight: float = 0.3,
                 relation_weight: float = 0.7):
        self.vertices_num = 0
        self._group_num = 0
        self.vertices = []  # arrange in groups
        self.string = text
        self.base = base
        self.word_weight = word_weight
        self.relation_weight = relation_weight
        self.set_graph(self.string, self.base)

    def set_graph(self, text: str, base: Dictionary):
        for num in range(len(text)):
            search_list = base.match_all(text, num)
            group = []
            for info in search_list:
                current_word = info
                current_start = num
                current_end = num + len(current_word.word)
                current_vertices = Vertices(current_start,
                                            current_end,
                                            current_word)
                group.append(current_vertices)
                self.vertices_num += 1
            self.vertices.append(group)
            self._group_num += 1

    def find_path(self):
        global start_word
        global end_word
        begin_paths = []
        for item in self.vertices[0]:
            path = [item]
            begin_paths.append(path)

        max_weight = 0
        max_path = None
        for path in self._find(begin_paths):
            weight = 0
            for i in range(len(path)):
                weight1 = (path[i].info.freq **
                           len(path[i].info.word)) * self.word_weight
                # 长词容易出现？
                # weight1 = path[i].info.freq * self.word_weight
                # 不采用上式因为切分效果差
                weight2 = 0
                if i == 0:
                    start_node = self.base.search(start_word)
                    connection = start_node.data.get_connection()
                    next_word = path[i].info.word
                elif i == len(path) - 1:
                    connection = path[i].info.get_connection()
                    next_word = end_word
                else:
                    connection = path[i].info.get_connection()
                    next_word = path[i + 1].info.word
                for k in connection:
                    if k.next == next_word:
                        weight2 = k.freq * self.relation_weight
                        break
                weight += (weight1 + weight2)
            if weight > max_weight:
                max_weight = weight
                max_path = path
        result = []
        for ver in max_path:
            result.append(ver.info.word)
        return result

    def _find(self, paths: list):
        out = True
        new_paths = []
        for path in paths:
            current_path = path
            target = current_path[-1].end
            if target < self._group_num:
                out = False
                for item in self.vertices[target]:
                    new_path = current_path + [item]
                    new_paths.append(new_path)
            else:
                new_paths.append(current_path)
        if out:
            return new_paths
        else:
            return self._find(new_paths)


def segment(string:str):
    dic = Dictionary()
    g = Graph(string,dic)
    return g.find_path()


if __name__ == '__main__':
    import time
    time1 = time.time()
    test = '他会来'
    print(segment(test))
    time2 = time.time()
    print(time2-time1)
