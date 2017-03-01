import pandas as pd

def annual_return(date_line,price_line ):
    df=pd.DataFrame({'date':date_line,'price':price_line})
    df.sour_values(by='date',inplace=True)
    df.reset_index(drop=True,inplace=True)
    rng=pd.period_range(df['date'].icol[0],df['date'].iloc[-1],freq='D')
    annual=pow(df.ix[len(df.index)-1,'price'] / df.ix[0,'price'],250/len(rng))-1
    print('年化收益： %f' %annual)

if __name__ == '__main__':
    annual_return()