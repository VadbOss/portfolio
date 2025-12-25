import os
import configparser
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
from pgdb import PGDatabase

config = configparser.ConfigParser()
config.read("config.ini")

COMPANIES = eval(config["COMPANIES"]["COMPANIES"])
SALES_PATH = config["Files"]["SALES_PATH"]
DATABASE_CREDS = config["Database"]

os.chdir(Path(__file__).parent)

sales_df = pd.DataFrame()
if os.path.exists(SALES_PATH):
    sales_df = pd.read_csv(SALES_PATH)
    print(sales_df)
    os.remove(SALES_PATH)   
  
historical_d = {}
for company in COMPANIES:
    try:
        # Используем yfinance.download вместо yahoo_fin.get_data
        start_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        end_date = (datetime.today() - timedelta(days=0)).strftime("%Y-%m-%d")
        
        # Скачиваем данные
        temp_data = yf.download(company, start=start_date, end=end_date, progress=False)
        
        # Проверяем, что данные не пустые
        if temp_data.empty:
            print(f"Предупреждение: Нет данных для {company} за указанный период. Возможно, это нерабочий день.")
            historical_d[company] = pd.DataFrame()  # Сохраняем пустой DataFrame
        else:
            # Сбрасываем индекс, чтобы 'Date' стал колонкой
            temp_data = temp_data.reset_index()
            # Добавляем колонку с тикером
            temp_data['Ticker'] = company
            # Переименовываем колонки, если нужно
            temp_data.columns = [col[0] if isinstance(col, tuple) else col for col in temp_data.columns]
            historical_d[company] = temp_data
            #print(f"Данные для {company} успешно загружены.")
            #print(f"Колонки в данных: {historical_d[company].columns.tolist()}")
            #print(historical_d[company].head())
            
    except Exception as e:
        print(f"Ошибка при загрузке данных для {company}: {e}")
        historical_d[company] = pd.DataFrame()  # Сохраняем пустой DataFrame в случае ошибки    
        
database = PGDatabase(
    host=DATABASE_CREDS['HOST'],
    database=DATABASE_CREDS['DATABASE'],
    user=DATABASE_CREDS['USER'],
    password=DATABASE_CREDS['PASSWORD']
)

# Вставляем данные в базу
# Сначала в таблицу sales
for i, row in sales_df.iterrows():
    query = f"INSERT INTO sales VALUES('{row['dt']}','{row['company']}','{row['transaction_type']}',{row['amount']})"
    database.post(query)

# Вставляем в таблицу stock
for company, data in historical_d.items():
    if not data.empty:  # Проверяем, что данные не пустые
        #print(f"\nВставляем данные для {company}")
        #print(f"Колонки в data: {data.columns.tolist()}")
        #print(f"Первая строка data: {data.iloc[0] if len(data) > 0 else 'Нет данных'}")
        
        # Преобразуем колонку Date в строковый формат
        if 'Date' in data.columns:
            data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
        else:
            print(f"Предупреждение: В данных для {company} нет колонки 'Date'")
            continue
            
        # Проверяем наличие необходимых колонок
        required_columns = ['Ticker', 'Open', 'Close']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            print(f"Ошибка: В данных для {company} отсутствуют колонки: {missing_columns}")
            continue
            
        for i, row in data.iterrows():
            try:
                # Формируем SQL-запрос
                query = f"INSERT INTO stock VALUES('{row['Date']}', '{row['Ticker']}', {row['Open']}, {row['Close']})"
                #print(f"Выполняем запрос: {query}")
                database.post(query)
            except Exception as e:
                print(f"Ошибка при вставке строки {i} для {company}: {e}")


'''for company, data in historical_d.items():                
    print(company, data)'''                