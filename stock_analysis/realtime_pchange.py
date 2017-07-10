#coding: utf-8
import logging
from datetime import datetime, timedelta

import pandas as pd
import tushare as ts
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='zs.log',
                filemode='a')

def work_all():
    # 连接数据库
    engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
    # 获取数据库连接
    conn = engine.connect()
    r = conn.execute("select code from new_stock_open where timeToOpen='3020-01-01'")
    res = r.fetchall()
    df_no = pd.DataFrame(res)
    df_no.columns = r.keys()

    df=ts.get_today_all()
    df_2 = df[['code', 'name', 'changepercent']]

    df_2.sort_values(by='changepercent', inplace=True, ascending=False)
    df_2=df_2[df_2['changepercent']<=11]
    df_o = df_2.merge(df_no, indicator=True, how='outer',on=['code'])
    df_o = df_o[df_o['_merge'] == 'left_only']
    print(df_o.head(40))


def runTask(func, day=0, hour=0, min=0, second=0):
  now = datetime.now()
  period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
  strnext_time = now.strftime('%Y-%m-%d %H:%M:%S')
  while True:
      iter_now = datetime.now()
      iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
      if str(iter_now_time) == str(strnext_time):
          func()
          iter_time = iter_now + period
          strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
          continue

runTask(work_all, min=3)
