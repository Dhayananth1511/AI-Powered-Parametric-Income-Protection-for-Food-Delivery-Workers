from pathlib import Path
import sys
import tempfile
import sqlite3
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent.parent

default_db_path = PROJECT_ROOT / "gigpulse.db"
test_db_path    = Path(tempfile.gettempdir()) / "gigpulse_test.db"
recovery_db_path = Path(tempfile.gettempdir()) / "gigpulse_recovered.db"

is_pytest = (
    "PYTEST_CURRENT_TEST" in os.environ
    or any("pytest" in arg.lower() for arg in sys.argv)
)

default_database_url = f"sqlite:///{test_db_path}" if is_pytest else f"sqlite:///{default_db_path}"
DATABASE_URL = default_database_url if is_pytest else os.getenv("DATABASE_URL", default_database_url)

# Render / Supabase / Neon fix: replace legacy "postgres://" prefix
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

IS_SQLITE = DATABASE_URL.startswith("sqlite")

# ── SQLite path resolution & integrity check ──────────────────────────────────
if IS_SQLITE:
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

# ── Engine configuration ───────────────────────────────────────────────────────
if IS_SQLITE:
    # SQLite — single-file, connection check_same_thread workaround
    engine_kwargs = {
        "connect_args": {"check_same_thread": False},
    }
else:
    # PostgreSQL (Supabase / Neon / Render) — production connection pool
    engine_kwargs = {
        "pool_size":     10,    # keep 10 warm connections in the pool
        "max_overflow":  20,    # allow 20 extra connections under peak load
        "pool_pre_ping": True,  # health-check connection before each use
        "pool_recycle":  300,   # recycle idle connections every 5 minutes
        "pool_timeout":  30,    # raise error if no connection available in 30s
        "echo":          False, # set True temporarily for query debugging
    }

engine = create_engine(DATABASE_URL, **engine_kwargs)

# ── SQLite performance PRAGMAs (WAL mode + large in-memory cache) ─────────────
if IS_SQLITE:
    @event.listens_for(engine, "connect")
    def _set_sqlite_pragmas(dbapi_conn, _record):
        """
        Applied once per raw DBAPI connection created by SQLAlchemy.
        WAL mode allows simultaneous readers + one writer (3-5x faster
        than the default DELETE journal under concurrent FastAPI load).
        """
        cur = dbapi_conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL")       # concurrent readers/writers
        cur.execute("PRAGMA synchronous=NORMAL")     # safe but faster than FULL
        cur.execute("PRAGMA cache_size=-32000")      # 32 MB shared page cache
        cur.execute("PRAGMA temp_store=MEMORY")      # temp tables live in RAM
        cur.execute("PRAGMA mmap_size=268435456")    # 256 MB memory-mapped I/O
        cur.execute("PRAGMA busy_timeout=5000")      # wait 5 s before SQLITE_BUSY
        cur.close()

# ── Session factory ───────────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,   # avoids extra SELECT after every commit
)

Base = declarative_base()


def get_db():
    """FastAPI dependency — yields a DB session and closes it on teardown."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
