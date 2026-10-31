import requests
import logging
from typing import Dict, Any, Optional


'''class APIClient:
    """Клиент для работы с внешним API"""
    
    def __init__(self, api_config, logger: logging.Logger = None):
        self.api_config = api_config
        self.logger = logger or logging.getLogger(__name__)
    
    def upload_data_by_api(self) -> Optional[Dict[str, Any]]:
        """Получение данных по API"""
        self.logger.info("Начало загрузки данных по API")
        
        try:
            response = requests.get(
                self.api_config.url,
                params=self.api_config.params,
                #timeout=30
            )
            
            if response.status_code == 200:
                self.logger.info("✅ Данные по API успешно получены")
                return response.json()
            else:
                self.logger.error(f"Ошибка API. Status code: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Ошибка подключения к API: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка при работе с API: {str(e)}")
            return None'''
            
class APIClient:
    """Клиент для работы с внешним API"""
    
    def __init__(self, api_config, logger: logging.Logger = None):
        self.api_config = api_config
        self.logger = logger or logging.getLogger(__name__)
    
    def upload_data_by_api(self) -> Optional[Dict[str, Any]]:
        """Получение данных по API"""
        self.logger.info("Начало загрузки данных по API")
        
        # Заголовок User-Agent обязателен, иначе сервер может блокировать запрос
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }
        
        try:
            response = requests.get(
                self.api_config.url,
                params=self.api_config.params,
                headers=headers,
                timeout=60  # обязательно, иначе запрос может висеть вечно
            )
            
            # Явно поднимаем исключение для 4xx/5xx, чтобы попасть в except
            response.raise_for_status()
            
            self.logger.info("✅ Данные по API успешно получены")
            return response.json()
                
        except requests.exceptions.Timeout:
            self.logger.error("Ошибка API: превышено время ожидания (60 сек). Сервер не отвечает.")
            return None
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"Ошибка API. Status code: {e.response.status_code}. Ответ: {e.response.text[:200]}")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Ошибка подключения к API: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка при работе с API: {str(e)}")
            return None