# 💸 Personal Expense Tracker

A modern personal expense tracker built with **Streamlit**, **SQLite**, **SQLAlchemy**, **Pandas**, and **Plotly**.

## Features

- **Dashboard** — summary cards (Total Expenses, This Month, Today, Total Transactions), a 14-day spending chart, and recent transactions.
- **Add Expense** — validated form (date, category, description, amount, payment method, notes).
- **Transactions** — search, filter (category / payment method / date range), inline edit, single & bulk delete.
- **Analytics** — monthly spending bar chart, category pie chart, payment method distribution, cumulative spending trend, and a category breakdown table.
- **Budget Tracker** — set a monthly budget, see remaining budget, and get color-coded alerts (green/amber/red) with a gauge chart.
- **Export** — download filtered transactions as CSV or Excel.

## Project Structure

```
expense_tracker/
├── app.py                  # Main entry point & sidebar navigation
├── database.py              # SQLAlchemy engine/session setup
├── models.py                 # ORM models: Expense, Budget
├── utils.py                   # CRUD, validation, exports, budget logic
├── style.py                    # Custom CSS + card rendering helpers
├── app_pages/
│   ├── dashboard.py
│   ├── add_expense.py
│   ├── transactions.py
│   ├── analytics.py
│   └── budget.py
├── requirements.txt
└── expenses.db               # SQLite database (auto-created on first run)
```

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

The SQLite database (`expenses.db`) is created automatically on first run — no manual setup needed.

## Deploy to Render

1. Create a Render account at https://render.com.
2. Connect your GitHub repository.
3. Add a new **Web Service** and select the `main` branch.
4. Use these settings:
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port $PORT --server.headless true`
5. Deploy and wait for Render to finish building.

Your app is ready to run on Render with the existing `render.yaml` config.

## Notes

- All database access goes through SQLAlchemy ORM (no raw SQL).
- Amounts must be positive numbers; date, category, description, and payment method are required fields.
- The budget is tracked per calendar month (`YYYY-MM`), so setting a new budget only affects the current month.
