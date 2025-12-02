import configparser
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any


@dataclass
class ApiConfig:
    """Конфигурация API"""
    url: str
    client: str
    client_key: str
    start: str
    end: str
    params: Dict[str, str]


@dataclass
class DatabaseConfig:
    """Конфигурация базы данных"""
    host: str
    port: int
    name: str
    user: str
    password: str
    table_name: str


@dataclass
class GoogleSheetsConfig:
    """Конфигурация Google Sheets"""
    credentials_json: Dict[str, Any]
    spreadsheet_url: str


@dataclass
class EmailConfig:
    """Конфигурация email"""
    smtp_server: str
    port: int
    sender_email: str
    password: str
    receiver_email: str


class ConfigManager:
    """Менеджер конфигурации приложения"""
    
    def __init__(self, config_file: str = 'config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser(interpolation=None)
        self._load_config()
    
    def _load_config(self):
        """Загрузка конфигурации из файла"""
        self.config.read(self.config_file)
    
    def get_api_config(self) -> ApiConfig:
        """Получение конфигурации API"""
        api_section = self.config['API']
        params = {
            'client': api_section['API_CLIENT'],
            'client_key': api_section['API_CLIENT_KEY'],
            'start': api_section['API_START'],
            'end': api_section['API_END']
        }
        
        return ApiConfig(
            url=api_section['API_URL'],
            client=api_section['API_CLIENT'],
            client_key=api_section['API_CLIENT_KEY'],
            start=api_section['API_START'],
            end=api_section['API_END'],
            params=params
        )
    
    def get_database_config(self) -> DatabaseConfig:
        """Получение конфигурации базы данных"""
        db_section = self.config['DATABASE']
        return DatabaseConfig(
            host=db_section['HOST'],
            port=int(db_section['PORT']),
            name=db_section['NAME'],
            user=db_section['USER'],
            password=db_section['PASSWORD'],
            table_name=db_section['TABLE_NAME']
        )
    
    def get_google_sheets_config(self) -> GoogleSheetsConfig:
        """Получение конфигурации Google Sheets"""
        sheets_section = self.config['GOOGLE_SERVICE_ACCOUNT']
        credentials_json = json.loads(sheets_section['CREDENTIALS_JSON'])
        
        return GoogleSheetsConfig(
            credentials_json=credentials_json,
            spreadsheet_url=sheets_section['GOOGLE_SHEATS']
        )
    
    def get_email_config(self) -> EmailConfig:
        """Получение конфигурации email"""
        email_section = self.config['EMAIL']
        return EmailConfig(
            smtp_server=email_section['SMTP_SERVER'],
            port=int(email_section['PORT']),
            sender_email=email_section['SENDER_EMAIL'],
            password=email_section['PASSWORD'],
            receiver_email=email_section['RECEIVER_EMAIL']
        )