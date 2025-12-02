import logging
import os
from datetime import datetime, timedelta
from pathlib import Path


class LogManager:
    """Менеджер логирования приложения"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.logger = None
        self._setup_logging()
    
    def _setup_logging(self):
        """Настройка системы логирования"""
        # Создаем папку для логов, если не существует
        self.log_dir.mkdir(exist_ok=True)
        
        # Название файла с текущей датой
        log_file = self.log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        
        # Настройка формата логирования
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Логирование инициализировано")
    
    def clean_old_logs(self, days_to_keep: int = 3):
        """Удаление логов старше указанного количества дней"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        for filename in os.listdir(self.log_dir):
            if filename.endswith('.log'):
                try:
                    file_path = self.log_dir / filename
                    file_date = datetime.strptime(filename.split('.')[0], '%Y-%m-%d')
                    
                    if file_date < cutoff_date:
                        file_path.unlink()
                        self.logger.info(f"Удален старый лог-файл: {filename}")
                except (ValueError, IndexError) as e:
                    self.logger.warning(f"Не удалось обработать файл {filename}: {e}")
    
    def get_logger(self):
        """Получение логгера"""
        return self.logger