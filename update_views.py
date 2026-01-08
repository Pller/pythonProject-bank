import re

print("Обновляем views.py...")

with open('src/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Новая функция home_page
new_home_page = '''
def home_page(date_str: str) -> Dict[str, Any]:
    """
    Генерирует данные для главной страницы.

    Args:
        date_str: Дата и время в формате "YYYY-MM-DD HH:MM:SS"

    Returns:
        JSON-ответ для главной страницы
    """
    try:
        # 1. Парсим дату и получаем приветствие
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        greeting = get_greeting(date)

        # 2. Загружаем транзакции
        transactions = read_excel_file(DATA_DIR / "operations.xlsx")

        # 3. Проверяем, что это DataFrame
        if not isinstance(transactions, pd.DataFrame):
            raise ValueError("Транзакции должны быть в формате DataFrame")

        # 4. Проверяем обязательные колонки
        required_columns = {"Дата операции", "Номер карты", "Сумма операции", "Кешбэк", "Категория", "Описание"}
        if not required_columns.issubset(transactions.columns):
            missing = required_columns - set(transactions.columns)
            raise ValueError(f"Отсутствуют обязательные колонки: {missing}")

        # 5. Фильтруем по текущему месяцу (используя дату из аргумента)
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
        current_month = date.replace(day=1)  # Используем дату из аргумента
        filtered = transactions[transactions["Дата операции"] >= current_month].copy()

        # 6. Данные по картам (как в примере)
        cards_data = []
        if "Номер карты" in filtered.columns:
            for card in filtered["Номер карты"].dropna().unique():
                card_str = str(card)
                last_digits = card_str[-4:] if len(card_str) > 4 else card_str
                card_trans = filtered[filtered["Номер карты"] == card]
                total_spent = card_trans["Сумма операции"].sum()
                cashback = card_trans["Кешбэк"].sum()
                cards_data.append(
                    {
                        "last_digits": last_digits,
                        "total_spent": round(float(total_spent), 2),
                        "cashback": round(float(cashback), 2),
                    }
                )

        # 7. Топ-5 транзакций (как в примере)
        top_trans_list = []
        if not filtered.empty:
            top_transactions = filtered.nlargest(5, "Сумма операции")
            top_trans_list = [
                {
                    "date": row["Дата операции"].strftime("%d.%m.%Y"),
                    "amount": round(row["Сумма операции"], 2),
                    "category": row["Категория"],
                    "description": row["Описание"],
                }
                for _, row in top_transactions.iterrows()
            ]

        # 8. Курс валют (загружаем из настроек пользователя)
        try:
            with open(Path(__file__).parent.parent / "user_settings.json", encoding="utf-8") as f:
                settings = json.load(f)
            user_currencies = settings.get("user_currencies", ["USD", "EUR", "GBP"])
            currency_rates = get_currency_rates(user_currencies)
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # Если нет настроек, используем дефолтные валюты
            currency_rates = get_currency_rates()

        # 9. Стоимость акций (загружаем из настроек пользователя)
        try:
            with open(Path(__file__).parent.parent / "user_settings.json", encoding="utf-8") as f:
                settings = json.load(f)
            user_stocks = settings.get("user_stocks", ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"])
            stock_prices = get_stock_prices(user_stocks)
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # Если нет настроек, используем дефолтные акции
            stock_prices = get_stock_prices()

        result = {
            "page": "home",
            "greeting": greeting,
            "cards": cards_data,
            "top_transactions": top_trans_list,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
            "status": "success",
            "generated_at": datetime.now().isoformat(),
        }

        logger.info("Сгенерирована главная страница")
        return result

    except Exception as e:
        logger.error(f"Ошибка генерации главной страницы: {e}")
        return {
            "page": "home",
            "error": str(e),
            "status": "error",
            "generated_at": datetime.now().isoformat(),
        }
'''

# Находим и заменяем старую функцию home_page
# Ищем от "def home_page" до "def events_page" или конца файла
import re

# Паттерн для поиска существующей функции home_page
pattern = re.compile(r'def home_page\(date_str: str\) -> Dict\[str, Any\]:.*?(?=\ndef events_page|\Z)', re.DOTALL)

if pattern.search(content):
    # Заменяем существующую функцию
    content = pattern.sub(new_home_page + '\n\ndef events_page', content)
    print("✅ Заменена существующая функция home_page")
else:
    # Если не нашли, добавляем новую
    print("❌ Не удалось найти функцию home_page для замены")
    # Попробуем другой подход - найдем конец импортов
    lines = content.split('\n')
    new_content = []
    in_home_page = False

    for line in lines:
        if line.strip().startswith('def home_page'):
            in_home_page = True
            new_content.append(new_home_page.strip())
        elif in_home_page and line.strip().startswith('def '):
            in_home_page = False
            new_content.append(line)
        elif not in_home_page:
            new_content.append(line)

    content = '\n'.join(new_content)
    print("✅ Вставлена новая функция home_page")

# Сохраняем обновленный файл
with open('src/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ views.py обновлен")
