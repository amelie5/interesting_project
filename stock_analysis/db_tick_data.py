# -*- coding: utf-8 -*-

__author__ = 'amelie'
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, DATE

NOT_OPEN_DATE = '2020-01-01'

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
tick_amount = Table('tick_amount', metadata,
                    Column('code', String(10), nullable=False),
                    Column('date', DATE, nullable=True),
                    Column('amount', FLOAT, nullable=True),
                    Column('type', String(10), nullable=True)
                    )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
conn.execute("delete from tick_amount")

date = '2017-05-25'

r1 = conn.execute(
    'select * from stock_basics where timeToMarket!=0000-00-00 and code not in (select code from new_stock_open where timeToOpen>=%s)',
    NOT_OPEN_DATE)
res = r1.fetchall()
for x in res:
    code = x[0]
    df = ts.get_tick_data(code, date=date,4,1)
    grouped = df.groupby(df['type']).sum()
    grouped.reset_index(level=0, inplace=True)
    grouped = grouped[['amount', 'type']]
    grouped['date'] = date
    grouped['code'] = code
    d = grouped.to_dict(orient='records')
    conn.execute(tick_amount.insert(), d)
