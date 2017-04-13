# coding=utf-8
import pandas as pd
import requests
from pyquery import PyQuery as pq


def get_holder(code):
    df = pd.DataFrame()
    url = 'http://stock.finance.qq.com/corp1/stk_holder_count.php?zqdm='+code
    html = requests.get(url).text
    p = pq(html).find('table.list>tr')
    cnt=0
    for d in p:
        cnt+=1
        if cnt==1:
            continue
        else:
            date = pq(d).find('td').eq(0).text()
            if date=='2014-06-30':
                break
            else:
                holders = pq(d).find('td').eq(1).text()
                holders = float(holders.replace(",", ''))
                amount = pq(d).find('td').eq(4).text()
                amount = float(amount.replace(",", ''))
                df = df.append({'code': code, 'holders': holders,'amount': amount, 'date': date},ignore_index=True)

    return df


def get_top10(code):
    df = pd.DataFrame()
    url = 'http://stock.finance.qq.com/corp1/stk_ciholder.php?zqdm=' + code+'&type=2016'
    html = requests.get(url).text
    p = pq(html).find('table.list>tr')
    cnt = 0
    for d in p:
        cnt += 1
        if cnt <= 2+13:
            continue
        else:
            name= pq(d).find('td').eq(1).text()
            if name=='':
                break
            else:
                amount =pq(d).find('td').eq(2).text()
                amount = amount.replace(",", '')
                amount = float(amount)
                type = pq(d).find('td').eq(3).text()
                percent = pq(d).find('td').eq(4).text()
                percent=float(percent.replace("%", ''))
                change = pq(d).find('td').eq(5).text()
                df = df.append({'code': code, 'amount': amount, 'company': name,'type': type, 'percent': percent, 'change': change,'date':''}, ignore_index=True)

    return df

if __name__ == '__main__':
    list=get_top10('600917')
    print(list)
