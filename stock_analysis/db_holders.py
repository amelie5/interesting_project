# -*- coding: utf-8 -*-

__author__ = 'amelie'
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String,DATE

from stock_analysis.spider_holder import get_holder

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
holder = Table('holder', metadata,
                  Column('code', String(10), nullable=False),
                  Column('holders', FLOAT, nullable=False),
                  Column('date', DATE , nullable=False)
               )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
conn.execute("delete from holder")

s1 = 'select * from stock_basics'  # 查询全表
r1 = conn.execute(s1)
res = r1.fetchall()
for x in res:
    code = x[0]
    print(code)
    df = get_holder(code)
    if (df.empty):
        pass
    else:
        d = df.to_dict(orient='records')
        conn.execute(holder.insert(), d)
