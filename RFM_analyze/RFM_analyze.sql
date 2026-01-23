with abc_sales as (
    select
    b.card client,
    sum(b.summ) as monetary,
    count(*) as frequency
    from bonuscheques b
    group by b.card
),
monetary_frequency as (
    select
    client, monetary,
    case
        when sum(monetary) over(order by monetary desc) / sum(monetary) over() <= 0.8 then '3'
        when sum(monetary) over(order by monetary desc) / sum(monetary) over() <= 0.95 then '2'
        else '1'
    end monetary_abc,
    frequency,
    case
        when sum(frequency) over(order by frequency desc) / sum(frequency) over() <= 0.8 then '3'
        when sum(frequency) over(order by frequency desc) / sum(frequency) over() <= 0.95 then '2'
        else '1'
    end frequency_abc
    from abc_sales
    where length(client) = 13
),
recancy1 as (
    select b.card, max(b.datetime)::date as max_date, min(b.datetime)::date as min_date
    from bonuscheques b
    where length(b.card) = 13
    group by 1
),
recancy2 as (
s   elect *, max_date - min_date as with_us, max(max_date) over() as total_max_date
    from recancy1
),
recancy3 as (
    select card, max_date, total_max_date, total_max_date - max_date as diff
    rom recancy2
),
recancy as (
    select card, diff,
    case
        when diff <= 48 then '3'
        when diff <= 147 then '2'
    else '1'
    end recancy_abc
    from recancy3
),
agg_rfm as (
    select m_f.client as client, r.recancy_abc as r, m_f.frequency_abc as f, m_f.monetary_abc as m
    from monetary_frequency m_f
    join recancy r
    on m_f.client = r.card
)
select client, r || f || m as rfm
from agg_rfm