# database.py
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Create a database connection"""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    """Initialize database tables"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Create tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id BIGINT PRIMARY KEY,
                text TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create ideas table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ideas (
                id BIGINT PRIMARY KEY,
                text TEXT NOT NULL,
                domain VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP,
                recommendations TEXT,
                feature_list TEXT,
                feature_list_generated_at TIMESTAMP
            )
        """)
        
        # Create indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_ideas_domain ON ideas(domain)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_ideas_updated ON ideas(updated_at)
        """)
        
        print("Database initialized successfully!")