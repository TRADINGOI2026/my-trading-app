import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Live OI & Vol Scanner", layout="wide")

st.title("🚀 Real-Time Market Scanner")
st.subheader("Highest OI & Volume Highlights")

# --- DATA SECTION (Abhi Sample hai, highlights check karne ke liye) ---
data = {
    "Symbol": ["NIFTY 22000 CE", "BANKNIFTY 48000 PE", "RELIANCE 2900 CE", "NIFTY 22100 PE", "SBIN 750 CE", "TATASTEEL 150 CE"],
    "LTP": [150.50, 210.30, 45.10, 110.00, 12.40, 3.50],
    "High": [180, 250, 60, 130, 15, 5],
    "Low": [120, 190, 30, 90, 10, 2],
    "ATP": [145.20, 205.00, 42.10, 105.00, 11.80, 3.20],
    "Volume %": [85.0, 12.0, 110.0, 45.0, 95.0, 150.0],
    "OI % Change": [12.5, -5.2, 25.8, 8.4, -2.1, 35.0]
}
df = pd.DataFrame(data)

# --- NEW HIGHLIGHTS SECTION ---
top_oi = df.sort_values(by="OI % Change", ascending=False).iloc[0]
top_vol = df.sort_values(by="Volume %", ascending=False).iloc[0]

col1, col2 = st.columns(2)
with col1:
    st.info("🔥 TOP OI GAINER")
    st.metric(label=top_oi["Symbol"], value=f"{top_oi['LTP']}", delta=f"{top_oi['OI % Change']}% OI")

with col2:
    st.warning("📊 VOLUME SPIKE")
    st.metric(label=top_vol["Symbol"], value=f"{top_vol['LTP']}", delta=f"{top_vol['Volume %']}% Vol")

st.write("---")

# --- FILTERS & SORTING ---
st.sidebar.header("Custom Filters")
time_filter = st.sidebar.selectbox("Timeframe", ["15m", "30m", "1h", "4h", "1 Day", "7 Days"])
sort_option = st.sidebar.radio("Sort Table By:", ["Highest OI % Change", "Highest Volume %"])

# Sorting Logic
if sort_option == "Highest OI % Change":
    df_display = df.sort_values(by="OI % Change", ascending=False)
else:
    df_display = df.sort_values(by="Volume %", ascending=False)

# --- DISPLAY TABLE ---
st.write(f"### {time_filter} Data (Sorted by {sort_option})")
st.dataframe(df_display.style.background_gradient(cmap='Greens', subset=['OI % Change', 'Volume %']), use_container_width=True)

st.success("Analysis complete. Highlighted rows show maximum market activity.")
