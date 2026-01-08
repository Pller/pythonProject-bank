import pandas as pd
import logging
import json
import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

logger = logging.getLogger(__name__)


def get_exchange_rates() -> Dict[str, float]:
    """
    Получает курсы валют от Центробанка России.

    Returns:
        Словарь с курсами валют (USD, EUR, GBP к RUB)
    """
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        rates = {
            "USD": data["Valute"]["USD"]["Value"],
            "EUR": data["Valute"]["EUR"]["Value"],
            "GBP": data["Valute"]["GBP"]["Value"],
        }

        logger.info(f"Получены курсы валют: {rates}")
        return rates

    except Exception as e:
        logger.error(f"Ошибка получения курсов валют: {e}")
        # Возвращаем заглушки в случае ошибки
        return {
            "USD": 90.5,
            "EUR": 98.2,
            "GBP": 114.3,
        }


def get_stock_prices() -> Dict[str, float]:
    """
    Получает цены акций из S&P500 через Yahoo Finance API.

    Returns:
        Словарь с ценами акций
    """
    try:
        symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
        prices = {}

        for symbol in symbols:
            try:
                # Используем Yahoo Finance API
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()

                price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
                prices[symbol] = price

            except Exception as e:
                logger.warning(f"Не удалось получить цену для {symbol}: {e}")
                # Заглушка в случае ошибки
                prices[symbol] = {
                    "AAPL": 185.2,
                    "GOOGL": 142.5,
                    "MSFT": 374.5,
                    "TSLA": 240.1,
                    "AMZN": 154.9,
                }.get(symbol, 0)

        logger.info(f"Получены цены для {len(prices)} акций")
        return prices

    except Exception as e:
        logger.error(f"Ошибка получения цен акций: {e}")
        # Возвращаем заглушки в случае ошибки
        return {
            "AAPL": 185.2,
            "GOOGL": 142.5,
            "MSFT": 374.5,
            "TSLA": 240.1,
            "AMZN": 154.9,
        }


def analyze_expenses(df: pd.DataFrame) -> dict:
    """
    Анализирует расходы из DataFrame.

    Args:
        df: DataFrame с транзакциями

    Returns:
        Словарь с анализом расходов
    """
    if df.empty:
        return {
            "total": 0,
            "main_categories": [],
            "other_categories": None,
            "transfers_cash": []
        }

    try:
        # Определяем столбец с суммой расходов
        amount_column = None
        for col in ['Сумма операции', 'Сумма платежа', 'amount']:
            if col in df.columns:
                amount_column = col
                break

        if amount_column is None:
            return {
                "total": 0,
                "main_categories": [],
                "other_categories": None,
                "transfers_cash": [],
            }

        # Фильтруем расходы (положительные суммы)
        expenses_df = df[df[amount_column] > 0].copy()

        if expenses_df.empty:
            return {
                "total": 0,
                "main_categories": [],
                "other_categories": None,
                "transfers_cash": [],
            }

        # Группируем по категориям
        if 'Категория' not in expenses_df.columns:
            expenses_df['Категория'] = 'Без категории'

        category_totals = expenses_df.groupby('Категория')[amount_column].sum()
        total_expenses = category_totals.sum()

        # Сортируем по убыванию
        sorted_categories = category_totals.sort_values(ascending=False)

        # Берем топ-7 категорий
        top_categories = []
        for i, (category, amount) in enumerate(sorted_categories.head(7).items()):
            top_categories.append({
                "category": str(category),
                "amount": float(amount),
                "percentage": round((amount / total_expenses * 100), 2) if total_expenses > 0 else 0,
            })

        # Суммируем остальные категории
        other_amount = sorted_categories.iloc[7:].sum() if len(sorted_categories) > 7 else 0

        # Категории "Переводы" и "Наличные"
        transfers_cash = []
        for category in ["Переводы", "Наличные"]:
            if category in sorted_categories.index:
                transfers_cash.append({
                    "category": category,
                    "amount": float(sorted_categories[category]),
                })

        # Сортируем переводы и наличные по убыванию
        transfers_cash.sort(key=lambda x: x["amount"], reverse=True)

        result = {
            "total": float(total_expenses),
            "main_categories": top_categories,
            "transfers_cash": transfers_cash,
        }

        # Добавляем other_categories только если есть остальные категории
        if other_amount > 0:
            result["other_categories"] = {
                "category": "Остальное",
                "amount": float(other_amount),
                "percentage": round((other_amount / total_expenses * 100), 2) if total_expenses > 0 else 0,
            }
        else:
            result["other_categories"] = None

        return result

    except Exception as e:
        logger.error(f"Ошибка анализа расходов: {e}")
        return {
            "total": 0,
            "main_categories": [],
            "other_categories": None,
            "transfers_cash": [],
        }


