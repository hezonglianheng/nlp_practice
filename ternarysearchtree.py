class Node:
    def __init__(self, char: int):
        self.left = None
        self.mid = None
        self.right = None
        self.data = None  # information of word
        self.char = char

    def __str__(self):
        return 'char:' + chr(self.char)


class TernarySearchTree:
    def __init__(self):
        self.root = None

    def create(self, word: str):
        letter_index = 0
        current_ch = ord(word[letter_index])
        if self.root is None:
            self.root = Node(current_ch)
            self.root.data = word[letter_index]
        current_node = self.root
        while True:
            compare = current_ch - current_node.char
            if compare == 0:
                letter_index += 1
                if letter_index == len(word):
                    current_node.data = word
                    return current_node
                current_ch = ord(word[letter_index])
                if current_node.mid is None:
                    current_node.mid = Node(current_ch)
                    if letter_index == 1:
                        current_node.mid.data = \
                            word[letter_index]
                current_node = current_node.mid
            elif compare > 0:
                if current_node.right is None:
                    current_node.right = Node(current_ch)
                current_node = current_node.right
            else:
                if current_node.left is None:
                    current_node.left = Node(current_ch)
                current_node = current_node.left

    def list_create(self, lst):
        if len(lst) == 1:
            self.create(lst[0][:-1])
        elif len(lst) > 1:
            middle = len(lst) // 2
            self.create(lst[middle][:-1])
            self.list_create(lst[:middle])
            self.list_create(lst[middle + 1:])

    def search(self, word: str):
        if self.root is None:
            return None
        else:
            letter_index = 0
            current_ch = ord(word[letter_index])
            current_node = self.root
            while True:
                compare = current_ch - current_node.char
                if compare == 0:
                    letter_index += 1
                    if letter_index == len(word):
                        return current_node
                    else:
                        current_ch = ord(word[letter_index])
                        if current_node.mid is None:
                            return None
                        else:
                            current_node = current_node.mid
                elif compare > 0:
                    if current_node.right is None:
                        return None
                    else:
                        current_node = current_node.right
                else:
                    if current_node.left is None:
                        return None
                    else:
                        current_node = current_node.left

    def match_long(self, string, start=0):
        result = []
        search = ''
        match = ''
        if self.root is None:
            return result
        current_node = self.root
        letter_index = start
        while True:
            if current_node is None:
                letter_index -= (len(search) - len(match))
                result.append(match)
                search = ''
                match = ''
                current_node = self.root
            else:
                compare = ord(string[letter_index]) - \
                    current_node.char
                if compare == 0:
                    if current_node.data is not None:
                        match = current_node.data
                    search += string[letter_index]
                    letter_index += 1
                    if letter_index == len(string):
                        result.append(search)
                        return result
                    else:
                        current_node = current_node.mid
                elif compare > 0:
                    current_node = current_node.right
                else:
                    current_node = current_node.left

    def match_all(self, string: str, start: int = 0) -> list:
        result = []
        if not string or not self.root or start >= len(string):
            return result
        current_node = self.root
        letter_index = start
        while True:
            if current_node is None:
                return result
            compare = ord(string[letter_index]) - \
                current_node.char
            if compare == 0:
                letter_index += 1
                if current_node.data is not None:
                    result.append(current_node.data)
                if letter_index == len(string):
                    return result
                else:
                    current_node = current_node.mid
            elif compare > 0:
                current_node = current_node.right
            else:
                current_node = current_node.left


if __name__ == '__main__':
    letter_dic = TernarySearchTree()
    f = open('chinese_for_test1.txt', 'r', encoding='utf-8')
    word_list = f.readlines()
    letter_dic.list_create(word_list)
    aim_word = '大学生活动中心'
    for n in range(len(aim_word)):
        print(letter_dic.match_all(aim_word, n))
