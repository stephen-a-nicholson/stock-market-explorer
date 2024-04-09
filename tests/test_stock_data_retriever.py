"""
This module contains unit tests for the `stock_data_retriever` module.

The `TestStockDataRetriever` class contains two test cases:
- `test_fetch_stock_data_success`: This test case tests the `fetch_stock_data` 
function with a successful response.
- `test_fetch_stock_data_error`: This test case tests the `fetch_stock_data` 
function with an error response.

These tests use the `unittest.mock.patch` decorator to mock the `requests.get` 
function used in `fetch_stock_data`.
"""
import unittest
from unittest.mock import patch
import pandas as pd
from stock_market_explorer.stock_data_retriever import (
    fetch_stock_data,
    process_stock_data,
)
from stock_market_explorer.exceptions import (
    StockDataFetchError,
)


class TestStockDataRetriever(unittest.TestCase):
    """
    A test case class for testing the StockDataRetriever class.
    """

    @patch("stock_market_explorer.stock_data_retriever.requests.get")
    def test_fetch_stock_data_success(self, mock_get):
        """
        Test case for successful fetching of stock data.
        """
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {"Time Series (1min)": {}}
        mock_get.return_value = mock_response

        data = fetch_stock_data("AAPL", "api_key", "1min")
        self.assertIsInstance(data, dict)
        self.assertIn("Time Series (1min)", data)

    @patch("stock_market_explorer.stock_data_retriever.requests.get")
    def test_fetch_stock_data_error(self, mock_get):
        """
        Test case for error handling when fetching stock data.
        """
        mock_get.side_effect = StockDataFetchError("Error fetching stock data")

        with self.assertRaises(StockDataFetchError):
            fetch_stock_data("AAPL", "api_key", "1min")

    def test_process_stock_data_success(self):
        """
        Test case for successful processing of stock data.
        """
        data = {
            "Time Series (1min)": {
                "2023-06-08 15:00:00": {
                    "1. open": "100.0",
                    "2. high": "101.0",
                    "3. low": "99.0",
                    "4. close": "100.5",
                    "5. volume": "1000",
                }
            }
        }
        interval = "1min"

        processed_data = process_stock_data(data, interval)
        self.assertIsInstance(processed_data, pd.DataFrame)
        self.assertEqual(len(processed_data), 1)
        self.assertEqual(processed_data.iloc[0]["Open"], 100.0)
        self.assertEqual(processed_data.iloc[0]["High"], 101.0)
        self.assertEqual(processed_data.iloc[0]["Low"], 99.0)
        self.assertEqual(processed_data.iloc[0]["Close"], 100.5)
        self.assertEqual(processed_data.iloc[0]["Volume"], 1000)

    def test_process_stock_data_error(self):
        """
        Test case for error handling when processing stock data.
        """
        data = {"Error Message": "Invalid API call"}
        interval = "1min"

        with self.assertRaises(ValueError):
            process_stock_data(data, interval)


if __name__ == "__main__":
    unittest.main()
