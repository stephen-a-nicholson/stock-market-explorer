"""
This module defines custom exceptions for handling errors in the stock data retrieval 
and parsing process.

Classes:
- StockDataFetchError: Exception raised when there is an error fetching stock data.
- StockDataParseError: Exception raised when there is an error parsing the stock data.
"""


class StockDataFetchError(Exception):
    """Exception raised when there is an error fetching stock data."""


class StockDataParseError(Exception):
    """Exception raised when there is an error parsing the stock data."""
