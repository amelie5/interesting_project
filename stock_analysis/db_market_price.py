# -*- coding: utf-8 -*-

__author__ = 'amelie'
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
market_price = Table('market_price', metadata,
                Column('code', String(10), nullable=False),
                Column('close', FLOAT, nullable=False)
                )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
conn.execute("delete from market_price")

r1 = conn.execute('select * from stock_basics where timeToMarket!=0000-00-00')
res = r1.fetchall()
for x in res:
    code = x[0]
    date=x[3]
    date = date.strftime('%Y-%m-%d')
    print(code)
    df = ts.get_k_data(code, start=date,end=date)
    df=df[['code','close']]
    d = df.to_dict(orient='records')
    conn.execute(market_price.insert(), d)
