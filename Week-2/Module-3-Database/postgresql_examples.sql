-- =====================================================================
-- Module 3: Database - PostgreSQL Specific Features
-- =====================================================================
-- This file contains PostgreSQL-specific features that extend beyond the 
-- ANSI SQL standard, enabling developers to build high-performance applications.
-- =====================================================================

-- =====================================================================
-- 1. JSONB Operations and Indexing
-- =====================================================================
-- Postgres allows storing JSON data. JSONB stores data in a decomposed binary
-- format, making it slower to insert but significantly faster to query and index.

-- Create table with JSONB column
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    metadata JSONB
);

-- Insert JSONB records
INSERT INTO user_profiles (username, metadata) VALUES
('john_doe', '{"role": "admin", "preferences": {"theme": "dark", "notifications": true}, "tags": ["tech", "admin"]}'),
('jane_smith', '{"role": "user", "preferences": {"theme": "light", "notifications": false}, "tags": ["finance"]}'),
('bob_jones', '{"role": "user", "preferences": {"theme": "dark", "notifications": true}, "tags": ["tech", "support"]}');

-- Query JSONB columns
-- Use `->` to get JSON object/field, `->>` to get text value
SELECT username, metadata->'preferences'->>'theme' as theme
FROM user_profiles
WHERE metadata->>'role' = 'user';

-- Check if JSONB contains a specific key-value pair (`@>`)
SELECT username 
FROM user_profiles 
WHERE metadata @> '{"preferences": {"theme": "dark"}}';

-- Check if array within JSONB contains element (`?` or `@>`)
SELECT username 
FROM user_profiles 
WHERE metadata->'tags' ? 'tech';

-- Create a GIN (Generalized Inverted Index) on the JSONB column for super-fast lookups
CREATE INDEX idx_user_profiles_metadata ON user_profiles USING GIN (metadata);
-- Or create a GIN index on a specific path within JSONB
CREATE INDEX idx_user_profiles_metadata_path ON user_profiles USING GIN ((metadata->'preferences'));


-- =====================================================================
-- 2. Full-Text Search (FTS)
-- =====================================================================
-- Postgres provides built-in Full-Text Search using `tsvector` (lexemes document)
-- and `tsquery` (search terms).

CREATE TABLE blog_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150),
    content TEXT,
    -- Combined search vector
    search_vector TSVECTOR
);

-- Insert sample posts
INSERT INTO blog_posts (title, content) VALUES
('SQL Optimization Guide', 'Learn to speed up your Postgres database with proper indexing and querying.'),
('Introduction to MongoDB', 'A NoSQL database alternative using documents instead of traditional SQL rows.'),
('Advanced Postgres Features', 'Deep dive into triggers, JSONB, and search vectors inside Postgres.');

-- Generate the tsvector values
UPDATE blog_posts 
SET search_vector = to_tsvector('english', coalesce(title, '') || ' ' || coalesce(content, ''));

-- Query using match operator `@@`
-- Search for documents containing 'postgres' AND 'database'
SELECT title, content 
FROM blog_posts 
WHERE search_vector @@ to_tsquery('english', 'postgres & database');

-- Create a GIN index to speed up FTS searches
CREATE INDEX idx_blog_posts_search ON blog_posts USING GIN (search_vector);


-- =====================================================================
-- 3. Upsert using ON CONFLICT
-- =====================================================================
-- Upsert allows you to either insert a new record or update an existing one if
-- a unique constraint violation occurs.

CREATE TABLE product_stock (
    sku VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(100),
    quantity INT NOT NULL DEFAULT 0
);

-- Insert initial value
INSERT INTO product_stock (sku, product_name, quantity) 
VALUES ('PROD-001', 'Wireless Mouse', 10);

-- Attempt insertion of same SKU - If conflict, UPDATE the existing quantity
INSERT INTO product_stock (sku, product_name, quantity)
VALUES ('PROD-001', 'Wireless Mouse', 5)
ON CONFLICT (sku) 
DO UPDATE SET quantity = product_stock.quantity + EXCLUDED.quantity;

-- Check result (quantity should be 15 now)
SELECT * FROM product_stock WHERE sku = 'PROD-001';


-- =====================================================================
-- 4. Array Types and Operations
-- =====================================================================
-- Postgres supports native column array data types.

CREATE TABLE student_grades (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    scores INT[] -- Integer array
);

INSERT INTO student_grades (name, scores) VALUES
('Alice', '{90, 85, 95}'),
('Bob', '{70, 75, 80}');

-- Query array index (1-based index in Postgres)
SELECT name, scores[1] as first_score 
FROM student_grades;

-- Filter where score contains a specific value
SELECT name, scores 
FROM student_grades 
WHERE 85 = ANY(scores);

-- Overlap operator (`&&`) checks if arrays have elements in common
SELECT name 
FROM student_grades 
WHERE scores && ARRAY[95, 100];


-- =====================================================================
-- 5. Database Triggers and Functions
-- =====================================================================
-- Triggers automatically execute a function when a specific database event
-- (INSERT, UPDATE, DELETE) happens on a table.

CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    action VARCHAR(50),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_value JSONB,
    new_value JSONB
);

-- 1. Create a Trigger Function (using PL/pgSQL language)
CREATE OR REPLACE FUNCTION log_stock_changes() 
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, action, old_value, new_value)
    VALUES (
        'product_stock',
        TG_OP,
        to_jsonb(OLD),
        to_jsonb(NEW)
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 2. Bind the function to the table with a trigger
CREATE TRIGGER trg_product_stock_audit
AFTER UPDATE OR DELETE ON product_stock
FOR EACH ROW
EXECUTE FUNCTION log_stock_changes();

-- Trigger update to test the function
UPDATE product_stock SET quantity = 20 WHERE sku = 'PROD-001';

-- View audit logs
SELECT * FROM audit_log;
