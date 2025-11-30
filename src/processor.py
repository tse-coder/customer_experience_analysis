# processor object to:
# 1 remove duplicates
# 2 handle missing data
# 3 Normalize data
from config import DATA_PATHES
import pandas as pd
class Processor:
    def __init__(self,df):
        self.raw_reviews_path = DATA_PATHES["raw_reviews"]
        self.processed_reviews_path = DATA_PATHES["processed_raws"]
        self.sentiment_results_path = DATA_PATHES["sentiment_results"]
        self.final_results_path = DATA_PATHES["final_results"]
        self.stats = {}
        self.df = df
    
    def remove_duplicates(self,df):
        df.drop_duplicates(inplace=True)
        return df
    
    def check_missing_data(self):
        print("\n looking for missing data...")
        missing = self.df.isnull().sum()
        pct_missing = (missing / len(self.df)) * 100
        for col in missing.index:
            self.stats[f"missing_{col}"] = pct_missing[col]
            print(f"{col}: {pct_missing[col]}% missing")
        # list the columns that are critical for analysis
        critical_cols = ["review_text","bank_name", "review_date","rating"]
        missing_critical = self.df[critical_cols].isnull().sum()
        print(f"warning: {missing_critical.sum()} critical columns have missing data")
        
    def handle_missing_data(self):
        # handle each missing data in the critical columns
        self.df["review_text"].fillna("No review", inplace=True)
        self.df["bank_name"].fillna("Unknown", inplace=True)
        self.df["review_date"].fillna("Unknown", inplace=True)
        self.df["rating"].fillna(0, inplace=True)
        return self.df
    
    def normalize_dates(self):
        self.df["review_date"] = pd.to_datetime(self.df["review_date"], format="%Y-%m-%d")
        self.df["review_month"] = self.df["review_date"].dt.month
        self.df["review_year"] = self.df["review_date"].dt.year
        print(f"the date range is from {self.df['review_date'].min()} to {self.df['review_date'].max()}")
        return self.df
