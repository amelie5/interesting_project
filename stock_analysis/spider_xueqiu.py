# coding=utf-8

import requests
import json
import pandas as pd
from pyquery import PyQuery as pq
import re
import time


def get_list():
    df = pd.DataFrame()
    for page in range(1, 2):
        print('page: ', page)
        url = 'https://xueqiu.com/cubes/discover/rank/cube/list.json?market=cn&sale_flag=1&stock_positions=0&sort=best_benefit&category=14&profit=monthly_gain&page=' + str(
            page) + '&count=100'
        headers = {'X-Requested-With': 'XMLHttpRequest',
                   'Referer': 'https://xueqiu.com/p/discover?action=money&market=cn&profit=monthly_gain',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                   'Host': 'xueqiu.com',
                   'Connection': 'keep-alive',
                   'Accept': '*/*',
                   'X-Requested-With': 'XMLHttpRequest',
                   'cookie': 'webp=0; s=1hoq18bsqj; u=141501557014457; device_id=7ab995c0921f21f14bcb0966aa222cd3; __utma=1.1274904483.1490686013.1501559133.1501656202.10; __utmz=1.1496979589.7.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; aliyungf_tc=AQAAACoToG0M2AoA0nkmag+RRR7YWeQf; xq_a_token=82d9cefaa0793743cb186e53294ec0e61ac2abec; xq_r_token=11b86433a20d1d1eef63ecc12252297196a20e10; Hm_lvt_1db88642e346389874251b5a1eded6e3=1501571669,1501656182,1502164869,1502164913; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1502165458'}
        html = requests.get(url, headers=headers).text
        data = json.loads(html)
        list = data['list']
        for d in list:
            owner = d['owner']['screen_name']
            symbol = d['symbol']
            name = d['name']
            daily_gain = d['daily_gain']
            monthly_gain = d['monthly_gain']
            total_gain = d['total_gain']
            net_value = d['net_value']
            follower_count = d['follower_count']
            last_rb_id=d['last_rb_id']
            created_at=d['created_at']
            x = time.localtime(created_at/1000)
            create = time.strftime('%Y-%m-%d', x)
            df = df.append(
                {"id": symbol, "name": name, "daily_gain": daily_gain, "monthly_gain": monthly_gain,
                 "total_gain": total_gain, "last_rb_id":last_rb_id,"net_value": net_value, "follower_count": follower_count, "owner": owner,"create":create},
                ignore_index=True)

    return df


def get_detail(id,rb_id):
    df = pd.DataFrame()
    url = 'https://xueqiu.com/cubes/rebalancing/show_origin.json?rb_id='+str(rb_id)+'&cube_symbol='+str(id)
    headers = {'X-Requested-With': 'XMLHttpRequest',
               'Referer': 'https://xueqiu.com/p/discover?action=money&market=cn&profit=monthly_gain',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
               'Host': 'xueqiu.com',
               'Connection': 'keep-alive',
               'Accept': '*/*',
               'X-Requested-With': 'XMLHttpRequest',
               'cookie': 'webp=0; s=1hoq18bsqj; u=141501557014457; device_id=7ab995c0921f21f14bcb0966aa222cd3; __utma=1.1274904483.1490686013.1501559133.1501656202.10; __utmz=1.1496979589.7.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; aliyungf_tc=AQAAACoToG0M2AoA0nkmag+RRR7YWeQf; xq_a_token=82d9cefaa0793743cb186e53294ec0e61ac2abec; xq_r_token=11b86433a20d1d1eef63ecc12252297196a20e10; Hm_lvt_1db88642e346389874251b5a1eded6e3=1501571669,1501656182,1502164869,1502164913; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1502165458'}
    html = requests.get(url, headers=headers).text
    data = json.loads(html)
    list = data['rebalancing']['rebalancing_histories']
    created_at = data['rebalancing']['updated_at']
    x = time.localtime(created_at / 1000)
    date = time.strftime('%Y-%m-%d %H:%m:%S', x)
    for d in list:
        stock_name=d['stock_name']
        price=d['price']
        prev_weight=d['prev_weight']
        target_weight=d['target_weight']

        df = df.append(
            {"zuhe_id": id, "rb_id": rb_id, "stock_name": stock_name, "price": price,
             "prev_weight": prev_weight, "target_weight": target_weight,"date":date},
            ignore_index=True)

    return df


if __name__ == '__main__':
    get_detail('ZH749518')
