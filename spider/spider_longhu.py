# coding=utf-8
import datetime
import requests
from pyquery import PyQuery as pq


def get_list(date):
    url_list = []
    url = 'http://data.10jqka.com.cn/market/longhu/date/' + date + '/'
    html = requests.get(url).text
    p = pq(html).find('div#lhdata>table.m_table>tbody>tr')
    for d in p:
        trader = pq(d).find('td').eq(1)
        url_list.append(pq(trader).find('a').text())

    return list(set(url_list))


def get_teding_date(code):
    date_list=[]
    url = 'http://data.10jqka.com.cn/market/lhbcjmx/code/' + code + '/#refCountId=data_55a3b816_507'
    html = requests.get(url).text
    p = pq(html).find('select>option')
    for d in p:
        date = pq(pq(d)).text()
        date_list.append(date)
    return date_list


# def get_one_data(code, ctime):
#     r_list = []
#     ntype = 'b'
#     trader = ''
#     cnt = 0
#     url = 'http://data.10jqka.com.cn/ifmarket/getnewlh/code/' + code + '/date/' + ctime + '/'
#     html = requests.get(url).text
#     p = pq(html).find('tr')
#     for d in p:
#         html_trader = pq(pq(d).find('td').eq(1)).find('a').text()
#         if (html_trader == ''):
#             cnt = cnt + 1
#         else:
#             if (trader == ''):
#                 trader = html_trader
#             else:
#                 trader = '%s%s%s' % (trader, ';', html_trader)
#         if (cnt == 3):
#             dict = {'code': code, 'ntype': ntype, 'traders': trader, 'ctime': ctime}
#             r_list.append(dict)
#             ntype = 's'
#             trader = ''
#             cnt = cnt + 1
#
#     dict = {'code': code, 'ntype': ntype, 'traders': trader, 'ctime': ctime}
#     r_list.append(dict)


def get_one_data(code, ctime):
    r_list = []
    ntype = 'b'
    trader = ''
    cnt = 0
    url = 'http://data.10jqka.com.cn/ifmarket/getnewlh/code/' + code + '/date/' + ctime + '/'
    html = requests.get(url).text
    p = pq(html).find('tr')
    for d in p:
        trader = pq(pq(d).find('td').eq(1)).find('a').text()
        if (trader == ''):
            cnt = cnt + 1
        else:
            if cnt<3:
                fund=pq(pq(d).find('td').eq(2)).text()
            else:
                fund=pq(pq(d).find('td').eq(4)).text()
            dict = {'code': code, 'ntype': ntype, 'trader': trader, 'ctime': ctime,'fund':fund}
            r_list.append(dict)
        if (cnt == 3):
            ntype = 's'
            trader = ''
            cnt = cnt + 1
    return r_list


def get_date():
    date_list = list()
    begin = datetime.date(2017, 2, 10)
    end = datetime.date(2017, 2, 10)
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        print(str(day))
        date_list.append(str(day))
    return date_list


def func():
    date_list = get_date()
    for date in date_list:
        code_list = get_list(date)
        for code in code_list:
            get_one_data(code, date)


def func_one(code):
    data_list=[]
    date_list = get_teding_date(code)
    for date in date_list:
        list=get_one_data(code, date)
        data_list.extend(list)
    return data_list


if __name__ == '__main__':
    list=get_one_data('300099', '2017-02-17')
    print(list)