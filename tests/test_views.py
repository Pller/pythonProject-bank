import os
import sys
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.utils import load_transactions
from src.views import generate_events_page, generate_main_page


class TestViews(unittest.TestCase):
    @patch('src.views.load_transactions')
    @patch('src.views.load_settings') 
    @patch('src.views.get_exchange_rates')
    @patch('src.views.get_stock_prices')
    def test_generate_main_page(self, mock_stock, mock_rates, mock_settings, mock_load):
        mock_load.return_value = []
        mock_settings.return_value = {'api_key': 'test'}
        mock_rates.return_value = {'USD': 90.0}
        mock_stock.return_value = {'AAPL': 150.0}
        
        result = generate_main_page()
        self.assertIn('cards', result)
        
    @patch('src.views.load_transactions')
    @patch('src.views.load_settings')
    @patch('src.views.get_exchange_rates')
    @patch('src.views.get_stock_prices')
    def test_generate_events_page(self, mock_stock, mock_rates, mock_settings, mock_load):
        mock_load.return_value = []
        mock_settings.return_value = {'api_key': 'test'}
        mock_rates.return_value = {'USD': 90.0}
        mock_stock.return_value = {'AAPL': 150.0}
        
        result = generate_events_page('M')
        self.assertIn('period', result)
        
    @patch('src.views.load_transactions')
    def test_generate_events_page_invalid_period(self, mock_load):
        mock_load.return_value = []
        
        result = generate_events_page('invalid')
        self.assertIn('error', result)

if __name__ == '__main__':
    unittest.main()
