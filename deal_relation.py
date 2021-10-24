import pickle
source = '2014_relation.txt'
result_file = 'relation_data.dat'


def cal_freq(text):
    relation_dic = {}
    with open(text, 'r', encoding='utf8') as file:
        relation_list = file.readlines()
        relation_sum = len(relation_list)
        file.close()
    for info in relation_list:
        info_list = info.split('@')
        info1 = info_list[0].split('/')[-1]
        info2 = info_list[-1][:-1].split('/')[-1]
        if info1[0] == 't' or info1[0] == 'x' or info2[0] == 't' or \
                info2[0] == 'x':
            continue
        else:
            new_info = info1 + '@' + info2
            if new_info not in relation_dic:
                relation_dic[new_info] = 1
            else:
                relation_dic[new_info] += 1
    for key in relation_dic:
        relation_dic[key] = relation_dic[key] / relation_sum
    return relation_dic


def save_data(dic:dict,file):
    with open(file,'wb+') as save_file:
        pickle.dump(dic,save_file)
        save_file.close()


if __name__ == '__main__':
    n = cal_freq(source)
    save_data(dic=n,file=result_file)
    print(n)
