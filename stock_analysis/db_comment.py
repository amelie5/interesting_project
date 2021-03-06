# -*- coding: utf-8 -*-

__author__ = 'amelie'
from sqlalchemy import create_engine, Table, Column, MetaData, INT, String,DATE

from stock_analysis.spider_all import get_comment

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
top_ten = Table('comment', metadata,
                            Column('code', String(10), nullable=False),
                            Column('date', DATE, nullable=False),
                            Column('cnt', INT, nullable=False)
                            )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
conn.execute("delete from comment")

r1 = conn.execute('select * from stock_basics b inner JOIN new_stock_open n where b.code=n.code and n.timeToOpen<%s', '2020-01-01')
res = r1.fetchall()
for x in res:
    code = x[0]
    if(code=='603033'):
        continue
    print(code)
    df = get_comment(code)
    if (df.empty):
        pass
    else:
        d = df.to_dict(orient='records')
        conn.execute(top_ten.insert(), d)
