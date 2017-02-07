# coding=utf-8

import requests
from pyquery import PyQuery as pq

url = 'http://zhixing.bjtu.edu.cn/portal.php'
r = requests.get(url)
print (r.text)
p = pq(r.text).find('#portal_block_617 li>a')
for d in p:
	print (pq(d).text())
	print ('http://zhixing.bjtu.edu.cn/'+pq(d).attr('href'))