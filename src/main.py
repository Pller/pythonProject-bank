"""Основной модуль приложения."""

import logging

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
from src.services import (
    investment_bank,
    profitable_cashback_categories,
    search_by_phone_numbers,
    search_person_transfers,
    simple_search,
)
from src.utils import read_excel_file
from src.views import events_page, home_page

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log", encoding="utf-8"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def check_data_structure(df):
    """Проверяет структуру данных."""
    print("Структура данных:")
    print(f"  Всего строк: {len(df)}")
    print(f"  Колонки: {list(df.columns)}")
    print(f"  Период: {df['Дата операции'].min()} - {df['Дата операции'].max()}")


def main():
    """Основная функция приложения."""
    try:
        print("Запуск приложения анализа банковских транзакций")

        # Загружаем данные
        print("Загрузка данных...")
        df = read_excel_file("data/operations.xlsx")

        if df.empty:
            print("Не удалось загрузить данные")
            return

        check_data_structure(df)
        print(f"Загружено {len(df)} транзакций")

        # Демонстрация функциональности
        print("Демонстрация веб-страниц:")

        # Главная страница
        home_response = home_page("2024-01-15 14:30:00")
        print(f"Главная страница: {len(home_response.get('cards', []))} карт")

        # Страница событий
        events_response = events_page("2024-01-15 14:30:00", "M")
        expenses_total = events_response.get("expenses", {}).get("total_amount", 0)
        print(f"Страница событий: расходы {expenses_total} руб.")

        # Сервисы
        print("Демонстрация сервисов:")
        transactions_list = df.to_dict("records")

        cashback_categories = profitable_cashback_categories(transactions_list, 2024, 1)
        print(f"Выгодные категории кешбэка: {len(cashback_categories)} категорий")

        investment = investment_bank("2024-01", transactions_list, 50)
        print(f"Инвесткопилка: {investment} руб.")

        search_results = simple_search(transactions_list, "магазин")
        print(f"Простой поиск: найдено {len(search_results)} транзакций")

        phone_transactions = search_by_phone_numbers(transactions_list)
        print(f"Поиск по телефонам: найдено {len(phone_transactions)} транзакций")

        person_transfers = search_person_transfers(transactions_list)
        print(f"Переводы физлицам: найдено {len(person_transfers)} транзакций")

        # Отчеты
        print("Демонстрация отчетов:")

        category_report = spending_by_category(df, "Супермаркеты")
        print(f"Отчет по категории: {len(category_report)} месяцев")

        weekday_report = spending_by_weekday(df)
        print(f"Отчет по дням недели: {len(weekday_report)} дней")

        workday_report = spending_by_workday(df)
        print(f"Отчет по типам дней: {len(workday_report)} категорий")

        print("Все функции успешно выполнены!")
        print("Отчеты сохранены в файлы с префиксом 'report_'")

    except Exception as e:
        logger.error(f"Ошибка в основном модуле: {e}")
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
