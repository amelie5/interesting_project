import tushare as ts


def transfer(x):
    ntype=''
    if x >= 9.0:
        ntype='10'
    elif x>=5:
        ntype='5-10'
    elif x>=1:
        ntype='1-5'
    elif x>=-1:
        ntype='-1-1'
    elif x>=-5:
        ntype='-5- -1'
    elif x>-9.0:
        ntype='-10- -5'
    else:
        ntype='-10'
    return ntype

df=ts.get_today_all()

df['c']=df.apply(lambda  x: transfer(x['changepercent']),axis=1)
cnt=df.groupby(df['c']).size().rename('counts')
print(cnt)

