
# **Week 2 — Task 1 & Partial Task 2: Mobile Banking Review Analysis**

## **Project Overview**

This project focuses on collecting, cleaning, and analyzing user reviews from Google Play for three major Ethiopian mobile banking apps:

* **Commercial Bank of Ethiopia (CBE)**
* **Bank of Abyssinia (BOA)**
* **Dashen Bank (DB)**

During **Task 1**, all reviews were scraped, cleaned, and normalized.
During **Task 2 (partial)**, sentiment analysis, keyword extraction, and topic modeling were implemented.

---

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

---

# **Task 1 — Scraping & Preprocessing (Completed)**

### **1. Scraping**

The scraper retrieves:

* Review text
* Rating
* Review date
* App name
* Bank name

Outputs are saved under `data/raw/`.

### **2. Processing**

The Processor:

* Removes duplicates
* Standardizes dates
* Handles missing fields
* Adds month/year columns

Cleaned datasets saved under `data/processed/`:

```
CBE.csv
BOA.csv
DB.csv
```

---

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

---

# **Task 2 — Sentiment & Keyword Analysis (Progress Up to Cell 6)**

Task 2 begins the analytical phase. Work completed includes:

### **✔ Sentiment Analysis**

Using **TextBlob** and **VADER**, each review now has:

* Polarity
* Subjectivity
* Sentiment label (positive / neutral / negative)
* VADER compound score

Outputs saved under:

```
data/sentiment_results/
```

### **✔ Text Preprocessing**

A standard NLP pipeline was applied:

* Lowercasing
* Removing punctuation
* Tokenization
* Stopword filtering

### **✔ Frequency-Based Keyword Extraction**

Computed per bank using:

* Bag-of-Words
* Token frequencies
* Top-N frequent terms

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

---

# **Next Steps for Task 2**

Remaining items:

* Visualizations (sentiment distribution, keyword plots)
* Bank-level comparison charts
* Summary export and reporting
