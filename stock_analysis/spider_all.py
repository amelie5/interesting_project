# coding=utf-8
import re
import pandas as pd
import requests
from pyquery import PyQuery as pq


def get_zs_tonghuashun():
    r_list = []
    cnt=0
    url = 'http://q.10jqka.com.cn/index/index/board/all/field/zs/order/desc/page/1/ajax/1/'
    html = requests.get(url).text
    p = pq(html).find('table.m-table>tbody>tr')
    for d in p:
        if cnt>4 :
            break;
        cnt=cnt+1
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

def get_concept(list):
    df = pd.DataFrame()
    for tup in list:
        for i in range(1,100):
            url = 'http://q.10jqka.com.cn/gn/detail/order/desc/page/{}/ajax/1/code/{}'.format(str(i),tup[1])
            html = requests.get(url).text
            p = pq(html).find('table.m-table>tbody>tr')
            if "暂无成份股数据" in p.html():
                break
            else:
                for d in p:
                    code = pq(d).find('td').eq(1).text()
                    df = df.append({"code": code, "concept": tup[0] },ignore_index=True)

    return df

def get_concept_name():
    list=[]
    url = 'http://q.10jqka.com.cn/gn/detail/code/300061/'
    html = requests.get(url).text
    p = pq(html).find('div.cate_items>a')
    for d in p:
        concept = pq(d).text()
        url=pq(d).attr('href')
        code = re.compile(r'code\/(.*)\/').findall(url)[0]
        tup=(concept,code)
        list.append(tup)
    return list


if __name__ == '__main__':
    df = get_zs_tonghuashun()
    print(df)

