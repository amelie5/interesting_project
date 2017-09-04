# -*- coding: utf-8 -*-
__author__ = 'amelie'

import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, Integer, String, DATE, FLOAT
import time
# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
subdata = Table('subdata', metadata,
                Column('code', String(10), nullable=False),
                Column('turnover', FLOAT, nullable=False),
                Column('volume', FLOAT, nullable=False),
                Column('selling', FLOAT, nullable=False),
                Column('buying', FLOAT, nullable=False),
                Column('fvalues', FLOAT, nullable=True),
                Column('avgprice', FLOAT, nullable=True),
                Column('strength', FLOAT, nullable=True),
                Column('activity', FLOAT, nullable=True),
                Column('attack', FLOAT, nullable=True),
                Column('interval3', FLOAT, nullable=True),
                Column('interval6', FLOAT, nullable=True),
                Column('date', DATE, nullable=True)
                )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()

today = time.strftime("%Y-%m-%d")
conn.execute('delete from subdata where date>=%s',today)

df = ts.get_day_all()
df = df[["code", "turnover", "volume", "selling", "buying", "fvalues", "avgprice", "strength", "activity", "attack", "interval3", "interval6"]]
df['date']=today
df = df.fillna(-9999)
d = df.to_dict(orient='records')

r = conn.execute(subdata.insert(), d)
