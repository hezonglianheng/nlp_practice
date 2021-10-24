word_file = open('2014_words.txt','r',encoding='utf8')
frequency_file1 = open('word_frequency.txt','w',encoding='utf8')
relation_file = open('2014_relation.txt','r',encoding='utf8')
frequency_file2 = open('relation_frequency.txt','w',
                       encoding='utf8')
word_list = word_file.readlines()
word_dict = {}
word_num = 0
relation_list = relation_file.readlines()
relation_dict = {}
relation_num = 0
for item in word_list:
    word_num += 1
    if item[:-1] not in word_dict:
        word_dict[item[:-1]] = 1
    else:
        word_dict[item[:-1]] += 1
for word in word_dict.keys():
    freq = word + ':' + str(word_dict[word])
    frequency_file1.write(freq)
    frequency_file1.write('\n')
for pair in relation_list:
    relation_num += 1
    if pair[:-1] not in relation_dict:
        relation_dict[pair[:-1]] = 1
    else:
        relation_dict[pair[:-1]] += 1
for p in relation_dict:
    freq = p + ":" + \
           str(relation_dict[p])
    frequency_file2.write(freq)
    frequency_file2.write('\n')
word_file.close()
frequency_file1.close()
relation_file.close()
frequency_file2.close()

