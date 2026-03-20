import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Live Market Watch", layout="wide")

st.title("📈 Real-Time Market Monitor")
st.subheader("Live Data via Google Sheets Bridge")

# --- APNA SHEET LINK ---
# Maine aapka link format fix kar diya hai
sheet_id = "1fygPji1DFm4gcf1D-3g2siTs1bV31FthfJaikLsinK4"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Data load karna
    df = pd.read_csv(csv_url)

    # Top Highlights (Metrics)
    if not df.empty:
        cols = st.columns(len(df))
        for i, row in df.iterrows():
            with cols[i]:
                # % Change se color decide karna
                change_val = float(row['% Change'].replace('%', ''))
                st.metric(
                    label=row['Symbol'], 
                    value=row['LTP'], 
                    delta=row['% Change']
                )

        st.write("---")
        
        # Detailed Table
        st.subheader("Watchlist Details")
        st.dataframe(
            df.style.background_gradient(cmap='RdYlGn', subset=['Change']), 
            use_container_width=True
        )
        
        st.info("Tip: Ye data har 1 minute mein Google Sheet se auto-refresh hota hai.")
    else:
        st.warning("Sheet mein data mil gaya hai par rows khali hain.")

except Exception as e:
    st.error(f"Error: Data load nahi ho raha. Check karein ki Google Sheet 'Anyone with the link' par set hai ya nahi.")
    st.info("Aapka Sheet ID: " + sheet_id)

st.caption("Market data powered by Yahoo Finance & Google Apps Script.")
