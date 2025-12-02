import sys
sys.path.append("..")
from database import Database

def create_tables():
    """
    Create the 'reviews' and 'sentiment_results' tables in the database.
    """
    db = Database(
        host="localhost",
        dbname="bank_reviews",
        user="postgres",
        password="your_password"
    )
    db.connect()
    cur = db.cursor()

    reviews_table = """
    CREATE TABLE IF NOT EXISTS reviews (
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

    sentiment_table = """
    CREATE TABLE IF NOT EXISTS sentiment_results (
        id SERIAL PRIMARY KEY,
        review_id TEXT,
        tb_polarity FLOAT,
        tb_subjectivity FLOAT,
        tb_sentiment TEXT,
        vader_compound FLOAT,
        vader_sentiment TEXT
    );
    """

    cur.execute(reviews_table)
    cur.execute(sentiment_table)
    db.commit()
    db.close()
    print("Tables created successfully")

if __name__ == "__main__":
    create_tables()
