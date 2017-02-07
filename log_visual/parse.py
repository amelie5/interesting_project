# coding=utf-8
f = open('www_access_20140823.log')
res = {}
for l in f:
    arr = l.split(' ')
    # 获取ip url 和status
    ip = arr[0]
    url = arr[6]
    status = arr[8]
    # ip url 和status当key，每次统计+1
    res[(ip,url,status)] = res.get((ip,url,status),0)+1
# 生成一个临时的list
res_list = [(k[0],k[1],k[2],v) for k,v in res.items()]
# 按照统计数量排序，打印前10
for k in sorted(res_list,key=lambda x:x[3],reverse=True)[:10]:
    print (k)