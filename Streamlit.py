import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Trader Behavior Dashboard", layout="wide")

st.title("📊 Hyperliquid Trader Performance vs Sentiment")
st.markdown("Explore how Fear & Greed impacts trader behavior and profitability.")

# Load processed data
@st.cache_data
def load_data():
    return pd.read_csv("processed_daily_metrics.csv")

df = load_data()
df = df[df['Sentiment'].isin(['Fear', 'Greed'])]

# Sidebar filters
st.sidebar.header("Filters")
sentiment_filter = st.sidebar.multiselect("Market Sentiment", options=['Fear', 'Greed'], default=['Fear', 'Greed'])
segment_filter = st.sidebar.multiselect("Trader Volume Segment", options=df['Volume_Segment'].unique(), default=df['Volume_Segment'].unique())

filtered_df = df[(df['Sentiment'].isin(sentiment_filter)) & (df['Volume_Segment'].isin(segment_filter))]

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Performance Breakdown")
    fig1 = px.box(filtered_df, x='Sentiment', y='Daily_PnL', color='Sentiment', title="Daily PnL Distribution (Log Scale)")
    fig1.update_yaxes(type="log")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Behavioral Shift (Trade Sizes)")
    fig2 = px.box(filtered_df, x='Sentiment', y='Avg_Trade_Size_USD', color='Sentiment', title="Average Position Size (Log Scale)")
    fig2.update_yaxes(type="log")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("High-Level Segment Averages")
st.dataframe(filtered_df.groupby(['Volume_Segment', 'Sentiment'])[['Daily_PnL', 'Total_Trades', 'Win_Rate']].mean().round(2))
