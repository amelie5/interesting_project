# -*- coding: utf-8 -*-

__author__ = 'ghost'
from sqlalchemy import create_engine, Table, Column, MetaData, Integer, String

from stock_analysis.spider_holder import get_holder

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
top_ten = Table('top_ten', metadata,
                            Column('code', String(10), nullable=False),
                            Column('company', String(100), nullable=False),
                            Column('amount', Integer(20), nullable=False),
                            Column('type', String(20), nullable=False),
                            Column('percent', String(10), nullable=False),
                            Column('change', String(10), nullable=True)
                            )
code_type = Table('code_type', metadata,
                  Column('code', String(10), nullable=False),
                  Column('ntype', String(10), nullable=False))
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
print('#' * 20)
# s1 = 'select * from code_type'  # 查询全表
# r1 = conn.execute(s1)
# res = r1.fetchall()
# for x in res:
code = '603117'
d = get_holder(code)
r = conn.execute(top_ten.insert(), d)  # conn.execute("delete from longhubang_shandong")




df,data=ts.top10_holders(code='600403',gdtype='1')#ddype=1 为流通前十大
df=df.sort_values('quarter',ascending=True)
print(df)