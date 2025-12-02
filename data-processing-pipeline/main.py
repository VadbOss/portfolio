#!/usr/bin/env python3
"""Главный файл приложения"""

import sys
import os

# Добавляем корневую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config_manager import ConfigManager
from core.log_manager import LogManager
from core.data_processor import DataProcessor
from services.api_client import APIClient
from services.database_manager import DatabaseManager
from services.google_sheets_client import GoogleSheetsClient
from services.email_sender import EmailSender


class DataProcessingApp:
    """Главный класс приложения для обработки данных"""
    
    def __init__(self, config_file: str = 'config.ini'):
        """Инициализация приложения"""
        # Инициализация менеджера конфигурации
        self.config_manager = ConfigManager(config_file)
        
        # Инициализация менеджера логирования
        self.log_manager = LogManager()
        self.logger = self.log_manager.get_logger()
        
        # Загрузка конфигураций
        self.api_config = self.config_manager.get_api_config()
        self.db_config = self.config_manager.get_database_config()
        self.sheets_config = self.config_manager.get_google_sheets_config()
        self.email_config = self.config_manager.get_email_config()
        
        # Инициализация компонентов
        self.api_client = APIClient(self.api_config, self.logger)
        self.data_processor = DataProcessor(self.logger)
        self.db_manager = DatabaseManager(self.db_config, self.logger)
        self.google_sheets_client = GoogleSheetsClient(self.sheets_config, self.logger)
        self.email_sender = EmailSender(self.email_config, self.logger)
        
        self.logger.info("Приложение инициализировано")
    
    def run(self):
        """Основной метод запуска приложения"""
        try:
            self.logger.info("=" * 50)
            self.logger.info("НАЧАЛО РАБОТЫ СКРИПТА")
            self.logger.info("=" * 50)
            
            # Шаг 1: Удаление логов старше 3 дней
            self.logger.info("Шаг 1: Очистка старых логов")
            self.log_manager.clean_old_logs(days_to_keep=3)
            
            # Шаг 2: Получение данных по API
            self.logger.info("Шаг 2: Получение данных по API")
            raw_data = self.api_client.upload_data_by_api()
            
            if not raw_data:
                self.logger.error("Не удалось получить данные от API. Завершение работы.")
                return
            
            # Шаг 3: Преобразование данных
            self.logger.info("Шаг 3: Преобразование данных")
            processed_data = self.data_processor.extract_attempt_data(raw_data)
            
            if not processed_data:
                self.logger.error("Нет данных для обработки. Завершение работы.")
                return
            
            # Шаг 4: Загрузка данных в базу PostgreSQL
            self.logger.info("Шаг 4: Загрузка данных в базу PostgreSQL")
            with self.db_manager:
                self.db_manager.insert_dict_list_to_table(processed_data)
            
            # Шаг 5: Вычисление метрик
            self.logger.info("Шаг 5: Вычисление метрик")
            metrics_result = self.data_processor.calculate_metrics(processed_data)
            
            if metrics_result.empty:
                self.logger.warning("Не удалось рассчитать метрики")
                metrics_result = pd.DataFrame()  # Создаем пустой DataFrame для совместимости
            
            # Шаг 6: Загрузка данных в Google Sheets
            self.logger.info("Шаг 6: Загрузка данных в Google Sheets")
            spreadsheet_url = self.google_sheets_client.upload_data(metrics_result)
            
            # Шаг 7: Отправка данных по почте
            self.logger.info("Шаг 7: Отправка данных по почте")
            self.email_sender.send_result_email(metrics_result, spreadsheet_url)
            
            self.logger.info("=" * 50)
            self.logger.info("СКРИПТ УСПЕШНО ЗАВЕРШЕН")
            self.logger.info("=" * 50)
            
            # Вывод ссылки на Google Sheets
            if spreadsheet_url:
                print(f"\n🔗 Ссылка на Google Sheets: {spreadsheet_url}")
            
        except Exception as e:
            self.logger.error(f"КРИТИЧЕСКАЯ ОШИБКА В РАБОТЕ СКРИПТА: {e}", exc_info=True)
            raise


if __name__ == '__main__':
    # Создание и запуск приложения
    app = DataProcessingApp('config.ini')
    app.run()