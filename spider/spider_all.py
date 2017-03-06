# coding=utf-8
from pandas import DataFrame
import pandas as pd
import requests
from pyquery import PyQuery as pq


def get_all():
    r_list = []
    for page in range(1, 145):
        url = 'http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/' + str(page) + '/ajax/1/'
        html = requests.get(url).text
        p = pq(html).find('table.m-table>tbody>tr')
        for d in p:
            code = pq(d).find('td').eq(1).text()
            name= pq(d).find('td').eq(2).text()
            price = pq(d).find('td').eq(3).text()
            change = pq(d).find('td').eq(4).text()
            speed = pq(d).find('td').eq(6).text()
            change_shou = pq(d).find('td').eq(7).text()
            dict = {'code': code, 'change':change,'price': price, 'speed': speed,'change_shou':change_shou}
            r_list.append(dict)
    df=pd.DataFrame(r_list)
    return df


if __name__ == '__main__':
    list = get_all()
    print(list)
