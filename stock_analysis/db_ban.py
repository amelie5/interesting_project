# -*- coding: utf-8 -*-

__author__ = 'amelie'
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, Integer, Date
import datetime

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
ban = Table('ban', metadata,
            Column('date', Date, nullable=True),
            Column('zhang_num', Integer, nullable=True),
            Column('zhang_feng_num', Integer, nullable=True),
            Column('zhang_daban', FLOAT, nullable=True),
            Column('open_num', Integer, nullable=True),
            Column('open_feng_num', Integer, nullable=True),
            Column('opne_daban', FLOAT, nullable=True)
            )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
#conn.execute("delete from ban")
date = datetime.date.today()
date = date.strftime('%Y-%m-%d')
date='2017-06-15'

sql = "insert into ban \n" \
      "select date,zhang_num,zhang_feng_num ,round(zhang_daban,2),open_num,open_feng_num,round(open_daban,2) from \n" \
      "(select date,count(1)as zhang_num,sum(case when change_0>9.9 then 1 else 0 end) as zhang_feng_num,sum(case when change_0>9.9 then 1 else 0 end)/count(1) as zhang_daban from zhang_stop \n" \
      "where date>='" + date + "' group by date)t1\n" \
                               "left join\n" \
                               "(select timeToOpen,count(1) as open_num,sum(case when f_0>9.9 then 1 else 0 end) as open_feng_num,sum(case when f_0>9.9 then 1 else 0 end)/count(1) as open_daban from new_stock_open \n" \
                               "where timeToOpen>='" + date + "' and timeToOpen!='3020-01-01'group by timeToOpen)t2\n" \
                                                              "on t1.date=t2.timeToOpen"

conn.execute(sql)
