# **Week 2 — Task 1 , Task 2 and Task 3 Mobile Banking Review Analysis**

## **Project Overview**

This project focuses on collecting, cleaning, and analyzing user reviews from Google Play for three major Ethiopian mobile banking apps:

- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank (DB)**

During **Task 1**, all reviews were scraped, cleaned, and normalized.
During **Task 2 (partial)**, sentiment analysis, keyword extraction, and topic modeling were implemented.

## **Folder Structure**

```
WEEK2/
│
├─ .github/workflows/
│   └─ ci.yml                 # CI pipeline for formatting, tests, and linting
│
├─ data/
│   ├─ raw/                   # Raw scraped reviews
│   ├─ processed/             # Cleaned CSV files per bank
│   ├─ sentiment_results/     # Sentiment outputs (TextBlob & VADER)
│   └─ final/                 # Combined outputs after keyword + LDA + nouns
│
├─ notebooks/
│   ├─ scraper.ipynb          # Task 1 workflow
│   └─ sentiment.ipynb   # Task 2 progress up to Cell 6
│
├─ src/
│   ├─ config.py              # Constants and settings
│   ├─ fileLoader.py          # File I/O utility
│   ├─ processor.py           # Cleaning & preprocessing pipeline
│   └─ scraper.py             # Google Play scraper
│
├─ tests/                     # Test suite (if implemented)
├─ requirements.txt
└─ .gitignore
```

# **Task 1 — Scraping & Preprocessing (Completed)**

### **1. Scraping**

The scraper retrieves:

- Review text
- Rating
- Review date
- App name
- Bank name

Outputs are saved under `data/raw/`.

### **2. Processing**

The Processor:

- Removes duplicates
- Standardizes dates
- Handles missing fields
- Adds month/year columns

Cleaned datasets saved under `data/processed/`:

```
CBE.csv
BOA.csv
DB.csv
```

## **How to Run Task 1**

### **Install dependencies**

```bash
pip install -r requirements.txt
```

### **Run scraper**

```bash
python src/scraper.py
```

### **Run processor**

```bash
python src/processor.py
```

# **Task 2 — Sentiment & Keyword Analysis (Progress Up to Cell 6)**

Task 2 begins the analytical phase. Work completed includes:

### **✔ Sentiment Analysis**

Using **TextBlob** and **VADER**, each review now has:

- Polarity
- Subjectivity
- Sentiment label (positive / neutral / negative)
- VADER compound score

Outputs saved under:

```
data/sentiment_results/
```

### **✔ Text Preprocessing**

A standard NLP pipeline was applied:

- Lowercasing
- Removing punctuation
- Tokenization
- Stopword filtering

### **✔ Frequency-Based Keyword Extraction**

Computed per bank using:

- Bag-of-Words
- Token frequencies
- Top-N frequent terms

### **✔ TF-IDF Keyword Extraction**

Ranked terms by importance using TF-IDF vectorizer.

### **✔ Topic Modeling (LDA)**

Extracted themes from reviews using Latent Dirichlet Allocation.

### **✔ Noun Extraction (spaCy)**

Extracted frequent nouns for theme discovery.

### **✔ Saving Outputs**

All intermediate results saved under:

```
data/final/
```

### **✔Visualizations (sentiment distribution, keyword plots)**
### **✔Bank-level comparison charts**
### **✔Summary export and reporting**

# Task 3 — Database (COMPLETED)

## What I finished for Task 3

- Designed and created per-bank Postgres tables for reviews and sentiment (CBE, BOA, DB).
- Added scripts to create tables and insert data: `src/scripts/create_tables.py` and `src/scripts/insert_data.py`.
- Added `src/dump.sql` with the full DDL for the project (per-bank tables), example INSERTs and example verification queries.

This means cleaned review data can be persisted, queried for analytics, and linked to your sentiment pipeline.

## How to run the DB setup and imports (Task 3)

1. Ensure Postgres is installed and running locally. Create the target DB (example):

```bash
sudo -u postgres createdb bank_reviews
sudo -u postgres createuser -P tsegaye   # or set your own user/password
```

2. Configure credentials in environment or `src/config.py` DB_CONFIG. The project looks for DB_CONFIG but you can also use environment variables to adapt scripts.

3. Create per-bank tables:

```bash
PYTHONPATH=src python -c "from scripts.create_tables import create_tables; create_tables(cbe=True, boa=True, db=True)"
```

4. Insert cleaned CSVs into DB (one bank at a time):

```bash
PYTHONPATH=src python -c "from scripts.insert_data import insert_reviews; insert_reviews('data/processed/CBE.csv','cbe')"
PYTHONPATH=src python -c "from scripts.insert_data import insert_reviews; insert_reviews('data/processed/BOA.csv','boa')"
PYTHONPATH=src python -c "from scripts.insert_data import insert_reviews; insert_reviews('data/processed/DB.csv','db')"
```

5. (Optional) Insert sentiment CSVs into their respective per-bank sentiment tables:

```bash
PYTHONPATH=src python -c "from scripts.insert_data import insert_sentiment; insert_sentiment('data/sentiment_results/CBE_sentiment.csv','cbe')"
```

## Where to find SQL artifacts

- `src/dump.sql` — comprehensive DDL + sample INSERTs + common verification/analytics queries (now updated to use per-bank tables reviews_cbe / sentiment_cbe etc.).

## Tests & verification

- Unit tests for the preprocessing pipeline are in `tests/` (run with pytest or unittest). Database integration tests (if run locally) can confirm tables exist and data inserted.
