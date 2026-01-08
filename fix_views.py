import os

print("Исправляем views.py...")

with open('src/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Находим функцию events_page и исправляем ее
# Нужно добавить обработку случая когда other_categories отсутствует

# Заменим часть кода где используется other_categories
new_content = content.replace(
    '''        result = {
            "page": "events",
            "period": period_name,
            "expenses": {
                "total": expenses_analysis["total"],
                "main": {
                    "categories": expenses_analysis["main_categories"],
                    "other": expenses_analysis["other_categories"],
                },
                "transfers_cash": expenses_analysis["transfers_cash"],
            },
            "incomes": {
                "total": incomes_analysis["total"],
                "main_categories": incomes_analysis["main_categories"],
            },
            "exchange_rates": exchange_rates,
            "stock_prices": stock_prices,
            "status": "success",
            "generated_at": datetime.now().isoformat(),
        }''',
    '''        # Собираем результат с проверкой наличия other_categories
        expenses_main = {
            "categories": expenses_analysis["main_categories"],
        }

        # Добавляем other только если он есть
        if "other_categories" in expenses_analysis and expenses_analysis["other_categories"] is not None:
            expenses_main["other"] = expenses_analysis["other_categories"]

        result = {
            "page": "events",
            "period": period_name,
            "expenses": {
                "total": expenses_analysis["total"],
                "main": expenses_main,
                "transfers_cash": expenses_analysis["transfers_cash"],
            },
            "incomes": {
                "total": incomes_analysis["total"],
                "main_categories": incomes_analysis["main_categories"],
            },
            "exchange_rates": exchange_rates,
            "stock_prices": stock_prices,
            "status": "success",
            "generated_at": datetime.now().isoformat(),
        }'''
)

with open('src/views.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ views.py исправлен")
