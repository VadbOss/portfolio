# Data Processing Pipeline

## Структура проекта
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


## Настройка

1. Скопируйте `config.ini.example` в `config.ini` и заполните настройки.
2. Установите зависимости: `pip install -r requirements.txt`
3. Запустите: `python main.py`

## Функциональность

- Загрузка данных по API
- Сохранение в PostgreSQL
- Расчет метрик
- Загрузка в Google Sheets
- Отправка отчетов на email
