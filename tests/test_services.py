"""
Тесты для модуля services.
"""
import pytest
from src.services import (
    analyze_cashback_categories,
    calculate_investment_piggybank,
    search_transactions,
    find_phone_transactions,
    find_personal_transfers,
)


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями для сервисов."""
    return [
        {
            "Категория": "Супермаркеты",
            "Кешбэк": 50,
            "Сумма операции": 1000,
            "Описание": "Покупка в магазине",
            "Округление на «Инвесткопилку»": 10,
        },
        {
            "Категория": "Транспорт",
            "Кешбэк": 10,
            "Сумма операции": 500,
            "Описание": "Такси 89161234567",
            "Округление на «Инвесткопилку»": 5,
        },
        {
            "Категория": "Рестораны",
            "Кешбэк": 100,
            "Сумма операции": 2000,
            "Описание": "Оплата за ужин",
            "Округление на «Инвесткопилку»": 20,
        },
    ]


def test_analyze_cashback_categories(sample_transactions):
    """Тест анализа категорий кешбэка."""
    result = analyze_cashback_categories(sample_transactions, "1/2024")
    assert len(result) > 0


def test_analyze_cashback_empty():
    """Тест с пустым списком транзакций."""
    result = analyze_cashback_categories([], "1/2024")
    assert result == []


def test_calculate_investment_piggybank(sample_transactions):
    """Тест расчета суммы инвесткопилки."""
    result = calculate_investment_piggybank(sample_transactions)
    assert isinstance(result, (int, float))


def test_calculate_investment_empty():
    """Тест с пустым списком транзакций."""
    result = calculate_investment_piggybank([])
    assert result == 0


@pytest.mark.parametrize(
    "search_term,expected_count",
    [
        ("магазин", 1),
        ("такси", 1),
        ("ресторан", 0),
        ("", 3),
    ],
)
def test_search_transactions(sample_transactions, search_term, expected_count):
    """Тест поиска транзакций."""
    result = search_transactions(sample_transactions, search_term)
    assert len(result) == expected_count


def test_find_phone_transactions(sample_transactions):
    """Тест поиска транзакций с телефонными номерами."""
    result = find_phone_transactions(sample_transactions)
    assert len(result) == 1


def test_find_personal_transfers():
    """Тест поиска переводов физлицам."""
    transactions = [
        {"Описание": "Перевод Ивану Иванову", "Сумма операции": 1000},
        {"Описание": "Оплата услуг", "Сумма операции": 500},
    ]
    result = find_personal_transfers(transactions)
    assert len(result) == 1
