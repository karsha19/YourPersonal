"""
app_pages/add_expense.py
--------------------------
Form for adding a new expense, with client-side + server-side
(validate_expense) validation.
"""

from datetime import date

import streamlit as st

from utils import add_expense, CATEGORIES, PAYMENT_METHODS


def render():
    st.title("➕ Add Expense")
    st.caption("Record a new transaction.")

    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    with st.form("add_expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            expense_date = st.date_input("Date *", value=date.today(), max_value=date.today())
            category = st.selectbox("Category *", CATEGORIES)
            amount = st.number_input(
                "Amount *", min_value=0.0, step=1.0, format="%.2f",
                help="Amount must be greater than zero."
            )
        with col2:
            payment_method = st.selectbox("Payment Method *", PAYMENT_METHODS)
            description = st.text_input("Description *", placeholder="e.g. Grocery shopping at Walmart")
            notes = st.text_area("Notes (optional)", placeholder="Any extra details...", height=68)

        submitted = st.form_submit_button("Save Expense", use_container_width=True)

        if submitted:
            success, message = add_expense(
                expense_date, category, description, amount, payment_method, notes
            )
            if success:
                st.success(f"✅ {message}")
                st.balloons()
            else:
                st.error(f"⚠️ {message}")

    st.markdown("</div>", unsafe_allow_html=True)

    st.info("Fields marked with * are required. Amount must be a positive number.")
