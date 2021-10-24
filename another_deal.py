# encoding:utf8
read_file = open('2014_corpus.txt', 'r', encoding='utf8')
sep_file = open('2014_split.txt', 'w', encoding='utf8')
save = []


def is_chinese(s: str) -> bool:
    for i in s:
        if '0' <= i <= '9' or 'a' <= i <= 'z' or \
                'A' <= i <= 'Z':
            return False
    return True


while 1:
    line = read_file.readline()
    if not line:
        break
    else:
        line_list = line.split()
        for item in line_list:
            if len(item) == 0:
                continue
            else:
                if not save:
                    if '[' in item:
                        n_item = item.split('[')[-1]
                        word = n_item.split('/')[0]
                        save.append(word)
                    else:
                        word = item.split('/')[0]
                        if is_chinese(word):
                            sep_file.write(word)
                            sep_file.write(' ')
                else:
                    if ']' in item:
                        n_item = item.split(']')[0]
                        word = n_item.split('/')[0]
                        save.append(word)
                        new = ''
                        for w in save:
                            new += w
                        sep_file.write(new)
                        sep_file.write(' ')
                        save = []
                    else:
                        word = item.split('/')[0]
                        save.append(word)
