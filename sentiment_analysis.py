import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import warnings
warnings.filterwarnings('ignore')

def load_and_clean_data(hist_path="historical_data.csv", fgi_path="fear_greed_index.csv"):
    hist_df = pd.read_csv(hist_path)
    fgi_df = pd.read_csv(fgi_path)
    
    # Check for missing/duplicates
    print(f"Historical Data -> Missing: {hist_df.isnull().sum().sum()}, Duplicates: {hist_df.duplicated().sum()}")
    print(f"FGI Data -> Missing: {fgi_df.isnull().sum().sum()}, Duplicates: {fgi_df.duplicated().sum()}")

    # Convert timestamps to daily Dates
    hist_df['Datetime'] = pd.to_datetime(hist_df['Timestamp IST'], format='%d-%m-%Y %H:%M', errors='coerce')
    hist_df['Date'] = pd.to_datetime(hist_df['Datetime'].dt.date)
    fgi_df['Date'] = pd.to_datetime(fgi_df['date'])

    # Simplify FGI classifications (Group extremes)
    def simplify_fgi(c):
        c = str(c).lower()
        if 'fear' in c: return 'Fear'
        elif 'greed' in c: return 'Greed'
        else: return 'Neutral'
        
    fgi_df['Sentiment'] = fgi_df['classification'].apply(simplify_fgi)
    
    # Merge datasets by Date
    df = pd.merge(hist_df, fgi_df[['Date', 'value', 'Sentiment']], on='Date', how='inner')
    return df

def feature_engineering(df):
    print("Engineering key metrics...")
    daily_trader_stats = []
    grouped = df.groupby(['Account', 'Date', 'Sentiment'])

    for name, group in grouped:
        account, date, sentiment = name
        daily_pnl = group['Closed PnL'].sum()
        total_trades = len(group)
        avg_trade_size = group['Size USD'].mean() # Proxy for position size/leverage
        
        # Win rate (calculated only on trades that closed a position)
        closing_trades = group[group['Closed PnL'] != 0]
        if len(closing_trades) > 0:
            win_rate = (closing_trades['Closed PnL'] > 0).sum() / len(closing_trades)
        else:
            win_rate = np.nan
            
        long_trades = len(group[group['Side'].str.upper() == 'BUY'])
        short_trades = len(group[group['Side'].str.upper() == 'SELL'])
        ls_ratio = long_trades / (short_trades + 1e-5) # avoid div by zero
        
        daily_trader_stats.append({
            'Account': account, 'Date': date, 'Sentiment': sentiment,
            'Daily_PnL': daily_pnl, 'Total_Trades': total_trades,
            'Avg_Trade_Size_USD': avg_trade_size, 'Win_Rate': win_rate,
            'Long_Short_Ratio': ls_ratio
        })

    daily_df = pd.DataFrame(daily_trader_stats)
    
    # Segment creation (High vs Low Volume, Frequent vs Infrequent)
    median_size = daily_df['Avg_Trade_Size_USD'].median()
    daily_df['Volume_Segment'] = np.where(daily_df['Avg_Trade_Size_USD'] > median_size, 'High_Volume', 'Low_Volume')
    
    return daily_df

def generate_charts(daily_df):
    print("Generating charts...")
    sns.set_theme(style="whitegrid")
    df_filtered = daily_df[daily_df['Sentiment'].isin(['Fear', 'Greed'])]

    # 1. Performance: PnL by Sentiment
    plt.figure(figsize=(8,5))
    sns.barplot(data=df_filtered, x='Sentiment', y='Daily_PnL', estimator=np.mean, ci=None, palette='muted')
    plt.title("Average Daily PnL per Trader by Market Sentiment")
    plt.ylabel("Avg Daily PnL (USD)")
    plt.savefig("pnl_by_sentiment.png")
    plt.close()

    # 2. Behavior: Trade Frequency by Sentiment
    plt.figure(figsize=(8,5))
    sns.barplot(data=df_filtered, x='Sentiment', y='Total_Trades', estimator=np.mean, ci=None, palette='pastel')
    plt.title("Average Trade Frequency by Market Sentiment")
    plt.ylabel("Trades per Day")
    plt.savefig("frequency_by_sentiment.png")
    plt.close()

    # 3. Segments: PnL by Volume Segment across Sentiment
    plt.figure(figsize=(9,6))
    sns.barplot(data=df_filtered, x='Volume_Segment', y='Daily_PnL', hue='Sentiment', ci=None)
    plt.title("Trader Performance: High vs Low Volume Segments")
    plt.ylabel("Avg Daily PnL (USD)")
    plt.savefig("segment_performance.png")
    plt.close()

def build_predictive_model(df):
    print("Training next-day profitability model (Bonus)...")
    df = df.sort_values(by=['Account', 'Date'])
    df['Next_Day_PnL'] = df.groupby('Account')['Daily_PnL'].shift(-1)
    df['Is_Profitable_Next_Day'] = (df['Next_Day_PnL'] > 0).astype(int)

    model_df = df.dropna(subset=['Next_Day_PnL']).copy()
    model_df['Sentiment_Fear'] = (model_df['Sentiment'] == 'Fear').astype(int)
    model_df['Sentiment_Greed'] = (model_df['Sentiment'] == 'Greed').astype(int)
    model_df['Win_Rate'] = model_df['Win_Rate'].fillna(0) # Impute NaNs for modeling

    features = ['Daily_PnL', 'Total_Trades', 'Avg_Trade_Size_USD', 'Win_Rate', 'Long_Short_Ratio', 'Sentiment_Fear', 'Sentiment_Greed']
    X = model_df[features]
    y = model_df['Is_Profitable_Next_Day']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    rf.fit(X_train, y_train)
    
    preds = rf.predict(X_test)
    print(f"Model Accuracy: {accuracy_score(y_test, preds):.2f}")
    
    joblib.dump(rf, 'profit_predictor.pkl')
    print("Model saved as profit_predictor.pkl")

if __name__ == "__main__":
    merged_df = load_and_clean_data(hist_path,fgi_path)
    daily_metrics = feature_engineering(merged_df)
    daily_metrics.to_csv("processed_daily_metrics.csv", index=False)
    generate_charts(daily_metrics)
    build_predictive_model(daily_metrics)
    print("Pipeline Complete! All assets generated.")
