"""
app_pages/analytics.py
------------------------
Interactive Plotly visualizations: monthly spending trend,
category-wise pie chart, payment method distribution, and a
cumulative spending trend line.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from utils import get_all_expenses_df, format_currency


def render():
    st.title("📈 Analytics")
    st.caption("Understand where your money goes.")

    df = get_all_expenses_df()

    if df.empty:
        st.info("Add some expenses first to unlock analytics.")
        return

    df["month"] = df["date"].dt.to_period("M").astype(str)

    # ---------------- Row 1: Monthly spending + Category pie ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Monthly Spending")
        monthly = df.groupby("month")["amount"].sum().reset_index().sort_values("month")
        fig = px.bar(
            monthly, x="month", y="amount",
            labels={"month": "Month", "amount": "Total Spent"},
            color_discrete_sequence=["#3b82f6"],
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=340,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Spending by Category")
        by_cat = df.groupby("category")["amount"].sum().reset_index()
        fig = px.pie(
            by_cat, names="category", values="amount", hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=340)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Row 2: Payment method + Trend ----------------
    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Payment Method Distribution")
        by_method = df.groupby("payment_method")["amount"].sum().reset_index()
        fig = px.bar(
            by_method.sort_values("amount"), x="amount", y="payment_method",
            orientation="h",
            labels={"amount": "Total Spent", "payment_method": "Method"},
            color_discrete_sequence=["#10b981"],
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=340,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Cumulative Spending Trend")
        daily = df.groupby(df["date"].dt.date)["amount"].sum().reset_index()
        daily.columns = ["date", "amount"]
        daily = daily.sort_values("date")
        daily["cumulative"] = daily["amount"].cumsum()
        fig = px.line(
            daily, x="date", y="cumulative", markers=True,
            labels={"date": "Date", "cumulative": "Cumulative Spend"},
            color_discrete_sequence=["#8b5cf6"],
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=340,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Category breakdown table ----------------
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("Category Breakdown")
    breakdown = df.groupby("category")["amount"].agg(["sum", "count", "mean"]).reset_index()
    breakdown.columns = ["Category", "Total Spent", "Transactions", "Avg per Transaction"]
    breakdown["Total Spent"] = breakdown["Total Spent"].apply(format_currency)
    breakdown["Avg per Transaction"] = breakdown["Avg per Transaction"].apply(format_currency)
    breakdown = breakdown.sort_values("Transactions", ascending=False)
    st.dataframe(breakdown, hide_index=True, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
