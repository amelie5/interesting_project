# -*- coding: utf-8 -*-

__author__ = 'amelie'
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, DATE, BIGINT
from spider_all import get_market

FIVE_DAY = 5
# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
fengkou = Table('fengkou', metadata,
                 Column('code', String(10), nullable=True),
                 Column('name', String(10), nullable=True),
                 Column('price', FLOAT, nullable=True),
                 Column('price_first', FLOAT, nullable=True),
                 Column('market', BIGINT, nullable=True),
                 Column('buy', BIGINT, nullable=True),
                 Column('sell', BIGINT, nullable=True),
                 Column('d', BIGINT, nullable=True),
                 Column('concept', String(100), nullable=True),
                 Column('trader', String(10), nullable=True),
                 Column('date', DATE, nullable=True)
                 )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()

date='2017-07-31'
df=get_market(date)
d = df.to_dict(orient='records')
conn.execute(fengkou.insert(), d)
