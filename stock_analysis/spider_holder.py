# coding=utf-8
import datetime
import requests
from pyquery import PyQuery as pq


def get_holder(code):
    r_list = []
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
                amount = pq(d).find('td').eq(1).text()
                dict = {'code': code, 'holder': amount, 'ctime': date}
                r_list.append(dict)

    return r_list


def get_top10(code):
    r_list = []
    url = 'http://stock.finance.qq.com/corp1/stk_ciholder.php?zqdm=' + code
    html = requests.get(url).text
    p = pq(html).find('table.list>tr')
    cnt = 0
    for d in p:
        cnt += 1
        if cnt <= 2:
            continue
        else:
            name= pq(d).find('td').eq(1).text()
            amount = pq(d).find('td').eq(2).text()
            type = pq(d).find('td').eq(3).text()
            percent = pq(d).find('td').eq(4).text()
            change = pq(d).find('td').eq(5).text()
            dict = {'code': code, 'amount': amount, 'name': name,'type': type, 'percent': percent, 'change': change}
            r_list.append(dict)

    return r_list

if __name__ == '__main__':
    list=get_holder('600403')
