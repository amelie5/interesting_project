@echo off  
D:  
cd D:\project\PycharmProjects\interesting_project\stock_analysis
start /wait db_basics.py
start /wait db_new_open.py
start /wait db_pchange.py
start /wait db_price.py
start /wait db_ma_price.py
start /wait db_fengkou.py
start /wait db_longhu.py
start /wait db_zhang_stop.py
start /wait db_market.py
start /wait db_open_ban.py
start /wait db_zhang_ban.py

rem 使用ping命令暂停3s，这样可以看到调用python后的结果
ping -n 3 127.0.0.1 > nul 