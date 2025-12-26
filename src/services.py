"""
Модуль сервисов для анализа транзакций.
"""
import logging
import re
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


def analyze_cashback_categories(
    transactions: List[Dict[str, Any]], period: str
) -> List[Dict[str, Any]]:
    """
    Анализирует категории с наилучшим кешбэком.
    
    Args:
        transactions: Список транзакций
        period: Период анализа
        
    Returns:
        Список категорий с кешбэком
    """
    try:
        cashback_by_category = {}
        
        for transaction in transactions:
            category = transaction.get("Категория", "Без категории")
            cashback = transaction.get("Кешбэк", 0)
            
            if isinstance(cashback, (int, float)) and cashback > 0:
                cashback_by_category[category] = (
                    cashback_by_category.get(category, 0) + cashback
                )
        
        # Сортируем по убыванию кешбэка
        result = [
            {"category": category, "cashback": cashback}
            for category, cashback in sorted(
                cashback_by_category.items(),
                key=lambda x: x[1],
                reverse=True
            )
        ]
        
        logger.info(f"Проанализированы категории кешбэка за {period}")
        return result
        
    except Exception as e:
        logger.error(f"Ошибка анализа кешбэка: {e}")
        return []


def calculate_investment_piggybank(
    transactions: List[Dict[str, Any]]
) -> float:
    """
    Рассчитывает сумму инвесткопилки.
    
    Args:
        transactions: Список транзакций
        
    Returns:
        Сумма инвесткопилки
    """
    try:
        total = 0.0
        
        for transaction in transactions:
            rounding = transaction.get("Округление на «Инвесткопилку»", 0)
            if isinstance(rounding, (int, float)):
                total += float(rounding)
        
        logger.info(f"Рассчитана сумма инвесткопилки: {total:.2f}")
        return round(total, 2)
        
    except Exception as e:
        logger.error(f"Ошибка расчета инвесткопилки: {e}")
        return 0.0


def search_transactions(
    transactions: List[Dict[str, Any]], search_term: str
) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по ключевому слову.
    
    Args:
        transactions: Список транзакций
        search_term: Ключевое слово для поиска
        
    Returns:
        Найденные транзакции
    """
    try:
        if not search_term:
            return transactions
        
        search_term_lower = search_term.lower()
        result = []
        
        for transaction in transactions:
            description = str(transaction.get("Описание", "")).lower()
            if search_term_lower in description:
                result.append(transaction)
        
        logger.info(f"Найдено {len(result)} транзакций по запросу '{search_term}'")
        return result
        
    except Exception as e:
        logger.error(f"Ошибка поиска транзакций: {e}")
        return []


def find_phone_transactions(
    transactions: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Находит транзакции с телефонными номерами.
    
    Args:
        transactions: Список транзакций
        
    Returns:
        Транзакции с телефонными номерами
    """
    try:
        phone_pattern = r'\b(?:\+7|8|7)?[\s\-()]*\d{3}[\s\-()]*\d{3}[\s\-()]*\d{2}[\s\-()]*\d{2}\b'
        result = []
        
        for transaction in transactions:
            description = str(transaction.get("Описание", ""))
            if re.search(phone_pattern, description):
                result.append(transaction)
        
        logger.info(f"Найдено {len(result)} транзакций с телефонными номерами")
        return result
        
    except Exception as e:
        logger.error(f"Ошибка поиска телефонных номеров: {e}")
        return []


def find_personal_transfers(
    transactions: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Находит переводы физлицам.
    
    Args:
        transactions: Список транзакций
        
    Returns:
        Переводы физлицам
    """
    try:
        transfer_keywords = ["перевод", "перевел", "перевод физ", "перевод част", "иванов", "петров"]
        result = []
        
        for transaction in transactions:
            description = str(transaction.get("Описание", "")).lower()
            if any(keyword in description for keyword in transfer_keywords):
                result.append(transaction)
        
        logger.info(f"Найдено {len(result)} переводов физлицам")
        return result
        
    except Exception as e:
        logger.error(f"Ошибка поиска переводов физлицам: {e}")
        return []
