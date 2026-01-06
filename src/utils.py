import pandas as pd
import logging
import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

logger = logging.getLogger(__name__)


def load_transactions(filepath: str = "data/operations.xlsx") -> List[Dict[str, Any]]:
    """
    Загружает транзакции из Excel файла.

    Аргументы:
        filepath: Путь к Excel файлу

    Возвращает:
        Список словарей с транзакциями
    """
    try:
        if not os.path.exists(filepath):
            logger.warning(f"Файл {filepath} не найден. Возвращаю пустой список.")
            return []

        df = pd.read_excel(filepath)
        logger.info(f"Успешно прочитано {len(df)} транзакций из {filepath}")
        logger.info(f"Колонки в данных: {list(df.columns)}")

        # Конвертируем даты если они есть
        date_columns = [col for col in df.columns if 'дата' in col.lower() or 'date' in col.lower()]
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

        return df.to_dict('records')

    except Exception as e:
        logger.error(f"Ошибка загрузки данных из {filepath}: {e}")
        return []


def load_settings(settings_file: str = ".env") -> Dict[str, str]:
    """
    Р—Р°РіСЂСѓР¶Р°РµС‚ РЅР°СЃС‚СЂРѕР№РєРё РёР· С„Р°Р№Р»Р°.

    Аргументы:
        settings_file: Путь к файлу с настройками

    Возвращает:
        Словарь с настройками
    """
    try:
        settings = {}
        if os.path.exists(settings_file):
            with open(settings_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            settings[key.strip()] = value.strip()

        # Добавляем переменные окружения
        for key in ['API_KEY', 'EXCHANGE_API_KEY', 'STOCK_API_KEY']:
            env_value = os.getenv(key)
            if env_value:
                settings[key] = env_value

        logger.info(f"Загружено {len(settings)} настроек")
        return settings

    except Exception as e:
        logger.error(f"Ошибка загрузки настроек: {e}")
        return {}


def save_report(report_data: Dict[str, Any], filename_prefix: str) -> str:
    """
    Сохраняет отчет в JSON файл.

    Аргументы:
        report_data: Данные отчета
        filename_prefix: Префикс имени файла

    Возвращает:
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


def get_exchange_rates(currency_codes: List[str] = None) -> Dict[str, float]:
    """
    Получает курсы валют (заглушка).

    Аргументы:
        currency_codes: Список кодов валют

    Возвращает:
        Словарь с курсами валют
    """
    try:
        # Заглушка для демонстрации
        # В реальном приложении здесь будет API запрос
        rates = {
            "USD": 90.5,
            "EUR": 98.2,
            "GBP": 114.3,
        }

        if currency_codes:
            rates = {code: rates.get(code, 0) for code in currency_codes}

        logger.info(f"Получены курсы для {len(rates)} валют")
        return rates

    except Exception as e:
        logger.error(f"Ошибка получения курсов валют: {e}")
        return {}


def get_stock_prices(stock_symbols: List[str] = None) -> Dict[str, float]:
    """
    Получает цены акций (заглушка).

    Аргументы:
        stock_symbols: Список символов акций

    Возвращает:
        Словарь с ценами акций
    """
    try:
        # Заглушка для демонстрации
        # В реальном приложении здесь будет API запрос
        prices = {
            "AAPL": 185.2,
            "GOOGL": 142.5,
            "MSFT": 374.5,
            "TSLA": 240.1,
            "AMZN": 154.9,
        }

        if stock_symbols:
            prices = {symbol: prices.get(symbol, 0) for symbol in stock_symbols}

        logger.info(f"Получены цены для {len(prices)} акций")
        return prices

    except Exception as e:
        logger.error(f"Ошибка получения цен акций: {e}")
        return {}


def format_amount(amount: float, currency: str = "RUB") -> str:
    """
    Форматирует сумму для вывода.

    Аргументы:
        amount: Сумма
        currency: Валюта

    Возвращает:
        Отформатированная строка
    """
    return f"{amount:,.2f} {currency}".replace(",", " ").replace(".", ",")


def filter_by_date_range(
        transactions: List[Dict[str, Any]],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        date_column: str = "Р”Р°С‚Р° РѕРїРµСЂР°С†РёРё"
) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по диапазону дат.

    Аргументы:
        transactions: Список транзакций
        start_date: Начальная дата (YYYY-MM-DD)
        end_date: Конечная дата (YYYY-MM-DD)
        date_column: Название колонки с датой

    Возвращает:
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


def calculate_statistics(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Р Р°СЃСЃС‡РёС‚С‹РІР°РµС‚ Р±Р°Р·РѕРІСѓСЋ СЃС‚Р°С‚РёСЃС‚РёРєСѓ РїРѕ С‚СЂР°РЅР·Р°РєС†РёСЏРј.

    Аргументы:
        transactions: Список транзакций

    Возвращает:
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

        amounts = [t.get("РЎСѓРјРјР° РѕРїРµСЂР°С†РёРё", 0) for t in transactions]

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


def read_excel_file(file_path: str = "data/operations.xlsx") -> pd.DataFrame:
    """
    Читает Excel файл и возвращает DataFrame.

    Аргументы:
        file_path: Путь к Excel файлу

    Возвращает:
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




def load_transactions(file_path: str | Path) -> pd.DataFrame:
    """Загружает транзакции из Excel-файла."""
    try:
        path = Path(file_path).resolve()

        if os.getenv("TESTING") != "True" and not path.exists():
            raise FileNotFoundError(f"Файл {path} не найден")

        df = pd.read_excel(path)
        logger.info("Успешно загружены транзакции из %s", path)
        return df
    except Exception as e:
        logger.error("Ошибка загрузки транзакций: %s", str(e))
        raise


def get_greeting(time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    if 12 <= hour < 17:
        return "Добрый день"
    if 17 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def get_currency_rates(currencies: List[str] = None) -> List[Dict[str, Any]]:
    """Получает текущие курсы валют из API."""
    try:
        if os.getenv("TESTING") == "True":
            # Для тестов возвращаем заглушку
            default_currencies = currencies or ["USD", "EUR", "GBP"]
            return [{"currency": c, "rate": 1.0} for c in default_currencies]

        # Здесь должен быть реальный API запрос
        # Пока используем заглушку
        rates = {
            "USD": 90.5,
            "EUR": 98.2,
            "GBP": 114.3,
            "CNY": 12.5,
            "JPY": 0.61,
        }

        if currencies:
            rates = {c: rates.get(c, 0.0) for c in currencies}

        return [
            {
                "currency": currency,
                "rate": rate,
            }
            for currency, rate in rates.items()
        ]

    except Exception as e:
        logger.error(f"Ошибка получения курсов валют: {e}")
        return []


def get_stock_prices(stocks: List[str] = None) -> List[Dict[str, Any]]:
    """Получает текущие цены акций из API."""
    try:
        if os.getenv("TESTING") == "True":
            # Для тестов возвращаем заглушку
            default_stocks = stocks or ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
            return [{"stock": s, "price": 100.0} for s in default_stocks]

        # Здесь должен быть реальный API запрос
        # Пока используем заглушку
        prices = {
            "AAPL": 185.2,
            "GOOGL": 142.5,
            "MSFT": 374.5,
            "TSLA": 240.1,
            "AMZN": 154.9,
        }

        if stocks:
            prices = {symbol: prices.get(symbol, 0) for symbol in stocks}

        return [
            {
                "stock": stock,
                "price": price,
            }
            for stock, price in prices.items()
        ]

    except Exception as e:
        logger.error(f"Ошибка получения цен акций: {e}")
        return []


def analyze_expenses(df: pd.DataFrame) -> dict:
    """
    Анализирует расходы из DataFrame.

    Аргументы:
        df: DataFrame с транзакциями

    Возвращает:
        Словарь с анализом расходов
    """
    if df.empty:
        return {
            "total": 0,
            "main_categories": [],
            "other_categories": None,  # Важно: None, а не []
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
    
    Аргументы:
        df: DataFrame с транзакциями
        
    Возвращает:
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
    
    Аргументы:
        df: DataFrame с транзакциями
        
    Возвращает:
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
    
    Аргументы:
        df: DataFrame с транзакциями
        limit: Количество транзакций в топе
        
    Возвращает:
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
    
    Возвращает:
        Приветствие
    """
    from datetime import datetime
    
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_greeting(time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    if 12 <= hour < 17:
        return "Добрый день"
    if 17 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def get_currency_rates(currencies: List[str] = None) -> List[Dict[str, Any]]:
    """
    Получает текущие курсы валют (заглушка для тестов).

    Аргументы:
        currencies: Список кодов валют

    Возвращает:
        Список словарей с курсами валют
    """
    try:
        if os.getenv("TESTING") == "True":
            # Для тестов возвращаем заглушку
            default_currencies = currencies or ["USD", "EUR", "GBP"]
            return [{"currency": c, "rate": 1.0} for c in default_currencies]

        # Здесь должен быть реальный API запрос
        # Пока используем заглушку
        rates = {
            "USD": 90.5,
            "EUR": 98.2,
            "GBP": 114.3,
            "CNY": 12.5,
            "JPY": 0.61,
        }

        if currencies:
            rates = {c: rates.get(c, 0.0) for c in currencies}

        return [
            {
                "currency": currency,
                "rate": rate,
            }
            for currency, rate in rates.items()
        ]

    except Exception as e:
        logger.error(f"Ошибка получения курсов валют: {e}")
        return []

def load_transactions(file_path: str | Path) -> pd.DataFrame:
    """Загружает транзакции из Excel-файла."""
    try:
        path = Path(file_path).resolve()

        if os.getenv("TESTING") != "True" and not path.exists():
            raise FileNotFoundError(f"Файл {path} не найден")

        df = pd.read_excel(path)
        logger.info("Успешно загружены транзакции из %s", path)
        return df
    except Exception as e:
        logger.error("Ошибка загрузки транзакций: %s", str(e))
        raise
