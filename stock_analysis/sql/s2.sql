#统计股东人数
select * from
(select t2.*,t1.holders-t2.holders cha from
(select * from holder where date='2017-03-31')t1
inner join
(select * from holder_new where date>'2017-03-31')t2
on t1.code=t2.code
)t
INNER JOIN
stock_basics b
on t.code=b.code
LEFT JOIN
(select code,group_concat(concept order by concept separator ",") as concept
 from concept
group by code) c
on t.code=c.code
order by cha desc