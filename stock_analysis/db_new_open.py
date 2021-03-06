from datetime import timedelta

import pandas as pd
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, DATE, Integer

NOTIFY_DAY = 60


def transfer(x):
    y = float(x)
    ntype = 'false'
    if y >= 9.0:
        ntype = 'true'
    return ntype


# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
new_stock_open = Table('new_stock_open', metadata,
                       Column('code', String(10), nullable=True),
                       Column('timeToOpen', DATE, nullable=True),
                       Column('days', Integer, nullable=True),
                       Column('f_0', FLOAT, nullable=True),
                       Column('f_1', FLOAT, nullable=True),
                       Column('f_2', FLOAT, nullable=True)
                       )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()


r_d = conn.execute(
    'select timeToMarket from(select * from new_stock_open)t INNER JOIN stock_basics b on t.code=b.code where f_2=%s order by timeToMarket limit 1',
    '-999')
res_d = r_d.fetchall()
start_date = res_d[0][0]
start_date = start_date.strftime("%Y-%m-%d")
conn.execute(
    'delete from new_stock_open where code in(select code from stock_basics where timeToMarket>=(select timeToMarket from (select * from new_stock_open)t INNER JOIN stock_basics b on t.code=b.code where f_2=%s order by timeToMarket limit 1))',
    '-999')


# conn.execute('delete from new_stock_open')
# start_date='2014-12-01'


r1 = conn.execute(
    'select * from stock_basics where timeToMarket!=0000-00-00 and timeToMarket>=%s order by timeToMarket', start_date)
res = r1.fetchall()
df_n = pd.DataFrame()
for x in res:
    timetoMark = x[3]
    code = x[0]
    print('new open:',code)
    name = x[1]

    end_date = timetoMark + timedelta(days=NOTIFY_DAY)
    end_date = end_date.strftime("%Y-%m-%d")

    df = ts.get_hist_data(code, end=end_date)
    df = df[['open', 'high', 'close', 'low', 'p_change']]
    df.reset_index(level=0, inplace=True)
    df.sort_values(by='date', inplace=True)
    df_c = df[(df['low'] == df['close']) & (df['high'] == df['close']) & (df['p_change'] != 0.0)]
    days = len(df_c)
    df_o = df.merge(df_c, indicator=True, how='outer')
    df_o = df_o[df_o['_merge'] == 'left_only']
    df_o = df_o[df_o['p_change'] < 30.0]
    if (df_o.empty):
        day_open = '3020-01-01'
        f_0 = -999
        f_1 = -999
        f_2 = -999
    elif (len(df_o) == 1):
        day_open = df_o.iloc[0, 0]
        f_0 = df_o.iloc[0, 5]
        f_1 = -999
        f_2 = -999
    elif (len(df_o) == 2):
        day_open = df_o.iloc[0, 0]
        f_0 = df_o.iloc[0, 5]
        f_1 = df_o.iloc[1, 5]
        f_2 = -999
    else:
        day_open = df_o.iloc[0, 0]
        f_0 = df_o.iloc[0, 5]
        f_1 = df_o.iloc[1, 5]
        f_2 = df_o.iloc[2, 5]

    # df_n=df_n.append({"code":code,"name":name,"timetoMark":timetoMark,"timeToOpen":day_open,"days":days,"f_0":f_0,"f_1":f_1,"f_2":f_2},ignore_index=True)
    df_n = df_n.append(
        {"code": code, "timeToOpen": day_open, "days": days, "f_0": float(f_0),
         "f_1": float(f_1), "f_2": float(f_2)}, ignore_index=True)

d = df_n.to_dict(orient='records')
conn.execute(new_stock_open.insert(), d)

# df_n['f_0_new']=df_n['f_0'].map(transfer)
# df_n['f_1_new']=df_n['f_1'].map(transfer)
# df_n['f_2_new']=df_n['f_2'].map(transfer)


# df_n.to_excel('d:/data/stock/new_stock.xlsx')
