# -*- coding: utf-8 -*-

__author__ = 'amelie'
import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, Integer, TIMESTAMP
from datetime import timedelta,datetime

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
market = Table('market', metadata,
               Column('date',TIMESTAMP , nullable=True),
               Column('total_num', Integer, nullable=True),
               Column('zhangting_num', Integer, nullable=True),
               Column('dieting_num', Integer, nullable=True),
               Column('zhang_num', Integer, nullable=True),
               Column('die_num', Integer, nullable=True),
               Column('volume', Integer, nullable=True),
               Column('p_change', FLOAT, nullable=True),
               Column('price', FLOAT, nullable=True)
               )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()

r_d = conn.execute("select max(date) from market")
res_d = r_d.fetchall()
start_date = res_d[0][0]
start_date = start_date + timedelta(days=1)
start_date = start_date.strftime("%Y-%m-%d")

while ts.is_holiday(start_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    start_date = start_date + timedelta(days=1)
    start_date = start_date.strftime("%Y-%m-%d")

conn.execute('delete from market where date>=%s',start_date)
r1 = conn.execute('select date from p_change where code=%s and date>=%s order by date','000001',start_date)
res = r1.fetchall()
for x in res:
    date = x[0]
    date = date.strftime("%Y-%m-%d")
    print(date)
    sql = "insert into market \n" \
          "select t1.date,cnt,zhangting_sum,dieting_sum,zhang_sum,die_sum,volume,p_change,price from\n" \
          "(select count(1)as cnt from stock_basics where timeToMarket!='0000-00-00' and code not in\n" \
          "(select code from new_stock_open where timeToOpen>'" + date + "')\n" \
                                                                         ")t2\n" \
                                                                         "LEFT JOIN\n" \
                                                                         "(select date,\n" \
                                                                         "count(case when ntype='涨停' then 1 else null end) as 'zhangting_sum',\n" \
                                                                         "count(case when ntype='跌停' then 1 else null end) as 'dieting_sum',\n" \
                                                                         "count(case when ntype='涨' then 1 else null end) as 'zhang_sum',\n" \
                                                                         "count(case when ntype='跌' then 1 else null end) as 'die_sum'\n" \
                                                                         "from\n" \
                                                                         "(SELECT date,\n" \
                                                                         "case\n" \
                                                                         "when p_change>=9.90 then '涨停'\n" \
                                                                         "when p_change<=-9.90 then '跌停'\n" \
                                                                         "when p_change>0 then '涨'\n" \
                                                                         "when p_change<0 then '跌'\n" \
                                                                         "else '0'\n" \
                                                                         "end as ntype\n" \
                                                                         "from p_change where date='" + date + "' and code!='sh' )t\n" \
                                                                                                               "group by 1)t1\n" \
                                                                                                               "on 1=1\n" \
                                                                                                               "LEFT JOIN\n" \
                                                                                                               "(select date,ROUND(avg(p_change),2) as p_change from p_change where date='" + date + "' and code!='sh' group by 1)t3\n" \
                                                                                                                                                                                                     "on t3.date=t1.date\n" \
                                                                                                                                                                                                     "LEFT JOIN\n" \
                                                                                                                                                                                                     "(select date,sum(ROUND(volume,0))as volume from p_change where date='" + date + "' and code!='sh' group by 1)t4\n" \
                                                                                                                                                                                                                                                                                      "on t4.date=t1.date\n" \
                                                                                                                                                                                                                                                                                      "LEFT JOIN\n" \
                                                                                                                                                                                                                                                                                      "(select date,ROUND(avg(close),2) as price from price_amount where date='" + date + "' and code!='sh' group by 1)t5\n" \
                                                                                                                                                                                                                                                                                                                                                                          "on t5.date=t1.date"
    conn.execute(sql)
