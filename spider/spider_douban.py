# coding=utf-8
import re
import requests
from pyquery import PyQuery as pq
import pandas as pd


def get_book_tag():
    df = pd.DataFrame()
    url = 'https://book.douban.com/tag/'
    html = requests.get(url).text
    p = pq(html).find('div.grid-16-8>div.article>div>div')
    for d in p:
        tag = pq(d).find('a').attr('name')
        p_s = pq(d).find('table.tagCol>tbody>tr>td')
        for d_s in p_s:
            tag_sub = pq(d_s).find('a').text()
            print(tag_sub)
            num_str = pq(d_s).find('b').text()
            num = int(re.findall(r'\((.*)\)', num_str)[0])
            df = df.append({"tag": tag, "sub_tag": tag_sub, "num": num}, ignore_index=True)

    return df


def get_book(tag,id):
    df = pd.DataFrame()
    for page in range(0,10000000):
        url = 'https://book.douban.com/tag/' + tag + '?start=' + str(page*20) + '&type=T'
        html = requests.get(url,proxies={'http': '210.22.159.83:8080'}).text
        p = pq(html).find('div.info')
        for d in p:
            name = pq(d).find('h2>a').attr('title')
            print(name)
            score = pq(d).find('div.star>span.rating_nums').text()
            user_str = pq(d).find('div.star>span.pl').text()
            if user_str=='(少于10人评价)':
                user=10
            else:
                user = int(re.findall(r'\((.*)人', user_str)[0])
            df = df.append({"name": name, "score": score, "user": user,"tag_id":id}, ignore_index=True)
    return df


if __name__ == '__main__':
    list = get_book("艺术",1)

