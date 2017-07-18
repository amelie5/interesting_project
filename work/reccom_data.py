# -*- coding: utf-8 -*-

__author__ = 'amelie'
from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, Integer, Date
import pandas as pd

def transfer(a_list,x):
    b_list=x.split(',')
    ret_list = list((set(a_list).union(set(b_list))) ^ (set(a_list) ^ set(b_list)))
    return len(ret_list)


engine = create_engine('mysql+pymysql://shaolianjie:abcd1234@127.0.0.1:8088/ns_crm_service?charset=utf8')
metadata = MetaData()
topic_rule = Table('topic_rule', metadata,
            Column('topic_origin', String(100), nullable=True),
            Column('topic_new', String(100), nullable=True)
            )
metadata.create_all(engine)
conn = engine.connect()
r_1 = conn.execute("select topic,num from topic_num where num>=100 order by num desc limit 50")
res_1 = r_1.fetchall()
df = pd.DataFrame(res_1)
df.columns = r_1.keys()
r = conn.execute("select topic from topic_num where num<=99 and num>90 order by num desc limit 100")
res = r.fetchall()
df_a = pd.DataFrame()
for x in res:
    topic_origin = x[0]
    topic_list=topic_origin.split(',')
    if(len(topic_list)==1):
        continue
    else:
        df_1=df
        df_1['b'] = df_1.apply(lambda x: transfer(topic_list,x['topic']), axis=1)
        df_1=df_1[df_1['b']>0]
        df_1.sort_values(by='num',ascending=False, inplace=True)
        topic_new=df_1.iloc[0, 0]
        df_a = df_a.append({"topic_origin": topic_origin, "topic_new": topic_new}, ignore_index=True)

d = df_a.to_dict(orient='records')
conn.execute(topic_rule.insert(), d)
