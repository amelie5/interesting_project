# -*- coding: utf-8 -*-
__author__ = 'ghost'

from sqlalchemy import create_engine,Table,Column,MetaData,Integer,String,DATE,FLOAT,select,TIMESTAMP
import tushare as ts
df=ts.get_stock_basics()
df.reset_index(level=0, inplace=True)
df1=df[["code","name","outstanding","timeToMarket","holders"]]
d = df1.to_dict(orient='records')
print(d)


#连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata=MetaData()
#定义表
stock_basics = Table('stock_basics', metadata,
        Column('code', String(10), nullable=False),
        Column('name', String(50), nullable=False),
        Column('outstanding', FLOAT, nullable=True),
        Column('timeToMarket',DATE , nullable=True),
        Column('holders', Integer, nullable=True)
    )
test = Table('price', metadata,
        Column('data', Integer, nullable=False),
        Column('ctime', TIMESTAMP, nullable=False)
    )
#初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
#r = conn.execute(stock_basics.insert(), d)
s1 = select([test])  # 查询全表
print(s1)
r1 = conn.execute(s1)
print(r1.fetchall())