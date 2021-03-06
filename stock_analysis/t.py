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

# line = '2017-12-15'
# import re
# a=re.findall(r'2017-(.*)-', line)
# print(a)


# df = ts.get_k_data('000005', start='1990-11-25',end='1990-12-10')
# print(df)
# df.reset_index(level=0, inplace=True)
# print(df)
# print(df['date'])


#df=ts.get_k_data('000001', start='2017-06-15')
#df=ts.trade_cal()
# df=ts.is_holiday('2017-06-18')
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, DATE
from datetime import timedelta,datetime

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
top_ten = Table('price_amount', metadata,
                Column('code', String(10), nullable=True),
                Column('open', FLOAT, nullable=True),
                Column('close', FLOAT, nullable=True),
                Column('high', FLOAT, nullable=True),
                Column('low', FLOAT, nullable=True),
                Column('volume', FLOAT, nullable=True),
                Column('date', DATE, nullable=True)
                )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
df = ts.get_hist_data('sh', start='2017-06-26')
df=df[['open','close','high','low','volume']]
df['code'] ='sh'
df.reset_index(level=0, inplace=True)
d = df.to_dict(orient='records')
conn.execute(top_ten.insert(), d)