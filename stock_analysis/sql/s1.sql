select t.*,b.name,c.concept,b.timeToMarket from
(select code,sum(p_change)s from p_change where date>='2017-04-06' and date<='2017-04-10'
group by code)t
left JOIN
stock_basics b
on t.code=b.code
LEFT JOIN
(select code,group_concat(concept order by concept separator ",") as concept
 from concept
group by code) c
on t.code=c.code
order by t.s desc
