import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, String, TIMESTAMP, FLOAT
import datetime

# 网格法则：
# 1.初始值（越低越好）
# 2.格子密度3%-5%
# 3.每个格子的资金（跌的越多越买）
# 4.每个格子卖多少


# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
# 获取数据库连接
conn = engine.connect()

FUND = 54000
START = 26.68
start = START
num = round(6000 / START, 0)
cang = round(num * START, 2)
fund_now = FUND - cang
GRID = 5
GRID_NUM = 10
GRID_PRICE = 3000
buy = sell = buy_num = sell_num = h_level = l_level = 0

r1 = conn.execute('select date,high,low,close from price_amount where code=%s and date>=%s order by date', '603628',
                  '2017-04-27')
res = r1.fetchall()
for x in res:
    date = x[0]
    high = x[1]
    low = x[2]
    close = x[3]

    n_h = (high - START) / START * 100
    n_l = (low - START) / START * 100

    if ((n_l < 0) & (n_l <= -GRID * (l_level + 1))):
        buy_num = round(GRID_PRICE / (START * GRID * (l_level + 1)), 0)
        buy = round(buy_num * START * GRID * (l_level + 1), 2)
        l_level = l_level + 1

    if ((n_l < 0) & (n_l <= -GRID * (l_level + 1))):
        buy_num = buy_num+round(GRID_PRICE / (START * GRID * (l_level + 1)), 0)
        buy = buy+round(round(GRID_PRICE / (START * GRID * (l_level + 1)), 0) * START * GRID * (l_level + 1), 2)
        l_level = l_level + 1

    if ((n_h > 0) & (n_h >= GRID * (h_level + 1))):
        if cang >= 100:
            sell_num = round(GRID_PRICE / (START * GRID * (h_level + 1)), 0)
            sell = round(sell_num * START * GRID * (h_level + 1), 2)
            if cang - sell < 0:
                sell_num = round(cang / (START * GRID * (h_level + 1)), 0)
                sell = round(sell_num * START * GRID * (h_level + 1), 2)

            h_level = h_level + 1

    if ((n_h > 0) & (n_h >= GRID * (h_level + 1))):
        if cang >= 100:
            sell_num = sell_num+round(GRID_PRICE / (START * GRID * (h_level + 1)), 0)
            sell = sell+round(round(GRID_PRICE / (START * GRID * (h_level + 1)), 0) * START * GRID * (h_level + 1), 2)
            if cang - sell < 0:
                sell_num = sell_num+round(cang / (START * GRID * (h_level + 1)), 0)
                sell = sell+round(round(cang / (START * GRID * (h_level + 1)), 0) * START * GRID * (h_level + 1), 2)

            h_level = h_level + 1

    num = round(num - sell_num + buy_num,0)
    cang = cang  + buy - sell
    cang_per = round(cang / FUND, 4) * 100
    fund_now = FUND - cang
    sum_new = round(num * close + fund_now, 2)
    profit = sum_new - FUND

    buy = sell = buy_num = sell_num = 0
    print(date, close, num, cang, cang_per, profit)

    buy = sell = buy_num = sell_num = 0
