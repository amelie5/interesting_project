import math
from datetime import datetime
from datetime import timedelta

import pandas as pd
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, String, TIMESTAMP, FLOAT,DATE

DAY_NEM = 5

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


def n_day_analysis():
    engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
    metadata = MetaData()
    # 定义表
    max_change = Table('max_change', metadata,
                    Column('code', String(10), nullable=False),
                    Column('max_change', FLOAT, nullable=False),
                    Column('start', DATE, nullable=False),
                    Column('end', DATE, nullable=False)
                    )
    # 初始化数据库
    metadata.create_all(engine)
    conn = engine.connect()
    conn.execute("delete from max_change where start>='2017-06-01'")
    r1 = conn.execute('select * from stock_basics b left JOIN new_stock_open n on b.code=n.code where  b.timeToMarket!=0000-00-00 and b.timeToMarket<%s', '2017-05-29')
    res1 = r1.fetchall()
    for x in res1:
        last = result = 0
        start = end = ''
        code = x[0]
        print(code)
        time_to_open=x[8]
        if time_to_open==None:
            time_to_open='2017-06-12'
        else:
            time_to_open=time_to_open.strftime("%Y-%m-%d")
        r = conn.execute('select * from p_change where code=%s and date>=%s and date>=%s and date<=%s order by date',code,time_to_open, '2017-06-12','2017-06-16')
        res = r.fetchall()
        if not res:
            continue
        new_start=res[0][0].strftime("%Y-%m-%d")
        for j in res:
            last =last + j[2]
            if last>=result:
                result=last
                start=new_start
                end=j[0]
            elif last<0:
                last=0
                new_start=j[0].strftime("%Y-%m-%d")
        if start=='':
            end=start=new_start
        d = {'start': start,'end':end, 'max_change': result, 'code': code}
        conn.execute(max_change.insert(), d)


    # d = df_a.to_dict(orient='records')
    # conn.execute("delete from max_change")

def get_data_sh():
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
    df=ts.get_hist_data('sh',start='2017-05-09')
    df = df[['p_change', 'volume']]
    df.reset_index(level=0, inplace=True)
    df['code'] = 'sh'
    dict = df.to_dict(orient='records')
    conn.execute(p_change.insert(), dict)



if __name__ == '__main__':
    n_day_analysis()
