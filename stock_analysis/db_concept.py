# -*- coding: utf-8 -*-
__author__ = 'amelie'

import tushare as ts
from sqlalchemy import create_engine,Table,Column,MetaData, String
from stock_analysis.spider_all import get_concept_name,get_concept

list = get_concept_name()
df=get_concept(list)
d = df.to_dict(orient='records')
print("get basics already!")

#连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata=MetaData()
#定义表
concept = Table('concept', metadata,
        Column('code', String(10), nullable=False),
        Column('concept', String(50), nullable=False)
    )
#初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
conn.execute("delete from concept")
r = conn.execute(concept.insert(), d)