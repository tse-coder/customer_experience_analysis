import unittest
import sys, os

# Make sure importing src works when running tests via discovery
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from database import Database
from scripts.insert_data import insert_reviews
from config import DB_CONFIG


class TestInsertData(unittest.TestCase):
    """
    Tests for verifying review insertion functionality.
    """

    def test_insert_single_review(self):
        """
        Insert one review into the database and check if it is stored correctly.
        """

        # Create a temporary CSV containing 1 sample review
        import pandas as pd
        temp_csv = "temp_test_review.csv"

        sample = {
            "reviewId": ["test123"],
            "review": ["Unit test review"],
            "rating": [5],
            "date": ["2024-01-01"],
            "bank_name": ["CBE"],
            "app_name": ["CBE Mobile App"],
            "month": [1],
            "year": [2024]
        }

        pd.DataFrame(sample).to_csv(temp_csv, index=False)

        # Call original function
        insert_reviews(temp_csv, DB_CONFIG)

        # Verify
        db = Database(**DB_CONFIG)
        db.connect()
        cur = db.cursor()

        cur.execute("""
            SELECT review_text, rating
            FROM reviews
            WHERE review_text = %s;
        """, ("Unit test review",))

        row = cur.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "Unit test review")
        self.assertEqual(row[1], 5)

        db.close()

        os.remove(temp_csv)


if __name__ == "__main__":
    unittest.main()
