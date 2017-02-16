import tushare as ts
from datetime import datetime
from pandas import DataFrame
a=datetime.now()
b=datetime.now()
print((b-a).seconds)

df=DataFrame({'data':[1,2,6,-6]})
cnt=df.groupby(df['data']).size()
print(list(cnt.index))
