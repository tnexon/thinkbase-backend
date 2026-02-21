-- migration_add_settings_table.sql
-- Run this script to add the settings table for storing application configuration

-- Create settings table
CREATE TABLE IF NOT EXISTS settings (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(255)
);

-- Add initial system_prompt setting (optional - can be set via Admin UI)
-- Uncomment the line below to set an initial default prompt
-- INSERT INTO settings (key, value, updated_by) 
-- VALUES ('system_prompt', 'Your default prompt here...', 'system') 
-- ON CONFLICT (key) DO NOTHING;

-- Verify the table was created
SELECT 'Settings table created successfully' as status;

-- Show table structure
\d settings
