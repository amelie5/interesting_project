from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, DATE, Integer, TIMESTAMP
from chanlun_util import find_peak_and_bottom,KLineDTO,fen_bi
from datetime import datetime
import matplotlib as mat
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import time
import pandas as pd
from numpy import array

date='2015-06-01'
date2='2017-09-06'

k_line_list=[]
# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
conn = engine.connect()
rr=conn.execute('select code,name,timeToMarket,pe,pb from stock_basics where timeToMarket!=0000-00-00 order by timeToMarket')
r_r = rr.fetchall()
for x in r_r:
    code = x[0]
    name=x[1]
    timeToMarket=x[2]
    pe=x[3]
    pb=x[4]
    r = conn.execute('select date,high,low,open,close from price_amount where code=%s and date>=%s and date<=%s order by date', code,
                     date, date2)
    res = r.fetchall()
    quotes = pd.DataFrame(res)
    quotes.columns = r.keys()
    uotes= quotes.dropna()
    Close=quotes['close']
    Open=quotes['open']
    High=quotes['high']
    Low=quotes['low']
    T0 = quotes['date']
    length=len(Close)

    '''K线图绘制开始'''
    fig = plt.figure(figsize=(16, 8))
    ax1 = plt.subplot2grid((10,4),(0,0),rowspan=10,colspan=4)
    #fig = plt.figure()
    #ax1 = plt.axes([0,0,3,2])

    X=np.array(range(0, length))
    pad_nan=X+np.nan

        #计算上 下影线
    max_clop=Close.copy()
    max_clop[Close<Open]=Open[Close<Open]
    min_clop=Close.copy()
    min_clop[Close>Open]=Open[Close>Open]

        #上影线
    line_up=np.array([High,max_clop,pad_nan])
    line_up=np.ravel(line_up,'F')
        #下影线
    line_down=np.array([Low,min_clop,pad_nan])
    line_down=np.ravel(line_down,'F')

        #计算上下影线对应的X坐标
    pad_nan=np.nan+X
    pad_X=np.array([X,X,X])
    pad_X=np.ravel(pad_X,'F')


        #画出实体部分,先画收盘价在上的部分
    up_cl=Close.copy()
    up_cl[Close<=Open]=np.nan
    up_op=Open.copy()
    up_op[Close<=Open]=np.nan

    down_cl=Close.copy()
    down_cl[Open<=Close]=np.nan
    down_op=Open.copy()
    down_op[Open<=Close]=np.nan


    even=Close.copy()
    even[Close!=Open]=np.nan

    #画出收红的实体部分
    pad_box_up=np.array([up_op,up_op,up_cl,up_cl,pad_nan])
    pad_box_up=np.ravel(pad_box_up,'F')
    pad_box_down=np.array([down_cl,down_cl,down_op,down_op,pad_nan])
    pad_box_down=np.ravel(pad_box_down,'F')
    pad_box_even=np.array([even,even,even,even,pad_nan])
    pad_box_even=np.ravel(pad_box_even,'F')

    #X的nan可以不用与y一一对应
    X_left=X-0.25
    X_right=X+0.25
    box_X=np.array([X_left,X_right,X_right,X_left,pad_nan])
    box_X=np.ravel(box_X,'F')

    #Close_handle=plt.plot(pad_X,line_up,color='k')

    vertices_up=array([box_X,pad_box_up]).T
    vertices_down=array([box_X,pad_box_down]).T
    vertices_even=array([box_X,pad_box_even]).T

    handle_box_up=mat.patches.Polygon(vertices_up,color='r',zorder=1)
    handle_box_down=mat.patches.Polygon(vertices_down,color='g',zorder=1)
    handle_box_even=mat.patches.Polygon(vertices_even,color='k',zorder=1)

    ax1.add_patch(handle_box_up)
    ax1.add_patch(handle_box_down)
    ax1.add_patch(handle_box_even)

    handle_line_up=mat.lines.Line2D(pad_X,line_up,color='k',linestyle='solid',zorder=0)
    handle_line_down=mat.lines.Line2D(pad_X,line_down,color='k',linestyle='solid',zorder=0)

    ax1.add_line(handle_line_up)
    ax1.add_line(handle_line_down)

    v=[0,length,Open.min()-0.5,Open.max()+0.5]
    plt.axis(v)
    T1=T0[-len(T0):].astype(dt.date)
    #T1 = tmp/1000000000
    Ti=[]
    interval=10
    for i in range(int(len(T0)/interval)):
        a=i*interval
        Ti.append(T1[a])
        #print tab

    Ti.append(T1[len(T0)-1])
    ax1.set_xticks(np.linspace(-2,len(Close)+2,len(Ti)))

    ll=Low.min()*0.97
    hh=High.max()*1.03
    ax1.set_ylim(ll,hh)

    ax1.set_xticklabels(Ti)
    import matplotlib.font_manager as fm
    myfont = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')
    plt.title(name+"   pe:"+str(pe)+"       pb:"+str(pb), fontproperties=myfont)

    plt.grid(True)
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    '''K线图绘制完毕'''


    plt.show()
    plt.close()
