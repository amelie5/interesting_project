# coding=utf-8
from pandas import DataFrame
import pandas as pd
import requests
from pyquery import PyQuery as pq


def get_zs_tonghuashun():
    r_list = []

    url = 'http://q.10jqka.com.cn/index/index/board/all/field/zs/order/desc/page/1/ajax/1/'
    html = requests.get(url).text
    p = pq(html).find('table.m-table>tbody>tr')
    for d in p:
        speed = pq(d).find('td').eq(6).text()
        code = pq(d).find('td').eq(1).text()
        name = pq(d).find('td').eq(2).text()
        price = pq(d).find('td').eq(3).text()
        change = pq(d).find('td').eq(4).text()
        speed = pq(d).find('td').eq(6).text()
        change_shou = pq(d).find('td').eq(7).text()
        dict = {'code': code, 'name': name, 'change': change, 'price': price, 'speed': float(speed),
                    'change_shou': change_shou}
        r_list.append(dict)

    df = pd.DataFrame(r_list)
    return df

def get_zs_dongfang():
    r_list = []
    url = 'http://quote.eastmoney.com/center/list.html#33'
    html = requests.get(url).text
    p = pq(html).find('table.m-table>tbody>tr')
    for d in p:
        speed = pq(d).find('td').eq(6).text()
        code = pq(d).find('td').eq(1).text()
        name = pq(d).find('td').eq(2).text()
        price = pq(d).find('td').eq(3).text()
        change = pq(d).find('td').eq(4).text()
        speed = pq(d).find('td').eq(6).text()
        change_shou = pq(d).find('td').eq(7).text()
        dict = {'code': code, 'name': name, 'change': change, 'price': price, 'speed': float(speed),
                    'change_shou': change_shou}
        r_list.append(dict)

    df = pd.DataFrame(r_list)
    return df

if __name__ == '__main__':
    df = get_zs()
    print(df)
