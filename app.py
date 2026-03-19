import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(page_title="My Trading Dashboard", layout="wide")

st.title("📈 Index & Stock Options Analysis")
st.subheader("Volume, OI & Price Comparison (15m to 7 Days)")

# Sidebar Filters
st.sidebar.header("Filters")
market_type = st.sidebar.selectbox("Market Segment", ["Index", "Stocks"])
symbol = st.sidebar.text_input("Enter Symbol (e.g. NIFTY, RELIANCE)", "NIFTY")
timeframe = st.sidebar.selectbox("Timeframe Filter", 
    ["15 MIN", "30 MIN", "1 HOUR", "2 HOUR", "4 HOUR", "1 DAY", "2 DAY", "3 DAY", "7 DAY"])

# Placeholder for Data (Scraping/API Logic will go here)
# Note: For real live data, use your broker API or NSE scrapers.
def get_mock_data():
    data = {
        "Option Strike": ["22000 CE", "22100 CE", "22000 PE", "22100 PE"],
        "LTP": [150.50, 80.20, 45.10, 110.00],
        "High": [180.00, 95.00, 60.00, 130.00],
        "Low": [120.00, 70.00, 30.00, 90.00],
        "ATP (Avg Price)": [145.20, 82.50, 42.10, 105.00],
        "Volume": [150000, 95000, 200000, 180000],
        "Vol % Change": ["+15%", "+10%", "-5%", "+22%"],
        "Open Interest (OI)": [1200000, 800000, 1500000, 1100000],
        "OI % Change": ["+5.2%", "+2.1%", "-1.5%", "+8.4%"]
    }
    return pd.DataFrame(data)

df = get_mock_data()

# Display Table
st.dataframe(df, use_container_width=True)

st.info(f"Showing analysis for {symbol} on {timeframe} timeframe.")
st.write("---")
st.caption("Note: To get LIVE NSE data, you need to connect this code with an NSE Scraper or Broker API.")
