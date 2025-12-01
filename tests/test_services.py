"""Тесты для модуля services."""

from src.services import (
    investment_bank,
    profitable_cashback_categories,
    search_by_phone_numbers,
    search_person_transfers,
    simple_search,
)


class TestServices:
    """Тесты для модуля services."""

    def setup_method(self):
        """Подготовка тестовых данных."""
        self.sample_transactions = [
            {
                "Дата операции": "2024-01-15",
                "Категория": "Супермаркеты",
                "Сумма операции": -1000.0,
                "Описание": "Покупка в магазине",
            },
            {
                "Дата операции": "2024-01-16",
                "Категория": "Транспорт",
                "Сумма операции": -500.0,
                "Описание": "Такси +7 999 123-45-67",
            },
            {
                "Дата операции": "2024-01-17",
                "Категория": "Переводы",
                "Сумма операции": -2000.0,
                "Описание": "Перевод Иванов И.",
            },
        ]

    def test_profitable_cashback_categories(self):
        """Тест анализа выгодных категорий кешбэка."""
        result = profitable_cashback_categories(self.sample_transactions, 2024, 1)

        assert isinstance(result, dict)
        assert "Супермаркеты" in result
        assert result["Супермаркеты"] == 50.0  # 1000 * 0.05

    def test_investment_bank(self):
        """Тест расчета инвесткопилки."""
        result = investment_bank("2024-01", self.sample_transactions, 50)

        assert isinstance(result, float)
        assert result > 0

    def test_simple_search_found(self):
        """Тест успешного поиска."""
        result = simple_search(self.sample_transactions, "магазин")

        assert len(result) == 1
        assert result[0]["Описание"] == "Покупка в магазине"

    def test_simple_search_not_found(self):
        """Тест поиска без результатов."""
        result = simple_search(self.sample_transactions, "несуществующий")

        assert len(result) == 0

    def test_search_by_phone_numbers(self):
        """Тест поиска по телефонным номерам."""
        result = search_by_phone_numbers(self.sample_transactions)

        assert len(result) == 1
        assert "999 123-45-67" in result[0]["Описание"]

    def test_search_person_transfers(self):
        """Тест поиска переводов физлицам."""
        result = search_person_transfers(self.sample_transactions)

        assert len(result) == 1
        assert result[0]["Категория"] == "Переводы"
        assert "Иванов И." in result[0]["Описание"]
