"""
database.py
------------
Handles the SQLAlchemy engine, session factory, and database
initialization for the Personal Expense Tracker.

All other modules should import `get_session()` / `SessionLocal`
from here rather than creating their own engine, so the whole
app shares a single SQLite database file.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

# ---------------------------------------------------------------
# Database configuration
# ---------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "expenses.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# `check_same_thread=False` is required because Streamlit can
# access the same connection from different threads/reruns.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    """Create all tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Return a new SQLAlchemy session."""
    return SessionLocal()
