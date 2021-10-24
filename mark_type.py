# encoding:utf8
from segment import *  # 注意 import XXX 和 from XXX import * 的区别
from sql_for_type import *
import pickle
import math
relation_data = 'relation_data.dat'
start_word = "始？？始"
start_tup = ('start', 1)
end_word = '末？？末'
end_tup = ('end', 1)


class Word:
    def __init__(self,word:str,info:tuple = None):
        self.word = word
        if info is None:
            self.info = []
        else:
            self.info = [info]

    def add_info(self,info:tuple):
        self.info.append(info)


def mark_type(string:str):
    global start_word
    global start_tup
    global end_word
    global end_tup
    seg_res = segment(string)

    start_w = Word(start_word, start_tup)
    all_words = [start_w]
    for item in seg_res:
        all_info = search_word(item)
        w = Word(item)
        all_words.append(w)
        for tup in all_info:
            w.add_info((tup[2],tup[3]))
    end_w = Word(end_word, end_tup)
    all_words.append(end_w)

    with open(relation_data,'rb+') as file:
        dic = pickle.load(file)
        file.close()
    result_info = []
    temp_res = []
    saved_prob = 0
    best_step_prob = -float('INFINITY')
    for i in range(len(all_words) - 1):
        former_word = all_words[i]
        after_word = all_words[i + 1]
        for x in former_word.info:
            for y in after_word.info:
                trans_prob = math.log10(float(dic[x[0] + '@' + y[0]]))
                emit_prob = math.log10(float(x[-1]))
                sum_prob = trans_prob + emit_prob + saved_prob
                if sum_prob > best_step_prob:
                    best_step_prob = sum_prob
                    temp_res = [y]
        saved_prob = best_step_prob
        best_step_prob = -float('INFINITY')
        if temp_res and temp_res[0][0] != 'end':
            result_info.append(temp_res[0])

    res = []
    for k in range(len(result_info)):
        res.append(all_words[k+1].word + '/' + result_info[k][0])
    return res


if __name__ == '__main__':
    print(mark_type('对企业的投资取得了巨大成功'))
