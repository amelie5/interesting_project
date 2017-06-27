# -*- coding: utf-8 -*-

__author__ = 'amelie'
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, DATE, INT
import pandas as pd
from datetime import timedelta, datetime
import tushare as ts

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
wm_price = Table('wm_price', metadata,
                 Column('code', String(10), nullable=True),
                 Column('close', FLOAT, nullable=True),
                 Column('ntype', String(10), nullable=True),
                 Column('cnt', INT, nullable=True),
                 Column('date', DATE, nullable=True)
                 )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()

r_d = conn.execute('select max(date) from price_amount where code=%s', 'sh')
res_d = r_d.fetchall()
start_date = res_d[0][0]
start_date = start_date + timedelta(days=1)
start_date = start_date.strftime("%Y-%m-%d")

while ts.is_holiday(start_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    start_date = start_date + timedelta(days=1)
    start_date = start_date.strftime("%Y-%m-%d")

conn.execute("delete from wm_price where date>=%s", start_date)

r_d = conn.execute('select date from price_amount where code=%s and date<=%s group by date order by date desc limit 22', 'sh',start_date)
res_d = r_d.fetchall()
end_date = res_d[21][0]
end_date = end_date.strftime("%Y-%m-%d")
r = conn.execute(
    'select code,avg(close)as close,count(1)as cnt from price_amount where code!=%s and date>=%s and date<=%s group by code',
    'sh',
    end_date, start_date)
res = r.fetchall()
df = pd.DataFrame(res)
df.columns = r.keys()
df['date'] = start_date
df['ntype'] = 'm'

d = df.to_dict(orient='records')
conn.execute(wm_price.insert(), d)

conn.execute("delete from wm_price where code is null")
