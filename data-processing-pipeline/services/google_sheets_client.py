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
    
    '''def upload_data(self, data: pd.DataFrame):
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
            raise'''
            
    def upload_data(self, data: pd.DataFrame):
        """Загрузка данных в Google Sheets с сохранением умной таблицы"""
        try:
            self.logger.info(f"Загружаем данные в Google-таблицу по URL")
            
            # Открываем таблицу по URL
            spreadsheet = self.client.open_by_url(self.sheets_config.spreadsheet_url)
            worksheet = spreadsheet.sheet1
            
            # 1. Очищаем старые данные ниже заголовков (стираем всё от A2 до Z10000)
            worksheet.batch_clear(["A2:Z10000"])
            
            # 2. Создаем копию DataFrame
            df_to_upload = data.copy()
            
            # 3. Переводим все колонки с датами в строки ISO (без использования deprecated errors='ignore')
            for col in df_to_upload.columns:
                if pd.api.types.is_datetime64_any_dtype(df_to_upload[col]) or df_to_upload[col].dtype == 'object':
                    try:
                        # Безопасная конвертация дат через явный отлов исключений (убирает FutureWarning)
                        converted = pd.to_datetime(df_to_upload[col])
                        df_to_upload[col] = converted.dt.strftime('%Y-%m-%d')
                    except Exception:
                        pass
            
            # 4. Преобразуем DataFrame в список списков без заголовков
            new_rows = df_to_upload.fillna("").values.tolist()
            
            # Дополнительное приведение объектов дат к строкам
            cleaned_rows = []
            for row in new_rows:
                cleaned_row = [str(cell) if hasattr(cell, 'strftime') else cell for cell in row]
                cleaned_rows.append(cleaned_row)
            
            # 5. Записываем данные СТРОГО начиная с ячейки A2 (поверх пустых строк таблицы)
            if cleaned_rows:
                # Находим конечную ячейку для точного диапазона (например, B10 или C150)
                end_col = chr(64 + len(cleaned_rows[0])) if len(cleaned_rows[0]) <= 26 else "Z"
                end_row = 1 + len(cleaned_rows)
                target_range = f"A2:{end_col}{end_row}"
                
                # Метод update с USER_ENTERED заставит умную таблицу сжаться/растянуться под этот диапазон
                worksheet.update(
                    range_name=target_range,
                    values=cleaned_rows,
                    value_input_option="USER_ENTERED"
                )
            
            self.logger.info(f"✅ Данные успешно загружены в Google-таблицу {spreadsheet.title}")
            self.logger.info(f"🔗 Ссылка: {spreadsheet.url}")
            
            return spreadsheet.url
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка при загрузке в Google Sheets: {e}")
            raise

        