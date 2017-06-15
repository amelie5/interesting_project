from datetime import timedelta

import pandas as pd
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, DATE, Integer, TIMESTAMP
import datetime

NOTIFY_DAY = 2
start_date = datetime.date.today()
start_date = start_date.strftime('%Y-%m-%d')
start_date = '2016-06-05'

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
zhang_stop = Table('zhang_stop', metadata,
                   Column('code', String(10), nullable=True),
                   Column('date', DATE, nullable=True),
                   Column('change_0', FLOAT, nullable=True),
                   Column('change_1', FLOAT, nullable=True),
                   Column('change_2', FLOAT, nullable=True),
                   Column('change_r', FLOAT, nullable=True)
                   )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
conn.execute("delete from zhang_stop")
r1 = conn.execute("select * from stock_basics where timeToMarket!='0000-00-00'")
res = r1.fetchall()
date = datetime.date.today()
date = date.strftime('%Y-%m-%d')
date='2017-06-15'

for x in res:
    code = x[0]
    print(code)
    r1 = conn.execute(
        'select t.date,t.code,p_change,close,high from (select * from price_amount where code=%s and date>=%s)t LEFT JOIN (select * from p_change where code=%s and date>=%s )n ' +
        'on t.code=n.code and t.date=n.date order by t.date',
        code, date, code, date)

    res = r1.fetchall()
    if (res):
        df = pd.DataFrame(res)
        df.columns = r1.keys()
        df['change_0'] = df['p_change']
        df['close_s'] = df['close'].shift(1)
        df['change_1'] = df['p_change'].shift(-1)
        df['change_2'] = df['p_change'].shift(-2)
        df['change_r'] = round((df['high'] - df['close_s']) / df['close_s'] * 100, 2)
        df=df.fillna(0)
        df = df[df['change_r'] >= 9.9]
        if (df.empty):
            pass
        else:
            d = df.to_dict(orient='records')
            conn.execute(zhang_stop.insert(), d)
    else:
        continue
