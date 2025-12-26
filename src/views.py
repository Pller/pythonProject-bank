import logging
from typing import Dict, Any
from src.utils import load_transactions

logger = logging.getLogger(__name__)


def home_page() -> Dict[str, Any]:
    """
    Генерирует данные для главной страницы.
    
    Returns:
        Словарь с данными для главной страницы
    """
    try:
        transactions = load_transactions()
        
        total_transactions = len(transactions)
        total_amount = sum(t.get("Сумма операции", 0) for t in transactions)
        unique_cards = len(set(t.get("Номер карты", "") for t in transactions))
        
        categories = {}
        for t in transactions:
            category = t.get("Категория", "Без категории")
            amount = t.get("Сумма операции", 0)
            categories[category] = categories.get(category, 0) + amount
        
        result = {
            "page": "Главная",
            "total_transactions": total_transactions,
            "total_amount": round(total_amount, 2),
            "unique_cards": unique_cards,
            "top_categories": dict(sorted(categories.items(),
                                          key=lambda x: x[1],
                                          reverse=True)[:5]),
            "status": "success",
        }
        
        logger.info("Сгенерирована главная страница")
        return result
        
    except Exception as e:
        logger.error(f"Ошибка генерации главной страницы: {e}")
        return {"page": "Главная", "error": str(e), "status": "error"}


def events_page(period: str = "M") -> Dict[str, Any]:
    """
    Генерирует данные для страницы событий.
    
    Args:
        period: Период (D - день, W - неделя, M - месяц)
    
    Returns:
        Словарь с данными для страницы событий
    """
    try:
        transactions = load_transactions()
        
        if period == "D":
            period_name = "день"
        elif period == "W":
            period_name = "неделя"
        else:
            period_name = "месяц"
        
        events_by_type = {}
        for t in transactions:
            event_type = t.get("Категория", "Другое")
            events_by_type[event_type] = events_by_type.get(event_type, 0) + 1
        
        total_events = len(transactions)
        result = {
            "page": "События",
            "period": period_name,
            "total_events": total_events,
            "events_by_type": events_by_type,
            "status": "success",
        }
        
        logger.info(f"Сгенерирована страница событий (период: {period})")
        return result
        
    except Exception as e:
        logger.error(f"Ошибка генерации страницы событий: {e}")
        return {"page": "События", "error": str(e), "status": "error"}
