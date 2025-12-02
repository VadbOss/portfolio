import psycopg2
from psycopg2.extras import execute_batch
import logging
from typing import List, Dict, Any


class DatabaseManager:
    """Менеджер для работы с базой данных PostgreSQL"""
    
    def __init__(self, db_config, logger: logging.Logger = None):
        self.db_config = db_config
        self.logger = logger or logging.getLogger(__name__)
        self.connection = None
    
    def connect(self):
        """Установка соединения с базой данных"""
        try:
            self.connection = psycopg2.connect(
                host=self.db_config.host,
                port=self.db_config.port,
                database=self.db_config.name,
                user=self.db_config.user,
                password=self.db_config.password
            )
            self.logger.info("Соединение с базой данных установлено")
        except psycopg2.Error as e:
            self.logger.error(f"Ошибка подключения к базе данных: {e}")
            raise
    
    def disconnect(self):
        """Закрытие соединения с базой данных"""
        if self.connection:
            self.connection.close()
            self.logger.info("Соединение с базой данных закрыто")
    
    def insert_dict_list_to_table(self, data_list: List[Dict[str, Any]]):
        """Вставка списка словарей в таблицу"""
        self.logger.info("Загрузка преобразованных данных в PostgreSQL")
        
        if not data_list:
            self.logger.error("Список данных пуст!")
            return
        
        # Получаем названия колонок из ключей первого словаря
        columns = list(data_list[0].keys())
        columns_str = ', '.join(columns)
        
        # Создаем плейсхолдеры для SQL запроса
        placeholders = ', '.join(['%s'] * len(columns))
        
        # SQL запрос
        sql = f"INSERT INTO {self.db_config.table_name} ({columns_str}) VALUES ({placeholders})"
        
        # Подготавливаем данные для вставки
        values_list = []
        for item in data_list:
            values = tuple(item[col] for col in columns)
            values_list.append(values)
        
        try:
            cursor = self.connection.cursor()
            
            # Массовая вставка
            execute_batch(cursor, sql, values_list)
            
            self.connection.commit()
            cursor.close()
            
            self.logger.info(f"✅ Успешно добавлено {len(values_list)} записей в таблицу '{self.db_config.table_name}'")
            
        except psycopg2.Error as e:
            self.logger.error(f"❌ Ошибка при вставке данных: {e}")
            self.connection.rollback()
            raise
    
    def __enter__(self):
        """Контекстный менеджер для соединения"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрытие соединения при выходе из контекста"""
        self.disconnect()