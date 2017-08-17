# coding=utf-8
import re
from datetime import datetime

import pandas as pd
import requests
from pyquery import PyQuery as pq
import tushare as ts
import time


def get_tx_minite():
    url = 'http://push2.gtimg.cn/q=sh603003'
    str = requests.get(url).text
    import re
    str = re.findall(r'(\d\d:\d\d:\d\d/.*)~2017', str)[0]
    str_arr = str.split('|')

    for str in str_arr[::-1]:
        print(str)


def get_zs_tonghuashun():
    r_list = []
    cnt = 0
    url = 'http://q.10jqka.com.cn/index/index/board/all/field/zs/order/desc/page/1/ajax/1/'
    html = requests.get(url).text
    p = pq(html).find('table.m-table>tbody>tr')
    for d in p:
        if cnt > 4:
            break;
        cnt = cnt + 1
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
        for i in range(1, 100):
            url = 'http://q.10jqka.com.cn/gn/detail/order/desc/page/{}/ajax/1/code/{}'.format(str(i), tup[1])
            html = requests.get(url).text
            p = pq(html).find('table.m-table>tbody>tr')
            if "暂无成份股数据" in p.html():
                break
            else:
                for d in p:
                    code = pq(d).find('td').eq(1).text()
                    concept = tup[0]
                    print(concept)
                    df = df.append({"code": code, "concept": concept}, ignore_index=True)

    return df


def get_industry(list):
    df = pd.DataFrame()
    for tup in list:
        for i in range(1, 100):
            url = 'http://q.10jqka.com.cn/thshy/detail/field/199112/order/desc/page/{}/ajax/1/code/{}'.format(str(i),
                                                                                                              tup[1])
            html = requests.get(url).text
            p = pq(html).find('table.m-table>tbody>tr')
            if "暂无成份股数据" in p.html():
                break
            else:
                for d in p:
                    code = pq(d).find('td').eq(1).text()
                    industry = tup[0]
                    print(industry)
                    df = df.append({"code": code, "industry": industry}, ignore_index=True)

    return df


def get_concept_name():
    list = []
    url = 'http://q.10jqka.com.cn/gn/detail/code/300061/'
    html = requests.get(url).text
    p = pq(html).find('div.cate_items>a')
    for d in p:
        concept = pq(d).text()
        url = pq(d).attr('href')
        code = re.compile(r'code\/(.*)\/').findall(url)[0]
        tup = (concept, code)
        list.append(tup)
    return list


def get_industry_name():
    list = []
    url = 'http://q.10jqka.com.cn/thshy/'
    html = requests.get(url).text
    p = pq(html).find('div.cate_items>a')
    for d in p:
        industry = pq(d).text()
        url = pq(d).attr('href')
        code = re.compile(r'code\/(.*)\/').findall(url)[0]
        tup = (industry, code)
        list.append(tup)
    return list


def get_spec_today():
    df = ts.get_today_all()
    df = df[['code', 'name', 'changepercent', 'amount', 'turnoverratio']]
    # 保留跌幅在7以上，但是成交量只有几千万
    df = df[df['changepercent'] <= -7]
    df = df[df['amount'] <= 100000000]
    df.sort_values(by='amount', inplace=True)
    print(df)
    df.to_excel('d:/data/stock/2017-04-17.xlsx')


def get_comment_1():
    code = '601003'
    cnt = 0
    for page in range(1, 10):
        url = 'http://guba.eastmoney.com/list,{},f_{}.html'.format(code, page)
        html = requests.get(url).text
        p = pq(html).find('div.articleh')
        for d in p:
            date = '2017-{}'.format(pq(d).find('span.l6').text())
            date = datetime.strptime(date, "%Y-%m-%d")
            if date >= datetime.strptime('2017-05-14', "%Y-%m-%d"):
                continue
            if date < datetime.strptime('2017-05-13', "%Y-%m-%d"):
                break
            content = pq(d).find('span.l3>a').text()
            print(content, date)
            cnt = cnt + 1
    print(code, cnt)


