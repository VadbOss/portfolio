with abc_sales as (
		select 	
			dr_ndrugs as product,
	        coalesce(sum(dr_kol), 0) as amount,
	        coalesce(sum(dr_kol*(dr_croz - dr_czak) - dr_sdisc), 0) as profit,
	        coalesce(sum(dr_kol*dr_croz - dr_sdisc), 0) as revenue
		from sales s
		group by s.dr_ndrugs
),
xyz_sales as (
		select
			dr_ndrugs as product,
			to_char(dr_dat, 'YYYY-WW') as yw,
			sum(dr_kol) as sales
		from sales s 
		group by 1, 2
),
xyz_analys as (
		select
			product,
			case 
				when stddev(sales) / avg(sales) > 0.25 then 'Z'
				when stddev(sales) / avg(sales) > 0.1 then 'Y'
				else 'X'
			end xyz_sales
		from xyz_sales
		group by 1
		having count(distinct yw) >= 4
)
select 
	s.product,
	case 
		when sum(amount) over(order by amount desc) / sum(amount) over() <= 0.8 then 'A'
		when sum(amount) over(order by amount desc) / sum(amount) over() <= 0.95 then 'B'
		else 'C'
	end amount_abc,
	case 
		when sum(profit) over(order by profit desc) / sum(profit) over() <= 0.8 then 'A'
		when sum(profit) over(order by profit desc) / sum(profit) over() <= 0.95 then 'B'
		else 'C'
	end profit_abc,
	case 
		when sum(revenue) over(order by revenue desc) / sum(revenue) over() <= 0.8 then 'A'
		when sum(revenue) over(order by revenue desc) / sum(revenue) over() <= 0.95 then 'B'
		else 'C'
	end revenue_abc,
	xyz.xyz_sales
from abc_sales s
left join xyz_analys xyz
on s.product = xyz.product
order by 1