--Платежная активность
--Есть витрина платежей, мне нужно определить нет ли пользователей с цепочкой платежей, нарушающих условия ПС.
--Условие: Сумма успешных платежей пользователя за 24 часа (можно поменять в зависимости от необходимости) не должна превышать некую сумму (20_000_000 рублей)
WITH 
24 AS hours,  
toUInt64(20_000_000) AS treshhold,
prepare AS (
	SELECT 
		account_id,  
		amount,
		operation_datetime - INTERVAL hours HOUR AS interval_start,
		operation_datetime AS interval_end,
		sum(amount) OVER (
			PARTITION BY account_id 
			ORDER BY operation_datetime 
			RANGE BETWEEN hours*60*60 PRECEDING AND CURRENT ROW
		) AS interval_amount,
		count(operation_id) OVER (
			PARTITION BY account_id 
			ORDER BY operation_datetime 
			RANGE BETWEEN hours*60*60 PRECEDING AND CURRENT ROW
		) AS interval_count
	FROM sandbox.payment 
	WHERE  
		status = 'completed'
)
SELECT   
	*,
	hours AS hours_in_interval 
FROM   
	prepare            
WHERE   
	interval_amount >= treshhold
;
