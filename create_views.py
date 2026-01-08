views_content = '''"""
Модуль для генерации веб-страниц.
Все вспомогательные функции вынесены в utils.py.
"""
import logging
from datetime import datetime
from typing import Dict, Any
import pandas as pd
from src.utils import (
    get_exchange_rates,
    get_stock_prices,
    analyze_expenses,
    analyze_incomes,
    analyze_cards,
    get_top_transactions,
    get_time_based_greeting,
)

logger = logging.getLogger(__name__)


def home_page(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Генерирует данные для главной страницы.

    Args:
        df: DataFrame с транзакциями

    Returns:
        JSON-ответ для главной страницы
    """
    try:
        # 1. Приветствие
        greeting = get_time_based_greeting()

        # 2. Данные по картам
        cards_data = analyze_cards(df)

        # 3. Топ-5 транзакций по сумме платежа
        top_transactions = get_top_transactions(df, 5)

        # 4. Курс валют
        exchange_rates = get_exchange_rates()

        # 5. Стоимость акций из S&P500
        stock_prices = get_stock_prices()

        result = {
            "page": "home",
            "greeting": greeting,
            "cards": cards_data,
            "top_transactions": top_transactions,
            "exchange_rates": exchange_rates,
            "stock_prices": stock_prices,
            "status": "success",
            "generated_at": datetime.now().isoformat(),
        }

        logger.info("Сгенерирована главная страница")
        return result

    except Exception as e:
        logger.error(f"Ошибка генерации главной страницы: {e}")
        return {
            "page": "home",
            "error": str(e),
            "status": "error",
            "generated_at": datetime.now().isoformat(),
        }


def events_page(df: pd.DataFrame, period: str = "M") -> Dict[str, Any]:
    """
    Генерирует данные для страницы событий.

    Args:
        df: DataFrame с транзакциями
        period: Период (D - день, W - неделя, M - месяц)

    Returns:
        JSON-ответ для страницы событий
    """
    try:
        # Определяем период (используется для фильтрации, если нужно)
        period_names = {"D": "день", "W": "неделя", "M": "месяц"}
        period_name = period_names.get(period, "месяц")

        # 1. Анализ расходов
        expenses_analysis = analyze_expenses(df)

        # 2. Анализ поступлений
        incomes_analysis = analyze_incomes(df)

        # 3. Курс валют
        exchange_rates = get_exchange_rates()

        # 4. Стоимость акций из S&P500
        stock_prices = get_stock_prices()

        # Собираем результат с проверкой наличия other_categories
        expenses_main = {
            "categories": expenses_analysis["main_categories"],
        }

        # Добавляем other только если он есть и не None
        if "other_categories" in expenses_analysis and expenses_analysis["other_categories"] is not None:
            expenses_main["other"] = expenses_analysis["other_categories"]

        result = {
            "page": "events",
            "period": period_name,
            "expenses": {
                "total": expenses_analysis["total"],
                "main": expenses_main,
                "transfers_cash": expenses_analysis["transfers_cash"],
            },
            "incomes": {
                "total": incomes_analysis["total"],
                "main_categories": incomes_analysis["main_categories"],
            },
            "exchange_rates": exchange_rates,
            "stock_prices": stock_prices,
            "status": "success",
            "generated_at": datetime.now().isoformat(),
        }

        logger.info(f"Сгенерирована страница событий (период: {period})")
        return result

    except Exception as e:
        logger.error(f"Ошибка генерации страницы событий: {e}")
        return {
            "page": "events",
            "error": str(e),
            "status": "error",
            "generated_at": datetime.now().isoformat(),
        }
'''

with open('src/views.py', 'w', encoding='utf-8') as f:
    f.write(views_content)

print("✅ views.py переписан")
