-- Создаем таблицу user_sessions 
CREATE TABLE user_sessions ( 
    session_id SERIAL PRIMARY KEY, -- Уникальный ID сеанса 
    user_id INT NOT NULL,          -- Уникальный ID пользователя 
    session_date DATE NOT NULL,    -- Дата сеанса 
    revenue DECIMAL(10, 2) DEFAULT 0.00 -- Доход, полученный в этом сеансе (например, покупка) 
); 
 -- Создаем таблицу marketing_campaigns 
CREATE TABLE marketing_campaigns ( 
    campaign_id SERIAL PRIMARY KEY, 
    campaign_name VARCHAR(255) NOT NULL, 
    campaign_date DATE NOT NULL 
); 

DO $$ 
DECLARE 
    v_user_id INT; 
    v_session_date DATE; 
    v_revenue DECIMAL(10, 2); 
    v_num_users INT := 100; -- Количество пользователей 
    v_start_date DATE := CURRENT_DATE - INTERVAL '90 days'; 
    v_end_date DATE := CURRENT_DATE; 
BEGIN 
    FOR v_user_id IN 1..v_num_users LOOP 
        -- Генерируем случайное количество сеансов для пользователя (от 1 до 15) 
        FOR i IN 1..(1 + (RANDOM() * 14)::INT) LOOP 
            -- Выбираем случайную дату сеанса между датами начала и окончания 
            v_session_date := v_start_date + (RANDOM() * (v_end_date - v_start_date))::INT * INTERVAL '1 
day'; 
 
            -- С вероятностью 30% генерируем доход, иначе 0 
            IF RANDOM() > 0.7 THEN 
                v_revenue := ROUND((RANDOM() * 100 + 10)::NUMERIC, 2); 
            ELSE 
                v_revenue := 0.00; 
            END IF; 
 
            INSERT INTO user_sessions (user_id, session_date, revenue) 
            VALUES (v_user_id, v_session_date, v_revenue); 
        END LOOP; 
    END LOOP; 
END $$; 
 -- Удаляем дубликаты сеансов для одного пользователя в один день (если таковые возникли) 
-- Это может произойти, если случайные даты совпали 
DELETE FROM user_sessions 
WHERE session_id NOT IN ( 
SELECT MIN(session_id) 
FROM user_sessions 
GROUP BY user_id, session_date 
);

-- Вставляем дату маркетинговой кампании (например, одна кампания) 
INSERT INTO marketing_campaigns (campaign_name, campaign_date) 
VALUES ('Summer Sale 2024', CURRENT_DATE - INTERVAL '30 days'); -- Кампания 30 дней назад 

-- Проверяем данные 
SELECT * FROM user_sessions ORDER BY user_id, session_date LIMIT 20;

SELECT * FROM marketing_campaigns;


/*Цель: Сегментировать пользователей по неделе первого сеанса и проанализировать удержание.
Определить пользователей, ушедших (churned), если они не были активны 21 день подряд.*/

-- Шаг 1: Найдем дату первого сеанса для каждого пользователя
WITH first_session AS (
 SELECT
 user_id,
 MIN(session_date) AS first_session_date
 FROM user_sessions
 GROUP BY user_id
),
-- Шаг 2: Присоединим дату первого сеанса к основной таблице
user_sessions_with_cohort AS (
 SELECT
 us.*,
 fs.first_session_date,
 -- Определяем когорту как неделю первой активности
 DATE_TRUNC('week', fs.first_session_date)::DATE AS cohort_week
 FROM user_sessions us
 JOIN first_session fs ON us.user_id = fs.user_id
),
-- Шаг 3: Рассчитаем неделю сеанса относительно недели первого сеанса (номер периода)
cohorts_with_periods AS (
 SELECT
 *,
 -- Вычисляем номер недели сеанса относительно недели первой активности
 EXTRACT('week' FROM session_date) - EXTRACT('week' FROM first_session_date) AS week_number
 FROM user_sessions_with_cohort
),
-- Шаг 4: Построим таблицу удержания
retention_table AS (
 SELECT
 cohort_week,
 week_number,
 COUNT(DISTINCT user_id) AS active_users
 FROM cohorts_with_periods
 -- Ограничиваем анализ, например, первыми 8 неделями
 WHERE week_number BETWEEN 0 AND 8
 GROUP BY cohort_week, week_number
),
-- Шаг 5: Найдем размер начальной когорты (неделя 0)
cohort_sizes AS (
 SELECT
 cohort_week,
 active_users AS cohort_size
 FROM retention_table
 WHERE week_number = 0
 )
 -- Шаг 6: Объединим таблицу удержания с размером когорты и посчитаем процент удержания
SELECT
 rt.cohort_week,
 rt.week_number,
 rt.active_users,
 cs.cohort_size,
 ROUND((rt.active_users::DECIMAL / cs.cohort_size) * 100, 2) AS retention_rate_pct
FROM retention_table rt
JOIN cohort_sizes cs ON rt.cohort_week = cs.cohort_week
ORDER BY rt.cohort_week, rt.week_number;


-- Анализ Churn:
-- Найдем для каждого пользователя даты сеансов и дату предыдущего сеанса
WITH user_session_lag AS (
 SELECT
 user_id,
 session_date,
 LAG(session_date) OVER (PARTITION BY user_id ORDER BY session_date) AS prev_session_date
 FROM user_sessions
),
-- Рассчитаем разницу в днях между сеансами
churn_calculation AS (
 SELECT
 user_id,
 session_date,
 prev_session_date,
 session_date - prev_session_date AS days_since_last_session
 FROM user_session_lag
 WHERE prev_session_date IS NOT NULL -- Исключаем первый сеанс
)
-- Найдем пользователей, ушедших (разница > 21 дня)
SELECT DISTINCT user_id, days_since_last_session
FROM churn_calculation
WHERE days_since_last_session > 21; -- Порог для churn