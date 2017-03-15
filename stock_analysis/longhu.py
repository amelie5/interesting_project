# -*- coding: utf-8 -*-

__author__ = 'ghost'
from sqlalchemy import create_engine, Table, Column, MetaData, String, FLOAT, DateTime

from stock_analysis.spider_longhu import func_one

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
longhubang_shandong = Table('longhubang_shandong', metadata,
                            Column('code', String(10), nullable=False),
                            Column('ctime', DateTime, nullable=False),
                            Column('trader', String(100), nullable=False),
                            Column('ntype', String(1), nullable=False),
                            Column('fund', FLOAT, nullable=True)
                            )
code_type = Table('code_type', metadata,
                  Column('code', String(10), nullable=False),
                  Column('ntype', String(10), nullable=False))
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
code = '300490'
d = func_one(code)
# conn.execute("delete from longhubang_shandong")
r = conn.execute(longhubang_shandong.insert(), d)

