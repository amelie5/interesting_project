#删除新股数据
delete from new_stock_open where code in(select code from stock_basics where timeToMarket>=(select timeToMarket from
(select * from new_stock_open)t
INNER JOIN
stock_basics b
on t.code=b.code where f_2='-999'
order by timeToMarket limit 1))

#