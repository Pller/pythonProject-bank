"""
Обновленные тесты для новой версии home_page (принимает строку даты)
"""
import pytest
from unittest.mock import patch, MagicMock
from src.views import home_page
import pandas as pd


class TestHomePageUpdated:
    """Тесты для обновленной функции home_page."""

    @patch("src.views.read_excel_file")
    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_home_page_structure(self, mock_stocks, mock_rates, mock_excel):
        """Тест структуры данных главной страницы."""
        # Создаем тестовый DataFrame с обязательными колонками
        data = {
            "Дата операции": ["2024-01-01", "2024-01-02"],
            "Номер карты": ["1234567812345678", "8765432187654321"],
            "Сумма операции": [1500.0, 3000.0],
            "Кешбэк": [15.0, 30.0],
            "Категория": ["Супермаркеты", "Услуги"],
            "Описание": ["Покупка в магазине", "Оплата услуг"],
        }
        df = pd.DataFrame(data)

        # Настраиваем моки
        mock_excel.return_value = df
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

        # Проверяем типы
        assert isinstance(result["greeting"], str)
        assert isinstance(result["cards"], list)
        assert isinstance(result["top_transactions"], list)
        assert isinstance(result["currency_rates"], list)
        assert isinstance(result["stock_prices"], list)

    def test_home_page_greetings(self):
        """Тест приветствий в разное время суток."""
        test_cases = [
            ("2024-01-01 08:30:00", "Доброе утро"),
            ("2024-01-01 14:30:00", "Добрый день"),
            ("2024-01-01 20:30:00", "Добрый вечер"),
            ("2024-01-01 02:30:00", "Доброй ночи"),
        ]

        for date_str, expected_greeting in test_cases:
            # Мокаем все внешние зависимости
            with patch("src.views.read_excel_file") as mock_excel, \
                 patch("src.views.get_currency_rates") as mock_rates, \
                 patch("src.views.get_stock_prices") as mock_stocks:

                # Создаем минимальный DataFrame с обязательными колонками
                df = pd.DataFrame({
                    "Дата операции": ["2024-01-01"],
                    "Номер карты": ["1234567812345678"],
                    "Сумма операции": [1000.0],
                    "Кешбэк": [10.0],
                    "Категория": ["Тест"],
                    "Описание": ["Тестовая транзакция"],
                })

                mock_excel.return_value = df
                mock_rates.return_value = []
                mock_stocks.return_value = []

                result = home_page(date_str)
                assert result["greeting"] == expected_greeting, \
                    f"Для {date_str} ожидалось '{expected_greeting}', получено '{result['greeting']}'"

    def test_home_page_invalid_date(self):
        """Тест с некорректной датой."""
        result = home_page("некорректная-дата")

        # Проверяем, что функция возвращает ответ с ошибкой
        assert result["status"] == "error"
        assert "error" in result

    @patch("src.views.read_excel_file")
    def test_home_page_file_error(self, mock_excel):
        """Тест обработки ошибки загрузки файла."""
        mock_excel.side_effect = Exception("Ошибка загрузки файла")

        result = home_page("2024-01-01 12:00:00")

        assert result["status"] == "error"
        assert "error" in result
        assert "Ошибка загрузки файла" in result["error"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
