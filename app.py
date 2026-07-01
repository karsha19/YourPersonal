"""
app.py
------
Entry point for the Personal Expense Tracker Streamlit app.

Run with:
    streamlit run app.py
"""

import streamlit as st

from database import init_db
from style import inject_custom_css
from app_pages import dashboard, add_expense, transactions, analytics, budget

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize DB tables (safe to call every run — no-op if they exist)
init_db()

# Inject custom CSS
inject_custom_css(st)

# ---------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------
with st.sidebar:
    st.markdown('<p class="sidebar-brand">💸 ExpenseTracker</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-sub">Manage your money, smartly.</p>', unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        options=["Dashboard", "Add Expense", "Transactions", "Analytics", "Budget Tracker"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.caption("Built with Streamlit · SQLAlchemy · Plotly")

# ---------------------------------------------------------------
# Page routing
# ---------------------------------------------------------------
PAGES = {
    "Dashboard": dashboard.render,
    "Add Expense": add_expense.render,
    "Transactions": transactions.render,
    "Analytics": analytics.render,
    "Budget Tracker": budget.render,
}

PAGES[page]()
