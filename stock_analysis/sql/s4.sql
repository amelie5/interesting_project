select t2.date,cnt,zhangting_sum,dieting_sum,zhang_sum,die_sum,volume,p_change,price from
(select '2017-05-22' as date,count(1)as cnt from stock_basics where timeToMarket!='0000-00-00' and code not in
(select code from new_stock_open where timeToOpen>'2017-05-22')
group by 1 )t2
LEFT JOIN
(select date,
count(case when ntype='涨停' then 1 else null end) as 'zhangting_sum',
count(case when ntype='跌停' then 1 else null end) as 'dieting_sum',
count(case when ntype='涨' then 1 else null end) as 'zhang_sum',
count(case when ntype='跌' then 1 else null end) as 'die_sum'
from
(SELECT date,
case
when p_change>=9.90 then '涨停'
when p_change<=-9.90 then '跌停'
when p_change>0 then '涨'
when p_change<0 then '跌'
else '0'
end as ntype
from p_change where date='2017-05-22' and code!='sh' )t
group by 1)t1
on t1.date=t2.date
LEFT JOIN
(select date,ROUND(avg(p_change),2) as p_change from p_change where date='2017-05-22' and code!='sh')t3
on t3.date=t2.date
LEFT JOIN
(select date,sum(ROUND(volume,0))as volume from p_change where date='2017-05-22' and code!='sh')t4
on t4.date=t2.date
LEFT JOIN
(select date,ROUND(avg(close),2) as price from price_amount where date='2017-05-22' and code!='sh')t5
on t5.date=t2.date