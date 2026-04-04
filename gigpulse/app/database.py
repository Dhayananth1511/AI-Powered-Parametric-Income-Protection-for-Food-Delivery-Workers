from pathlib import Path
import sys
import tempfile
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent.parent

default_db_path = PROJECT_ROOT / "gigpulse.db"
test_db_path = Path(tempfile.gettempdir()) / "gigpulse_test.db"
recovery_db_path = Path(tempfile.gettempdir()) / "gigpulse_recovered.db"

is_pytest = (
    "PYTEST_CURRENT_TEST" in os.environ
    or any("pytest" in arg.lower() for arg in sys.argv)
)
default_database_url = f"sqlite:///{test_db_path}" if is_pytest else f"sqlite:///{default_db_path}"

DATABASE_URL = default_database_url if is_pytest else os.getenv("DATABASE_URL", default_database_url)

if DATABASE_URL.startswith("sqlite:///"):
    sqlite_path = Path(DATABASE_URL.replace("sqlite:///", "", 1))
    if not sqlite_path.is_absolute():
        sqlite_path = (PROJECT_ROOT / sqlite_path).resolve()

    sqlite_path.parent.mkdir(parents=True, exist_ok=True)

    if not is_pytest and sqlite_path.exists():
        try:
            conn = sqlite3.connect(sqlite_path)
            conn.execute("PRAGMA integrity_check;").fetchone()
            conn.close()
        except sqlite3.Error:
            sqlite_path = recovery_db_path.resolve()
            sqlite_path.parent.mkdir(parents=True, exist_ok=True)

    DATABASE_URL = f"sqlite:///{sqlite_path}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
