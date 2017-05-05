# -*- coding: utf-8 -*-
__author__ = 'amelie'

import tushare as ts
from sqlalchemy import create_engine,Table,Column,MetaData,Integer,String,DATE,FLOAT

df=ts.get_stock_basics()
df.reset_index(level=0, inplace=True)
df1=df[["code","name","outstanding","timeToMarket","holders"]]
d = df1.to_dict(orient='records')
print("get basics already!")

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
#初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
conn.execute("delete from stock_basics")
r = conn.execute(stock_basics.insert(), d)