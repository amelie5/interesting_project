# -*- coding: utf-8 -*-

__author__ = 'amelie'
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, DATE

NOT_OPEN_DATE = '2020-01-01'

start_date='2017-06-15'
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
conn.execute('delete from price_amount where date>=%s',start_date)

r1 = conn.execute(
    'select * from stock_basics where timeToMarket!=0000-00-00')
res = r1.fetchall()
for x in res:
    code = x[0]
    print(code)
    df = ts.get_k_data(code, start=start_date)
    df.reset_index(level=0, inplace=True)
    d = df.to_dict(orient='records')
    conn.execute(top_ten.insert(), d)


df = ts.get_k_data('sh', start=start_date)
df.reset_index(level=0, inplace=True)
d = df.to_dict(orient='records')
conn.execute(top_ten.insert(), d)

conn.execute('delete from price_amount where code is null')