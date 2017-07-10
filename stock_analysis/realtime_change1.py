#coding: utf-8
import logging
from datetime import datetime, timedelta
from spider_all import get_zs_tonghuashun

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='zs.log',
                filemode='a')

def work():
    df=get_zs_tonghuashun()
    print(df)


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

runTask(work, min=3)
