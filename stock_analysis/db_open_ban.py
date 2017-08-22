# -*- coding: utf-8 -*-

__author__ = 'amelie'
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, Integer, Date
from datetime import timedelta,datetime

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
ban = Table('open_ban', metadata,
            Column('date', Date, nullable=True),
            Column('num', Integer, nullable=True),
            Column('feng_num', Integer, nullable=True),
            Column('daban_rate', FLOAT, nullable=True),
            Column('next_zhang_num', Integer, nullable=True),
            Column('feng_next_zhang_num', Integer, nullable=True),
            Column('feng_next_2_zhang_num', Integer, nullable=True)
            )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()

r_d = conn.execute("select max(date) from open_ban")
res_d = r_d.fetchall()
date = res_d[0][0]
if (date==None):
    date = '2015-01-01'
else:
    date = date - timedelta(days=1)
    date = date.strftime("%Y-%m-%d")

    while ts.is_holiday(date):
        date = datetime.strptime(date, "%Y-%m-%d")
        date = date - timedelta(days=1)
        date = date.strftime("%Y-%m-%d")

    conn.execute('delete from open_ban where date>=%s', date)


print('open_ban: ',date)
sql = "insert into open_ban \n" \
      "select timeToOpen,num,feng_num,round(daban_rate,2),next_zhang_num,feng_next_zhang_num,feng_next_2_zhang_num from \n" \
      "(select timeToOpen,count(1) as num," \
      "sum(case when f_0>=9.9 then 1 else 0 end) as feng_num," \
      "sum(case when f_0>=9.9 then 1 else 0 end)/count(1) as daban_rate, " \
      "sum(case when f_1>0 then 1 else 0 end) as next_zhang_num," \
      "sum(case when (f_1>0 and f_0>=9.9)  then 1 else 0 end) as feng_next_zhang_num," \
      "sum(case when (f_2>0 and f_0>=9.9)  then 1 else 0 end) as feng_next_2_zhang_num \n" \
      "from new_stock_open \n" \
      "where timeToOpen>='" + date + "' and timeToOpen!='3020-01-01'group by timeToOpen)t2\n" \


conn.execute(sql)
