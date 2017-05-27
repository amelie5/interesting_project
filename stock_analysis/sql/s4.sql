

select date,ntype,count(1) from
(SELECT date,
case 
when p_change>=9.90 then '涨停'
when p_change<=-9.90 then '跌停'
when p_change>0 then '涨' 
when p_change<0 then '跌' 
else '0'
end as ntype
from p_change where date='2017-05-22' and code!='sh' 
)t
group by 1,2


select avg(p_change) from p_change where date='2017-05-22' and code!='sh'


select sum(ROUND(volume,0)) from p_change where date='2017-05-22' and code!='sh'

select avg(ROUND(close,2)) from price_amount where date='2017-05-22' and code!='sh'




