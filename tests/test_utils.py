"""
Тесты для модуля utils.py
"""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.utils import (
    get_exchange_rates,
    get_stock_prices,
    analyze_expenses,
    analyze_incomes,
    analyze_cards,
    get_top_transactions,
    get_time_based_greeting,
)


class TestExchangeRates:
    """Тесты для функции get_exchange_rates"""

    @patch('src.utils.requests.get')
    def test_get_exchange_rates_success(self, mock_get):
        """Тест успешного получения курсов валют"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 90.5},
                "EUR": {"Value": 98.2},
                "GBP": {"Value": 114.3},
            }
        }
        mock_get.return_value = mock_response

        rates = get_exchange_rates()

        assert isinstance(rates, dict)
        assert "USD" in rates
        assert "EUR" in rates
        assert "GBP" in rates
        assert rates["USD"] == 90.5
        assert rates["EUR"] == 98.2
        assert rates["GBP"] == 114.3

    @patch('src.utils.requests.get')
    def test_get_exchange_rates_fallback(self, mock_get):
        """Тест возврата заглушек при ошибке"""
        mock_get.side_effect = Exception("Network error")

        rates = get_exchange_rates()

        assert isinstance(rates, dict)
        assert "USD" in rates
        assert rates["USD"] == 90.5  # Значение из заглушки


class TestStockPrices:
    """Тесты для функции get_stock_prices"""

    @patch('src.utils.requests.get')
    def test_get_stock_prices_success(self, mock_get):
        """Тест успешного получения цен акций"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "chart": {
                "result": [{
                    "meta": {"regularMarketPrice": 185.2}
                }]
            }
        }
        mock_get.return_value = mock_response

        prices = get_stock_prices()

        assert isinstance(prices, dict)
        assert len(prices) > 0
        assert "AAPL" in prices
        assert isinstance(prices["AAPL"], float)


class TestAnalyzeExpenses:
    """Тесты для функции analyze_expenses"""

    def test_analyze_expenses_empty(self):
        """Тест с пустым DataFrame"""
        df = pd.DataFrame()
        result = analyze_expenses(df)

        assert result["total"] == 0
        assert result["main_categories"] == []
        assert result["other_categories"] is None
        assert result["transfers_cash"] == []

    def test_analyze_expenses_with_data(self):
        """Тест с данными"""
        data = {
            "Сумма операции": [1000, 500, 300, 200, 150, 100, 80, 60, 40, 20],
            "Категория": ["Супермаркеты", "Транспорт", "Рестораны", "Развлечения",
                          "Одежда", "Техника", "Книги", "Спорт", "Красота", "Другое"]
        }
        df = pd.DataFrame(data)

        result = analyze_expenses(df)

        assert result["total"] == 2450
        assert len(result["main_categories"]) == 7  # Топ-7 категорий
        assert "other_categories" in result
        assert isinstance(result["transfers_cash"], list)


class TestAnalyzeIncomes:
    """Тесты для функции analyze_incomes"""

    def test_analyze_incomes_empty(self):
        """Тест с пустым DataFrame"""
        df = pd.DataFrame()
        result = analyze_incomes(df)

        assert result["total"] == 0
        assert result["main_categories"] == []

    def test_analyze_incomes_with_negative(self):
        """Тест с отрицательными суммами (доходы)"""
        data = {
            "Сумма операции": [-2000, -1500, -1000],
            "Категория": ["Зарплата", "Бонус", "Проценты"]
        }
        df = pd.DataFrame(data)

        result = analyze_incomes(df)

        assert result["total"] == 4500  # Абсолютные значения
        assert len(result["main_categories"]) == 3


class TestAnalyzeCards:
    """Тесты для функции analyze_cards"""

    def test_analyze_cards_empty(self):
        """Тест с пустым DataFrame"""
        df = pd.DataFrame()
        result = analyze_cards(df)

        assert result == []

    def test_analyze_cards_with_data(self):
        """Тест с данными по картам"""
        data = {
            "Номер карты": ["1234567812345678", "1234567812345678", "8765432187654321"],
            "Сумма операции": [1000, 500, 1500],
            "Кешбэк": [10, 5, 15]
        }
        df = pd.DataFrame(data)

        result = analyze_cards(df)

        assert len(result) == 2  # 2 уникальные карты
        for card in result:
            assert "card_last_four" in card
            assert "total_spent" in card
            assert "total_cashback" in card


class TestTopTransactions:
    """Тесты для функции get_top_transactions"""

    def test_get_top_transactions_empty(self):
        """Тест с пустым DataFrame"""
        df = pd.DataFrame()
        result = get_top_transactions(df)

        assert result == []

    def test_get_top_transactions_limit(self):
        """Тест ограничения количества транзакций"""
        data = {
            "Сумма платежа": [100, 200, 300, 400, 500, 600],
            "Описание": ["Транзакция"] * 6,
            "Категория": ["Категория"] * 6,
            "Дата операции": ["2024-01-01"] * 6
        }
        df = pd.DataFrame(data)

        result = get_top_transactions(df, limit=3)

        assert len(result) == 3
        # Проверяем что суммы отсортированы по убыванию
        amounts = [t["amount"] for t in result]
        assert amounts == [600, 500, 400]


class TestTimeGreeting:
    """Тесты для функции get_time_based_greeting"""

    @patch('src.utils.datetime')
    def test_morning_greeting(self, mock_datetime):
        """Тест приветствия для утра"""
        mock_now = MagicMock()
        mock_now.hour = 8
        mock_datetime.now.return_value = mock_now

        greeting = get_time_based_greeting()
        assert greeting == "Доброе утро"

    @patch('src.utils.datetime')
    def test_night_greeting(self, mock_datetime):
        """Тест приветствия для ночи"""
        mock_now = MagicMock()
        mock_now.hour = 2
        mock_datetime.now.return_value = mock_now

        greeting = get_time_based_greeting()
        assert greeting == "Доброй ночи"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
