import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, String, TIMESTAMP, FLOAT
import datetime

start_date =datetime.date.today()
start_date=start_date.strftime('%Y-%m-%d')
start_date='2015-01-01'

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

r1 = conn.execute('select * from stock_basics where timeToMarket!=0000-00-00 ' )
res = r1.fetchall()
for x in res:
    code = x[0]
    print(code)
    df = ts.get_hist_data(code, start=start_date)
    df = df[['p_change', 'volume']]
    df.reset_index(level=0, inplace=True)
    df['code'] = code
    dict = df.to_dict(orient='records')
    conn.execute(p_change.insert(), dict)

df_sh = ts.get_hist_data('sh', start=start_date)
df_sh = df_sh[['p_change', 'volume']]
df_sh.reset_index(level=0, inplace=True)
df_sh['code'] = 'sh'
dict_sh = df_sh.to_dict(orient='records')
conn.execute(p_change.insert(), dict_sh)
