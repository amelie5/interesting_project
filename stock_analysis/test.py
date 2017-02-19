import tushare as ts
from datetime import datetime
from pandas import DataFrame

a = datetime.now()
b = datetime.now()
print((b - a).seconds)

df = DataFrame({'data': [1, 2, 6, -6]})
cnt = df.groupby(df['data']).size()
df = ts.get_tick_data('600848', date='2017-02-17').sort(columns='time').head(5)

start_price = df['price'].head(1).values

print(start_price)
# list_price = df.apply(lambda x: x['changepercent'] - start_price, axis=1).values
# print(list_price)
