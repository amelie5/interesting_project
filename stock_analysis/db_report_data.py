# -*- coding: utf-8 -*-

__author__ = 'amelie'
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, INT

FIVE_DAY = 5
# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
longhu = Table('report_data', metadata,
               Column('code', String(10), nullable=True),
               Column('name', String(10), nullable=True),
               Column('eps', FLOAT, nullable=True),
               Column('eps_yoy', FLOAT, nullable=True),
               Column('bvps', FLOAT, nullable=True),
               Column('roe', FLOAT, nullable=True),
               Column('epcf', FLOAT, nullable=True),
               Column('net_profits', FLOAT, nullable=True),
               Column('profits_yoy', FLOAT, nullable=True),
               Column('distrib', String(100), nullable=True),
               Column('report_date', String(10), nullable=True),
               Column('year', INT, nullable=True),
               Column('q', INT, nullable=True)

               )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()

year = 2015
q=1
df = ts.get_report_data(year, q)
df = df.fillna(-9999)
df['year'] = year
df['q'] = q
d = df.to_dict(orient='records')
conn.execute(longhu.insert(), d)
