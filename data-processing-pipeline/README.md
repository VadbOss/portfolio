# Data Processing Pipeline

Проект для обработки данных из API, сохранения в PostgreSQL, расчета метрик, загрузки в Google Sheets и отправки отчетов по email.

## Структура проекта
data-processing-pipeline/
├── core/
│ ├── init.py
│ ├── config_manager.py
│ ├── log_manager.py
│ └── data_processor.py
├── services/
│ ├── init.py
│ ├── api_client.py
│ ├── database_manager.py
│ ├── google_sheets_client.py
│ └── email_sender.py
├── logs/ # папка для логов (не в репозитории)
├── .venv/ # виртуальное окружение (не в репозитории)
├── main.py
├── requirements.txt
├── config.ini.example # пример конфигурации
├── .gitignore
└── README.md

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
