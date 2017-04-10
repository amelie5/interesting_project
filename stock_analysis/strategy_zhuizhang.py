import tushare as ts
import pandas as pd

df=ts.get_hist_data('002807',start='2017-01-01')
print(df)

# df_1=df.reset_index(level=0)
# df_s=df.shift(-1)
# df_s.reset_index(level=0, inplace=True)
# df_c=pd.merge(df_1,df_s,on='index')
# df=df_c[['code_x','date_y','open_y','close_x','high_y','close_y']]
# df=df[df['open_y']>df['close_x']]
# df=df[df['close_y']==df['high_y']]
# print(df)


