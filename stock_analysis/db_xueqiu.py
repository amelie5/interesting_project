# -*- coding: utf-8 -*-

__author__ = 'amelie'
from sqlalchemy import create_engine, Table, Column, MetaData, BIGINT, String, FLOAT, INT, DATE, TIMESTAMP
from spider_xueqiu import get_list, get_detail
import time

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
xueqiu_zuhe_list = Table('xueqiu_zuhe_list', metadata,
                         Column('id', String(50), nullable=True),
                         Column('name', String(100), nullable=True),
                         Column('owner', String(100), nullable=True),
                         Column('daily_gain', FLOAT, nullable=True),
                         Column('monthly_gain', FLOAT, nullable=True),
                         Column('total_gain', FLOAT, nullable=True),
                         Column('net_value', FLOAT, nullable=True),
                         Column('follower_count', INT, nullable=True),
                         Column('last_rb_id', BIGINT, nullable=True),
                         Column('create', DATE, nullable=True)
                         )

xueqiu_zuhe_cang = Table('xueqiu_zuhe_cang', metadata,
                         Column('zuhe_id', String(50), nullable=True),
                         Column('rb_id', BIGINT, nullable=True),
                         Column('stock_name', String(50), nullable=True),
                         Column('price', FLOAT, nullable=True),
                         Column('prev_weight', FLOAT, nullable=True),
                         Column('target_weight', FLOAT, nullable=True),
                         Column('date', TIMESTAMP, nullable=True),
                         )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()

# r = conn.execute("delete from xueqiu_zuhe_list ")
# df = get_list()
# d = df.to_dict(orient='records')
# conn.execute(xueqiu_zuhe_list.insert(), d)



conn.execute("delete from xueqiu_zuhe_cang")
r=conn.execute("select id,last_rb_id from xueqiu_zuhe_list")
res = r.fetchall()
for x in res:
    id = x[0]
    rb_id = x[1]
    print(id)
    df = get_detail(id,rb_id)
    d = df.to_dict(orient='records')
    conn.execute(xueqiu_zuhe_cang.insert(), d)
    time.sleep(0.1)
