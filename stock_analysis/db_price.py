# -*- coding: utf-8 -*-

__author__ = 'amelie'
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, DATE
from datetime import timedelta,datetime
import time
import sys

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
price_amount = Table('price_amount', metadata,
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

r_d = conn.execute("select max(date) from price_amount where code='sh'")
res_d = r_d.fetchall()
start_date = res_d[0][0]

sd=start_date.strftime("%Y-%m-%d")
today=time.strftime("%Y-%m-%d")
if sd==today:
    print('数据已经是最新的了！！')
    sys.exit(0)

start_date = start_date + timedelta(days=1)
start_date = start_date.strftime("%Y-%m-%d")

while ts.is_holiday(start_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    start_date = start_date + timedelta(days=1)
    start_date = start_date.strftime("%Y-%m-%d")

conn.execute('delete from price_amount where date>=%s',start_date)

r1 = conn.execute('select * from stock_basics b left join new_stock_open o on o.code=b.code where b.timeToMarket!=0000-00-00')
res = r1.fetchall()
for x in res:
    code = x[0]
    print('price: ',code)
    df = ts.get_hist_data(code, start=start_date)
    df=df[['open','close','high','low','volume']]
    df['code']=code
    df.reset_index(level=0, inplace=True)
    d = df.to_dict(orient='records')
    conn.execute(price_amount.insert(), d)
    timeToOpen = x[8]
    if timeToOpen != None:
        timeToOpen = timeToOpen.strftime('%Y-%m-%d')
        conn.execute('delete from price_amount where code=%s and date<%s and date>=%s', code, timeToOpen, '2017-06-21')

df = ts.get_hist_data('sh', start=start_date)
df=df[['open','close','high','low','volume']]
df['code'] ='sh'
df.reset_index(level=0, inplace=True)
d = df.to_dict(orient='records')
conn.execute(price_amount.insert(), d)

df = ts.get_hist_data('hs300', start=start_date)
df=df[['open','close','high','low','volume']]
df['code'] ='hs300'
df.reset_index(level=0, inplace=True)
d = df.to_dict(orient='records')
conn.execute(price_amount.insert(), d)

df = ts.get_hist_data('sz50', start=start_date)
df=df[['open','close','high','low','volume']]
df['code'] ='sz50'
df.reset_index(level=0, inplace=True)
d = df.to_dict(orient='records')
conn.execute(price_amount.insert(), d)

conn.execute('delete from price_amount where code is null')