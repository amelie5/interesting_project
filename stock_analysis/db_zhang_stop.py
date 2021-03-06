from datetime import timedelta,datetime

import pandas as pd
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, DATE, Integer, TIMESTAMP
import time
import sys

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
                   Column('yizi', FLOAT, nullable=True)
                   )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
r_d=conn.execute('select max(date) from zhang_stop ')
res_d = r_d.fetchall()
start_date = res_d[0][0]

sd=start_date.strftime("%Y-%m-%d")
today=time.strftime("%Y-%m-%d")
if sd==today:
    print('数据已经是最新的了！！')
    sys.exit(0)

date = start_date - timedelta(days=1)
date = date.strftime("%Y-%m-%d")
while ts.is_holiday(date):
    date = datetime.strptime(date, "%Y-%m-%d")
    date = date - timedelta(days=1)
    date = date.strftime("%Y-%m-%d")


conn.execute('delete from zhang_stop where date>=%s',start_date)


r1 = conn.execute("select * from stock_basics where timeToMarket!='0000-00-00'")
res1 = r1.fetchall()
for x in res1:
    code = x[0]
    print('zhang_stop: ',code)
    r = conn.execute(
        'select t.date,t.code,p_change,close,high,low from (select * from price_amount where code=%s and date>=%s)t LEFT JOIN (select * from p_change where code=%s and date>=%s )n ' +
        'on t.code=n.code and t.date=n.date order by t.date',
        code, date, code, date)

    res = r.fetchall()
    if (res):
        df = pd.DataFrame(res)
        df.columns = r.keys()
        df['change_0'] = df['p_change']
        df['close_s'] = df['close'].shift(1)
        df['change_1'] = df['p_change'].shift(-1)
        df['change_2'] = df['p_change'].shift(-2)
        df['change_r'] = round((df['high'] - df['close_s']) / df['close_s'] * 100, 2)
        df['yizi']=round((df['high']-df['low'])/df['low'],2)

        df=df.drop(0)
        df=df.fillna(-999)
        df = df[df['change_r'] >= 9.9]
        if (df.empty):
            pass
        else:
            d = df.to_dict(orient='records')
            conn.execute(zhang_stop.insert(), d)
    else:
        continue
