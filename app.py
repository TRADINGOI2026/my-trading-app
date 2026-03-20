import streamlit as st
import pandas as pd

st.set_page_config(page_title="Nifty Options Scanner", layout="wide")
st.title("🎯 Nifty Options Scanner (OI & Volume)")

sheet_id = "1fygPji1DFm4gcf1D-3g2siTs1bV31FthfJaikLsinK4"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

try:
    df = pd.read_csv(csv_url)
    
    # Scanner Analysis
    st.subheader("🔥 Market Insights")
    c1, c2 = st.columns(2)
    
    with c1:
        st.write("**Top OI Gainers (Smart Money Activity)**")
        top_oi = df.sort_values(by='OI_Chng', ascending=False).head(5)
        st.dataframe(top_oi[['Strike', 'Type', 'OI_Chng', 'LTP']], hide_index=True)
        
    with c2:
        st.write("**High Volume Strikes (Intraday Action)**")
        top_vol = df.sort_values(by='Volume', ascending=False).head(5)
        st.dataframe(top_vol[['Strike', 'Type', 'Volume', 'LTP']], hide_index=True)

    st.write("---")
    st.subheader("Full Option Chain Scanner")
    st.dataframe(df.style.background_gradient(subset=['OI_Chng'], cmap='RdYlGn'), use_container_width=True, hide_index=True)

except Exception as e:
    st.error("Data abhi load nahi ho raha. Pehle Google Apps Script ko 'Run' karein.")
