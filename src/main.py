"""
Главный модуль приложения для анализа банковских транзакций.
"""
import logging
from src.utils import load_transactions
from src.services import (
    analyze_cashback_categories,
    calculate_investment_piggybank,
    search_transactions,
    find_phone_transactions,
    find_personal_transfers,
)
from src.reports import (
    generate_spending_by_category_report,
    generate_spending_by_weekday_report,
    generate_spending_by_workday_report,
)
from src.views import home_page, events_page

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Основная функция приложения."""
    print("Запуск приложения анализа банковских транзакций")
    
    try:
        # Загрузка данных
        print("Загрузка данных...")
        transactions = load_transactions()
        print(f"Загружено {len(transactions)} транзакций")
        
        # Демонстрация веб-страниц
        print("\nДемонстрация веб-страниц:")
        home_data = home_page()
        print(f"Главная страница: {home_data.get('total_transactions', 0)} транзакций, {len(home_data.get('cards', []))} карт")
        
        events_data = events_page("M")
        expenses_total = events_data.get("expenses", {}).get("total", 0)
        print(f"Страница событий: {events_data.get('total_events', 0)} событий, расходы: {expenses_total:.2f} руб.")
        
        # Демонстрация сервисов
        print("\nДемонстрация сервисов:")
        cashback_categories = analyze_cashback_categories(transactions, "1/2024")
        print(f"Выгодные категории кешбэка: {len(cashback_categories)} категорий")
        
        piggybank = calculate_investment_piggybank(transactions)
        print(f"Инвесткопилка: {piggybank} руб.")
        
        search_results = search_transactions(transactions, "магазин")
        print(f"Простой поиск: найдено {len(search_results)} транзакций")
        
        phone_transactions = find_phone_transactions(transactions)
        print(f"Поиск по телефонам: найдено {len(phone_transactions)} транзакций")
        
        personal_transfers = find_personal_transfers(transactions)
        print(f"Переводы физлицам: найдено {len(personal_transfers)} транзакций")
        
        # Демонстрация отчетов
        print("\nДемонстрация отчетов:")
        category_report = generate_spending_by_category_report(
            transactions, "Супермаркеты"
        )
        print(f"Отчет по категории: {len(category_report.get('months', []))} месяцев")
        
        weekday_report = generate_spending_by_weekday_report(transactions)
        print(f"Отчет по дням недели: {len(weekday_report.get('days', []))} дней")
        
        workday_report = generate_spending_by_workday_report(transactions)
        print(f"Отчет по типам дней: {len(workday_report.get('categories', []))} категорий")
        
        print("\nВсе функции успешно выполнены!")
        print("Отчеты сохранены в файлы с префиксом 'report_'")
        
    except Exception as e:
        logger.error(f"Ошибка в работе приложения: {e}")
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
