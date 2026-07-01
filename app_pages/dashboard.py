"""
app_pages/dashboard.py
-----------------------
The landing page: summary metric cards + a quick recent-activity
view and a small trend chart.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from utils import get_summary_metrics, get_all_expenses_df, format_currency
from style import render_metric_card


def render():
    st.title("📊 Dashboard")
    st.caption("A quick snapshot of your spending.")

    metrics = get_summary_metrics()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card(
            st, "💰", "Total Expenses",
            format_currency(metrics["total_expenses"]), "card-blue"
        )
    with col2:
        render_metric_card(
            st, "📅", "This Month",
            format_currency(metrics["this_month"]), "card-green"
        )
    with col3:
        render_metric_card(
            st, "☀️", "Today's Expenses",
            format_currency(metrics["today"]), "card-orange"
        )
    with col4:
        render_metric_card(
            st, "🧾", "Total Transactions",
            f"{metrics['total_transactions']:,}", "card-purple"
        )

    st.write("")
    st.write("")

    df = get_all_expenses_df()

    left, right = st.columns([1.4, 1])

    with left:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Spending — Last 14 Days")
        if df.empty:
            st.info("No expenses yet. Add your first expense to see trends here.")
        else:
            cutoff = pd.Timestamp.today().normalize() - pd.Timedelta(days=13)
            recent = df[df["date"] >= cutoff]
            daily = recent.groupby(recent["date"].dt.date)["amount"].sum().reset_index()
            daily.columns = ["date", "amount"]
            fig = px.bar(
                daily, x="date", y="amount",
                labels={"date": "Date", "amount": "Amount"},
                color_discrete_sequence=["#3b82f6"],
            )
            fig.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=320,
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Recent Transactions")
        if df.empty:
            st.info("Nothing to show yet.")
        else:
            recent_txns = df.head(6)[["date", "category", "description", "amount"]].copy()
            recent_txns["date"] = recent_txns["date"].dt.strftime("%b %d, %Y")
            recent_txns["amount"] = recent_txns["amount"].apply(format_currency)
            st.dataframe(recent_txns, hide_index=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
