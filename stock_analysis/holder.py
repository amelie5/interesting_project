import tushare as ts

df,data=ts.top10_holders(code='600000',gdtype='1')#ddype=1 为流通前十大
df=df.sort_values('quarter',ascending=True)
print(df)