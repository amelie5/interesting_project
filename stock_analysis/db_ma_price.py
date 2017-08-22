# -*- coding: utf-8 -*-

__author__ = 'amelie'
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, DATE, INT
import pandas as pd
from datetime import timedelta, datetime
import tushare as ts

FIVE_DAY=5
# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
ma_price = Table('ma_price', metadata,
                 Column('code', String(10), nullable=True),
                 Column('ma5', FLOAT, nullable=True),
                 Column('ma10', FLOAT, nullable=True),
                 Column('ma20', FLOAT, nullable=True),
                 Column('date', DATE, nullable=True)
                 )

# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()

r_d = conn.execute('select max(date) from ma_price where code=%s', 'sh')
res_d = r_d.fetchall()
start_date = res_d[0][0]
if (start_date==None):
    start_date = '2015-01-09'
else:
    start_date = start_date + timedelta(days=1)
    start_date = start_date.strftime("%Y-%m-%d")

    while ts.is_holiday(start_date):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        start_date = start_date + timedelta(days=1)
        start_date = start_date.strftime("%Y-%m-%d")


    conn.execute("delete from ma_price where date>=%s", start_date)

r_code = conn.execute('select code from stock_basics where holders!=0')
r_code = r_code.fetchall()
for x in r_code:
    code = x[0]
    print('ma_price: ',code)
    df=ts.get_hist_data(code,start=start_date)
    df=df[['ma5','ma10','ma20']]
    df['code']=code
    df.reset_index(level=0, inplace=True)
    d = df.to_dict(orient='records')
    conn.execute(ma_price.insert(), d)

conn.execute("delete from ma_price where code is null")
