# -*- coding: utf-8 -*-

__author__ = 'amelie'
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, TIMESTAMP

NOT_OPEN_DATE = '2020-01-01'
# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
top_ten = Table('wm_price', metadata,
                Column('code', String(10), nullable=False),
                Column('open', FLOAT, nullable=False),
                Column('close', FLOAT, nullable=False),
                Column('high', FLOAT, nullable=False),
                Column('low', FLOAT, nullable=False),
                Column('volume', FLOAT, nullable=True),
                Column('ntype', String(10), nullable=False),
                Column('date', TIMESTAMP, nullable=True)
                )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
conn.execute("delete from wm_price")

r1 = conn.execute('select * from stock_basics where timeToMarket!=0000-00-00 and code!=%s and code not in (select code from new_stock_open where timeToOpen>=%s)','603909',
                  NOT_OPEN_DATE)
res = r1.fetchall()
for x in res:
    code = x[0]
    print(code)
    df = ts.get_k_data(code, start='2017-01-01',ktype='W')
    df['ntype']='w'
    d = df.to_dict(orient='records')
    conn.execute(top_ten.insert(), d)
    df = ts.get_k_data(code, start='2017-01-01', ktype='M')
    df['ntype'] = 'm'
    d = df.to_dict(orient='records')
    conn.execute(top_ten.insert(), d)