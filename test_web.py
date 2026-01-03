print("=== Тест веб-функций ===")

from src.views import home_page, events_page

print("\n1. Тест home_page():")
home_data = home_page()
print(f"   Статус: {home_data.get('status')}")
print(f"   Приветствие: {home_data.get('greeting')}")
print(f"   Карты: {len(home_data.get('cards', []))}")
print(f"   Топ транзакций: {len(home_data.get('top_transactions', []))}")
print(f"   Курсы валют: {list(home_data.get('exchange_rates', {}).keys())}")
print(f"   Акции: {list(home_data.get('stock_prices', {}).keys())}")

print("\n2. Тест events_page():")
events_data = events_page("M")
print(f"   Статус: {events_data.get('status')}")
print(f"   Период: {events_data.get('period')}")

expenses = events_data.get("expenses", {})
print(f"   Общие расходы: {expenses.get('total', 0)}")

main_expenses = expenses.get("main", {})
print(f"   Основные расходы: {len(main_expenses.get('top', []))} категорий")

transfers = expenses.get("transfers_cash", [])
print(f"   Переводы/наличные: {len(transfers)}")

incomes = events_data.get("incomes", {})
print(f"   Поступления: {incomes.get('total', 0)}")

print("\n✅ Тест завершен!")
