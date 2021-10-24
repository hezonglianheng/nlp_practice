import ternarysearchtree as tree
if __name__ == '__main__':
    chinese_dic = tree.TernarySearchTree()
    file = open('chinese_for_test1.txt', 'r', encoding='utf8')
    chinese_list = file.readlines()
    chinese_dic.list_create(chinese_list)
    print(chinese_dic.match_long('大学生活动中心'))