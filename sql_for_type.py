# encoding:utf8
# 本文件处理词的词性和发射概率
import sqlite3
textbook = 'word_frequency.txt'


def create_table():
    con = sqlite3.connect('word_type.db')
    cur = con.cursor()
    cur.execute('''create table if not exists word_info
    (id int primary key not null,
    word text not null,
    type text,
    prob float)''')
    con.commit()
    cur.close()


def add_data(book):
    con = sqlite3.connect('word_type.db')
    cur = con.cursor()
    type_dic = {}
    temp_list = []
    with open(book,encoding='utf8') as file:
        word_list = file.readlines()
        # word_sum = len(word_list)
        file.close()
        flag = 0
    for i in word_list:
        info = i[:-1]
        info_list = info.split(':')
        freq = int(info_list[-1])
        word_plus_type = info_list[0].split('/')
        word = word_plus_type[0]
        word_type = word_plus_type[-1]
        if word_type not in type_dic:
            type_dic[word_type] = freq
        else:
            type_dic[word_type] += freq
        temp_list.append([word,word_type,freq])
    for item in temp_list:
        if capture(item[0]):
            continue
        else:
            flag += 1
            cur.execute('''insert into word_info (id,word,type,prob) 
            values (?,?,?,?)''',(flag, item[0], item[1],
                                 item[2]/type_dic[item[1]]))
    print(flag)
    con.commit()
    cur.close()


def search_all():
    con = sqlite3.connect('word_type.db')
    cur = con.cursor()
    cur.execute('''select * from word_info''')
    res = cur.fetchall()
    return res


def search_word(word):
    con = sqlite3.connect('word_type.db')
    cur = con.cursor()
    cur.execute('''select * from word_info 
    where word = ?''',(word,))
    res = cur.fetchall()
    if not res:
        raise ValueError('word not found')
    return res


def capture(word:str) -> bool:
    for ch in word:
        if 'a' <= ch <= 'z' or '0' <= ch <= '9':
            return True
    return False


if __name__ == '__main__':
    # create_table()
    # add_data(textbook)
    print(search_word('投资'))
