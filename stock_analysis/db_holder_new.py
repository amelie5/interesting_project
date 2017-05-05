# -*- coding: utf-8 -*-

__author__ = 'amelie'
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String,DATE

from stock_analysis.spider_holder import get_holder,get_holder_dongfang

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
holder = Table('holder_new', metadata,
                  Column('code', String(10), nullable=False),
                  Column('holders', FLOAT, nullable=False),
                  Column('date', DATE , nullable=False)
               )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
conn.execute("delete from holder_new")

df = get_holder_dongfang()
d = df.to_dict(orient='records')
conn.execute(holder.insert(), d)
