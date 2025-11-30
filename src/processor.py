from config import DATA_PATHES
import pandas as pd

class Processor:
    def __init__(self, df, app_id):
        # path to processed data storage
        self.processed = DATA_PATHES["processed"]
        self.df = df
        self.app_id = app_id

    # 1 remove duplicates
    def remove_duplicates(self):
        """
        Remove exact duplicate reviews based on text, rating, and date.
        Using drop_duplicates WITHOUT inplace=True (future-proof).
        """
        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=["review", "rating", "date"])
        removed = before - len(self.df)
        print(f"Removed {removed} duplicate rows")
        return self.df

    # check for missing data
    def check_missing_data(self):
        """
        Print percentage of missing values for each column,
        and specifically warn about missing values in critical columns.
        """
        print("\nLooking for missing data...")

        missing = self.df.isnull().sum()
        pct_missing = (missing / len(self.df)) * 100
        
        for col in missing.index:
            print(f"{col}: {pct_missing[col]:.2f}% missing")

        # check only columns that actually exist to prevent KeyErrors
        critical_cols = [c for c in ["review", "bank_name", "date", "app_name", "rating"]
                         if c in self.df.columns]
        
        missing_critical = self.df[critical_cols].isnull().sum()
        print(f"Warning: {missing_critical.sum()} missing values in critical columns")

    # 2 handle missing data
    def handle_missing_data(self):
        """
        Fill missing fields with meaningful default values.
        Convert date column to a proper datetime type.
        """
        self.df["review"] = self.df["review"].fillna("No review")
        self.df["app_name"] = self.df["app_name"].fillna("Unknown")

        # only fill if bank_name exists
        if "bank_name" in self.df.columns:
            self.df["bank_name"] = self.df["bank_name"].fillna("Unknown Bank")

        self.df["rating"] = self.df["rating"].fillna(0)

        # convert dates safely
        self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")

        print("Handled missing data.")
        return self.df

    # 3 Normalize data (mainly dates)
    def normalize_dates(self):
        """
        Convert date column to datetime and extract year/month.
        """
        self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")
        self.df["month"] = self.df["date"].dt.month
        self.df["year"] = self.df["date"].dt.year

        print(f"Date range: {self.df['date'].min()} → {self.df['date'].max()}")
        print("Normalized dates.")
        return self.df

    # Save processed reviews
    def save(self):
        """
        Export processed df to a CSV using the app_id as filename.
        """
        path = f"{self.processed}/{self.app_id}.csv"
        try:
            self.df.to_csv(path, index=False)
            print(f"Processed reviews are now available at {path}\n")
            return True
        except Exception as e:
            print(e)
            return False
