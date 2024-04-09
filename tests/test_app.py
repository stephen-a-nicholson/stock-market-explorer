"""
This module contains unit tests for the `app.py` module.

The `TestStockMarketApp` class contains two test cases:
- `test_fetch_data_success`: This test case tests the `fetch_data` method 
of the `StockMarketApp` class when data is successfully fetched.
- `test_fetch_data_error`: This test case tests the `fetch_data` method 
of the `StockMarketApp` class when an error occurs while fetching data.

These tests use the `unittest.mock.patch` decorator to mock the `fetch_stock_data` 
function used in `fetch_data`.
"""
import unittest
from unittest.mock import patch
from streamlit_app.app import StockMarketApp
from stock_market_explorer.exceptions import StockDataFetchError


class TestStockMarketApp(unittest.TestCase):
    """
    A test case for the StockMarketApp class.
    """

    def setUp(self):
        self.app = StockMarketApp()

    @patch("stock_market_explorer.app.fetch_stock_data")
    def test_fetch_data_success(self, mock_fetch_stock_data):
        """
        Test the fetch_data method when data is successfully fetched.
        """
        mock_fetch_stock_data.return_value = {"Time Series (1min)": {}}

        data = self.app.fetch_data("AAPL", "api_key", "1min")
        self.assertIsInstance(data, dict)

    @patch("stock_market_explorer.app.fetch_stock_data")
    def test_fetch_data_error(self, mock_fetch_stock_data):
        """
        Test the fetch_data method when an error occurs while fetching data.
        """
        mock_fetch_stock_data.side_effect = StockDataFetchError(
            "Error fetching stock data"
        )

        data = self.app.fetch_data("AAPL", "api_key", "1min")
        self.assertIsNone(data)

    def test_display_data_error(self):
        """
        Test the display_data method when an error message is provided.
        """
        data = {"Error Message": "Invalid API call"}
        with patch("streamlit.error") as mock_error:
            self.app.display_data("AAPL", data)
            mock_error.assert_called_once_with("Invalid API call")

    def test_create_candlestick_chart(self):
        """
        Test the create_candlestick_chart method.
        """
        data = {
            "Date": ["2023-06-08"],
            "Open": [100.0],
            "High": [101.0],
            "Low": [99.0],
            "Close": [100.5],
        }
        chart = self.app.create_candlestick_chart(data)
        self.assertIsNotNone(chart)


if __name__ == "__main__":
    unittest.main()
