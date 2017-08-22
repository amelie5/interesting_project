# -*- coding: utf-8 -*-

__author__ = 'amelie'
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, DATE, BIGINT
from spider_all import get_longhu
import tushare as ts
from datetime import timedelta, datetime

FIVE_DAY = 5
# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
longhu = Table('longhu', metadata,
               Column('code', String(10), nullable=True),
               Column('name', String(10), nullable=True),
               Column('p_change', FLOAT, nullable=True),
               Column('market', BIGINT, nullable=True),
               Column('buy', BIGINT, nullable=True),
               Column('sell', BIGINT, nullable=True),
               Column('d', BIGINT, nullable=True),
               Column('concept', String(1000), nullable=True),
               Column('trader', String(10), nullable=True),
               Column('date', DATE, nullable=True)
               )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()

r_d = conn.execute("select max(date) from longhu")
res_d = r_d.fetchall()
start_date = res_d[0][0]
start_date = start_date + timedelta(days=1)
start_date = start_date.strftime("%Y-%m-%d")

while ts.is_holiday(start_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    start_date = start_date + timedelta(days=1)
    start_date = start_date.strftime("%Y-%m-%d")

conn.execute('delete from longhu where date>=%s',start_date)

sql="select date from p_change where code='sh' and date>='"+start_date+ "' order by date"
r_d = conn.execute(sql)
res = r_d.fetchall()
for x in res:
    date = x[0]
    date = date.strftime("%Y-%m-%d")
    df = get_longhu(date)
    d = df.to_dict(orient='records')
    print('longhu: ', date)
    conn.execute(longhu.insert(), d)


