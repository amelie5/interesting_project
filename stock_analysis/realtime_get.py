#coding: utf-8
from datetime import datetime, timedelta
import logging
from stock_analysis.spider_all import get_zs_tonghuashun

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='zs.log',
                filemode='a')

def work():
    df = get_zs_tonghuashun()
    logging.info(df)
    print(df)


def runTask(func, day=0, hour=0, min=0, second=0):
  # Init time
  now = datetime.now()
  strnow = now.strftime('%Y-%m-%d %H:%M:%S')

  # First next run time
  period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
  next_time = now + period
  strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
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

runTask(work, min=60/60)
#runTask(work, day=1, hour=2, min=1)