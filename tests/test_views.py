"""
Тесты для модуля views с DataFrame на входе.
"""
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.views import home_page


@pytest.fixture
def sample_dataframe():
    """Фикстура с тестовым DataFrame."""
    data = {
        "Дата операции": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "Номер карты": ["1234567812345678", "8765432187654321", "1234567812345678"],
        "Сумма операции": [1500.0, 3000.0, 2000.0],
        "Кешбэк": [15.0, 30.0, 20.0],
        "Категория": ["Супермаркеты", "Услуги", "Транспорт"],
        "Описание": ["Покупка в магазине", "Оплата услуг", "Транспорт"],
    }
    return pd.DataFrame(data)


class TestHomePage:
    """Тесты для функции home_page."""

    @patch("src.views.read_excel_file")
    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_home_page_structure(self, mock_stocks, mock_rates, mock_excel, sample_dataframe):
        """Тест структуры данных главной страницы."""
        # Настраиваем моки с правильными колонками
        mock_excel.return_value = sample_dataframe
        mock_rates.return_value = [{"currency": "USD", "rate": 90.5}]
        mock_stocks.return_value = [{"stock": "AAPL", "price": 185.2}]

        result = home_page("2024-01-01 14:30:00")

        # Проверяем структуру
        assert result["page"] == "home"
        assert result["status"] == "success"
        assert "greeting" in result
        assert "cards" in result
        assert "top_transactions" in result
        assert "currency_rates" in result
        assert "stock_prices" in result
        assert "generated_at" in result

    @patch("src.views.read_excel_file")
    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_home_page_empty_dataframe(self, mock_stocks, mock_rates, mock_excel):
        """Тест с пустым DataFrame."""
        # Создаем пустой DataFrame с правильными колонками
        empty_df = pd.DataFrame(columns=[
            "Дата операции", "Номер карты", "Сумма операции",
            "Кешбэк", "Категория", "Описание"
        ])

        mock_excel.return_value = empty_df
        mock_rates.return_value = []
        mock_stocks.return_value = []

        result = home_page("2024-01-01 12:00:00")

        assert result["page"] == "home"
        assert result["status"] == "success"  # Пустой DF не ошибка
        assert result["cards"] == []
        assert result["top_transactions"] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
