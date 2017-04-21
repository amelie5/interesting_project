import tushare as ts
import pandas as pd

code='002755'
df=ts.get_hist_data(code,start='2016-06-10',end='2016-08-25')
df.reset_index(level=0, inplace=True)
df=df[['date','p_change','volume','v_ma5','v_ma10','v_ma20','close','open','high','low','volume']]
df['code']=code
print(df)

#1、连续10天小阴线或小阳线，阳多阴少，不放大量
#2.10日内最大交易量不超过10日均量的1.5倍。
#3、10天前收盘价为10日内收盘价最低
#4、10日内最高价比最新收盘价高不超过2%
#5、最新收盘价比10日前收盘价高5%且不超过10%
#6、5日均量超过10日均量








