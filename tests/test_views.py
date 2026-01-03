\"\"\"
Тесты для модуля views.
\"\"\"
import pytest
from unittest.mock import patch
from src.views import home_page, events_page


@pytest.fixture
def mock_transactions():
    \"\"\"Фикстура с тестовыми транзакциями.\"\"\"
    return [
        {
            \"Дата операции\": \"2024-01-01\",
            \"Сумма операции\": 1000,
            \"Категория\": \"Супермаркеты\",
            \"Номер карты\": \"1234\",
        },
        {
            \"Дата операции\": \"2024-01-02\",
            \"Сумма операции\": 500,
            \"Категория\": \"Транспорт\",
            \"Номер карты\": \"5678\",
        },
        {
            \"Дата операции\": \"2024-01-03\",
            \"Сумма операции\": 2000,
            \"Категория\": \"Супермаркеты\",
            \"Номер карты\": \"1234\",
        },
    ]


class TestHomePage:
    \"\"\"Тесты для функции home_page.\"\"\"
    
    @patch(\"src.views.load_transactions\")
    def test_home_page_success(self, mock_load, mock_transactions):
        \"\"\"Тест успешной генерации главной страницы.\"\"\"
        mock_load.return_value = mock_transactions
        
        result = home_page()
        
        assert result[\"page\"] == \"Главная\"
        assert result[\"status\"] == \"success\"
        assert result[\"total_transactions\"] == 3
        assert result[\"total_amount\"] == 3500
        assert result[\"unique_cards\"] == 2
        assert \"Супермаркеты\" in result[\"top_categories\"]
    
    @patch(\"src.views.load_transactions\")
    def test_home_page_error(self, mock_load):
        \"\"\"Тест обработки ошибки в главной странице.\"\"\"
        mock_load.side_effect = Exception(\"Test error\")
        
        result = home_page()
        
        assert result[\"page\"] == \"Главная\"
        assert result[\"status\"] == \"error\"
        assert \"error\" in result


class TestEventsPage:
    \"\"\"Тесты для функции events_page.\"\"\"
    
    @pytest.mark.parametrize(
        \"period,expected_name\",
        [
            (\"D\", \"день\"),
            (\"W\", \"неделя\"),
            (\"M\", \"месяц\"),
            (\"invalid\", \"месяц\"),  # default case
        ],
    )
    @patch(\"src.views.load_transactions\")
    def test_events_page_periods(
        self, mock_load, mock_transactions, period, expected_name
    ):
        \"\"\"Тест разных периодов для страницы событий.\"\"\"
        mock_load.return_value = mock_transactions
        
        result = events_page(period)
        
        assert result[\"page\"] == \"События\"
        assert result[\"period\"] == expected_name
        assert result[\"status\"] == \"success\"
        assert result[\"total_events\"] == 3
    
    @patch(\"src.views.load_transactions\")
    def test_events_page_error(self, mock_load):
        \"\"\"Тест обработки ошибки в странице событий.\"\"\"
        mock_load.side_effect = Exception(\"Test error\")
        
        result = events_page()
        
        assert result[\"page\"] == \"События\"
        assert result[\"status\"] == \"error\"
        assert \"error\" in result
