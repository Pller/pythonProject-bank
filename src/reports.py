"""
Модуль для генерации отчетов.
"""
import logging
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from src.utils import save_report

logger = logging.getLogger(__name__)


def generate_spending_by_category_report(
    transactions: List[Dict[str, Any]], category: str
) -> Dict[str, Any]:
    """Генерирует отчет по категории."""
    try:
        df = pd.DataFrame(transactions)
        if df.empty:
            return {"category": category, "months": [], "total": 0}
        
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")
        df["month"] = df["Дата операции"].dt.to_period("M")
        
        category_df = df[df["Категория"] == category]
        
        monthly_data = []
        total = 0
        
        for month, group in category_df.groupby("month"):
            month_total = group["Сумма операции"].sum()
            monthly_data.append({
                "month": str(month),
                "amount": float(month_total),
                "count": len(group)
            })
            total += month_total
        
        report = {
            "category": category,
            "months": monthly_data,
            "total": float(total),
            "generated_at": datetime.now().isoformat()
        }
        
        save_report(report, "report_spending_by_category")
        logger.info(f"Сгенерирован отчет по категории '{category}'")
        return report
        
    except Exception as e:
        logger.error(f"Ошибка генерации отчета по категории: {e}")
        return {"category": category, "error": str(e)}


def generate_spending_by_weekday_report(
    transactions: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Генерирует отчет по дням недели."""
    try:
        df = pd.DataFrame(transactions)
        if df.empty:
            return {"days": [], "total": 0}
        
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")
        df["weekday"] = df["Дата операции"].dt.day_name()
        
        weekdays_order = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                         "Friday", "Saturday", "Sunday"]
        
        daily_data = []
        total = 0
        
        for day in weekdays_order:
            day_df = df[df["weekday"] == day]
            day_total = day_df["Сумма операции"].sum()
            daily_data.append({
                "day": day,
                "amount": float(day_total),
                "count": len(day_df)
            })
            total += day_total
        
        report = {
            "days": daily_data,
            "total": float(total),
            "generated_at": datetime.now().isoformat()
        }
        
        save_report(report, "report_spending_by_weekday")
        logger.info("Сгенерирован отчет по дням недели")
        return report
        
    except Exception as e:
        logger.error(f"Ошибка генерации отчета по дням недели: {e}")
        return {"error": str(e)}


def generate_spending_by_workday_report(
    transactions: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Генерирует отчет по рабочим/выходным дням."""
    try:
        df = pd.DataFrame(transactions)
        if df.empty:
            return {"categories": [], "total": 0}
        
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")
        df["weekday"] = df["Дата операции"].dt.dayofweek
        df["day_type"] = df["weekday"].apply(
            lambda x: "Рабочий день" if x < 5 else "Выходной"
        )
        
        categories_data = []
        total = 0
        
        for day_type in ["Рабочий день", "Выходной"]:
            type_df = df[df["day_type"] == day_type]
            type_total = type_df["Сумма операции"].sum()
            categories_data.append({
                "category": day_type,
                "amount": float(type_total),
                "count": len(type_df)
            })
            total += type_total
        
        report = {
            "categories": categories_data,
            "total": float(total),
            "generated_at": datetime.now().isoformat()
        }
        
        save_report(report, "report_spending_by_workday")
        logger.info("Сгенерирован отчет по рабочим/выходным дням")
        return report
        
    except Exception as e:
        logger.error(f"Ошибка генерации отчета по типам дней: {e}")
        return {"error": str(e)}
