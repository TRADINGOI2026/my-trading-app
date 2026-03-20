import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Live Market Watch", layout="wide")

st.title("📈 Real-Time Market Monitor")
st.caption("Live Data via Google Sheets & Yahoo Finance")

# Aapka Sheet ID
sheet_id = "1fygPji1DFm4gcf1D-3g2siTs1bV31FthfJaikLsinK4"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

try:
    # Data load karna
    df = pd.read_csv(csv_url)
    
    if not df.empty:
        # 1. Top Highlights (Patti jaisa dikhega)
        cols = st.columns(len(df))
        for i, row in df.iterrows():
            with cols[i]:
                st.metric(label=row['Symbol'], value=str(row['LTP']), delta=str(row['% Change']))
        
        st.write("---")
        
        # 2. Watchlist Details (Sahi table)
        st.subheader("Watchlist Details")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.success("✅ Dashboard is Live and Updating every 1 minute.")
    else:
        st.warning("Sheet load ho gayi hai par usme koi data nahi mila.")

except Exception as e:
    st.error("Connection Error: Please check your Google Sheet Share settings.")

st.info("Tip: Naye stocks add karne ke liye Google Apps Script mein symbols update karein.")
