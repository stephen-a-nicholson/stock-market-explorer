# Stock Market Explorer

The Stock Market Explorer is a web application that allows users to fetch and visualise stock market data using the Alpha Vantage API. It provides an interactive interface to explore stock prices, volume, and other relevant information.

## Features

- Fetch stock market data using the Alpha Vantage free API for personal, non-commercial use
- Display interactive candlestick charts for in-depth price analysis
- Show line charts of closing prices to track market movements
- Visualise volume data to gauge market interest
- Customise time intervals for flexible data exploration
- Error handling and user-friendly feedback for seamless usage

## Technologies Used

- Python
- Streamlit
- Bokeh
- Alpha Vantage API
- Pandas
- Poetry (for dependency management)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/stephen-a-nicholson/stock-market-explorer.git
   ```

2. Navigate to the project directory:
   ```
   cd stock-market-explorer
   ```

3. Install Poetry (if not already installed):
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   For more installation options, refer to the [Poetry documentation](https://python-poetry.org/docs/#installation).

4. Install the project dependencies using Poetry:
   ```
   poetry install
   ```

5. Obtain an API key from Alpha Vantage:
   - Sign up for a free account at [Alpha Vantage](https://www.alphavantage.co/)
   - Retrieve your API key from the Alpha Vantage dashboard

## Usage

1. Activate the Poetry virtual environment:
   ```
   poetry shell
   ```

2. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

3. Open your web browser and navigate to the provided URL (usually `http://localhost:8501`).

4. Enter the required information in the sidebar:
   - Stock symbol: Enter the stock symbol you want to fetch data for (e.g., "AAPL" for Apple Inc.)
   - Alpha Vantage API key: Paste your Alpha Vantage API key
   - Interval: Select the desired time interval for the stock data (e.g., "1min", "5min", "15min", "30min", "60min")
   - Month (optional): Enter the specific month in the format "YYYY-MM" to fetch data for a particular month

5. Click the "Fetch Stock Data" button to retrieve the stock market data.

6. Explore the visualised data:
   - Candlestick chart: Interact with the candlestick chart to analyse price movements and patterns
   - Closing prices line chart: Observe the trend of closing prices over time
   - Volume bar chart: Assess the trading volume of the stock

7. Customise the time interval and month as needed to focus on specific periods.

## Contributing

Contributions are welcome! If you find any bugs, have suggestions for improvements, or want to add new features, please open an issue or submit a pull request.

## Licence

This project is licensed under the [MIT Licence](LICENCE).

## Acknowledgements

- [Alpha Vantage](https://www.alphavantage.co/) for providing the stock market data API
- [Streamlit](https://streamlit.io/) for the awesome web application framework
- [Bokeh](https://bokeh.org/) for the interactive visualisation library
- [Poetry](https://python-poetry.org/) for the dependency management and packaging tool
- This project is for personal, non-commercial use only and complies with the Alpha Vantage terms of service.