import sqlite3
import time
import tushare as ts

# sql ="select * from table"
#　f = pd.read_sql(sql,rc)

rc = sqlite3.connect(":memory:");                         # 建内存数据库
# 获取“小时分钟”数据
n =int(str(time.localtime(time.time()).tm_hour).zfill(2) + str(time.localtime(time.time()).tm_min).zfill(2))
i = n
min_list = []
while i < 929:
    a = str(time.localtime(time.time()).tm_hour).zfill(2) + str(time.localtime(time.time()).tm_min).zfill(2)
    i = int(a)
    print('等开',a)
    time.sleep(60)
while i < 1131:
    a = str(time.localtime(time.time()).tm_hour).zfill(2) + str(time.localtime(time.time()).tm_min).zfill(2)
    df = ts.get_today_all()
    df.to_sql(name= a, con=rc, if_exists='append')                        # 以小时分钟为表名
    min_list.append(a)                                                # 数据库中表名列表
    print(a)
    time.sleep(60)
    i = int(a)
while i < 1300:
    a = str(time.localtime(time.time()).tm_hour).zfill(2) + str(time.localtime(time.time()).tm_min).zfill(2)
    print('等下午开',a)
    time.sleep(60)
    i = int(a)
while i < 1501:
    a = str(time.localtime(time.time()).tm_hour).zfill(2) + str(time.localtime(time.time()).tm_min).zfill(2)
    df = ts.get_today_all()
    df.to_sql(name= a, con=rc, if_exists='append')
    min_list.append(a)
    print(a)
    i = int(a)
    time.sleep(60)