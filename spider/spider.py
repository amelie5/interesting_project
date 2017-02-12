# coding=utf-8
import datetime
import requests
from pyquery import PyQuery as pq


def get_list(date):
    url_list=[]
    url = 'http://data.10jqka.com.cn/market/longhu/date/'+date+'/'
    html = requests.get(url).text
    p = pq(html).find('div#lhdata>table.m_table>tbody>tr')
    for d in p:
        trader = pq(d).find('td').eq(1)
        url_list.append(pq(trader).find('a').text())

    return list(set(url_list))

def get_data(code,ctime):
        r_list=[]
        ntype='b'
        trader=''
        cnt=0
        url='http://data.10jqka.com.cn/ifmarket/getnewlh/code/'+code+'/date/'+ctime+'/'
        html = requests.get(url).text
        p = pq(html).find('tr')
        for d in p:
            html_trader=pq(pq(d).find('td').eq(1)).find('a').text()
            if(html_trader==''):
                cnt=cnt+1
            else:
                if(trader==''):
                    trader=html_trader
                else:
                    trader = '%s%s%s' % (trader, ';', html_trader)
            if(cnt==3):
                dict={'code': code, 'ntype': ntype, 'traders':trader, 'ctime':ctime}
                r_list.append(dict)
                ntype='s'
                trader=''
                cnt=cnt+1
            dict={'code': code, 'ntype': ntype, 'traders':trader, 'ctime':ctime}
            r_list.append(dict)

        print(r_list)

def get_date():
    date_list=list()
    begin = datetime.date(2017,2, 10)
    end = datetime.date(2017, 2, 10)
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        print(str(day))
        date_list.append(str(day))
    return date_list

def func():
    date_list=get_date()
    for date in date_list:
        code_list=get_list(date)
        for code in code_list:
            get_data(code,date)



if __name__=='__main__':
    func()