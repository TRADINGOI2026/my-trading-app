import streamlit as st
import pandas as pd
from nsepython import nse_optionchain_scrapper, nse_quote_ltp

# Page Config
st.set_page_config(page_title="Live Trading Scanner Pro", layout="wide")

st.title("📊 Live Index & Stock Options Scanner")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Market Settings")
market_symbol = st.sidebar.text_input("Enter Symbol (NIFTY / BANKNIFTY / SBIN)", "NIFTY")
timeframe = st.sidebar.selectbox("Select Timeframe Filter", 
    ["15 MIN", "30 MIN", "1 HOUR", "4 HOUR", "1 DAY", "7 DAYS"])

sort_by = st.sidebar.radio("Sort Top Results By:", ["OI % Change", "Volume % Change"])

# --- DATA FETCHING LOGIC ---
@st.cache_data(ttl=60) # Har 60 seconds mein data refresh hoga
def fetch_data(symbol):
    try:
        # NSE se data khinchne ka function
        payload = nse_optionchain_scrapper(symbol)
        data = payload['filtered']['data']
        
        rows = []
        for d in data:
            strike = d['strikePrice']
            if 'CE' in d:
                ce = d['CE']
                rows.append({
                    "Strike": f"{strike} CE",
                    "LTP": ce['lastPrice'],
                    "High": ce.get('highPrice', 0),
                    "Low": ce.get('lowPrice', 0),
                    "ATP": ce.get('underlyingValue', 0), # ATP logic
                    "Volume": ce['totalTradedVolume'],
                    "OI": ce['openInterest'],
                    "OI Change %": ce['pchangeinOpenInterest']
                })
            if 'PE' in d:
                pe = d['PE']
                rows.append({
                    "Strike": f"{strike} PE",
                    "LTP": pe['lastPrice'],
                    "High": pe.get('highPrice', 0),
                    "Low": pe.get('lowPrice', 0),
                    "ATP": pe.get('underlyingValue', 0),
                    "Volume": pe['totalTradedVolume'],
                    "OI": pe['openInterest'],
                    "OI Change %": pe['pchangeinOpenInterest']
                })
        return pd.DataFrame(rows)
    except:
        return pd.DataFrame()

# --- DISPLAY LOGIC ---
df = fetch_data(market_symbol)

if not df.empty:
    # Sorting logic for Highlights
    top_oi = df.sort_values(by="OI Change %", ascending=False).iloc[0]
    top_vol = df.sort_values(by="Volume", ascending=False).iloc[0]

    # TOP HIGHLIGHTS CARDS
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"🔥 TOP OI GAINER: {top_oi['Strike']}")
        st.metric("OI Change %", f"{top_oi['OI Change %']}%", f"LTP: {top_oi['LTP']}")
    with c2:
        st.warning(f"📊 HIGHEST VOLUME: {top_vol['Strike']}")
        st.metric("Volume", f"{top_vol['Volume']}", f"LTP: {top_vol['LTP']}")

    st.write("---")

    # Final Table with Sorting
    if sort_by == "OI % Change":
        df_final = df.sort_values(by="OI Change %", ascending=False)
    else:
        df_final = df.sort_values(by="Volume", ascending=False)

    st.subheader(f"Detailed Analysis: {market_symbol} ({timeframe})")
    st.dataframe(df_final.style.background_gradient(cmap='RdYlGn', subset=['OI Change %']), use_container_width=True)

else:
    st.error("Market data fetch nahi ho raha. Check if Symbol is correct or NSE is busy.")

st.caption("Data is fetched directly from NSE via nsepython. Use for analysis only.")
