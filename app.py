import streamlit as st
import pandas as pd
import requests

# Page setup
st.set_page_config(page_title="Live Trading Scanner Pro", layout="wide")

st.title("🚀 Live Index & Stock Options Scanner")

# --- DATA FETCHING WITH HEADERS (NSE BLOCK FIX) ---
def get_nse_data(symbol):
    # NSE ko lagna chahiye ki ye browser se aa raha hai
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    base_url = "https://www.nseindia.com/"
    # Index ya Stock ke hisaab se URL badlega
    if symbol in ["NIFTY", "BANKNIFTY", "FINNIFTY"]:
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    else:
        url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"

    try:
        session = requests.Session()
        # Pehle main page visit karke cookies lena zaroori hai
        session.get(base_url, headers=headers, timeout=10)
        # Ab asli data lena
        response = session.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()['filtered']['data']
        else:
            return None
    except Exception as e:
        return None

# --- SIDEBAR ---
st.sidebar.header("Market Settings")
market_symbol = st.sidebar.text_input("Enter Symbol (NIFTY / BANKNIFTY / SBIN)", "NIFTY").upper()
sort_by = st.sidebar.radio("Sort By:", ["OI % Change", "Volume"])

# --- PROCESS DATA ---
raw_data = get_nse_data(market_symbol)

if raw_data:
    rows = []
    for d in raw_data:
        strike = d['strikePrice']
        for side in ['CE', 'PE']:
            if side in d:
                opt = d[side]
                rows.append({
                    "Strike": f"{strike} {side}",
                    "LTP": opt['lastPrice'],
                    "Vol %": opt.get('pChangeInUnderlying', 0), # Temporary for Vol calculation
                    "Volume": opt['totalTradedVolume'],
                    "OI": opt['openInterest'],
                    "OI % Change": opt['pchangeinOpenInterest'],
                    "ATP": opt.get('underlyingValue', 0),
                    "High": opt.get('highPrice', 0),
                    "Low": opt.get('lowPrice', 0)
                })
    
    df = pd.DataFrame(rows)

    # Highlights
    top_oi = df.sort_values(by="OI % Change", ascending=False).iloc[0]
    top_vol = df.sort_values(by="Volume", ascending=False).iloc[0]

    c1, c2 = st.columns(2)
    with c1:
        st.info(f"🔥 TOP OI GAINER: {top_oi['Strike']}")
        st.metric("OI Change", f"{top_oi['OI % Change']}%", f"LTP: {top_oi['LTP']}")
    with c2:
        st.warning(f"📊 HIGHEST VOLUME: {top_vol['Strike']}")
        st.metric("Volume", f"{top_vol['Volume']}", f"LTP: {top_vol['LTP']}")

    st.write("---")
    
    # Sorting & Display
    if sort_by == "OI % Change":
        df = df.sort_values(by="OI % Change", ascending=False)
    else:
        df = df.sort_values(by="Volume", ascending=False)

    st.dataframe(df.style.background_gradient(cmap='RdYlGn', subset=['OI % Change']), use_container_width=True)
else:
    st.error("NSE ki website abhi busy hai. 1-2 minute baad 'Refresh' karein ya Symbol check karein.")

st.caption("Note: Live market mein data har 1-3 minute mein update hota hai.")
