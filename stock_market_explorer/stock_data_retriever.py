"""
Module for retrieving and processing stock market data from the Alpha Vantage API.

This module provides functions to fetch stock data from the Alpha Vantage API and process
the retrieved data into a Pandas DataFrame for further analysis and visualization.
"""

import json
from datetime import datetime

import pandas as pd
import requests

from stock_market_explorer.exceptions import (
    StockDataFetchError,
    StockDataParseError,
)


def fetch_stock_data(symbol, api_key, interval="1min", month=None):
    """
    Fetches stock data for a given symbol from Alpha Vantage API.

    Args:
        symbol (str): The stock symbol to fetch data for.
        api_key (str): The API key for accessing the Alpha Vantage API.
        interval (str, optional): The time interval for the data. Defaults to "1min".
        month (str, optional): The specific month to fetch data for. Defaults to None.

    Returns:
        dict: The fetched stock data in JSON format.

    Raises:
        StockDataFetchError: If there is an error fetching the stock data.
        StockDataParseError: If there is an error parsing the JSON response.

    """
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "adjusted": "true",
        "outputsize": "full",
        "apikey": api_key,
    }

    if month:
        params["month"] = month

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        raise StockDataFetchError(f"Error fetching stock data: {e}") from e
    except json.JSONDecodeError as e:
        raise StockDataParseError(f"Error parsing JSON response: {e}") from e


def process_stock_data(data, interval):
    """
    Process the retrieved stock market data into a Pandas DataFrame.

    Args:
        data (dict): The retrieved stock market data in JSON format.
        interval (str): The selected time interval.

    Returns:
        pandas.DataFrame: The processed stock market data as a Pandas DataFrame.

    Raises:
        ValueError: If there is an error message in the retrieved data or if the 
        time series key is missing.
    """
    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    time_series_key = f"Time Series ({interval})"
    if time_series_key not in data:
        raise ValueError(
            f"Invalid data format. Missing '{time_series_key}' key."
        )

    time_series_data = data[time_series_key]
    dates = list(time_series_data.keys())
    dates.reverse()

    stock_data = []
    for date in dates:
        stock_data.append(
            {
                "Date": datetime.strptime(date, "%Y-%m-%d %H:%M:%S"),
                "Close": float(time_series_data[date]["4. close"]),
                "Open": float(time_series_data[date]["1. open"]),
                "High": float(time_series_data[date]["2. high"]),
                "Low": float(time_series_data[date]["3. low"]),
                "Volume": int(time_series_data[date]["5. volume"]),
            }
        )

    return pd.DataFrame(stock_data)
