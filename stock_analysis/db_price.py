# -*- coding: utf-8 -*-

__author__ = 'amelie'
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String,DATE,TIMESTAMP
import tushare as ts

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
top_ten = Table('price_amount', metadata,
                            Column('code', String(10), nullable=False),
                            Column('open', FLOAT, nullable=False),
                            Column('close', FLOAT, nullable=False),
                            Column('high', FLOAT, nullable=False),
                            Column('low', FLOAT, nullable=False),
                            Column('volume', FLOAT, nullable=True),
                            Column('amount', FLOAT, nullable=True),
                            Column('date', TIMESTAMP, nullable=True)
                            )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
conn.execute("delete from price_amount")

s1 = 'select * from stock_basics'  # 查询全表
r1 = conn.execute(s1)
res = r1.fetchall()
for x in res:
    code = x[0]
    print(code)
    df = ts.get_h_data(code,start='2015-01-01')
    df.reset_index(level=0, inplace=True)
    date=df.ix[0]['date']
    start_date = date.strftime('%Y-%m-%d')
    df['code']=code
    d = df.to_dict(orient='records')
    conn.execute(top_ten.insert(), d)
