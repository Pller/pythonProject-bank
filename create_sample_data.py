"""Скрипт для создания тестовых данных."""
import pandas as pd
from datetime import datetime, timedelta
import random

# Создаем тестовые данные
categories = ['Супермаркеты', 'Транспорт', 'Рестораны', 'Одежда', 'Развлечения', 'Медицина', 'Переводы']
descriptions = {
    'Супермаркеты': ['Пятерочка', 'Магнит', 'Перекресток', 'Ашан'],
    'Транспорт': ['Такси', 'Метро', 'Автобус', 'Заправка'],
    'Рестораны': ['Макдональдс', 'KFC', 'Суши', 'Пицца'],
    'Переводы': ['Перевод Иванов И.', 'Перевод Петров П.', 'Перевод Сидоров С.']
}

data = []
start_date = datetime(2024, 1, 1)

for i in range(1000):
    date = start_date + timedelta(days=random.randint(0, 90))
    category = random.choice(categories)
    amount = -random.uniform(50, 5000)  # Отрицательные суммы - расходы
    
    if random.random() < 0.1:  # 10% транзакций - пополнения
        amount = abs(amount)
        category = 'Пополнение'
    
    description = random.choice(descriptions.get(category, ['Покупка']))
    
    # Добавляем телефонные номера в некоторые описания
    if random.random() < 0.05:
        phone = f"+7 {random.randint(900, 999)} {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        description += f" {phone}"
    
    data.append({
        'Дата операции': date,
        'Дата платежа': date + timedelta(days=random.randint(1, 5)),
        'Номер карты': f"{random.randint(1000, 9999)}",
        'Статус': 'OK' if random.random() > 0.05 else 'FAILED',
        'Сумма операции': round(amount, 2),
        'Валюта операции': 'RUB',
        'Сумма платежа': round(amount, 2),
        'Валюта платежа': 'RUB',
        'Кешбэк': round(abs(amount) * 0.01, 2) if amount < 0 else 0,
        'Категория': category,
        'MCC': random.randint(1000, 9999),
        'Описание': description,
        'Бонусы (включая кешбэк)': round(abs(amount) * 0.01, 2) if amount < 0 else 0,
        'Округление на «Инвесткопилку»': 0,
        'Сумма операции с округлением': round(amount, 2)
    })

# Создаем DataFrame
df = pd.DataFrame(data)

# Сохраняем в Excel
df.to_excel('data/operations.xlsx', index=False)
print("Тестовые данные созданы в data/operations.xlsx")
print(f"Создано {len(df)} транзакций")
