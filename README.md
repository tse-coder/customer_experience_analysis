# **Week 2 — Final Mobile Banking Review Analysis**

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
├─ .github/workflows/         # CI pipeline for formatting, tests and linting
│  └─ ci.yml
│
├─ data/
│  ├─ raw/                    # Raw scraped reviews per bank
│  ├─ processed/              # Cleaned CSV files per bank (CBE.csv, BOA.csv, DB.csv)
│  ├─ sentiment_results/      # Sentiment outputs (TextBlob & VADER)
│  └─ final/                  # Combined outputs after keyword + LDA + nouns
│
├─ notebooks/                 # analysis notebooks
│  ├─ scraper.ipynb           # Task 1: scraping & preprocessing demo
│  ├─ sentiment.ipynb         # Task 2: sentiment + keyword exploration
│  └─ database.ipynb          # DB exploration / quick queries (optional)
│
├─ reports/                   # Task 3/Task 4 artifacts and writeups
│  ├─ report.md               # Task 4 detailed write-up and recommendations
│  └─ figures/                # generated figures (PNG) used in reporting
│
├─ src/                       # source code and utilities
│  ├─ config.py               # constants / env handling
│  ├─ fileLoader.py           # CSV load/save helper
│  ├─ processor.py            # cleaning & preprocessing pipeline
│  ├─ scraper.py              # google-play-scraper wrapper
│  ├─ task4_insights.py       # new Task 4 analysis script (visuals + summary)
│  ├─ database.py             # DB helpers
│  ├─ dump.sql                # SQL schema / examples
│  └─ scripts/                # DB helpers / bulk insert scripts
│     ├─ create_tables.py
│     └─ insert_data.py
│
├─ tests/                     # unit tests
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

---

# Task 4 — Insights & Recommendations (IN PROGRESS)

This repository includes a Task 4 analysis script and artifacts which summarize business insights and recommendations per bank.

### Artifacts

- `reports/report.md` — detailed Task 4 write-up with findings, recommendations, ethics and next steps (not the final stakeholder report).
- `reports/figures/` — created visuals: rating_distribution.png, sentiment_counts.png, top_keywords_cbe.png, top_keywords_boa.png, top_keywords_db.png
- `reports/summary_task4.json` — compact machine-readable summary produced by `src/task4_insights.py`.

### How to run Task 4 analysis

1. Ensure processed CSVs and sentiment result CSVs exist in `data/processed/` and `data/sentiment_results/` respectively.
2. Run the insights script to regenerate visuals:

```bash
PYTHONPATH=src venv/bin/python src/task4_insights.py
```

This writes visual outputs to `reports/figures` and a summary JSON to `reports/`.

---

If you want I can now produce an executive-ready final report PDF using the generated visuals, or continue improving the theme extraction with more advanced NLP (LDA / BERTopic) — which would improve theme quality and grouping.
