import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from trading_strategy import get_stock_data, calculate_moving_averages, identify_golden_cross, implement_strategy

# Load and process data
TICKER = "MSFT"
data = get_stock_data(TICKER)
data = calculate_moving_averages(data)
data = identify_golden_cross(data)
positions_df = implement_strategy(data)
positions = positions_df.to_dict('records')

# Prepare buy/sell points
buy_points = [(pos['BuyDate'], pos['BuyPrice']) for pos in positions]
sell_points = [(pos['SellDate'], pos['SellPrice']) for pos in positions]

# Streamlit app structure
st.set_page_config(page_title="Trading Strategy Dashboard", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Price Chart", "Trade Statistics", "Detailed Trades"])

if page == "Price Chart":
    st.title("Price Chart with Moving Averages and Trades")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data['Close'], label='Stock Price', color='blue')
    ax.plot(data.index, data['MA50'], label='MA50', color='orange')
    ax.plot(data.index, data['MA200'], label='MA200', color='green')
    # Buy points
    if buy_points:
        ax.scatter([x[0] for x in buy_points], [x[1] for x in buy_points], color='red', label='Buy', marker='o', s=80)
    # Sell points
    if sell_points:
        ax.scatter([x[0] for x in sell_points], [x[1] for x in sell_points], color='purple', label='Sell', marker='o', s=80)
    ax.legend()
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    st.pyplot(fig)

elif page == "Trade Statistics":
    st.title("Trade Statistics")
    total_trades = len(positions)
    winning_trades = sum(1 for pos in positions if pos['ProfitPct'] > 0)
    losing_trades = total_trades - winning_trades
    avg_profit = np.mean([pos['ProfitPct'] for pos in positions]) if positions else 0
    st.metric("Total Trades", total_trades)
    st.metric("Winning Trades", winning_trades)
    st.metric("Losing Trades", losing_trades)
    st.metric("Average Profit (%)", f"{avg_profit:.2f}")

elif page == "Detailed Trades":
    st.title("Detailed Trades Record")
    df_trades = pd.DataFrame(positions)
    st.dataframe(df_trades)
