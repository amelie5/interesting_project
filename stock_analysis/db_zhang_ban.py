# -*- coding: utf-8 -*-

__author__ = 'amelie'
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, Integer, Date
from datetime import timedelta,datetime

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
ban = Table('zhang_ban', metadata,
            Column('date', Date, nullable=True),
            Column('num', Integer, nullable=True),
            Column('feng_num', Integer, nullable=True),
            Column('daban_rate', FLOAT, nullable=True),
            Column('yizi_num', Integer, nullable=True),
            Column('next_zhang_num', Integer, nullable=True),
            Column('feng_next_zhang_num', Integer, nullable=True),
            Column('yizi_next_zhang_num', Integer, nullable=True),
            Column('next_2_zhang_num', Integer, nullable=True),
            Column('feng_next_2_zhang_num', Integer, nullable=True),
            Column('yizi_next_2_zhang_num', Integer, nullable=True)
            )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()

r_d = conn.execute("select max(date) from zhang_ban")
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

    conn.execute('delete from zhang_ban where date>=%s',date)

sql = "insert into zhang_ban \n" \
      "select date,num,feng_num ,round(daban_rate,2),yizi_num,next_zhang_num,feng_next_zhang_num,yizi_next_zhang_num,next_2_zhang_num,feng_next_2_zhang_num,yizi_next_2_zhang_num from \n" \
      "(select date,count(1)as num," \
      "sum(case when change_0>=9.9 then 1 else 0 end) as feng_num, " \
      "sum(case when change_1>0 then 1 else 0 end) as next_zhang_num," \
      "sum(case when change_2>0 then 1 else 0 end) as next_2_zhang_num," \
      "sum(case when (change_1>0 and change_0>=9.9) then 1 else 0 end) as feng_next_zhang_num, " \
      "sum(case when (change_2>0 and change_0>=9.9) then 1 else 0 end) as feng_next_2_zhang_num, " \
      "sum(case when yizi=0 then 1 else 0 end) as yizi_num, " \
      "sum(case when (yizi=0 and change_1>0) then 1 else 0 end) as yizi_next_zhang_num, " \
      "sum(case when (yizi=0 and change_2>0) then 1 else 0 end) as yizi_next_2_zhang_num, " \
      "sum(case when change_0>=9.9 then 1 else 0 end)/count(1) as daban_rate from zhang_stop \n" \
      "where date>='" + date + "' group by date)t1\n" \

conn.execute(sql)
