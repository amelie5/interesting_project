# coding=utf-8
import re
from collections import Counter


def cal(filename='love.txt'):
    with open(filename, 'r') as f:
        data = f.read()
    data = data.lower()
    # 替换除了n't这类连字符外的所有非单词字符和数字字符
    datalist = re.split(r'[\s\n]+', data)
    return Counter(datalist).most_common()


if __name__ == '__main__':
    dic = cal()
    for i in range(len(dic)):
        print('%15s  ---->   %3s' % (dic[i][0], dic[i][1]))
