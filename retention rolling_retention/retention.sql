with retention as (
	select 
		u.user_id, 		
		extract(days from u.entry_at - u2.date_joined) as diff,
		to_char(u2.date_joined, 'YYYY-MM') as cohort
	from userentry u 
	join users u2 
	on u2.id = u.user_id 
	where to_char(u2.date_joined, 'YYYY') = '2022'
)
select 
	cohort,
	round(count(distinct case when diff = 0 then user_id end) * 100.0 / count(distinct case when diff = 0 then user_id end)) as "0 %",
	round(count(distinct case when diff = 3 then user_id end) * 100.0 / count(distinct case when diff = 0 then user_id end), 2) as "3 (%)",
	round(count(distinct case when diff = 5 then user_id end) * 100.0 / count(distinct case when diff = 0 then user_id end), 2) as "5 (%)",
	round(count(distinct case when diff = 7 then user_id end) * 100.0 / count(distinct case when diff = 0 then user_id end), 2) as "7 (%)",
	round(count(distinct case when diff = 14 then user_id end) * 100.0 / count(distinct case when diff = 0 then user_id end), 2) as "14 (%)",
	round(count(distinct case when diff = 21 then user_id end) * 100.0 / count(distinct case when diff = 0 then user_id end), 2) as "21 (%)",
	round(count(distinct case when diff = 30 then user_id end) * 100.0 / count(distinct case when diff = 0 then user_id end), 2) as "30 (%)",
	round(count(distinct case when diff = 60 then user_id end) * 100.0 / count(distinct case when diff = 0 then user_id end), 2) as "60 (%)",
	round(count(distinct case when diff = 90 then user_id end) * 100.0 / count(distinct case when diff = 0 then user_id end), 2) as "90 (%)",
	max('retention') as "cohort_analys"
from retention
group by cohort
union all
select 
	cohort,
	round(count(distinct case when diff >= 0 then user_id end) * 100.0 / count(distinct case when diff >= 0 then user_id end)) as "0 %",
	round(count(distinct case when diff >= 3 then user_id end) * 100.0 / count(distinct case when diff >= 0 then user_id end), 2) as "3 (%)",
	round(count(distinct case when diff >= 5 then user_id end) * 100.0 / count(distinct case when diff >= 0 then user_id end), 2) as "5 (%)",
	round(count(distinct case when diff >= 7 then user_id end) * 100.0 / count(distinct case when diff >= 0 then user_id end), 2) as "7 (%)",
	round(count(distinct case when diff >= 14 then user_id end) * 100.0 / count(distinct case when diff >= 0 then user_id end), 2) as "14 (%)",
	round(count(distinct case when diff >= 21 then user_id end) * 100.0 / count(distinct case when diff >= 0 then user_id end), 2) as "21 (%)",
	round(count(distinct case when diff >= 30 then user_id end) * 100.0 / count(distinct case when diff >= 0 then user_id end), 2) as "30 (%)",
	round(count(distinct case when diff >= 60 then user_id end) * 100.0 / count(distinct case when diff >= 0 then user_id end), 2) as "60 (%)",
	round(count(distinct case when diff >= 90 then user_id end) * 100.0 / count(distinct case when diff >= 0 then user_id end), 2) as "90 (%)",
	max('rolling_retention')
from retention
group by cohort