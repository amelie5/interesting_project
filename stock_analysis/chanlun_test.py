from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, DATE, Integer, TIMESTAMP
from chanlun_util import find_peak_and_bottom, KLineDTO, fen_bi
from datetime import datetime

date = '2017-06-01'
date2 = '2017-07-20'
code = '601318'
k_line_list=[]

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
conn = engine.connect()

r = conn.execute('select date,high,low,open,close from price_amount where code=%s and date>=%s and date<=%s order by date', code,
                 date, date2)
res = r.fetchall()
for x in res:
    date_time = x[0]
    open_price = x[3]
    close_price = x[4]
    high_price = x[1]
    low_price = x[2]
    k_line_dto = KLineDTO(date_time, date_time, date_time, open_price, high_price, low_price, close_price)
    k_line_list.append(k_line_dto)

merge_line_list = find_peak_and_bottom(k_line_list, "down")
fenbi_result, final_result_array, fenbi_seq_list = fen_bi(merge_line_list,True)
