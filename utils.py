"""
utils.py
--------
Business-logic / helper layer sitting between the Streamlit pages
and the database. Keeping all CRUD, validation, and export logic
here means the page modules stay thin and focused on UI.
"""

import io
from datetime import date, datetime

import pandas as pd

from database import get_session
from models import Expense, Budget

CATEGORIES = [
    "Food & Dining",
    "Groceries",
    "Transportation",
    "Housing & Rent",
    "Utilities",
    "Entertainment",
    "Health & Fitness",
    "Shopping",
    "Travel",
    "Education",
    "Insurance",
    "Personal Care",
    "Gifts & Donations",
    "Other",
]

PAYMENT_METHODS = [
    "Cash",
    "Credit Card",
    "Debit Card",
    "UPI",
    "Net Banking",
    "Wallet",
    "Other",
]


# ---------------------------------------------------------------
# Validation
# ---------------------------------------------------------------
def validate_expense(expense_date, category, description, amount, payment_method):
    """
    Validate expense form input.
    Returns (is_valid: bool, error_message: str)
    """
    errors = []

    if expense_date is None:
        errors.append("Date is required.")

    if not category:
        errors.append("Category is required.")

    if not description or not description.strip():
        errors.append("Description is required.")

    if amount is None or amount <= 0:
        errors.append("Amount must be a positive number greater than zero.")

    if not payment_method:
        errors.append("Payment method is required.")

    if errors:
        return False, " | ".join(errors)
    return True, ""


# ---------------------------------------------------------------
# CRUD - Create
# ---------------------------------------------------------------
def add_expense(expense_date, category, description, amount, payment_method, notes=""):
    """Insert a new expense record. Returns (success, message)."""
    is_valid, error = validate_expense(
        expense_date, category, description, amount, payment_method
    )
    if not is_valid:
        return False, error

    session = get_session()
    try:
        expense = Expense(
            date=expense_date,
            category=category,
            description=description.strip(),
            amount=round(float(amount), 2),
            payment_method=payment_method,
            notes=(notes or "").strip(),
            created_at=datetime.utcnow(),
        )
        session.add(expense)
        session.commit()
        return True, "Expense added successfully!"
    except Exception as exc:  # pragma: no cover
        session.rollback()
        return False, f"Error adding expense: {exc}"
    finally:
        session.close()


# ---------------------------------------------------------------
# CRUD - Read
# ---------------------------------------------------------------
def get_all_expenses_df():
    """Return all expenses as a Pandas DataFrame, sorted by date desc."""
    session = get_session()
    try:
        records = session.query(Expense).order_by(Expense.date.desc(), Expense.id.desc()).all()
        data = [r.to_dict() for r in records]
        df = pd.DataFrame(
            data,
            columns=[
                "id", "date", "category", "description",
                "amount", "payment_method", "notes", "created_at",
            ],
        )
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
        return df
    finally:
        session.close()


def get_expense_by_id(expense_id):
    session = get_session()
    try:
        return session.query(Expense).filter(Expense.id == expense_id).first()
    finally:
        session.close()


# ---------------------------------------------------------------
# CRUD - Update
# ---------------------------------------------------------------
def update_expense(expense_id, expense_date, category, description, amount, payment_method, notes=""):
    """Update an existing expense. Returns (success, message)."""
    is_valid, error = validate_expense(
        expense_date, category, description, amount, payment_method
    )
    if not is_valid:
        return False, error

    session = get_session()
    try:
        expense = session.query(Expense).filter(Expense.id == expense_id).first()
        if expense is None:
            return False, "Expense not found."

        expense.date = expense_date
        expense.category = category
        expense.description = description.strip()
        expense.amount = round(float(amount), 2)
        expense.payment_method = payment_method
        expense.notes = (notes or "").strip()

        session.commit()
        return True, "Expense updated successfully!"
    except Exception as exc:  # pragma: no cover
        session.rollback()
        return False, f"Error updating expense: {exc}"
    finally:
        session.close()


# ---------------------------------------------------------------
# CRUD - Delete
# ---------------------------------------------------------------
def delete_expense(expense_id):
    """Delete an expense by id. Returns (success, message)."""
    session = get_session()
    try:
        expense = session.query(Expense).filter(Expense.id == expense_id).first()
        if expense is None:
            return False, "Expense not found."
        session.delete(expense)
        session.commit()
        return True, "Expense deleted successfully!"
    except Exception as exc:  # pragma: no cover
        session.rollback()
        return False, f"Error deleting expense: {exc}"
    finally:
        session.close()


def delete_multiple_expenses(expense_ids):
    """Bulk-delete a list of expense ids. Returns (success, message)."""
    if not expense_ids:
        return False, "No expenses selected."
    session = get_session()
    try:
        session.query(Expense).filter(Expense.id.in_(expense_ids)).delete(
            synchronize_session=False
        )
        session.commit()
        return True, f"Deleted {len(expense_ids)} expense(s)."
    except Exception as exc:  # pragma: no cover
        session.rollback()
        return False, f"Error deleting expenses: {exc}"
    finally:
        session.close()


# ---------------------------------------------------------------
# Summary / dashboard metrics
# ---------------------------------------------------------------
def get_summary_metrics():
    """Compute the key numbers shown on the Dashboard summary cards."""
    df = get_all_expenses_df()

    today = pd.Timestamp(date.today())
    this_month_start = today.replace(day=1)

    total_expenses = df["amount"].sum() if not df.empty else 0.0
    total_transactions = len(df)

    if not df.empty:
        this_month_total = df.loc[df["date"] >= this_month_start, "amount"].sum()
        today_total = df.loc[df["date"] == today, "amount"].sum()
    else:
        this_month_total = 0.0
        today_total = 0.0

    return {
        "total_expenses": total_expenses,
        "this_month": this_month_total,
        "today": today_total,
        "total_transactions": total_transactions,
    }


# ---------------------------------------------------------------
# Budget
# ---------------------------------------------------------------
def get_current_month_key():
    return date.today().strftime("%Y-%m")


def get_budget(month_key=None):
    """Return the budget limit_amount for the given month (defaults to current)."""
    month_key = month_key or get_current_month_key()
    session = get_session()
    try:
        budget = session.query(Budget).filter(Budget.month == month_key).first()
        return budget.limit_amount if budget else 0.0
    finally:
        session.close()


def set_budget(amount, month_key=None):
    """Create or update the budget for a given month. Returns (success, message)."""
    if amount is None or amount < 0:
        return False, "Budget must be a non-negative number."

    month_key = month_key or get_current_month_key()
    session = get_session()
    try:
        budget = session.query(Budget).filter(Budget.month == month_key).first()
        if budget:
            budget.limit_amount = float(amount)
        else:
            budget = Budget(month=month_key, limit_amount=float(amount))
            session.add(budget)
        session.commit()
        return True, "Budget updated successfully!"
    except Exception as exc:  # pragma: no cover
        session.rollback()
        return False, f"Error updating budget: {exc}"
    finally:
        session.close()


# ---------------------------------------------------------------
# Export helpers
# ---------------------------------------------------------------
def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert a DataFrame to CSV bytes for st.download_button."""
    return df.to_csv(index=False).encode("utf-8")


def dataframe_to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Convert a DataFrame to an in-memory Excel file (bytes)."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Expenses")
    buffer.seek(0)
    return buffer.getvalue()


# ---------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------
def format_currency(value, symbol="$"):
    try:
        return f"{symbol}{value:,.2f}"
    except (TypeError, ValueError):
        return f"{symbol}0.00"
