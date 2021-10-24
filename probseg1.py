class WordInfo:
    """每个词在节点中的表现形式的类，用于字典生成"""

    def __init__(self, word: str, types: set = None,
                 log_prob: float = 0.0):
        self.word = word
        self.types = types
        self.log_prob = log_prob

    def add_type(self, new_type):
        self.types.add(new_type)


class Node:
    """字典的组成单元"""

    def __init__(self, char_num: int):
        self.char_num = char_num  # 字符的Unicode值，为一个整数
        self.left = None
        self.right = None
        self.mid = None
        self.data = None  # 设计为WordInfo对象


class SearchTree:
    """生成一棵树，即切词用的字典"""

    def __init__(self):
        self.root = None

    def word_create(self, word: str, log_prob: float = 0.0,
                    types: set = None):
        """目前采用公式生成的方法来得到log_prob的值\n
           词的性质参数省略"""
        char_index = 0
        current_ch_num = ord(word[char_index])
        if self.root is None:
            self.root = Node(current_ch_num)
            self.root.data = WordInfo(word[char_index],
                                      log_prob=prob_stimulation(word[char_index]))
        current_node = self.root
        while True:
            compare = current_ch_num - current_node.char_num
            if compare == 0:
                char_index += 1
                if char_index == len(word):
                    current_node.data = WordInfo(word,
                                                 log_prob=prob_stimulation(word))
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

    def word_list_create(self, lst: list):
        if len(lst) == 1:
            self.word_create(lst[0])
        elif len(lst) > 1:
            middle = len(lst) // 2
            self.word_create(lst[middle])
            self.word_list_create(lst[:middle])
            self.word_list_create(lst[middle + 1:])

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
    """代表词的图中节点，用于生成图"""

    def __init__(self, start: int, end: int, word: str, log_prob: float = 0.0,
                 types: set = None):
        self.start = start  # 开始位置
        self.end = end  # 结束位置
        self.word = word  # 这条边所代表的词
        self.log_prob = log_prob
        self.types = None


class Graph:
    """将中文的字符串生成图"""

    def __init__(self, text: str, base_dic: SearchTree):
        self.vertices_num = 0
        self.__group_num = 0
        self.vertices = []  # arrange in groups
        self.string = text

        def set_graph(string, base):
            for i in range(len(string)):
                search_list = base.match_all(string, i)
                group = []
                for info in search_list:
                    current_word = info.word
                    current_types = info.types
                    current_log_prob = info.log_prob
                    current_start = i
                    current_end = i + len(current_word)
                    current_vertices = Vertices(current_start, current_end, current_word,
                                                current_log_prob, current_types)
                    group.append(current_vertices)
                    self.vertices_num += 1
                self.vertices.append(group)
                self.__group_num += 1

        set_graph(text, base_dic)

    def find_path(self) -> list:
        begin = []
        for item in self.vertices[0]:
            path = [item]
            begin.append(path)
        max_prob = -float('infinity')
        max_path = None
        for path in self.__find(begin):
            prob = 0
            for v in path:
                prob += v.log_prob
            if prob > max_prob:
                max_prob = prob
                max_path = path
        result = []
        for ver in max_path:
            result.append(ver.word)
        return result

    def __find(self,path_list:list) -> list:
        out = True
        new_path_list = []
        for path in path_list:
            current_path = path
            target = current_path[-1].end
            if target < self.__group_num:
                out = False
                for item in self.vertices[target]:
                    new_path = current_path + [item]
                    new_path_list.append(new_path)
            else:
                new_path_list.append(current_path)
        if out:
            return new_path_list
        else:
            return self.__find(new_path_list)


def prob_stimulation(word):  # 用来模拟得到一个词的概率的函数
    return len(word) - 5


if __name__ == '__main__':
    chinese_dic = SearchTree()
    file = open('chinese_for_test1.txt', 'r', encoding='utf8')
    word_list = file.readlines()
    for n in word_list:
        chinese_dic.word_create(n[:-1])
    test_string = '大学生活动中心'
    chinese_graph = Graph(test_string, chinese_dic)
    print(chinese_graph.find_path())
