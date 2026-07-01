"""
app_pages/transactions.py
---------------------------
Full transaction browser: search + filter + inline edit/delete.
"""

import streamlit as st
import pandas as pd

from utils import (
    get_all_expenses_df,
    update_expense,
    delete_expense,
    delete_multiple_expenses,
    CATEGORIES,
    PAYMENT_METHODS,
    format_currency,
    dataframe_to_csv_bytes,
    dataframe_to_excel_bytes,
)


def _apply_filters(df, search, categories, methods, date_range):
    filtered = df.copy()

    if search:
        mask = (
            filtered["description"].str.contains(search, case=False, na=False)
            | filtered["notes"].fillna("").str.contains(search, case=False, na=False)
        )
        filtered = filtered[mask]

    if categories:
        filtered = filtered[filtered["category"].isin(categories)]

    if methods:
        filtered = filtered[filtered["payment_method"].isin(methods)]

    if date_range and len(date_range) == 2:
        start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        filtered = filtered[(filtered["date"] >= start) & (filtered["date"] <= end)]

    return filtered


def _edit_dialog(row):
    """Inline edit form shown inside an expander for a given row."""
    with st.form(f"edit_form_{row['id']}"):
        col1, col2 = st.columns(2)
        with col1:
            new_date = st.date_input("Date", value=row["date"].date(), key=f"date_{row['id']}")
            new_category = st.selectbox(
                "Category", CATEGORIES,
                index=CATEGORIES.index(row["category"]) if row["category"] in CATEGORIES else 0,
                key=f"cat_{row['id']}",
            )
            new_amount = st.number_input(
                "Amount", min_value=0.0, value=float(row["amount"]), step=1.0,
                format="%.2f", key=f"amt_{row['id']}",
            )
        with col2:
            new_method = st.selectbox(
                "Payment Method", PAYMENT_METHODS,
                index=PAYMENT_METHODS.index(row["payment_method"])
                if row["payment_method"] in PAYMENT_METHODS else 0,
                key=f"pm_{row['id']}",
            )
            new_description = st.text_input("Description", value=row["description"], key=f"desc_{row['id']}")
            new_notes = st.text_area("Notes", value=row["notes"] or "", key=f"notes_{row['id']}", height=68)

        col_a, col_b = st.columns(2)
        with col_a:
            save = st.form_submit_button("💾 Save Changes", use_container_width=True)
        with col_b:
            cancel = st.form_submit_button("Cancel", use_container_width=True)

        if save:
            success, message = update_expense(
                row["id"], new_date, new_category, new_description,
                new_amount, new_method, new_notes,
            )
            if success:
                st.success(message)
                st.session_state.pop(f"editing_{row['id']}", None)
                st.rerun()
            else:
                st.error(message)

        if cancel:
            st.session_state.pop(f"editing_{row['id']}", None)
            st.rerun()


def render():
    st.title("📋 Transactions")
    st.caption("Search, filter, edit, or delete your expenses.")

    df = get_all_expenses_df()

    if df.empty:
        st.info("No transactions recorded yet. Head over to **Add Expense** to get started.")
        return

    # ---------------- Filters ----------------
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns([1.4, 1, 1, 1.2])
    with f1:
        search = st.text_input("🔍 Search description / notes")
    with f2:
        categories = st.multiselect("Category", CATEGORIES)
    with f3:
        methods = st.multiselect("Payment Method", PAYMENT_METHODS)
    with f4:
        min_date = df["date"].min().date()
        max_date = df["date"].max().date()
        date_range = st.date_input("Date range", value=(min_date, max_date))
    st.markdown("</div>", unsafe_allow_html=True)

    filtered_df = _apply_filters(df, search, categories, methods, date_range)

    st.markdown(
        f"**{len(filtered_df)}** transaction(s) found &nbsp;·&nbsp; "
        f"Total: **{format_currency(filtered_df['amount'].sum())}**"
    )

    # ---------------- Export ----------------
    exp_col1, exp_col2, _ = st.columns([1, 1, 3])
    with exp_col1:
        st.download_button(
            "⬇️ Export CSV",
            data=dataframe_to_csv_bytes(filtered_df.drop(columns=["created_at"])),
            file_name="expenses.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with exp_col2:
        st.download_button(
            "⬇️ Export Excel",
            data=dataframe_to_excel_bytes(filtered_df.drop(columns=["created_at"])),
            file_name="expenses.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    st.write("")

    # ---------------- Bulk delete ----------------
    display_df = filtered_df.copy()
    display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
    display_df["amount_fmt"] = display_df["amount"].apply(format_currency)

    st.markdown("### Transaction List")

    select_all = st.checkbox("Select all visible for bulk delete")
    selected_ids = []

    for _, row in filtered_df.iterrows():
        row_id = row["id"]
        with st.container():
            cols = st.columns([0.4, 1, 1.3, 2.3, 1.1, 1.3, 0.7, 0.7])
            checked = cols[0].checkbox("", value=select_all, key=f"sel_{row_id}", label_visibility="collapsed")
            if checked:
                selected_ids.append(row_id)
            cols[1].write(row["date"].strftime("%b %d, %Y"))
            cols[2].write(row["category"])
            cols[3].write(row["description"])
            cols[4].write(row["payment_method"])
            cols[5].write(format_currency(row["amount"]))
            if cols[6].button("✏️", key=f"edit_btn_{row_id}"):
                st.session_state[f"editing_{row_id}"] = True
            if cols[7].button("🗑️", key=f"del_btn_{row_id}"):
                success, message = delete_expense(row_id)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

            if st.session_state.get(f"editing_{row_id}"):
                with st.expander(f"Edit expense #{row_id}", expanded=True):
                    _edit_dialog(row)

        st.divider()

    if selected_ids:
        if st.button(f"🗑️ Delete {len(selected_ids)} selected", type="primary"):
            success, message = delete_multiple_expenses(selected_ids)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
