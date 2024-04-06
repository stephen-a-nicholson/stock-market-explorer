from stock_market_explorer.stock_data_retriever import fetch_stock_data
import streamlit as st

st.title("Real-time Stock Market Data Analysis")

symbol = st.selectbox("Select a stock symbol", ["AAPL", "GOOGL", "AMZN"])

api_key = "YOUR_API_KEY"
data = fetch_stock_data(symbol, api_key)

# Display stock price chart
st.line_chart(data["Close"])
