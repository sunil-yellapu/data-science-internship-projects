# Market sentiment Analysis
# 📊 Trader Behavior vs Market Sentiment Analysis

## Project Overview

This project analyzes how **crypto trader performance and behavior change under different market sentiment conditions**, specifically **Fear vs Greed** periods based on the **Crypto Fear & Greed Index (FGI)**.

The analysis merges:

* **Trader historical transaction data**
* **Market sentiment data (Fear & Greed Index)**

The objective is to determine:

1. Whether **trading performance differs between Fear and Greed days**
2. Whether **trader behavior changes based on sentiment**
3. Identify **key trader segments**
4. Provide **data-backed insights using charts and tables**

---

# 📂 Dataset

### 1️⃣ Historical Trading Data

Contains:

| Column     | Description                       |
| ---------- | --------------------------------- |
| Account    | Trader ID                         |
| Date       | Trading date                      |
| Closed PnL | Profit or loss from closed trades |
| Size USD   | Position size                     |
| Leverage   | Trade leverage                    |
| Side       | Long / Short                      |
| Trade ID   | Unique trade                      |

---

### 2️⃣ Fear & Greed Index

Contains daily sentiment classification:

| Date       | Sentiment              |
| ---------- | ---------------------- |
| YYYY-MM-DD | Fear / Greed / Neutral |

---

# ⚙️ Data Processing Pipeline

### Step 1 — Data Cleaning

* Load historical trading dataset
* Load Fear & Greed Index dataset
* Convert timestamps to **date level**
* Merge datasets on **Date**

Result: Combined dataset containing **trader activity + sentiment**

---

### Step 2 — Feature Engineering

The dataset is aggregated **per trader per day per sentiment**.

Generated metrics:

| Feature        | Description                          |
| -------------- | ------------------------------------ |
| Daily_PnL      | Total profit/loss per trader per day |
| Total_Trades   | Number of trades executed            |
| Avg_Trade_Size | Average position size                |
| Avg_Leverage   | Average leverage used                |
| Win_Rate       | % of profitable trades               |
| Long_Ratio     | Percentage of long positions         |
| Short_Ratio    | Percentage of short positions        |

---

# 📊 Key Analysis Questions

---

# 1️⃣ Does performance differ between Fear vs Greed days?

### Chart: Average Daily PnL by Sentiment

Interpretation:

| Sentiment | Avg Daily PnL |
| --------- | ------------- |
| Fear      | Lower         |
| Greed     | Higher        |

### Insight

During **Greed periods**, traders tend to generate **higher average PnL**, likely due to strong bullish momentum.

During **Fear periods**, market volatility increases and profits decline.

---

# 2️⃣ Do traders change behavior based on sentiment?

The following behavioral metrics were analyzed:

| Behavior Metric    | Observation                      |
| ------------------ | -------------------------------- |
| Trade Frequency    | Higher during Greed              |
| Position Size      | Larger during Greed              |
| Leverage           | Higher during Fear               |
| Long vs Short Bias | More long positions during Greed |

### Chart Examples

Your notebook generates:

1️⃣ **Average Trade Size by Sentiment**
2️⃣ **Average Leverage by Sentiment**
3️⃣ **Win Rate by Sentiment**

### Key Behavior Insight

Traders become:

**Aggressive in Greed markets**

* Larger position sizes
* More trades
* Long bias

**Defensive or speculative in Fear markets**

* Higher leverage
* More short trades

---

# 3️⃣ Trader Segmentation

Three key trader segments were identified.

---

## Segment 1 — High Leverage vs Low Leverage Traders

| Segment               | Characteristics   |
| --------------------- | ----------------- |
| High Leverage Traders | Use leverage > 5x |
| Low Leverage Traders  | Use leverage ≤ 5x |

### Insight

High leverage traders experience:

* Higher profits in Greed
* Larger drawdowns in Fear

Low leverage traders show **more stable performance**.

---

## Segment 2 — Frequent vs Infrequent Traders

| Segment            | Definition            |
| ------------------ | --------------------- |
| Frequent Traders   | > Median daily trades |
| Infrequent Traders | ≤ Median daily trades |

### Insight

Frequent traders:

* Trade more during **Greed periods**
* Capture momentum opportunities

Infrequent traders:

* Exhibit **more stable win rates**
* Less exposed to volatility

---

## Segment 3 — Consistent vs Inconsistent Traders

| Segment              | Definition     |
| -------------------- | -------------- |
| Consistent Winners   | Win rate > 60% |
| Inconsistent Traders | Win rate ≤ 60% |

### Insight

Consistent traders:

* Maintain profitability regardless of sentiment
* Use **lower leverage**
* Maintain **controlled trade sizes**

Inconsistent traders:

* Overtrade during Greed
* Experience heavy losses during Fear

---

# 📈 Key Insights (Backed by Charts)

## Insight 1 — Market Sentiment Influences Profitability

Greed periods show **higher average trader profitability** compared to Fear periods.

Reason:

* Strong bullish momentum
* Higher liquidity

---

## Insight 2 — Trader Risk Behavior Changes With Sentiment

During Fear markets:

* Traders increase **leverage**
* Attempt to capture sharp rebounds

This increases **risk exposure and drawdowns**.

---

## Insight 3 — Aggressive Traders Perform Worse Long Term

High-leverage and frequent traders show:

* Higher volatility in profits
* Lower overall consistency

More disciplined traders maintain **better long-term profitability**.

---

# 📊 Charts Generated

The notebook automatically generates the following visualizations:

1️⃣ Average PnL by Sentiment
2️⃣ Average Trade Size by Sentiment
3️⃣ Average Leverage by Sentiment

These charts provide visual confirmation of behavioral differences between **Fear and Greed markets**.

---

# 🤖 Predictive Modeling

A **Random Forest model** was trained to predict:

### Target

```
Is the next trading day profitable?
```

### Features used

* Lagged Daily PnL
* Lagged Win Rate
* Trade Frequency
* Average Trade Size
* Average Leverage
* Sentiment

### Model Goal

Predict trader profitability based on:

* Past performance
* Market sentiment
* Trading behavior

---

# 🧰 Tech Stack

* Python
* Pandas
* NumPy
* Seaborn
* Matplotlib
* Scikit-Learn

---

# 🚀 How to Run

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

Run notebook:

```
sentiment_analysis.ipynb
```

Output generated:

```
processed_daily_metrics.csv
```

---

# 📌 Conclusion

The analysis shows that **market sentiment strongly influences trader behavior and performance**.

Key takeaways:

1️⃣ Traders perform better during **Greed periods**
2️⃣ **Risk-taking increases during Fear markets**
3️⃣ **Disciplined traders outperform aggressive traders over time**

Understanding these patterns can help trading platforms:

* Identify risk-prone users
* Improve risk management systems
* Build better trading analytics tools.

---

Give me a structured readme file with clear structure: Business statement-> Approach-> Key Insights -> Model explanation
