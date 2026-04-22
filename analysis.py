import pandas as pd
import numpy as np
from queries import (
    customer_lifetime_value,
    repeat_vs_new_customers,
    monthly_revenue,
    cohort_analysis,
    top_customer_contribution,
    product_performance,
    total_revenue
)
def get_customer_segments():
    df = customer_lifetime_value()
    df['segment'] = pd.qcut(
        df['lifetime_value'],
        q=3,
        labels=['Low', 'Mid', 'High']
    )
    return df

def get_revenue_share_by_segment():
    df = get_customer_segments()
    segment_revenue = df.groupby('segment')['lifetime_value'].sum().reset_index()
    segment_revenue['revenue_share_%'] = (
        segment_revenue['lifetime_value'] / segment_revenue['lifetime_value'].sum() * 100
    ).round(2)
    return segment_revenue

def get_top20_revenue_contribution():
    df = top_customer_contribution()
    top_20_cutoff = int(len(df) * 0.2)
    top_20_revenue = df.head(top_20_cutoff)['revenue'].sum()
    total = df['total_revenue'].iloc[0]
    contribution = round((top_20_revenue / total) * 100, 2)
    return contribution

def get_retention_rates():
    df = cohort_analysis()
    cohort_sizes = df[df['cohort_month'] == df['order_month']][['cohort_month', 'users']]
    cohort_sizes = cohort_sizes.rename(columns={'users': 'cohort_size'})
    df = df.merge(cohort_sizes, on='cohort_month')
    df['retention_%'] = (df['users'] / df['cohort_size'] * 100).round(2)
    return df

def get_churn_rate():
    df = repeat_vs_new_customers()
    one_time = df['one_time_customers'].iloc[0]
    total = one_time + df['repeat_customers'].iloc[0]
    churn_rate = round((one_time / total) * 100, 2)
    return churn_rate

if __name__ == "__main__":
    print("Customer Segments:")
    print(get_customer_segments().head())
    print("\nRevenue Share by Segment:")
    print(get_revenue_share_by_segment())
    print("\nTop 20% Customer Revenue Contribution:")
    print(get_top20_revenue_contribution(), "%")
    print("\nChurn Rate:")
    print(get_churn_rate(), "%")
    print("\nRetention Rates (first 5 rows):")
    print(get_retention_rates().head())