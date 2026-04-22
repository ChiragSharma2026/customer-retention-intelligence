import streamlit as st
import os
from loader import main as build_database
if not os.path.exists("retail.db"):
    build_database()
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from analysis import (
    get_customer_segments,
    get_revenue_share_by_segment,
    get_top20_revenue_contribution,
    get_churn_rate,
    get_retention_rates
)

from queries import (
    total_revenue,
    monthly_revenue,
    product_performance,
    repeat_vs_new_customers
)

st.set_page_config(
    page_title="Customer Retention & Revenue Intelligence",
    page_icon="📊",
    layout="wide"
)
st.title("📊 Customer Retention & Revenue Intelligence System")
st.markdown("**Dataset:** Olist Brazilian E-Commerce | **Records:** 96,478 delivered orders")
st.markdown("---")
st.header("🟢 Section 1: Business Overview")
col1, col2, col3, col4 = st.columns(4)
rev = total_revenue()['total_revenue'].iloc[0]
repeat_df = repeat_vs_new_customers()
one_time = repeat_df['one_time_customers'].iloc[0]
repeat = repeat_df['repeat_customers'].iloc[0]
total_customers = one_time + repeat
churn = get_churn_rate()
top20 = get_top20_revenue_contribution()

with col1:
    st.metric("💰 Total Revenue", f"R$ {rev:,.2f}")
with col2:
    st.metric("👥 Total Customers", f"{total_customers:,}")
with col3:
    st.metric("🔁 Churn Rate", f"{churn}%")
with col4:
    st.metric("🏆 Top 20% Revenue Share", f"{top20}%")

st.markdown("---")
st.header("🟢 Section 2: Monthly Revenue Trend")
monthly_df = monthly_revenue()

fig1 = px.line(
    monthly_df,
    x='month',
    y='revenue',
    title='Monthly Revenue Trend',
    markers=True,
    labels={'month': 'Month', 'revenue': 'Revenue (R$)'}
)
fig1.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig1, use_container_width=True)
st.markdown("---")
st.header("🟢 Section 3: Customer Segmentation")
seg_df = get_revenue_share_by_segment()
col1, col2 = st.columns(2)

with col1:
    fig2 = px.pie(
        seg_df,
        names='segment',
        values='lifetime_value',
        title='Revenue Share by Customer Segment',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    fig3 = px.bar(
        seg_df,
        x='segment',
        y='revenue_share_%',
        title='Revenue Share % by Segment',
        color='segment',
        text='revenue_share_%',
        labels={'revenue_share_%': 'Revenue Share (%)'}
    )
    fig3.update_traces(texttemplate='%{text}%', textposition='outside')
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.header("🟢 Section 4: Retention & Cohort Analysis")
retention_df = get_retention_rates()
cohort_pivot = retention_df.pivot_table(
    index='cohort_month',
    columns='order_month',
    values='retention_%'
).fillna(0)

fig4 = go.Figure(data=go.Heatmap(
    z=cohort_pivot.values,
    x=cohort_pivot.columns.tolist(),
    y=cohort_pivot.index.tolist(),
    colorscale='Blues',
    text=cohort_pivot.values.round(1),
    texttemplate='%{text}%'
))
fig4.update_layout(
    title='Cohort Retention Heatmap',
    xaxis_title='Order Month',
    yaxis_title='Cohort Month',
    xaxis_tickangle=-45
)
st.plotly_chart(fig4, use_container_width=True)
st.markdown("---")

st.header("🟢 Section 5: Product Performance")
prod_df = product_performance()
fig5 = px.bar(
    prod_df,
    x='revenue',
    y='category',
    orientation='h',
    title='Top 15 Product Categories by Revenue',
    color='revenue',
    color_continuous_scale='Blues',
    labels={'revenue': 'Revenue (R$)', 'category': 'Category'}
)
fig5.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig5, use_container_width=True)
st.markdown("---")

st.header("🔴 Section 6: Key Business Insights")
st.markdown(f"""
- 💰 **Total revenue of R$ {rev:,.2f}** generated across all delivered orders.
- 🏆 **Top 20% of customers contribute {top20}% of total revenue** — classic power law distribution.
- 📉 **{churn}% of customers never return after their first purchase** — churn is the biggest threat to growth.
- 👥 Out of **{total_customers:,} unique customers**, only **{repeat:,} are repeat buyers**.
- 📦 **Health & Beauty is the top revenue category** — ideal target for loyalty programs.
- 📆 **Cohort analysis shows retention collapses after month 1** — onboarding experience is critical.
""")
st.markdown("---")

st.header("🔴 Section 7: Business Recommendations")
st.markdown("""
- 🎯 **Launch a loyalty program targeting High-value segment** — they drive 67.8% of revenue and must be retained.
- 📧 **Implement post-purchase email sequences** — most churn happens after order 1, automated follow-ups can recover buyers.
- 🛍️ **Cross-sell Health & Beauty with Watches & Gifts** — top 2 categories, high affinity likely exists.
- 📊 **Investigate Oct-Nov 2016 cohort drop-off** — sharp retention fall visible in cohort heatmap needs root cause analysis.
- 💳 **Introduce subscription or bundle offers for Mid-value segment** — easiest group to push into High value.
""")

