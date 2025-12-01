"""Модуль для генерации отчетов."""

import logging
from datetime import datetime, timedelta
from functools import wraps

import pandas as pd

logger = logging.getLogger(__name__)


def report_decorator(filename=None):
    """Декоратор для сохранения результатов отчетов в файл."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if filename is None:
                report_filename = f"report_{func.__name__}_" f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            else:
                report_filename = filename

            try:
                if isinstance(result, pd.DataFrame):
                    result.to_json(report_filename, orient="records", force_ascii=False, indent=2)
                else:
                    import json

                    with open(report_filename, "w", encoding="utf-8") as f:
                        json.dump(result, f, ensure_ascii=False, indent=2)

                logger.info(f"Отчет сохранен в файл: {report_filename}")
            except Exception as e:
                logger.error(f"Ошибка сохранения отчета: {e}")

            return result

        return wrapper

    return decorator


@report_decorator()
def spending_by_category(transactions, category, date=None):
    """Анализирует траты по категории за последние 3 месяца."""
    try:
        if date is None:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(date, "%Y-%m-%d")

        start_date = end_date - timedelta(days=90)

        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
        mask = (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= end_date)
        filtered_data = transactions[mask]

        category_data = filtered_data[filtered_data["Категория"] == category]

        category_data = category_data.copy()
        category_data["month"] = category_data["Дата операции"].dt.to_period("M")

        expenses = category_data[category_data["Сумма операции"] < 0].copy()
        expenses["Сумма операции"] = expenses["Сумма операции"].abs()

        monthly_spending = expenses.groupby("month")["Сумма операции"].sum().reset_index()
        monthly_spending["month"] = monthly_spending["month"].astype(str)

        logger.info(f"Сгенерирован отчет по категории '{category}'")
        return monthly_spending

    except Exception as e:
        logger.error(f"Ошибка генерации отчета по категории: {e}")
        return pd.DataFrame()


@report_decorator()
def spending_by_weekday(transactions, date=None):
    """Анализирует средние траты по дням недели."""
    try:
        if date is None:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(date, "%Y-%m-%d")

        start_date = end_date - timedelta(days=90)

        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
        mask = (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= end_date)
        filtered_data = transactions[mask]

        expenses = filtered_data[filtered_data["Сумма операции"] < 0].copy()
        expenses["Сумма операции"] = expenses["Сумма операции"].abs()

        expenses["weekday"] = expenses["Дата операции"].dt.day_name()

        weekday_spending = expenses.groupby("weekday")["Сумма операции"].mean().round(2).reset_index()

        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday_spending["weekday"] = pd.Categorical(
            weekday_spending["weekday"], categories=weekday_order, ordered=True
        )
        weekday_spending = weekday_spending.sort_values("weekday")

        logger.info("Сгенерирован отчет по дням недели")
        return weekday_spending

    except Exception as e:
        logger.error(f"Ошибка генерации отчета по дням недели: {e}")
        return pd.DataFrame()


@report_decorator()
def spending_by_workday(transactions, date=None):
    """Анализирует средние траты в рабочие и выходные дни."""
    try:
        if date is None:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(date, "%Y-%m-%d")

        start_date = end_date - timedelta(days=90)

        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
        mask = (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= end_date)
        filtered_data = transactions[mask]

        expenses = filtered_data[filtered_data["Сумма операции"] < 0].copy()
        expenses["Сумма операции"] = expenses["Сумма операции"].abs()

        expenses["is_weekend"] = expenses["Дата операции"].dt.weekday >= 5

        day_type_spending = expenses.groupby("is_weekend")["Сумма операции"].mean().round(2).reset_index()
        day_type_spending["day_type"] = day_type_spending["is_weekend"].map({True: "Выходной", False: "Рабочий"})
        day_type_spending = day_type_spending[["day_type", "Сумма операции"]]

        logger.info("Сгенерирован отчет по рабочим/выходным дням")
        return day_type_spending

    except Exception as e:
        logger.error(f"Ошибка генерации отчета по типам дней: {e}")
        return pd.DataFrame()
