read_file = open('2014_corpus.txt', 'r', encoding='utf8')
word_file = open('2014_words.txt', 'w+', encoding='utf8')
relation_file = open('2014_relation.txt', 'w+',
                     encoding='utf8')
start_simulation = '始？？始/start'
end_simulation = '末？？末/end'
flag = 0
save = []
while 1:
    line = read_file.readline()
    if not line:
        break
    else:
        line_list = line.split()
        last_word = start_simulation
        word_file.write(start_simulation + '\n')
        for item in line_list:
            if item[-1] == 'w':
                word_file.write(item + '\n')
                if item[0] == '，' or item[0] == '。':
                    word_file.write(end_simulation + '\n')
                    end_relation = last_word + '@' + \
                                   end_simulation + '\n'
                    relation_file.write(end_relation)
                    last_word = start_simulation
                    word_file.write(start_simulation + '\n')
            else:
                if flag == 0 and '[' not in item:
                    record = item + '\n'
                    word_file.write(record)
                    relation = last_word + '@' + item + '\n'
                    relation_file.write(relation)
                    last_word = item
                elif '[' in item:
                    flag = 1
                    lst = item.split('/')
                    save.append(lst[0][1:])
                elif ']' in item:
                    flag = 0
                    lst = item.split('/')
                    save.append(lst[0])
                    z_word = ''
                    for n in save:
                        z_word += n
                    save = []
                    z_word = z_word + '/' + lst[-1]
                    record = z_word + '\n'
                    word_file.write(record)
                    relation = last_word + '@' + z_word + '\n'
                    relation_file.write(relation)
                    last_word = z_word
                else:
                    lst = item.split('/')
                    save.append(lst[0])

read_file.close()
word_file.close()
relation_file.close()
