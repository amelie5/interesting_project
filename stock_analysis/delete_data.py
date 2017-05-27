# -*- coding: utf-8 -*-

__author__ = 'amelie'
from sqlalchemy import create_engine

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
# 获取数据库连接
conn = engine.connect()

r1 = conn.execute('select * from new_stock_open')
res = r1.fetchall()
for x in res:
    code = x[0]
    print(code)
    date=x[1]
    date = date.strftime('%Y-%m-%d')
    conn.execute('delete from price_amount where code=%s and date<%s',code,date)
