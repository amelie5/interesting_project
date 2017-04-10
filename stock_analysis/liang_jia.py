import math
import tushare as ts
import pandas as pd

# df = ts.get_tick_data('600848',date='2014-01-09')
# df_b=df[df['type']=='买盘']
# df_s=df[df['type']=='卖盘']
# b=df_b['amount'].sum()
# s=df_s['amount'].sum()
# b_v=df_b['volume'].sum()
# s_v=df_s['volume'].sum()
# print('买量是 %i,卖量是 %i，买进手为%i，卖出手为%i'%(b,s,b_v,s_v))

day_num=5
#df=ts.get_today_ticks('600403')
df=ts.get_today_all()
print(df)
# df=ts.get_today_all()
# df1=ts.get_today_all()
# r=pd.merge(df,df1,on='code')
# r=r.apply(lambda x: x['changepercent_y']-x['changepercent_x'], axis=1)

