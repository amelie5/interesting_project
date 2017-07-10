#coding: utf-8
import logging
from datetime import datetime, timedelta
import tushare as ts

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='zs.log',
                filemode='a')

def transfer(x):
    ntype=''
    if x >= 9.9:
        ntype='10'
    elif x>=5:
        ntype='5-9'
    elif x>=0:
        ntype='0-5'
    elif x>=-5:
        ntype='-5-0'
    elif x >= -9.9:
        ntype = '-10- -5'
    else:
        ntype='-10'
    return ntype

def work():
    #get_tx_minite()
    df=ts.get_today_all()
    df=df[['code','name','changepercent','trade']]
    df.sort_values(by='changepercent', ascending=False, inplace=True)
    print(df.head(30))


def work_all():
    df=ts.get_today_all()
    df=df[['changepercent','trade','volume']]
    print(df.describe())
    df['c'] = df.apply(lambda x: transfer(x['changepercent']), axis=1)
    cnt = df.groupby(df['c']).size()
    #logging.info(cnt)
    print(cnt)


def runTask(func, day=0, hour=0, min=0, second=0):
  # Init time
  now = datetime.now()
  period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
  strnext_time = now.strftime('%Y-%m-%d %H:%M:%S')
  while True:
      # Get system current time
      iter_now = datetime.now()
      iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
      if str(iter_now_time) == str(strnext_time):
          # Get every start work time
          #print ("start work: %s" % iter_now_time)
          # Call task func
          func()

          # Get next iteration time
          iter_time = iter_now + period
          strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')

          # Continue next iteration
          continue

runTask(work_all, min=3)
#runTask(work, day=1, hour=2, min=1)