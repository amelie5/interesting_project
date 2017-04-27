from aiohttp import ClientSession
url = 'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq2017&param=sh600004,day,2017-01-01,2018-12-31,640,qfq'
count = 0
async def hello_aio():
    async with ClientSession() as session:
        async with session.get(url)as response:
            response = await response.text()#read()


task_list = []
for i in range(1000):
    task_list.append(hello_aio())
import time

start = time.clock()

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(task_list))

end = time.clock()
print(end - start)
print('count:{}'.format(count))