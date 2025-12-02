-- SQL schema + example statements used by the project
--
-- This file collects the CREATE TABLE statements, example INSERT statements
-- and a few verification queries used by the repository's scripts (create_tables
-- and insert_data).
--
-- Tables used by the project:
--  1) reviews            -- holds each scraped mobile-app review
--  2) sentiment_results  -- holds sentiment analysis results for a review
--
-- Notes:
--  - The project creates these tables with the same structure shown below.
--  - insert_data.py populates these tables using bulk insertion or single-row
--    insert helpers which match the columns in `reviews` and `sentiment_results`.
--

-- ---------------------------------------------------------------
-- 1) reviews table (DDL used by src/scripts/create_tables.py)
--    stores the raw/processed review text, rating, bank/app metadata and
--    basic date fields for easy aggregation.
-- ---------------------------------------------------------------
-- NOTE: this project creates per-bank review tables (reviews_cbe/reviews_boa/reviews_db)
-- so the DDL below defines the three per-bank review tables used by the scripts.

CREATE TABLE IF NOT EXISTS reviews_cbe (
	id SERIAL PRIMARY KEY,
	review_id TEXT,
	review_text TEXT,
	rating INT,
	app_name TEXT,
	bank_name TEXT,
	date TIMESTAMP,
	month INT,
	year INT
);

CREATE TABLE IF NOT EXISTS reviews_boa (
	id SERIAL PRIMARY KEY,
	review_id TEXT,
	review_text TEXT,
	rating INT,
	app_name TEXT,
	bank_name TEXT,
	date TIMESTAMP,
	month INT,
	year INT
);

CREATE TABLE IF NOT EXISTS reviews_db (
	id SERIAL PRIMARY KEY,
	review_id TEXT,
	review_text TEXT,
	rating INT,
	app_name TEXT,
	bank_name TEXT,
	date TIMESTAMP,
	month INT,
	year INT
);

-- ---------------------------------------------------------------
-- 2) sentiment_results table (DDL used by src/scripts/create_tables.py)
--    stores results from sentiment pipeline (TextBlob, VADER etc.)
-- ---------------------------------------------------------------
-- Create per-bank sentiment tables used by the pipeline
CREATE TABLE IF NOT EXISTS sentiment_cbe (
	id SERIAL PRIMARY KEY,
	review_id TEXT,
	tb_polarity FLOAT,
	tb_subjectivity FLOAT,
	tb_sentiment TEXT,
	vader_compound FLOAT,
	vader_sentiment TEXT
);

CREATE TABLE IF NOT EXISTS sentiment_boa (
	id SERIAL PRIMARY KEY,
	review_id TEXT,
	tb_polarity FLOAT,
	tb_subjectivity FLOAT,
	tb_sentiment TEXT,
	vader_compound FLOAT,
	vader_sentiment TEXT
);

CREATE TABLE IF NOT EXISTS sentiment_db (
	id SERIAL PRIMARY KEY,
	review_id TEXT,
	tb_polarity FLOAT,
	tb_subjectivity FLOAT,
	tb_sentiment TEXT,
	vader_compound FLOAT,
	vader_sentiment TEXT
);


-- ---------------------------------------------------------------
-- Example INSERT statements (the project uses python/psycopg2 to insert)
-- These are examples showing the shape of the inserted data.
-- ---------------------------------------------------------------
-- Insert a single review into CBE table (fields must align with the per-bank reviews table):
INSERT INTO reviews_cbe (review_id, review_text, rating, app_name, bank_name, date, month, year)
VALUES ('abc-123', 'Love the app, but transfers are slow', 4, 'CBE Mobile', 'Commercial Bank of Ethiopia', '2025-01-01 12:34:56', 1, 2025);

-- Insert an equivalent sentiment row for the CBE review into sentiment_cbe:
INSERT INTO sentiment_cbe (review_id, tb_polarity, tb_subjectivity, tb_sentiment, vader_compound, vader_sentiment)
VALUES ('abc-123', 0.1, 0.2, 'neutral', 0.12, 'neutral');


-- ---------------------------------------------------------------
-- Example verification / reporting queries used when validating imports
-- or doing quick analytics. Useful for sanity checks and QA in the project.
-- ---------------------------------------------------------------
-- Example aggregated queries across per-bank tables.

-- Count reviews per bank (uses UNION across each per-bank table):
SELECT 'CBE' AS bank_name, COUNT(*) AS review_count FROM reviews_cbe
UNION ALL
SELECT 'BOA', COUNT(*) FROM reviews_boa
UNION ALL
SELECT 'DB', COUNT(*) FROM reviews_db
ORDER BY review_count DESC;

-- Average rating per bank (simple per-table aggregation):
SELECT 'CBE' AS bank_name, AVG(rating) AS avg_rating, COUNT(*) AS n_reviews FROM reviews_cbe
UNION ALL
SELECT 'BOA', AVG(rating), COUNT(*) FROM reviews_boa
UNION ALL
SELECT 'DB', AVG(rating), COUNT(*) FROM reviews_db
ORDER BY avg_rating DESC;

-- Find the most negative (1-star) recent reviews across all banks (combined via UNION):
SELECT review_id, review_text, rating, date, app_name, bank_name
FROM (
	SELECT * FROM reviews_cbe
	UNION ALL
	SELECT * FROM reviews_boa
	UNION ALL
	SELECT * FROM reviews_db
) all_reviews
WHERE rating = 1
ORDER BY date DESC
LIMIT 20;

-- Join sentiment and reviews to compare predicted sentiment vs rating
-- Join reviews and sentiment for a given bank
SELECT r.review_id, r.review_text, r.rating, s.tb_sentiment, s.vader_sentiment
FROM reviews_cbe r
LEFT JOIN sentiment_cbe s ON s.review_id = r.review_id
ORDER BY r.date DESC
LIMIT 50;
