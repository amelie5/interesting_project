import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, String, TIMESTAMP, FLOAT
import datetime

# 网格法则：
# 1.初始值（越低越好）
# 2.格子密度3%
# 3.每个格子的资金（跌的越多越买）
# 4.每个格子卖多少


# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
# 获取数据库连接
conn = engine.connect()

FUND = 100000
START = 9.10
num=round(10000/START,0)
cang=round(num*START,2)
fund_now=FUND-cang
GRID=3
GRID_PRICE=10000
buy=sell=buy_num=sell_num=0

r1 = conn.execute('select date,close from price_amount where code=%s and date>=%s order by date','000001','2017-01-01')
res = r1.fetchall()
for x in res:
    date=x[0]
    now = x[1]

    n = (now - START)/ START*100

    if ((n < 0)& (n/-GRID>=1)):
        buy_num = round(GRID_PRICE / START, 0)
        buy = round(buy_num*START,2)
        START = now

    if ((n > 0) & (n/GRID>=1)):
        sell_num = round(GRID_PRICE / START, 0)
        sell = round(sell_num*START,2)
        START=now

    num=num-sell_num+buy_num
    cang = cang + buy - sell
    cang_per=round(cang/FUND,4)*100
    fund_now = FUND - cang
    sum_new=round(num*now+fund_now,2)

    buy = sell = buy_num = sell_num = 0
    print(date,now,num,cang,cang_per,fund_now,sum_new)

