"""
Тесты для модуля views с DataFrame на входе.
"""
import pytest
from unittest.mock import patch
import pandas as pd
from src.views import home_page, events_page


@pytest.fixture
def sample_dataframe():
    """Фикстура с тестовым DataFrame."""
    data = {
        "Номер карты": ["1234567812345678", "8765432187654321", "1234567812345678"],
        "Сумма операции": [1500.0, 3000.0, 2000.0],
        "Кешбэк": [15.0, 30.0, 20.0],
        "Сумма платежа": [1500.0, 3000.0, 2000.0],
        "Описание": ["Покупка в магазине", "Оплата услуг", "Транспорт"],
        "Категория": ["Супермаркеты", "Услуги", "Транспорт"],
        "Дата операции": ["2024-01-01", "2024-01-02", "2024-01-03"],
    }
    return pd.DataFrame(data)


class TestHomePage:
    """Тесты для функции home_page."""

    @patch("src.views.get_exchange_rates")  # Исправлено: было get_currency_rates
    @patch("src.views.get_stock_prices")
    def test_home_page_structure(self, mock_stocks, mock_rates, sample_dataframe):
        """Тест структуры данных главной страницы."""
        mock_rates.return_value = {"USD": 90.5, "EUR": 98.2}
        mock_stocks.return_value = {"AAPL": 185.2, "GOOGL": 142.5}

        result = home_page(sample_dataframe)

        # Проверяем структуру
        assert result["page"] == "home"
        assert result["status"] == "success"
        assert "greeting" in result
        assert "cards" in result
        assert "top_transactions" in result
        assert "exchange_rates" in result
        assert "stock_prices" in result
        assert "generated_at" in result

        # Проверяем данные карт
        assert len(result["cards"]) == 2  # 2 уникальные карты

        # Проверяем топ транзакций
        assert len(result["top_transactions"]) <= 5

    @patch("src.views.get_exchange_rates")  # Исправлено: было get_currency_rates
    @patch("src.views.get_stock_prices")
    def test_home_page_empty_dataframe(self, mock_stocks, mock_rates):
        """Тест с пустым DataFrame."""
        mock_rates.return_value = {"USD": 90.5, "EUR": 98.2}
        mock_stocks.return_value = {"AAPL": 185.2, "GOOGL": 142.5}

        empty_df = pd.DataFrame()

        result = home_page(empty_df)

        assert result["page"] == "home"
        assert result["status"] == "success"
        assert result["cards"] == []
        assert result["top_transactions"] == []


class TestEventsPage:
    """Тесты для функции events_page."""

    @patch("src.views.get_exchange_rates")  # Исправлено: было get_currency_rates
    @patch("src.views.get_stock_prices")
    def test_events_page_structure(self, mock_stocks, mock_rates):
        """Тест структуры данных страницы событий."""
        # Создаем DataFrame с расходами и доходами
        data = {
            "Сумма операции": [1000.0, 500.0, -2000.0, 300.0],
            "Категория": ["Супермаркеты", "Транспорт", "Зарплата", "Переводы"],
            "Описание": ["Продукты", "Такси", "Начисление", "Перевод другу"],
        }
        df = pd.DataFrame(data)

        mock_rates.return_value = {"USD": 90.5}
        mock_stocks.return_value = {"AAPL": 185.2}

        result = events_page(df, "M")

        # Проверяем структуру
        assert result["page"] == "events"
        assert result["period"] == "месяц"
        assert result["status"] == "success"

        # Проверяем разделы
        assert "expenses" in result
        assert "incomes" in result
        assert "exchange_rates" in result
        assert "stock_prices" in result

        # Проверяем расходы
        expenses = result["expenses"]
        assert "total" in expenses
        assert expenses["total"] > 0
        assert "main" in expenses
        assert "transfers_cash" in expenses

        # Проверяем поступления
        incomes = result["incomes"]
        assert "total" in incomes
        assert incomes["total"] > 0
        assert "main_categories" in incomes

    @pytest.mark.parametrize("period,expected_name", [
        ("D", "день"),
        ("W", "неделя"),
        ("M", "месяц"),
        ("invalid", "месяц"),
    ])
    @patch("src.views.get_exchange_rates")  # Исправлено: было get_currency_rates
    @patch("src.views.get_stock_prices")
    def test_events_page_periods(self, mock_stocks, mock_rates, period, expected_name):
        """Тест разных периодов."""
        mock_rates.return_value = {}
        mock_stocks.return_value = {}
        df = pd.DataFrame({"Сумма операции": [1000.0]})

        result = events_page(df, period)

        assert result["period"] == expected_name

    @patch("src.views.get_exchange_rates")  # Исправлено: было get_currency_rates
    @patch("src.views.get_stock_prices")
    def test_events_page_empty_dataframe(self, mock_stocks, mock_rates):
        """Тест с пустым DataFrame."""
        mock_rates.return_value = {}
        mock_stocks.return_value = {}
        empty_df = pd.DataFrame()

        result = events_page(empty_df, "M")

        assert result["page"] == "events"
        assert result["status"] == "success"
        assert result["expenses"]["total"] == 0
        assert result["expenses"]["other_categories"] is None
        assert result["incomes"]["total"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
