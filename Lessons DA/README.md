# 📊 Тестовое задание на позицию Data Analitics / Аналитика

## 📋 Содержание
- [📌 Общая информация](#-общая-информация)
- [📊 Раздел 1: Теория вероятностей и логика](#-раздел-1-теория-вероятностей-и-логика)
- [🐍 Раздел 2: Python](#-раздел-2-python)
- [🗃️ Раздел 3: SQL](#️-раздел-3-sql)
- [📈 Раздел 4: Статистика и АБ-тесты](#-раздел-4-статистика-и-аб-тесты)
- [🧠 Раздел 5: ML Base](#-раздел-5-ml-base)

---

## 📌 Общая информация

| Параметр | Значение |
|----------|----------|
| **Дата выполнения** | `2026 - 02 - 07` |
| **Формат** | Теоретические задачи и практические кейсы |
| **Уровень сложности** | Junior+ |
| **Статус** | ✅ Выполнено |

---

## 📊 Раздел 1: Теория вероятностей и логика

### ✅ Решенные задачи:

| Задача | Тема | Сложность | Статус |
|--------|------|-----------|--------|
| **Задача 1** | Фермер | 🟡 Средняя | ✅ Решено |
| **Задача 2** | Кулинарное соревнование | 🟡 Средняя | ✅ Решено |
| **Задача 3** | Одинокая дорога | 🟡 Средняя | ✅ Решено |


### 🎯 Ключевые навыки:
- Работа с условными вероятностями
- Решение комбинаторных задач
- Логический анализ условий

---

## 🐍 Раздел 2: Python

### ✅ Выполненные задания:

```python
# Пример решения задачи
def is_isomorphic(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    def equal(sym: str):
        d = {}
        lst = []
        for i, s in enumerate(sym):
            if s not in d:
                d[s] = i
            lst.append(d[s])
        return lst
    return equal(s) == equal(t)


s = 'paper'
t = 'title'
print(is_isomorphic(s, t))

```python
# Пример решения задачи
def missing_number(nums: list) -> int:
    n = len(nums) + 1
    return n * (n + 1) // 2 - sum(nums)

```python
# Пример решения задачи
def prime_factors(n: int) -> list:
    factors = []
    # обрабатываем делитель 2 отдельно
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    # теперь проверяем только нечётные делители
    d = 3
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 2  # только нечётные
    if n > 1:
        factors.append(n)
    return factors
```


## 🗃️ Раздел 3: SQL

### ✅ Выполненные задания:

```PostgreSQL

1-е Задание

SELECT
   id,
   scores,
   DENSE_RANK() OVER (ORDER BY scores DESC) AS position
FROM table
ORDER BY  –сортировка
LIMIT  –ограничение количества выводимых строк
OFFSET;

3-е Задание

WITH  purshase AS (
	SELECT t.account_id AS client,
		   sum(t.amount)
	FROM transaction t
	JOIN account a ON t.account_id = a.client_id
	WHERE t.TYPE = 'PUR'
	GROUP BY t.account_id
	HAVING sum(t.amount) < 50000
)
SELECT client 
FROM purshase
ORDER BY client;
```

## 📈 Раздел 4: Статистика и АБ-тесты
### 📊 Решенные задачи:
1. Тесты
2. Тесты
3. Параметрический тест


## 🧠 Раздел 5: ML Base
### 🤖 Решенные кейсы:
Задание 1: Выбор модели классификации
Задание 2: Ручной счёт ROC_AUC
Задание 3: Ручной счёт корреляции




