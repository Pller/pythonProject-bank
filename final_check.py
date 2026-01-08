# final_check.py
from src.views import home_page
from datetime import datetime

print('=== ФИНАЛЬНАЯ ПРОВЕРКА ===')

# 1. Проверка функции
try:
    result = home_page('2024-01-01 14:30:00')
    print('✅ Функция home_page работает')
    print(f'   Статус: {result["status"]}')
    print(f'   Приветствие: {result["greeting"]}')
    print(f'   Карты: {len(result["cards"])}')
    print(f'   Топ транзакций: {len(result["top_transactions"])}')
    print(f'   Валюты: {len(result["currency_rates"])}')
    print(f'   Акции: {len(result["stock_prices"])}')
except Exception as e:
    print(f'❌ Ошибка: {e}')
    import traceback
    traceback.print_exc()

# 2. Проверка структуры
if 'result' in locals():
    print('\n=== ПРОВЕРКА СТРУКТУРЫ ===')
    required_fields = ['page', 'greeting', 'cards', 'top_transactions', 'currency_rates', 'stock_prices', 'status', 'generated_at']
    for field in required_fields:
        if field in result:
            print(f'   ✅ {field}')
        else:
            print(f'   ❌ {field} - отсутствует')

print('\n=== ГОТОВО К ЗАГРУЗКЕ НА GITHUB ===')
