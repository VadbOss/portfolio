import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime
import logging
import pandas as pd


class EmailSender:
    """Отправитель email уведомлений"""
    
    def __init__(self, email_config, logger: logging.Logger = None):
        self.email_config = email_config
        self.logger = logger or logging.getLogger(__name__)
    
    def send_result_email(self, result: pd.DataFrame, spreadsheet_url: str = None):
        """Отправка результатов по email"""
        self.logger.info("Формируем письмо с результатами для отправки по почте")
        
        try:
            # Создаем безопасный контекст
            context = ssl.create_default_context()
            
            # Формируем письмо
            msg = EmailMessage()
            msg['Subject'] = f"Данные скрипта + Google-таблица - {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            msg['From'] = self.email_config.sender_email
            msg['To'] = self.email_config.receiver_email
            
            # Формируем сообщение
            message = self._create_message_body(result, spreadsheet_url)
            msg.set_content(message)
            
            # Отправляем письмо
            with smtplib.SMTP_SSL(
                self.email_config.smtp_server,
                self.email_config.port,
                context=context
            ) as server:
                server.login(self.email_config.sender_email, self.email_config.password)
                server.send_message(msg)
            
            self.logger.info(f"✅ Письмо с результатами успешно отправлено на {self.email_config.receiver_email}!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка при отправке email: {e}")
            return False
    
    def _create_message_body(self, result: pd.DataFrame, spreadsheet_url: str = None) -> str:
        """Создание тела сообщения"""
        if result.empty:
            results_text = "Нет данных для отображения"
        else:
            # Выбираем только нужные колонки для отчета
            if 'date' in result.columns and 'successful_attempts' in result.columns:
                report_data = result[['date', 'successful_attempts']].copy()
                # Преобразуем дату в строку для читаемости
                report_data['date'] = report_data['date'].astype(str)
                results_text = report_data.to_string(index=False)
            else:
                results_text = result.to_string(index=False)
        
        # Форматируем сообщение
        message = f"""\
ОТЧЕТ О ВЫПОЛНЕНИИ СКРИПТА

📅 Дата и время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

📊 РЕЗУЛЬТАТЫ РАБОТЫ СКРИПТА:
{results_text}

🔗 GOOGLE-ТАБЛИЦА С ДАННЫМИ:
{spreadsheet_url if spreadsheet_url else "Ссылка недоступна"}

📋 КРАТКОЕ СОДЕРЖАНИЕ:
Данные были успешно обработаны скриптом и сохранены в указанную Google-таблицу.
Для просмотра полных данных перейдите по ссылке выше.

---
Автоматическая отправка от Python-скрипта"""
        
        return message