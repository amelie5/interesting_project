import pandas as pd
import tushare as ts

def get_data():
    code='002337'
    df = ts.get_k_data(code, start='2015-01-01', end='2015-02-16', autype='hfq')
    df = df[['date', 'close']]
    df.sort_values(by='date', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def get_all_data():
    code='002337'
    df = ts.get_hist_data(code, start='2015-01-01', end='2015-02-16')
    df=df[[ 'p_change']]
    df.reset_index(level=0, inplace=True)
    benchmark = ts.get_hist_data('sh', start='2015-01-01', end='2015-02-16')
    benchmark=benchmark[['p_change']]
    benchmark.reset_index(level=0, inplace=True)
    df_all=pd.merge(df,benchmark,how='left',on='date')
    df_all.rename(columns={'p_change_x': 'rtn', 'p_change_y': 'benchmark_rtn'}, inplace=True)
    return df_all


def annual_return(df ):
    rng=pd.period_range(df['date'].iloc[0],df['date'].iloc[-1],freq='D')
    annual=pow((1+df.ix[len(df.index)-1,'close'] / df.ix[0,'close']),250/len(rng))-1
    print('年annual： %f' %annual)


def max_drawdown(df):
    df['max2here']=pd.expanding_max(df['close'])
    df['dd2here']=df['close']/df['max2here']-1
    temp=df.sort_values(by='dd2here').iloc[0][['date','dd2here']]
    max_dd=temp['dd2here']
    end_date=temp['date']
    df=df[df['date']<=end_date]
    start_date=df.sort_values(by='close',ascending=False).iloc[0]['date']
    print('最大回车：%f,开始时间：%s,结束日期：%s'%(max_dd,start_date,end_date))


def beta(df):
    b=df['rtn'].cov(df['benchmark_rtn'])/df['benchmark_rtn'].var()
    print('beta: %f'%b)

if __name__ == '__main__':
    beta(get_all_data())