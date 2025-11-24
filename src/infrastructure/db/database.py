import sqlite3
from contextlib import contextmanager
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'users.db')

def init_db():
    """Inicializa o banco de dados e cria as tabelas se não existirem"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Tabela de users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT 1,
            phone TEXT,
            salary REAL DEFAULT 0.0,
            position TEXT,
            department TEXT,
            employment_type TEXT,
            manager_id INTEGER,
            hire_date TEXT,
            birth_date TEXT,
            address TEXT,
            FOREIGN KEY (manager_id) REFERENCES users(id)
        )
    ''')
    
    # Tabela de eventos (eventstore)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            aggregate_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            occurred_at TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_events_aggregate 
        ON events(aggregate_id, event_type)
    ''')
    
    conn.commit()
    conn.close()

@contextmanager
def get_db_connection():
    """Context manager para conexão com o banco de dados"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
