import sys
sys.path.append("..")
from database import Database
from psycopg2.extras import execute_batch
from fileLoader import FileLoader
from config import DB_CONFIG

def insert_reviews(csv_path,app):
    db = Database(**DB_CONFIG)
    db.connect()
    cur = db.cursor()
    print(f"Inserting {csv_path} into database...")
    df = FileLoader(csv_path).load()
    sql = f"""
    INSERT INTO reviews_{app} (review_id, review_text, rating, app_name, bank_name, date, month, year)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
    """

    data = [
        (
            row["reviewId"],
            row["review"],
            int(row["rating"]),
            row["app_name"],
            row["bank_name"],
            row["date"],
            int(row["month"]),
            int(row["year"])
        )
        for _, row in df.iterrows()
    ]

    execute_batch(cur, sql, data)
    db.commit()
    db.close()
    print(f"Inserted {len(df)} rows into reviews_{app}")


def insert_sentiment(csv_path, app):
    db = Database(**DB_CONFIG)
    db.connect()
    cur = db.cursor()
    
    df = FileLoader(csv_path).load()
    sql = f"""
    INSERT INTO sentiment_{app} (review_id, tb_polarity, tb_subjectivity, tb_sentiment, vader_compound, vader_sentiment)
    VALUES (%s,%s,%s,%s,%s,%s);
    """
    
    data = [
        (
            row["reviewId"],
            row["tb_polarity"],
            row["tb_subjectivity"],
            row["tb_sentiment"],
            row["vader_compound"],
            row["vader_sentiment"]
        )
        for _, row in df.iterrows()
    ]
    
    execute_batch(cur, sql, data)
    db.commit()
    db.close()
    print(f"Inserted {len(df)} rows into sentiment_{app}")


if __name__ == "__main__":
    insert_reviews("data/processed/CBE.csv","cbe")
    insert_reviews("data/processed/BOA.csv","boa")
    insert_reviews("data/processed/DB.csv","db")
