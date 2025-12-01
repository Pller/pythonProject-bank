"""Модуль сервисов для анализа транзакций."""

import logging
import re
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def profitable_cashback_categories(data: List[Dict[str, Any]], year: int, month: int) -> Dict[str, float]:
    """Анализирует выгодные категории для повышенного кешбэка."""
    try:
        category_cashback = defaultdict(float)

        for transaction in data:
            # Проверяем дату операции
            op_date = transaction.get("Дата операции")
            if not op_date:
                continue

            if isinstance(op_date, str):
                try:
                    op_date = datetime.strptime(op_date, "%Y-%m-%d")
                except ValueError:
                    continue

            if op_date.year == year and op_date.month == month:
                category = transaction.get("Категория", "Другое")
                amount = abs(transaction.get("Сумма операции", 0))

                # Предполагаем повышенный кешбэк 5%
                cashback = amount * 0.05
                category_cashback[category] += cashback

        # Округляем значения
        result = {category: round(cashback, 2) for category, cashback in category_cashback.items()}

        logger.info(f"Проанализированы категории кешбэка за {month}/{year}")
        return result

    except Exception as e:
        logger.error(f"Ошибка анализа категорий кешбэка: {e}")
        return {}


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Рассчитывает сумму для инвесткопилки через округление трат."""
    try:
        total_investment = 0.0

        for transaction in transactions:
            # Проверяем дату операции
            op_date = transaction.get("Дата операции")
            if not op_date:
                continue

            if isinstance(op_date, str):
                try:
                    op_date = datetime.strptime(op_date, "%Y-%m-%d")
                except ValueError:
                    continue

            # Проверяем что транзакция в нужном месяце
            if op_date.strftime("%Y-%m") == month:
                amount = transaction.get("Сумма операции", 0)

                # Округляем только расходы (отрицательные суммы)
                if amount < 0:
                    rounded_amount = _round_to_limit(abs(amount), limit)
                    investment = rounded_amount - abs(amount)
                    total_investment += investment

        logger.info(f"Рассчитана сумма инвесткопилки: {total_investment:.2f}")
        return round(total_investment, 2)

    except Exception as e:
        logger.error(f"Ошибка расчета инвесткопилки: {e}")
        return 0.0


def _round_to_limit(amount: float, limit: int) -> float:
    """Округляет сумму до ближайшего кратного limit."""
    return ((amount + limit - 1) // limit) * limit


def simple_search(transactions: List[Dict[str, Any]], search_query: str) -> List[Dict[str, Any]]:
    """Простой поиск транзакций по описанию или категории."""
    try:
        query_lower = search_query.lower()
        results = []

        for transaction in transactions:
            description = transaction.get("Описание", "").lower()
            category = transaction.get("Категория", "").lower()

            if query_lower in description or query_lower in category:
                results.append(transaction)

        logger.info(f"Найдено {len(results)} транзакций по запросу '{search_query}'")
        return results

    except Exception as e:
        logger.error(f"Ошибка простого поиска: {e}")
        return []


def search_by_phone_numbers(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Ищет транзакции с телефонными номерами в описании."""
    try:
        # Регулярное выражение для российских телефонных номеров
        phone_pattern = r"(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}"

        results = []
        for transaction in transactions:
            description = transaction.get("Описание", "")

            if re.search(phone_pattern, description):
                results.append(transaction)

        logger.info(f"Найдено {len(results)} транзакций с телефонными номерами")
        return results

    except Exception as e:
        logger.error(f"Ошибка поиска по телефонным номерам: {e}")
        return []


def search_person_transfers(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Ищет переводы физическим лицам."""
    try:
        # Паттерн для имени и фамилии с точкой
        name_pattern = r"[А-Я][а-я]+\s[А-Я]\."

        results = []
        for transaction in transactions:
            category = transaction.get("Категория", "")
            description = transaction.get("Описание", "")

            if category == "Переводы" and re.search(name_pattern, description):
                results.append(transaction)

        logger.info(f"Найдено {len(results)} переводов физлицам")
        return results

    except Exception as e:
        logger.error(f"Ошибка поиска переводов физлицам: {e}")
        return []
