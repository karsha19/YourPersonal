"""
app_pages/budget.py
---------------------
Set a monthly budget, visualize how much has been spent vs.
remaining, and show clear alerts when the limit is exceeded.
"""

from datetime import date

import streamlit as st
import plotly.graph_objects as go

from utils import get_budget, set_budget, get_all_expenses_df, format_currency, get_current_month_key


def render():
    st.title("🎯 Budget Tracker")
    st.caption("Stay in control of your monthly spending.")

    month_key = get_current_month_key()
    month_label = date.today().strftime("%B %Y")

    current_budget = get_budget(month_key)

    # ---------------- Set budget ----------------
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader(f"Monthly Budget — {month_label}")
    col1, col2 = st.columns([2, 1])
    with col1:
        new_budget = st.number_input(
            "Set your budget amount", min_value=0.0, step=50.0,
            value=float(current_budget), format="%.2f",
        )
    with col2:
        st.write("")
        st.write("")
        if st.button("💾 Save Budget", use_container_width=True):
            success, message = set_budget(new_budget, month_key)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
    st.markdown("</div>", unsafe_allow_html=True)

    if current_budget <= 0:
        st.info("Set a monthly budget above to start tracking your progress.")
        return

    # ---------------- Spend vs budget ----------------
    df = get_all_expenses_df()
    if df.empty:
        spent = 0.0
    else:
        month_start = date.today().replace(day=1)
        spent = df.loc[df["date"] >= str(month_start), "amount"].sum()

    remaining = current_budget - spent
    pct_used = (spent / current_budget * 100) if current_budget > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Budget", format_currency(current_budget))
    with col2:
        st.metric("Spent So Far", format_currency(spent))
    with col3:
        st.metric("Remaining", format_currency(remaining), delta=None)

    # ---------------- Alert banner ----------------
    if pct_used >= 100:
        st.markdown(
            f'<div class="budget-danger">🚨 You have exceeded your budget by '
            f'{format_currency(abs(remaining))} ({pct_used:.0f}% used)!</div>',
            unsafe_allow_html=True,
        )
    elif pct_used >= 80:
        st.markdown(
            f'<div class="budget-warn">⚠️ You have used {pct_used:.0f}% of your budget. '
            f'Only {format_currency(remaining)} left this month.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="budget-ok">✅ You are on track — {pct_used:.0f}% of your budget used, '
            f'{format_currency(remaining)} remaining.</div>',
            unsafe_allow_html=True,
        )

    st.write("")

    # ---------------- Gauge chart ----------------
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    gauge_color = "#ef4444" if pct_used >= 100 else ("#f59e0b" if pct_used >= 80 else "#10b981")
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=min(pct_used, 150),
            number={"suffix": "%"},
            title={"text": "Budget Utilization"},
            gauge={
                "axis": {"range": [0, 150]},
                "bar": {"color": gauge_color},
                "steps": [
                    {"range": [0, 80], "color": "#ecfdf5"},
                    {"range": [80, 100], "color": "#fffbeb"},
                    {"range": [100, 150], "color": "#fef2f2"},
                ],
                "threshold": {
                    "line": {"color": "black", "width": 3},
                    "thickness": 0.8,
                    "value": 100,
                },
            },
        )
    )
    fig.update_layout(height=320, margin=dict(l=20, r=20, t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
