"""
models.py
---------
SQLAlchemy ORM models used by the Personal Expense Tracker.

Expense  -> a single transaction record
Budget   -> the monthly budget limit set by the user (single row table)
"""

from datetime import datetime, date

from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Expense(Base):
    """Represents a single expense transaction."""

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False, default=date.today)
    category = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert the ORM object into a plain dict (handy for Pandas)."""
        return {
            "id": self.id,
            "date": self.date,
            "category": self.category,
            "description": self.description,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "notes": self.notes,
            "created_at": self.created_at,
        }


class Budget(Base):
    """
    Stores the monthly budget limit.

    We keep this as a simple table keyed by 'YYYY-MM' so that a
    different budget can (optionally) be set for each month, while
    the utils layer always reads/writes the current month's row.
    """

    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(String(7), unique=True, nullable=False)  # e.g. "2026-07"
    limit_amount = Column(Float, nullable=False, default=0.0)
