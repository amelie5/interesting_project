import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, String, TIMESTAMP, FLOAT
from datetime import timedelta, datetime
import time
import sys

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
p_change = Table('p_change', metadata,
                 Column('date', TIMESTAMP, nullable=True),
                 Column('volume', FLOAT, nullable=True),
                 Column('p_change', FLOAT, nullable=True),
                 Column('code', String(10), nullable=True)
                 )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()

r_d = conn.execute("select max(date) from p_change where code='sh'")
res_d = r_d.fetchall()
start_date = res_d[0][0]

sd=start_date.strftime("%Y-%m-%d")
today=time.strftime("%Y-%m-%d")
if sd==today:
    print('数据已经是最新的了！！')
    sys.exit(0)

start_date = start_date + timedelta(days=1)
start_date = start_date.strftime("%Y-%m-%d")

while ts.is_holiday(start_date):
    start_date=datetime.strptime(start_date, "%Y-%m-%d")
    start_date = start_date + timedelta(days=1)
    start_date = start_date.strftime("%Y-%m-%d")

conn.execute('delete from p_change where date>=%s ',start_date)

r1 = conn.execute('select * from stock_basics b left join new_stock_open o on o.code=b.code where b.timeToMarket!=0000-00-00')
res = r1.fetchall()
for x in res:
    code = x[0]
    print('pchange: ',code)
    df = ts.get_hist_data(code, start=start_date)
    df = df[['p_change', 'volume']]
    df.reset_index(level=0, inplace=True)
    df['code'] = code
    dict = df.to_dict(orient='records')
    conn.execute(p_change.insert(), dict)
    timeToOpen=x[8]
    if timeToOpen!=None:
        timeToOpen = timeToOpen.strftime('%Y-%m-%d')
        conn.execute('delete from p_change where code=%s and date<%s and date>=%s', code, timeToOpen, '2017-06-21')

df_sh = ts.get_hist_data('sh', start=start_date)
df_sh = df_sh[['p_change', 'volume']]
df_sh.reset_index(level=0, inplace=True)
df_sh['code'] = 'sh'
dict_sh = df_sh.to_dict(orient='records')
conn.execute(p_change.insert(), dict_sh)

df_sh = ts.get_hist_data('hs300', start=start_date)
df_sh = df_sh[['p_change', 'volume']]
df_sh.reset_index(level=0, inplace=True)
df_sh['code'] = 'hs300'
dict_sh = df_sh.to_dict(orient='records')
conn.execute(p_change.insert(), dict_sh)

df_sh = ts.get_hist_data('sz50', start=start_date)
df_sh = df_sh[['p_change', 'volume']]
df_sh.reset_index(level=0, inplace=True)
df_sh['code'] = 'sz50'
dict_sh = df_sh.to_dict(orient='records')
conn.execute(p_change.insert(), dict_sh)

conn.execute('delete from p_change where code is null')
