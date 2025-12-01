"""Вспомогательные функции для работы с данными."""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логгера
logger = logging.getLogger(__name__)


def read_excel_file(file_path: str) -> pd.DataFrame:
    """Читает Excel файл с транзакциями."""
    try:
        df = pd.read_excel(file_path)

        # Преобразуем даты
        date_columns = ["Дата операции", "Дата платежа"]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        logger.info(f"Успешно прочитано {len(df)} транзакций из {file_path}")
        logger.info(f"Колонки в данных: {list(df.columns)}")

        return df
    except Exception as e:
        logger.error(f"Ошибка чтения файла {file_path}: {e}")
        return pd.DataFrame()


def get_currency_rates(currencies: List[str]) -> List[Dict[str, float]]:
    """Получает текущие курсы валют."""
    try:
        # Заглушка для демонстрации
        rates = []
        for currency in currencies:
            # В реальном приложении здесь будет API запрос
            if currency == "USD":
                rates.append({"currency": currency, "rate": 75.5})
            elif currency == "EUR":
                rates.append({"currency": currency, "rate": 85.2})
            else:
                rates.append({"currency": currency, "rate": 1.0})

        logger.info(f"Получены курсы для {len(rates)} валют")
        return rates
    except Exception as e:
        logger.error(f"Ошибка получения курсов валют: {e}")
        return []


def get_stock_prices(stocks: List[str]) -> List[Dict[str, float]]:
    """Получает текущие цены акций."""
    try:
        # Заглушка для демонстрации
        prices = []
        for stock in stocks:
            # В реальном приложении здесь будет API запрос
            if stock == "AAPL":
                prices.append({"stock": stock, "price": 150.12})
            elif stock == "AMZN":
                prices.append({"stock": stock, "price": 135.5})
            elif stock == "GOOGL":
                prices.append({"stock": stock, "price": 125.8})
            elif stock == "MSFT":
                prices.append({"stock": stock, "price": 330.2})
            elif stock == "TSLA":
                prices.append({"stock": stock, "price": 210.7})
            else:
                prices.append({"stock": stock, "price": 100.0})

        logger.info(f"Получены цены для {len(prices)} акций")
        return prices
    except Exception as e:
        logger.error(f"Ошибка получения цен акций: {e}")
        return []


def get_greeting_by_time() -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def filter_data_by_date_range(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    """Фильтрует данные по диапазону дат."""
    try:
        df["Дата операции"] = pd.to_datetime(df["Дата операции"])
        mask = (df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)
        return df[mask]
    except Exception as e:
        logger.error(f"Ошибка фильтрации по дате: {e}")
        return df


def load_user_settings() -> Dict[str, Any]:
    """Загружает пользовательские настройки."""
    try:
        with open("user_settings.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Ошибка загрузки настроек: {e}")
        return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}
import logging
from typing import Any, Dict, List

import pandas as pd

logger = logging.getLogger(__name__)

def load_transactions(filepath: str = "data/operations.xlsx") -> List[Dict[str, Any]]:
    \"\"\"
    Загружает транзакции из Excel файла.
    
    Args:
        filepath: Путь к Excel файлу
        
    Returns:
        Список словарей с транзакциями
    \"\"\"
    try:
        df = pd.read_excel(filepath)
        logger.info(f"Успешно прочитано {len(df)} транзакций из {filepath}")
        logger.info(f"Колонки в данных: {list(df.columns)}")
        return df.to_dict('records')
    except Exception as e:
        logger.error(f"Ошибка загрузки данных: {e}")
        return []

# ... остальной код utils.py ...
