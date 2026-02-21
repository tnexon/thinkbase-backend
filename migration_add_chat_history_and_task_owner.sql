-- migration_add_chat_history_and_task_owner.sql
-- Run this script to update your existing database schema

-- Add chat_history column to ideas table (if not exists)
DO $$ 
BEGIN
    BEGIN
        ALTER TABLE ideas ADD COLUMN chat_history JSONB DEFAULT '[]'::jsonb;
        RAISE NOTICE 'Added chat_history column to ideas table';
    EXCEPTION
        WHEN duplicate_column THEN 
            RAISE NOTICE 'chat_history column already exists in ideas table';
    END;
END $$;

-- Add ai_feedback column to ideas table (if not exists)
DO $$ 
BEGIN
    BEGIN
        ALTER TABLE ideas ADD COLUMN ai_feedback TEXT;
        RAISE NOTICE 'Added ai_feedback column to ideas table';
    EXCEPTION
        WHEN duplicate_column THEN 
            RAISE NOTICE 'ai_feedback column already exists in ideas table';
    END;
END $$;

-- Add created_by column to ideas table (if not exists)
DO $$ 
BEGIN
    BEGIN
        ALTER TABLE ideas ADD COLUMN created_by VARCHAR(255);
        RAISE NOTICE 'Added created_by column to ideas table';
    EXCEPTION
        WHEN duplicate_column THEN 
            RAISE NOTICE 'created_by column already exists in ideas table';
    END;
END $$;

-- Add task_owner column to tasks table (if not exists)
DO $$ 
BEGIN
    BEGIN
        ALTER TABLE tasks ADD COLUMN task_owner VARCHAR(255);
        RAISE NOTICE 'Added task_owner column to tasks table';
    EXCEPTION
        WHEN duplicate_column THEN 
            RAISE NOTICE 'task_owner column already exists in tasks table';
    END;
END $$;

-- Add due_date column to tasks table (if not exists)
DO $$ 
BEGIN
    BEGIN
        ALTER TABLE tasks ADD COLUMN due_date DATE;
        RAISE NOTICE 'Added due_date column to tasks table';
    EXCEPTION
        WHEN duplicate_column THEN 
            RAISE NOTICE 'due_date column already exists in tasks table';
    END;
END $$;

-- Verify the changes
SELECT 'Ideas table columns:' as info;
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'ideas'
ORDER BY ordinal_position;

SELECT 'Tasks table columns:' as info;
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'tasks'
ORDER BY ordinal_position;
