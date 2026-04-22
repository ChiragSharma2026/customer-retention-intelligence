# 📊 Customer Retention & Revenue Intelligence System

A end-to-end data analysis system built to analyze customer purchase behavior,
identify revenue drivers, detect churn patterns, and provide actionable business
recommendations.

---

## 🗂️ Dataset

- **Source:** [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle)
- **Records:** 96,478 delivered orders
- **Customers:** 93,358 unique customers
- **Period:** October 2016 – August 2018

---

## 🛠️ Tech Stack

- **Python** — data cleaning, analysis, segmentation
- **SQLite** — relational database with 4 normalized tables
- **SQL** — revenue analysis, cohort analysis, window functions, CTEs
- **Pandas & NumPy** — data manipulation and retention calculations
- **Plotly** — interactive charts and cohort heatmap
- **Streamlit** — web dashboard

---

## 🧱 Database Design

Four normalized tables built from raw CSVs:

- `customers` — unique customer IDs and state
- `orders` — order ID, customer ID, order date
- `order_items` — product, quantity, unit price, total price
- `products` — product ID and category

---

## 🔥 SQL Analysis

Queries written against SQLite covering:

- Total revenue aggregation
- Monthly revenue trend
- Repeat vs one-time customer segmentation
- Customer Lifetime Value (CLV)
- Top customer revenue contribution using **window functions**
- **Cohort analysis** using CTEs to track retention month-over-month
- Product category performance

---

## 📊 Key Business Insights

| Metric | Value |
|---|---|
| Total Revenue | R$ 15,843,553.24 |
| Total Unique Customers | 93,358 |
| Repeat Customers | 2,801 |
| Churn Rate | 97.0% |
| Top 20% Customer Revenue Share | 53.52% |
| High Segment Revenue Share | 67.8% |

- 🏆 **Top 20% of customers drive 53.52% of total revenue** — classic power law
- 📉 **97% of customers never return after first purchase** — churn is the core business problem
- 📦 **Health & Beauty is the #1 revenue category** at R$ 1.44M
- 📆 **Retention collapses after Month 1** across all cohorts — onboarding is broken

---

## 💡 Business Recommendations

- 🎯 Launch a loyalty program targeting the High-value segment — they drive 67.8% of revenue
- 📧 Implement post-purchase email sequences — most churn happens after order 1
- 🛍️ Cross-sell Health & Beauty with Watches & Gifts — top 2 categories
- 📊 Investigate Oct-Nov 2016 cohort drop-off visible in the heatmap
- 💳 Introduce bundle offers for Mid-value segment to push them into High

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/ChiragSharma2026/customer-retention-intelligence

# Install dependencies
pip install -r requirements.txt

# Build the database
python loader.py

# Launch the dashboard
streamlit run app.py
```

---

## 📁 Project Structure
├── archive/                  # Raw Olist CSV files
├── loader.py                 # Data cleaning + SQLite ingestion
├── queries.py                # SQL analysis queries
├── analysis.py               # Segmentation + retention calculations
├── app.py                    # Streamlit dashboard
├── requirements.txt
└── README.md

---