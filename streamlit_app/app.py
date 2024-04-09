"""
This module contains the StockMarketApp class which is used to 
run a web application for exploring stock market data.

The StockMarketApp class uses the Streamlit library to create a web application. 
It fetches stock market data using the Alpha Vantage API and displays it in various ways, 
including an interactive candlestick chart using the Bokeh library.

The StockMarketApp class has the following attributes:
- symbol: The stock symbol to fetch data for.
- api_key: The API key for the Alpha Vantage API.
- data: The fetched stock data.

The StockMarketApp class has the following methods:
- run: Runs the Stock Market App.
- fetch_data: Fetches the stock data.
- display_data: Displays the stock data.
- create_candlestick_chart: Creates an interactive candlestick chart from the fetched data.
"""

import streamlit as st
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Viridis
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from stock_market_explorer.exceptions import (
    StockDataFetchError,
    StockDataParseError,
)
from stock_market_explorer.stock_data_retriever import (
    fetch_stock_data,
    process_stock_data,
)
from streamlit_bokeh_events import streamlit_bokeh_events


class StockMarketApp:
    """
    A class representing a Stock Market App.

    Attributes:
        symbol (str): The stock symbol.
        api_key (str): The Alpha Vantage API key.
        data (dict): The fetched stock data.

    Methods:
        run(): Runs the Stock Market App.
        fetch_data(symbol, api_key): Fetches the stock data.
        display_data(symbol, data): Displays the stock data.
        create_candlestick_chart(data): Creates an interactive candlestick chart.
    """

    def __init__(self):
        self.symbol = ""
        self.api_key = ""
        self.data = None

    def run(self):
        """
        Runs the Stock Market Explorer application.

        This method sets the page configuration, displays the title,
        and handles user inputs.
        It fetches stock data when the "Fetch Stock Data" button is clicked
        and displays the data if available.
        """
        st.set_page_config(page_title="Stock Market App", layout="wide")
        st.title("Stock Market Explorer")

        with st.sidebar:
            st.header("User Inputs")
            self.symbol = st.text_input("Enter the stock symbol")
            self.api_key = st.text_input("Enter your Alpha Vantage API key")
            interval = st.selectbox(
                "Select the interval",
                ("1min", "5min", "15min", "30min", "60min"),
                index=0,
            )
            month = st.text_input("Select the month (YYYY-MM)", value="")
            st.info(
                "Please enter a valid stock symbol, API key, interval, and month to fetch the data."
            )

        if st.sidebar.button("Fetch Stock Data"):
            if self.symbol and self.api_key and interval:
                self.data = self.fetch_data(
                    self.symbol, self.api_key, interval, month
                )
                if self.data:
                    self.display_data(self.symbol, self.data)
            else:
                st.error("Please provide all the required inputs.")

    @staticmethod
    @st.cache_data
    def fetch_data(
        symbol: str, api_key: str, interval: str, month: str = None
    ) -> dict:
        """
        Fetches the stock data using the provided stock symbol and API key.

        Args:
            symbol (str): The stock symbol.
            api_key (str): The Alpha Vantage API key.
            interval (str): The time interval for intraday data.
            month (str): The month in the format "YYYY-MM" (optional).

        Returns:
            dict: The fetched stock data.
        """
        try:
            with st.spinner("Fetching stock data..."):
                raw_data = fetch_stock_data(symbol, api_key, interval, month)
                if "Error Message" in raw_data:
                    return raw_data  # Return the error message as a dictionary
                df = process_stock_data(raw_data, interval)
                data = df.to_dict("index")
                return data
        except (StockDataFetchError, StockDataParseError) as e:
            st.error(str(e))
            return None

    def display_data(self, symbol: str, data: dict):
        """
        Displays the fetched stock data, including line chart,
        candlestick chart, volume chart, and raw data.

        Args:
            symbol (str): The stock symbol.
            data (dict): The fetched stock data.
        """
        if "Error Message" in data:
            st.error(data["Error Message"])
        else:
            st.subheader(f"Stock Data for {symbol}")

            dates = [data_point["Date"] for data_point in data.values()]
            dates.sort()  # Sort the dates in ascending order
            closing_prices = [
                data_point["Close"] for data_point in data.values()
            ]

            # Line chart of closing prices
            st.subheader("Closing Prices")
            st.line_chart(closing_prices)
            st.write(
                "This line chart displays the closing prices of the stock over time."
            )

            # Candlestick chart
            open_prices = [data_point["Open"] for data_point in data.values()]
            high_prices = [data_point["High"] for data_point in data.values()]
            low_prices = [data_point["Low"] for data_point in data.values()]

            candlestick_data = {
                "Date": dates,
                "Open": open_prices,
                "High": high_prices,
                "Low": low_prices,
                "Close": closing_prices,
            }

            st.subheader("Candlestick Chart")
            st.write(
                "Explore the candlestick chart to analyze price movements and patterns."
            )
            candlestick_chart = self.create_candlestick_chart(candlestick_data)
            streamlit_bokeh_events(
                candlestick_chart,
                events="pan,wheel_zoom,reset",
                key="candlestick_chart",
            )

            # Display volume data
            volumes = [
                int(data_point["Volume"]) for data_point in data.values()
            ]

            st.subheader("Volume")
            st.write(
                "This bar chart represents the trading volume of the stock."
            )
            st.bar_chart(volumes)

            st.subheader("Raw Data")
            st.write(data)

    def create_candlestick_chart(self, data: dict) -> figure:
        """
        Creates an interactive candlestick chart using the provided data.

        Args:
            data (dict): The candlestick data.

        Returns:
            bokeh.plotting.figure.Figure: The created candlestick chart.
        """
        source = ColumnDataSource(data)

        p = figure(
            x_axis_type="datetime",
            width=1200,
            height=600,
            title=f"Candlestick Chart for {self.symbol}",
            tools="pan,wheel_zoom,box_zoom,reset,save",
        )
        p.title.text_font_size = "20pt"
        p.title.align = "center"
        p.grid.grid_line_alpha = 0.3
        p.xaxis.axis_label = "Date"
        p.yaxis.axis_label = "Price"

        p.segment(
            x0="Date",
            y0="High",
            x1="Date",
            y1="Low",
            source=source,
            color="black",
            line_width=1,
        )
        p.vbar(
            x="Date",
            width=0.8,
            top="Open",
            bottom="Close",
            source=source,
            fill_color=factor_cmap(
                "Open", palette=Viridis[6], factors=data["Open"]
            ),
            line_color="black",
        )

        hover = HoverTool(
            tooltips=[
                ("Date", "@Date{%F}"),
                ("Open", "$@Open{0.2f}"),
                ("High", "$@High{0.2f}"),
                ("Low", "$@Low{0.2f}"),
                ("Close", "$@Close{0.2f}"),
            ],
            formatters={"@Date": "datetime"},
            mode="vline",
        )
        p.add_tools(hover)

        return p


if __name__ == "__main__":
    app = StockMarketApp()
    app.run()
