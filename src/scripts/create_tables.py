import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'src')))
from database import Database
from config import DB_CONFIG

def create_tables(**kwargs):
    """
    Create dynamic 'reviews' and 'sentiment_results' tables for each app in kwargs.
    Example: create_tables(app1=True, app2=True)
    """
    db = Database(**DB_CONFIG)
    db.connect()
    cur = db.cursor()

    for app_name in kwargs.keys():
        # Create reviews table for the app
        reviews_table = f"""
        CREATE TABLE IF NOT EXISTS reviews_{app_name} (
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
        """
        cur.execute(reviews_table)
        print(f"Table reviews_{app_name} created successfully")

        # Create sentiment table for the app
        sentiment_table = f"""
        CREATE TABLE IF NOT EXISTS sentiment_{app_name} (
            id SERIAL PRIMARY KEY,
            review_id TEXT,
            tb_polarity FLOAT,
            tb_subjectivity FLOAT,
            tb_sentiment TEXT,
            vader_compound FLOAT,
            vader_sentiment TEXT
        );
        """
        cur.execute(sentiment_table)
        print(f"Table sentiment_{app_name} created successfully")

    db.commit()
    db.close()
    return True

if __name__ == "__main__":
    # Example: creates reviews_app1, sentiment_app1, reviews_app2, sentiment_app2
    create_tables(cbe=True, boa=True, db=True)
