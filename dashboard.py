import streamlit as st
import pandas as pd
import os
import csv
from price_feed import get_current_price
from portfolio import load_portfolio
from config import HISTORY_FILE, SYMBOL
from indicators import calculate_rsi

st.set_page_config(page_title="Litecoin Paper Trading Dashboard", layout="wide")

st.title("📊 Litecoin Paper Trading Bot Dashboard")

# --- Current Price ---
price = get_current_price()
st.metric(label="📈 Current LTC Price (USD)", value=f"${price:.2f}")

# --- Portfolio Stats ---
portfolio = load_portfolio()
ltc_value = portfolio['ltc'] * price
total_value = portfolio['usd'] + ltc_value

col1, col2, col3 = st.columns(3)
col1.metric("💵 USD Balance", f"${portfolio['usd']:.2f}")
col2.metric("🪙 LTC Holdings", f"{portfolio['ltc']:.4f}")
col3.metric("📊 Total Value", f"${total_value:.2f}")

# --- RSI Chart ---
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        reader = csv.reader(f)
        prices = [float(row[0]) for row in reader if row]

    if len(prices) >= 15:
        rsi = calculate_rsi(prices)
        st.subheader("📉 RSI Indicator")
        st.line_chart(prices[-30:], height=200)
        st.text(f"Current RSI: {rsi:.2f}")
    else:
        st.info("Not enough price data yet to calculate RSI.")

else:
    st.warning("Price history not found.")

# --- Trade Log ---
trades_file = "data/trades.csv"
if os.path.exists(trades_file):
    st.subheader("📋 Trade Log")
    df = pd.read_csv(trades_file)
    st.dataframe(df[::-1], use_container_width=True)
else:
    st.warning("No trades recorded yet.")
