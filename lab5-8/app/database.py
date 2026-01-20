import logging
import os
import time
from contextlib import contextmanager
from logging.handlers import RotatingFileHandler
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

os.makedirs('logs', exist_ok=True)

sql_logger = logging.getLogger('sqlalchemy.engine')
sql_logger.setLevel(logging.INFO)

sql_file_handler = RotatingFileHandler('logs/sql_queries.log', maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8')
sql_file_handler.setLevel(logging.INFO)
sql_file_handler.setFormatter(
    logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
)
sql_logger.addHandler(sql_file_handler)

app_logger = logging.getLogger('app')
app_logger.setLevel(logging.INFO)

app_file_handler = RotatingFileHandler('logs/app.log', maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8')
app_file_handler.setLevel(logging.INFO)
app_file_handler.setFormatter(
    logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
)
app_logger.addHandler(app_file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
)
sql_logger.addHandler(console_handler)
app_logger.addHandler(console_handler)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./library.db")

engine = create_engine(
    DATABASE_URL,
    echo=False,  
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

_query_start_times = {}

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Логирует SQL-запросы перед выполнением"""
    _query_start_times[id(cursor)] = time.time()
    
    formatted_statement = statement.replace('\n', ' ').strip()
    sql_logger.info(f"SQL Query: {formatted_statement}")
    if parameters:
        sql_logger.info(f"Parameters: {parameters}")
    return statement, parameters

@event.listens_for(Engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Логирует время выполнения SQL-запросов"""
    cursor_id = id(cursor)
    if cursor_id in _query_start_times:
        elapsed = time.time() - _query_start_times[cursor_id]
        sql_logger.info(f"Query executed in: {elapsed:.4f} seconds")
        del _query_start_times[cursor_id]

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