def analyze_incomes(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Анализирует поступления по категориям.

    Args:
        df: DataFrame с транзакциями

    Returns:
        Словарь с анализом поступлений
    """
    try:
        # Проверяем что DataFrame не пустой
        if df.empty:
            return {"total": 0, "main_categories": []}

        # Определяем столбец с суммой
        amount_column = None
        for col in ['Сумма операции', 'Сумма платежа', 'amount']:
            if col in df.columns:
                amount_column = col
                break

        if amount_column is None:
            return {"total": 0, "main_categories": []}

        # Поступления могут быть отрицательными числами или положительными с определенными категориями
        # Сначала ищем отрицательные суммы (традиционный подход для доходов)
        incomes_df = df[df[amount_column] < 0].copy()

        # Если нет отрицательных, ищем определенные категории
        if incomes_df.empty and 'Категория' in df.columns:
            income_categories = ['Пополнение', 'Зачисление', 'Возврат', 'Начисление', 'Доход', 'Зарплата']
            mask = df['Категория'].astype(str).str.contains('|'.join(income_categories), case=False, na=False)
            incomes_df = df[mask & (df[amount_column] > 0)].copy()

        if incomes_df.empty:
            return {"total": 0, "main_categories": []}

        # Группируем по категориям
        if 'Категория' not in incomes_df.columns:
            incomes_df['Категория'] = 'Поступления'

        # Для отрицательных сумм берем модуль
        if (incomes_df[amount_column] < 0).any():
            incomes_df['income_amount'] = incomes_df[amount_column].abs()
        else:
            incomes_df['income_amount'] = incomes_df[amount_column]

        category_totals = incomes_df.groupby('Категория')['income_amount'].sum()
        total_income = category_totals.sum()

        # Сортируем по убыванию
        sorted_categories = category_totals.sort_values(ascending=False)

        main_categories = []
        for category, amount in sorted_categories.items():
            main_categories.append({
                "category": str(category),
                "amount": float(amount),
                "percentage": round((amount / total_income * 100), 2) if total_income > 0 else 0,
            })

        return {
            "total": float(total_income),
            "main_categories": main_categories,
        }

    except Exception as e:
        logger.error(f"Ошибка анализа поступлений: {e}")
        return {"total": 0, "main_categories": []}


def analyze_cards(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Анализирует данные по картам.

    Args:
        df: DataFrame с транзакциями

    Returns:
        Список с данными по картам
    """
    try:
        # Проверяем наличие необходимых колонок
        required_columns = ['Номер карты', 'Сумма операции']
        if not all(col in df.columns for col in required_columns):
            return []

        # Группируем по картам
        cards_summary = {}

        for _, row in df.iterrows():
            card_number = str(row.get('Номер карты', '')).strip()
            if not card_number:
                continue

            # Берем последние 4 цифры
            last_four = card_number[-4:] if len(card_number) >= 4 else card_number

            amount = float(row.get('Сумма операции', 0))
            # Расходы - положительные суммы
            if amount <= 0:
                continue

            cashback = float(row.get('Кешбэк', 0))

            if last_four not in cards_summary:
                cards_summary[last_four] = {
                    "card_last_four": last_four,
                    "total_spent": 0.0,
                    "cashback_amount": 0.0,
                }

            cards_summary[last_four]["total_spent"] += amount
            cards_summary[last_four]["cashback_amount"] += cashback

        # Рассчитываем дополнительный кешбэк: 1 рубль на каждые 100 рублей
        result = []
        for card_data in cards_summary.values():
            calculated_cashback = card_data["total_spent"] / 100
            card_data["calculated_cashback"] = calculated_cashback
            card_data["total_cashback"] = card_data["cashback_amount"] + calculated_cashback
            result.append(card_data)

        return result

    except Exception as e:
        logger.error(f"Ошибка анализа карт: {e}")
        return []


def get_top_transactions(df: pd.DataFrame, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Возвращает топ транзакций по сумме платежа.

    Args:
        df: DataFrame с транзакциями
        limit: Количество транзакций в топе

    Returns:
        Список топ транзакций
    """
    try:
        # Определяем столбец с суммой платежа
        amount_column = None
        for col in ['Сумма платежа', 'Сумма операции', 'amount']:
            if col in df.columns:
                amount_column = col
                break

        if amount_column is None:
            return []

        # Берем топ по убыванию суммы
        top_df = df.nlargest(limit, amount_column)

        result = []
        for i, (_, row) in enumerate(top_df.iterrows(), 1):
            result.append({
                "rank": i,
                "amount": float(row[amount_column]),
                "description": str(row.get('Описание', ''))[:50],
                "category": str(row.get('Категория', '')),
                "date": str(row.get('Дата операции', ''))[:10],
            })

        return result

    except Exception as e:
        logger.error(f"Ошибка получения топ транзакций: {e}")
        return []


def get_time_based_greeting() -> str:
    """
    Возвращает приветствие в зависимости от времени суток.

    Returns:
        Приветствие
    """
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def read_excel_file(file_path: str = "data/operations.xlsx") -> pd.DataFrame:
    """
    Читает Excel файл и возвращает DataFrame.

    Args:
        file_path: Путь к Excel файлу

    Returns:
        DataFrame с данными
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден")

        df = pd.read_excel(file_path)
        logger.info(f"Прочитан файл {file_path}. Строк: {len(df)}, Колонок: {len(df.columns)}")
        return df

    except Exception as e:
        logger.error(f"Ошибка чтения файла {file_path}: {e}")
        raise


def load_transactions(filepath: str = "data/operations.xlsx") -> List[Dict[str, Any]]:
    """
    Загружает транзакции из Excel файла.
    (Алиас для совместимости со старым кодом)

    Args:
        filepath: Путь к Excel файлу

    Returns:
        Список словарей с транзакциями
    """
    try:
        df = read_excel_file(filepath)
        return df.to_dict('records')
    except Exception as e:
        logger.error(f"Ошибка загрузки транзакций: {e}")
        return []

def save_report(report_data: Dict[str, Any], filename_prefix: str) -> str:
    """
    Сохраняет отчет в JSON файл.

    Args:
        report_data: Данные отчета
        filename_prefix: Префикс имени файла

    Returns:
        Путь к сохраненному файлу
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        logger.info(f"Отчет сохранен в файл: {filename}")
        return filename

    except Exception as e:
        logger.error(f"Ошибка сохранения отчета: {e}")
        return ""


def calculate_statistics(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Рассчитывает базовую статистику по транзакциям.

    Args:
        transactions: Список транзакций

    Returns:
        Словарь со статистикой
    """
    try:
        if not transactions:
            return {
                "total_count": 0,
                "total_amount": 0,
                "avg_amount": 0,
                "min_amount": 0,
                "max_amount": 0,
            }

        amounts = [t.get("Сумма операции", 0) for t in transactions]

        return {
            "total_count": len(transactions),
            "total_amount": sum(amounts),
            "avg_amount": sum(amounts) / len(amounts) if amounts else 0,
            "min_amount": min(amounts) if amounts else 0,
            "max_amount": max(amounts) if amounts else 0,
        }

    except Exception as e:
        logger.error(f"Ошибка расчета статистики: {e}")
        return {}


def filter_by_date_range(
        transactions: List[Dict[str, Any]],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        date_column: str = "Дата операции"
) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по диапазону дат.

    Args:
        transactions: Список транзакций
        start_date: Начальная дата (YYYY-MM-DD)
        end_date: Конечная дата (YYYY-MM-DD)
        date_column: Название колонки с датой

    Returns:
        Отфильтрованный список транзакций
    """
    try:
        if not transactions:
            return []

        filtered = transactions.copy()

        if start_date:
            start = pd.to_datetime(start_date)
            filtered = [t for t in filtered if pd.to_datetime(t.get(date_column, '')) >= start]

        if end_date:
            end = pd.to_datetime(end_date)
            filtered = [t for t in filtered if pd.to_datetime(t.get(date_column, '')) <= end]

        logger.info(f"Отфильтровано {len(filtered)} из {len(transactions)} транзакций")
        return filtered

    except Exception as e:
        logger.error(f"Ошибка фильтрации по дате: {e}")
        return transactions


def format_amount(amount: float, currency: str = "RUB") -> str:
    """
    Форматирует сумму для вывода.

    Args:
        amount: Сумма
        currency: Валюта

    Returns:
        Отформатированная строка
    """
    return f"{amount:,.2f} {currency}".replace(",", " ").replace(".", ",")


def read_excel_file(file_path: str = "data/operations.xlsx") -> pd.DataFrame:
    """
    Читает Excel файл и возвращает DataFrame.

    Args:
        file_path: Путь к Excel файлу

    Returns:
        DataFrame с данными
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден")

        df = pd.read_excel(file_path)
        logger.info(f"Прочитан файл {file_path}. Строк: {len(df)}, Колонок: {len(df.columns)}")
        return df

    except Exception as e:
        logger.error(f"Ошибка чтения файла {file_path}: {e}")
        raise


def load_transactions(filepath: str = "data/operations.xlsx") -> List[Dict[str, Any]]:
    """
    Загружает транзакции из Excel файла.
    (Алиас для совместимости со старым кодом)

    Args:
        filepath: Путь к Excel файлу

    Returns:
        Список словарей с транзакциями
    """
    try:
        df = read_excel_file(filepath)
        return df.to_dict('records')
    except Exception as e:
        logger.error(f"Ошибка загрузки транзакций: {e}")
        return []
