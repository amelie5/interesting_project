#coding=utf-8
import tushare as ts
from datetime import datetime
from pandas import DataFrame
import numpy as np

# a = datetime.now()
# b = datetime.now()
# print((b - a).seconds)

# c=np.random.rand(10)*100
# print(c)
# df = DataFrame({'data': [1, 2, 6, -6]})
# cnt = df.groupby(df['data']).size()
# #df= ts.get_today_ticks('300599')
# r= np.array([[1,2],[3,4]])
# t=r.tolist()[0]
#
# print(t)


# list_price = df.apply(lambda x: x['changepercent'] - start_price, axis=1).values
# print(list_price)

# line = 'asdf fjdk; afed, fjek,asdf, foo'
import re
# a=re.split(r'[;,\s]', line)
# print(a)

# import re
# s='ObjectId("529a269da7f18312480a38e9")'
# result=re.compile(r'ObjectId\(\"(.*)\"\)').findall(s)
# print(result)

import pandas as pd
#from spider_all import get_zs
#设置最大打印行数
# pd.set_option('display.max_rows', 3000)
# df = get_zs()
# print(df)
code='002807'
df = ts.get_tick_data(code,date='2017-02-10')
#直接保存
df.to_excel('d:/data/stock/%s.xlsx'%code)