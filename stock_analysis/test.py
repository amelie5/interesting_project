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

import re
# s='流通股东名单 报告期： 2016-12-31 公告日期： --'
# result=re.compile(r'报告期： (.*) 公告日期').findall(s)
# print(13/13)


import pandas as pd
#from spider_all import get_zs
#设置最大打印行数
# pd.set_option('display.max_rows', 3000)
# df = get_zs()
# print(df)
code='300603'
#df = ts.get_tick_data(code,date='2017-02-03')
#直接保存
#df.to_excel('d:/data/stock/%s.xlsx'%code)



# df=ts.get_concept_classified()
# print(df)

#取补集
# df1 = DataFrame({
# 'Buyer': ['Carl', 'Carl', 'Carl'],
# 'Quantity': [18, 3, 5, ]})
#
# df2 = DataFrame({
# 'Buyer': ['Carl', 'Mark', 'Carl', 'Carl'],
# 'Quantity': [2, 1, 18, 5]})
# df= df1.merge(df2, indicator=True, how='outer')
# df=df[df['_merge'] == 'right_only']
# print(df)


# ints = [8, 23, 45, 12, 78]
# for idx, val in enumerate(ints):
#     print (idx, val)
#
# print(ints[3])


# line = 'v_sz000078="51~海王生物~000078~5.88~5.90~5.90~61558~26547~35011~5.88~2148~5.87~3196~5.86~2064~5.85~3057~5.84~1105~5.89~443~5.90~3738~5.91~1221~5.92~1366~5.93~1387~14:14:06/5.88/1/S/588/7829|14:13:57/5.88/2/S/1176/7823|14:13:51/5.88/234/S/137592/7820|14:13:42/5.88/2/S/1176/7813|14:13:39/5.88/17/S/10290/7811|14:13:30/5.88/7/S/4116/7805~20170426141409~-0.02~-0.34~5.92~5.86~5.88/61557/36235463~61558~3624~0.33~37.22~~5.92~5.86~1.02~108.43~155.71~2.90~6.49~5.31~0.74";'
# import re
# a=re.findall(r'(\d\d:\d\d:\d\d/.*)~2017', line)
# print(a)

df = ts.get_today_ticks('000078') #Single stock symbol
print(df)