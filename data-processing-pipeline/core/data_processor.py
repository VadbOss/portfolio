import pandas as pd
import ast
from datetime import datetime
from typing import List, Dict, Any
import logging


class DataProcessor:
    """Процессор данных для извлечения и расчета метрик"""
    
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
    
    def extract_attempt_data(self, attempts_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Извлекаем и преобразовываем данные с обработкой отсутствующих значений"""
        self.logger.info("Извлекаем и преобразовываем данные с обработкой отсутствующих значений")
        
        extracted_data = []
        
        for attempt in attempts_list:
            try:
                # Базовые поля с проверкой на наличие
                user_id = attempt.get('lti_user_id')
                
                # Обрабатываем passback_params
                passback_params_str = attempt.get('passback_params', '{}')
                try:
                    # Пробуем распарсить строку как словарь
                    passback_params = ast.literal_eval(passback_params_str) if passback_params_str else {}
                except (ValueError, SyntaxError):
                    # Если не получается распарсить, используем пустой словарь
                    passback_params = {}
                
                # Извлекаем данные с подстановкой None для отсутствующих значений
                extracted_attempt = {
                    'user_id': user_id,
                    'oauth_consumer_key': passback_params.get('oauth_consumer_key'),
                    'lis_result_sourcedid': passback_params.get('lis_result_sourcedid'),
                    'lis_outcome_service_url': passback_params.get('lis_outcome_service_url'),
                    'is_correct': attempt.get('is_correct'),
                    'attempt_type': attempt.get('attempt_type'),
                    'created_at': datetime.strptime(attempt.get('created_at'),
                                                    '%Y-%m-%d %H:%M:%S.%f') if attempt.get('created_at') else None
                }
                
                extracted_data.append(extracted_attempt)
                
            except Exception as e:
                self.logger.warning(f"Ошибка при обработке попытки: {e}")
                continue
        
        self.logger.info(f"✅ Данные успешно обработаны. Обработано {len(extracted_data)} записей")
        return extracted_data
    
    def calculate_metrics(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        """Расчет метрик на основе данных"""
        # Создаем датафрейм с данными согласно БД Postgres
        df = pd.DataFrame(data)
        
        if df.empty:
            self.logger.warning("Нет данных для расчета метрик")
            return pd.DataFrame()
        
        # Преобразуем дату
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Считаем необходимые метрики
        result = df.groupby(df['created_at'].dt.date).agg(
            unique_users=('user_id', 'nunique'),
            run_attempts=('attempt_type', lambda x: (x == 'run').sum()),
            submit_attempts=('attempt_type', lambda x: (x == 'submit').sum()),
            successful_attempts=('is_correct', lambda x: (x == 1).sum())
        ).reset_index()
        
        # Переименуем колонку с датой для ясности
        result.rename(columns={'created_at': 'date'}, inplace=True)
        
        self.logger.info(f"✅ Рассчитано {len(result)} метрик")
        return result