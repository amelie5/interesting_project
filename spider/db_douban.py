# -*- coding: utf-8 -*-

__author__ = 'amelie'
from sqlalchemy import create_engine, Table, Column, MetaData, BIGINT, String,FLOAT,INT
from spider_douban import get_book_tag,get_book

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
douban_book_tag = Table('douban_book_tag', metadata,
            Column('tag', String(100), nullable=True),
            Column('sub_tag', String(100), nullable=True),
            Column('num',BIGINT , nullable=True)
            )

douban_book = Table('douban_book', metadata,
            Column('tag_id', INT, nullable=True),
            Column('name', String(100), nullable=True),
            Column('score',FLOAT , nullable=True),
            Column('user',BIGINT , nullable=True)
            )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()

# r=conn.execute("delete from douban_book_tag ")
# df = get_book_tag()
# d = df.to_dict(orient='records')
# conn.execute(douban_book_tag.insert(), d)

conn.execute("delete from douban_book")
r=conn.execute("select sub_tag,id from douban_book_tag where tag='文化'")
res = r.fetchall()
for x in res:
    tag = x[0]
    id = x[1]
    print(tag)
    df = get_book(tag,id)
    d = df.to_dict(orient='records')
    conn.execute(douban_book.insert(), d)



