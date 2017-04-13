import math
from datetime import datetime
from datetime import timedelta

import pandas as pd
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, String, TIMESTAMP, FLOAT

DAY_NEM = 5


def get_data():
    # 连接数据库
    engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
    metadata = MetaData()
    # 定义表
    p_change = Table('p_change', metadata,
                     Column('date', TIMESTAMP, nullable=True),
                     Column('volume', FLOAT, nullable=True),
                     Column('p_change', FLOAT, nullable=True),
                     Column('turnover', FLOAT, nullable=True),
                     Column('code', String(10), nullable=True)
                     )
    # 初始化数据库
    metadata.create_all(engine)
    # 获取数据库连接
    conn = engine.connect()
    r1 = conn.execute('select * from stock_basics where timeToMarket!=0000-00-00 and timeToMarket<%s', '2017-03-27')
    res = r1.fetchall()
    a_list=[]
    for x in res:
        code = x[0]
        print(code)
        df = ts.get_hist_data(code, start='2017-04-11')
        df = df[['p_change', 'volume']]
        df.reset_index(level=0, inplace=True)
        df['code'] = code
        df['turnover']=0
        dict = df.to_dict(orient='records')
        r = conn.execute(p_change.insert(), dict)


    # df_all = pd.DataFrame(a_list)
    # dict_2 = df_all.to_dict(orient='records')
    # r = conn.execute(p_change.insert(), dict_2)


def analysis():
    engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
    conn = engine.connect()
    r1 = conn.execute('select * from stock_basics where timeToMarket!=0000-00-00')
    res = r1.fetchall()

    for x in res:
        code = x[0]
        a_list = []
        r2 = conn.execute('select * from p_change where code=' + code)
        res1 = r2.fetchall()
        if (len(res1) == 0):
            continue
        for y in res1:
            dict = {'date': y[1], 'p_change': y[3], 'index': y[0]}
            a_list.append(dict)
        df = pd.DataFrame(a_list)
        df.sort_values(by='index', inplace=True)
        r_list = []
        for i in range(0, 10000):
            index = -1 * i
            df_shift = df.shift(index).head(DAY_NEM)
            if (math.isnan(df_shift.ix[DAY_NEM - 1, 1])):
                break
            else:
                sum = df_shift.sum()
                dict = {'date': str(df_shift.ix[0, 0]), 'p_change': sum.p_change}
                r_list.append(dict)
        df = pd.DataFrame(r_list)
        df['code'] = code
        df.sort_values(by='p_change', ascending=False, inplace=True)
        print(df)


def three_day_for_day(end_date, day_day):
    a_list = []
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = (end_date - timedelta(days=10)).strftime("%Y-%m-%d")
    engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
    conn = engine.connect()
    r1 = conn.execute('select * from stock_basics where timeToMarket!=0000-00-00 and timeToMarket<%s', '2017-03-20')
    res = r1.fetchall()
    for x in res:
        code = x[0]
        name = x[1]
        df = ts.get_hist_data(code, start=str(start_date), end=str(end_date))
        df.reset_index(level=0, inplace=True)
        df = df[['date', 'p_change']]
        df = df[0:day_day].sum()
        dict = {'date': df[0], 'p_change': df[1], 'code': code, 'name': name}
        a_list.append(dict)

    df_all = pd.DataFrame(a_list)
    df_all.sort_values(by='p_change', inplace=True, ascending=False)
    df_all.to_excel('d:/data/stock/%s_day_%s.xlsx' % (day_day, end_date))


if __name__ == '__main__':
    get_data()
