# -*- coding: utf-8 -*-

__author__ = 'amelie'
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, INT

FIVE_DAY = 5
# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
grown = Table('grown', metadata,
               Column('code', String(10), nullable=True),
               Column('name', String(10), nullable=True),
               Column('epsg', FLOAT, nullable=True),
               Column('year', INT, nullable=True),
               Column('q', INT, nullable=True)

               )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()

year = 2017
q=2
df = ts.get_growth_data(year, q)
df=df[['code','name','epsg']]
df = df.fillna(-9999)
df['year'] = year
df['q'] = q
d = df.to_dict(orient='records')
conn.execute(grown.insert(), d)
