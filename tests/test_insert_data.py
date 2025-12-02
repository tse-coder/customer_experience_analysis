import unittest
import sys
sys.path.append("../src")
from database import get_connection
from scripts.insert_data import insert_review


class TestInsertData(unittest.TestCase):
    """
    Tests for verifying review insertion functionality.
    """

    def test_insert_single_review(self):
        """
        Insert one review into the database and check if it is stored correctly.
        """
        conn = get_connection()

        # Sample review dictionary
        sample = {
            "review": "Unit test review",
            "rating": 5,
            "date": "2024-01-01",
            "bank_name": "CBE",
            "app_name": "CBE Mobile App"
        }

        # Insert review
        result = insert_review(conn, sample)
        self.assertTrue(result, "insert_review() did not return True.")

        # Verify record exists
        cur = conn.cursor()
        cur.execute("""
            SELECT review, rating
            FROM reviews
            WHERE review = %s;
        """, (sample["review"],))

        row = cur.fetchone()
        self.assertIsNotNone(row, "Inserted review not found in database.")
        self.assertEqual(row[0], sample["review"], "Inserted review text does not match.")
        self.assertEqual(row[1], sample["rating"], "Inserted rating does not match.")

        conn.close()


if __name__ == "__main__":
    unittest.main()
