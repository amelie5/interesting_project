select date,zhang_num,zhang_feng_num ,z_daban,open_num,open_feng_num,o_daban from
(select date,count(1)as zhang_num,sum(case when change_0>9.9 then 1 else 0 end) as zhang_feng_num,sum(case when change_0>9.9 then 1 else 0 end)/count(1) as z_daban from zhang_stop
where date>='2017-06-08' group by date)t1
left join
(select timeToOpen,count(1)as open_num,sum(case when f_0>9.9 then 1 else 0 end) as open_feng_num,sum(case when f_0>9.9 then 1 else 0 end)/count(1) as o_daban from new_stock_open
where timeToOpen>='2017-06-08' and timeToOpen!='3020-01-01'group by timeToOpen)t2
on t1.date=t2.timeToOpen