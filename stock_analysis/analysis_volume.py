import tushare as ts
from sqlalchemy import create_engine, Table, Column, MetaData, String, TIMESTAMP, FLOAT
import datetime
import matplotlib.pyplot as plt

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
metadata = MetaData()
# 定义表
p_change = Table('p_change_2', metadata,
                 Column('date', TIMESTAMP, nullable=True),
                 Column('volume', FLOAT, nullable=True),
                 Column('p_change', FLOAT, nullable=True),
                 Column('rate', FLOAT, nullable=True)
                 )
# 初始化数据库
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()
conn.execute("truncate table p_change_2")

df = ts.get_hist_data('002809', start='2016-06-01')
df = df[[ 'p_change','volume']]
df['rate']=df['volume'].pct_change()
df=df.fillna(0)
df.reset_index(level=0, inplace=True)

# df.sort_values(by='date', inplace=True)
# df=df[[ 'rate']]
# df.plot()
# plt.show()


dict = df.to_dict(orient='records')
conn.execute(p_change.insert(), dict)


