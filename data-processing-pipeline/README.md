# Data Processing Pipeline

Проект для автоматической обработки данных из API, сохранения в базу данных PostgreSQL, расчета метрик, загрузки результатов в Google Sheets и отправки отчетов по email.

## 📁 Структура проекта

<pre>
data-processing-pipeline/
├── core/
│   ├── __init__.py
│   ├── config_manager.py
│   ├── log_manager.py
│   └── data_processor.py
├── services/
│   ├── __init__.py
│   ├── api_client.py
│   ├── database_manager.py
│   ├── google_sheets_client.py
│   └── email_sender.py
├── main.py
├── requirements.txt
├── config.ini.example
└── README.md
</pre>

## ⚙️ Функциональность

✅ **Получение данных** через REST API  
✅ **Обработка и преобразование** данных с учетом отсутствующих значений  
✅ **Сохранение** в базу данных PostgreSQL  
✅ **Расчет метрик** (уникальные пользователи, типы попыток, успешные попытки)  
✅ **Экспорт результатов** в Google Sheets  
✅ **Автоматическая отправка** отчетов по email  
✅ **Логирование** с очисткой старых логов  
✅ **Обработка ошибок** на всех этапах  

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/VadbOss/portfolio.git
cd portfolio/data-processing-pipeline

## Настройка

1. Скопируйте `config.ini.example` в `config.ini` и заполните настройки.
2. Установите зависимости: `pip install -r requirements.txt`
3. Запустите: `python main.py`