def get_comment(code):
    df = pd.DataFrame()

    flag = True
    for page in range(1, 10000000000):
        if (flag):
            url = 'http://guba.eastmoney.com/list,{},f_{}.html'.format(code, page)

            html = requests.get(url).text
            p = pq(html).find('div.articleh')
            for d in p:
                date = '2017-{}'.format(pq(d).find('span.l6').text())
                month = re.findall(r'2017-(.*)-', date)[0]
                if month == '12':
                    flag = False
                    break
                else:
                    df = df.append({'date': date}, ignore_index=True)
        else:
            break
    grouped = df.groupby(df['date']).size()
    df = pd.DataFrame(grouped.values, index=grouped.index, columns=['cnt'])
    df.reset_index(level=0, inplace=True)
    df['code'] = code
    return df


def get_market(date):
    import json
    import datetime
    url = 'http://phbapi.yidiancangwei.com/w1/api/index.php'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Content-Lengthv": "66",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "phbapi.yidiancangwei.com",
        "Origin": "http://phb.yidiancangwei.com",
        "Referer": "http://phb.yidiancangwei.com/scfk.html"
    }
    data = {
        "c": 'StockFengKData',
        "a": 'GetFengKList',
        "Order": "11",
        "Index": "0",
        "st": "500",
        "Time": '',
        "Day": date
    }

    html = requests.post(url, data=data, headers=headers).text
    data = json.loads(html)
    list = data['List']
    df = pd.DataFrame()
    # 调用事件模块

    if date == '':
        today = datetime.date.today()  # 获取今天日期
        date = today.strftime('%Y-%m-%d')

    for tuple in list:
        code = tuple[0]
        name = tuple[1]
        price = tuple[2]
        price_first = tuple[3]
        market = tuple[4]
        buy = tuple[5]
        sell = tuple[6]
        d = tuple[7]
        concept = tuple[8]
        trader = tuple[10]
        df = df.append(
            {"code": code, "name": name, "price": price, "price_first": price_first, "market": market, "buy": buy,
             "sell": sell, "d": d, "concept": concept, "trader": trader, "date": date}, ignore_index=True)
    return df


def get_longhu(date):
    import json
    import datetime
    url = 'http://phbapi.yidiancangwei.com/w1/api/index.php'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Content-Lengthv": "103",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "phbapi.yidiancangwei.com",
        "Origin": "http://phb.yidiancangwei.com",
        "Referer": "http://phb.yidiancangwei.com/scfk.html"
    }
    data = {
        "c": 'StockRanking',
        "a": 'RealRankingInfo',
        "Date": date,
        "RStart": '',
        "REnd": '',
        "Ratio": 1000,
        "Tpye": 1,
        "Order": "1",
        "Index": "1",
        "st": "4000"
    }

    html = requests.post(url, data=data, headers=headers).text
    data = json.loads(html)
    list = data['list']
    df = pd.DataFrame()
    # 调用事件模块

    if date == '':
        today = datetime.date.today()  # 获取今天日期
        date = today.strftime('%Y-%m-%d')

    for tuple in list:
        code = tuple[0]
        name = tuple[1]
        p_change = tuple[2]
        market = tuple[3]
        concept = tuple[4]
        buy = tuple[5]
        sell = tuple[6]
        d = tuple[7]
        trader = tuple[9]
        df = df.append(
            {"code": code, "name": name, "p_change":p_change,"market": market, "buy": buy,
             "sell": sell, "d": d, "concept": concept, "trader": trader, "date": date}, ignore_index=True)
    return df


if __name__ == '__main__':
    import time

    a = "2017-08-02 09:31"
    t = int(time.mktime(time.strptime(a, '%Y-%m-%d %H:%M')))

    df = get_longhu('2017-08-09')
    print(df)
