# coding=utf-8
import pandas as pd
import requests
from pyquery import PyQuery as pq
import re
import json


def get_holder(code):
    df = pd.DataFrame()
    url = 'http://stock.finance.qq.com/corp1/stk_holder_count.php?zqdm=' + code
    html = requests.get(url).text
    p = pq(html).find('table.list>tr')
    cnt = 0
    for d in p:
        cnt += 1
        if cnt == 1:
            continue
        else:
            date = pq(d).find('td').eq(0).text()
            if date == '2013-12-31':
                break
            else:
                holders = pq(d).find('td').eq(1).text()
                holders = float(holders.replace(",", ''))
                df = df.append({'code': code, 'holders': holders, 'date': date}, ignore_index=True)
    return df

def get_holder_dongfang():
    df = pd.DataFrame()
    for page in range(1,16):
        print('page: {}'.format(page))
        url = 'http://data.eastmoney.com/DataCenter_V3/gdhs/GetList.ashx?pagesize=200&page='+str(page)
        html = requests.get(url).text
        json_list = json.loads(html)
        data = json_list['data']
        for one in data:
            code=one['SecurityCode']
            date=one['EndDate']
            date = re.findall(r'(.*)T', date)[0]
            holders=one['HolderNum']
            df = df.append({'code': code, 'holders': holders, 'date': date}, ignore_index=True)
    return df


def get_top10_2017(code):
    df = pd.DataFrame()
    url = 'http://stock.finance.qq.com/corp1/stk_ciholder.php?zqdm=' + code + '&type=2017'
    html = requests.get(url).text
    p = pq(html).find('table.list>tr')
    cnt = 0
    for d in p:
        if cnt % 13 == 0:
            date = pq(d).find('th').text()
            if date == "流通股东名单":
                break
            #date = re.compile(r'报告期： (.*) 公告日期').findall(date)[0]
            date='2017-03-31'
        if (cnt % 13 == 0) | ((cnt - 1) % 13 == 0) | ((cnt - 12) % 13 == 0):
            cnt = cnt + 1
            continue
        else:
            name = pq(d).find('td').eq(1).text()
            if name == '':
                break
            else:
                amount = pq(d).find('td').eq(2).text()
                amount = amount.replace(",", '')
                amount = float(amount)
                type = pq(d).find('td').eq(3).text()
                percent = pq(d).find('td').eq(4).text()
                percent = float(percent.replace("%", ''))
                change = pq(d).find('td').eq(5).text()
                df = df.append({'code': code, 'amount': amount, 'company': name, 'type': type, 'percent': percent,
                                'change': change, 'date': date}, ignore_index=True)
                cnt += 1
    return df


def get_top10(code):
    df = pd.DataFrame()
    url = 'http://stock.finance.qq.com/corp1/stk_ciholder.php?zqdm=' + code + '&type=2015'
    html = requests.get(url).text
    p = pq(html).find('table.list')
    cnt = 0
    for d in p:
        date = pq(d).find('th').text()
        if date == "流通股东名单":
            break
        date = re.compile(r'报告期： (.*) 公告日期').findall(date)[0]
        p_p = pq(d).find('tr')
        cnt = 0
        for d_d in p_p:
            if cnt <2:
                cnt = cnt + 1
                continue
            else:
                name = pq(d_d).find('td').eq(1).text()
                if name == '':
                    break
                else:
                    amount = pq(d_d).find('td').eq(2).text()
                    amount = amount.replace(",", '')
                    amount = float(amount)
                    type = pq(d_d).find('td').eq(3).text()
                    percent = pq(d_d).find('td').eq(4).text()
                    percent = float(percent.replace("%", ''))
                    change = pq(d_d).find('td').eq(5).text()
                    df = df.append({'code': code, 'amount': amount, 'company': name, 'type': type, 'percent': percent,
                                    'change': change, 'date': date}, ignore_index=True)
                    cnt += 1
    return df


if __name__ == '__main__':
    get_holder_dongfang()
