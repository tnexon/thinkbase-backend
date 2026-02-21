# database.py
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/todo_db"
)

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        conn.autocommit = True
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize database tables with updated schema"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Create tasks table with task_owner and due_date columns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                task_owner VARCHAR(255),
                due_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create ideas table with chat_history JSONB column, ai_feedback, and created_by
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ideas (
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                domain VARCHAR(100),
                recommendations TEXT,
                ai_feedback TEXT,
                feature_list TEXT,
                chat_history JSONB DEFAULT '[]'::jsonb,
                created_by VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP,
                feature_list_generated_at TIMESTAMP
            )
        """)
        
        # Add chat_history column to existing ideas table if it doesn't exist
        cursor.execute("""
            DO $$ 
            BEGIN
                BEGIN
                    ALTER TABLE ideas ADD COLUMN chat_history JSONB DEFAULT '[]'::jsonb;
                EXCEPTION
                    WHEN duplicate_column THEN 
                        NULL;
                END;
            END $$;
        """)
        
        # Add ai_feedback column to existing ideas table if it doesn't exist
        cursor.execute("""
            DO $$ 
            BEGIN
                BEGIN
                    ALTER TABLE ideas ADD COLUMN ai_feedback TEXT;
                EXCEPTION
                    WHEN duplicate_column THEN 
                        NULL;
                END;
            END $$;
        """)
        
        # Add created_by column to existing ideas table if it doesn't exist
        cursor.execute("""
            DO $$ 
            BEGIN
                BEGIN
                    ALTER TABLE ideas ADD COLUMN created_by VARCHAR(255);
                EXCEPTION
                    WHEN duplicate_column THEN 
                        NULL;
                END;
            END $$;
        """)
        
        # Add task_owner column to existing tasks table if it doesn't exist
        cursor.execute("""
            DO $$ 
            BEGIN
                BEGIN
                    ALTER TABLE tasks ADD COLUMN task_owner VARCHAR(255);
                EXCEPTION
                    WHEN duplicate_column THEN 
                        NULL;
                END;
            END $$;
        """)
        
        # Add due_date column to existing tasks table if it doesn't exist
        cursor.execute("""
            DO $$ 
            BEGIN
                BEGIN
                    ALTER TABLE tasks ADD COLUMN due_date DATE;
                EXCEPTION
                    WHEN duplicate_column THEN 
                        NULL;
                END;
            END $$;
        """)
        
        # Create settings table for application-wide configuration
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key VARCHAR(100) PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_by VARCHAR(255)
            )
        """)
        
        print("✅ Database initialized successfully")
        print("   - Tasks table: id, text, completed, task_owner, due_date, created_at")
        print("   - Ideas table: id, text, domain, recommendations, ai_feedback, feature_list, chat_history, created_by, created_at, updated_at")
        print("   - Settings table: key, value, updated_at, updated_by")
