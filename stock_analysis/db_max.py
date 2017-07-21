# -*- coding: utf-8 -*-

__author__ = 'amelie'
import pandas as pd
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, Date

date='2017-07-03'
start_date='2017-04-01'
df = pd.DataFrame()
# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
max_data = Table('max_data', metadata,
            Column('date', Date, nullable=True),
            Column('code', String(10), nullable=True),
            Column('high', FLOAT, nullable=True),
            Column('ntype', String(10), nullable=True)
            )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
conn.execute('delete from max_data')
r = conn.execute('select code from price_amount where date=%s and code!=%s',date,'sh')
res = r.fetchall()
for x in res:
    code=x[0]
    print(code)
    r_d = conn.execute('select max(high) from price_amount where code=%s and date<%s and date>=%s',code,date,start_date)
    res_d = r_d.fetchall()
    high = res_d[0][0]

    df = df.append({"code": code, "date": date, "high": high, "ntype": '3m'}, ignore_index=True)

df.dropna()
d = df.to_dict(orient='records')
conn.execute(max_data.insert(), d)


