# Week 2 — Task 1: Scraping and Preprocessing Mobile Banking Reviews

## Project Overview

This project collects and processes user reviews from Google Play for three Ethiopian bank apps:

* **Commercial Bank of Ethiopia (CBE)**
* **Bank of Abyssinia (BOA)**
* **Dashen Bank (DB)**

The goal of Task 1 is to **scrape reviews, clean the data, and save processed datasets** for later sentiment and thematic analysis.

---

## Folder Structure

```
WEEK2/
│
├─ .github/workflows/        # GitHub Actions workflow
│   └─ ci.yml
│
├─ data/
│   ├─ raw/                  # Raw scraped CSV files
│   └─ processed/            # Cleaned CSV files per bank
│
├─ notebooks/                # Jupyter notebooks
│   └─ scraper.ipynb
│
├─ src/                      # Python modules
│   ├─ config.py             # Configuration constants
│   ├─ fileLoader.py         # File I/O helper
│   ├─ processor.py          # Data cleaning & normalization
│   └─ scraper.py            # Google Play scraper
│
├─ tests/                    # Unit tests (if any)
├─ requirements.txt          # Python dependencies
└─ .gitignore
```

---

## How to Run Task 1

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Run scraper**
   Scrapes reviews from Google Play for all three banks and saves raw CSV files:

```bash
python src/scraper.py
```

3. **Process the data**
   Removes duplicates, handles missing data, normalizes dates, and saves cleaned CSVs:

```bash
python src/processor.py
```

4. **Outputs**
   Processed CSV files are saved under:

```
data/processed/
- CBE.csv
- BOA.csv
- DB.csv
```

---

## Key Features

* **Scraper**: Fetches review text, rating, date, app name, and bank name.
* **Processor**: Cleans data, handles missing values, normalizes dates, removes duplicates.
* **FileLoader**: Handles saving and loading CSVs safely.
* **Notebook**: `scraper.ipynb` shows the scraping and processing workflow interactively.
