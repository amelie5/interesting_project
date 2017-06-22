# coding:utf-8
import random
import string

# 激活码生成
def activation_code(count, length):
    # count 数量
    # length 长度
    base = string.ascii_uppercase + string.ascii_lowercase + string.digits    # 生成激活码可能包含的字符集（大写字母、小写字母、数字）
    code = []
    while len(code) < count:
        key = ''
        for j in range(length):
            key += random.choice(base)
        if key in code:
            continue
        else:
            code.append(key)
    return code
print (activation_code(10, 16))   # 获取10个长度为16个字符的激活码





import uuid
for i in range(2):
    print (uuid.uuid1())
