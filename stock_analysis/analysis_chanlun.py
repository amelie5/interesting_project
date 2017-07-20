# -*- coding: utf-8 -*-

__author__ = 'amelie'
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, Integer, Date
from datetime import timedelta,datetime
date='2017-06-27'

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
conn = engine.connect()

r = conn.execute('select code from (select close,t1.code,m5 from '
                   '(select close,code from price_amount where date=%s)t1 '
                   'INNER JOIN (select close as m5,code from five_day_price where date=%s)t2 '
                   'on t1.code=t2.code)t where close>m5 and code not like %s',date,date,'%300%' )
res = r.fetchall()
for x in res:
    code=x[0]
    r_1=conn.execute('select low,high,close from price_amount where code=%s and date<=%s order by date desc limit 3', code, date)
    res_1=r_1.fetchall()
    low3=res_1[0][0]
    low2 = res_1[1][0]
    low1 = res_1[2][0]
    high3=res_1[0][1]
    high2 = res_1[1][1]
    high1 = res_1[2][1]
    close3=res_1[0][2]
    if(low1>low2 and low3>low2 and high1>high2 and high3>high2):

        if(high3>high1 and close3>(high1+low1)/2):
            r_2 = conn.execute(
                'select p_change from p_change where code=%s and date=%s order by date desc limit 3', code,date)
            res_2 = r_2.fetchall()
            p_change = res_2[0][0]
            if(p_change>=3):
                print(code)





