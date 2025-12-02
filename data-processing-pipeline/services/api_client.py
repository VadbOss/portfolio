import requests
import logging
from typing import Dict, Any, Optional


class APIClient:
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
            return None