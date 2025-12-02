import gspread
from google.oauth2.service_account import Credentials
import json
import logging
import pandas as pd


class GoogleSheetsClient:
    """Клиент для работы с Google Sheets"""
    
    def __init__(self, sheets_config, logger: logging.Logger = None):
        self.sheets_config = sheets_config
        self.logger = logger or logging.getLogger(__name__)
        self.client = None
        self._authenticate()
    
    def _authenticate(self):
        """Аутентификация в Google Sheets API"""
        try:
            scope = ['https://www.googleapis.com/auth/spreadsheets']
            creds = Credentials.from_service_account_info(
                self.sheets_config.credentials_json,
                scopes=scope
            )
            self.client = gspread.authorize(creds)
            self.logger.info("✅ Авторизация в Google Sheets успешна")
        except Exception as e:
            self.logger.error(f"❌ Ошибка авторизации в Google Sheets: {e}")
            raise
    
    def upload_data(self, data: pd.DataFrame):
        """Загрузка данных в Google Sheets"""
        try:
            self.logger.info(f"Загружаем данные в Google-таблицу по URL")
            
            # Открываем таблицу по URL
            spreadsheet = self.client.open_by_url(self.sheets_config.spreadsheet_url)
            worksheet = spreadsheet.sheet1
            
            # Очищаем лист
            worksheet.clear()
            
            # Преобразуем DataFrame в список списков
            data_list = [data.columns.tolist()]  # заголовки
            for row in data.values:
                data_list.append([str(cell) for cell in row])  # данные как строки
            
            # Загружаем данные
            worksheet.update(data_list)
            
            self.logger.info(f"✅ Данные успешно загружены в Google-таблицу {spreadsheet.title}")
            self.logger.info(f"🔗 Ссылка: {spreadsheet.url}")
            
            return spreadsheet.url
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка при загрузке в Google Sheets: {e}")
            raise