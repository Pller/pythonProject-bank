from src.views import home_page
import traceback

try:
    result = home_page('2024-01-01 10:30:00')
    print('✅ home_page выполнена успешно')
    print(f"Статус: {result['status']}")
    print(f"Приветствие: {result['greeting']}")
    print(f"Карт проанализировано: {len(result['cards'])}")
    print(f"Топ транзакций: {len(result['top_transactions'])}")
except Exception as e:
    print(f'❌ Ошибка: {e}')
    traceback.print_exc()
