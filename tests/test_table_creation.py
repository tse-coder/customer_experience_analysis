import unittest
import sys, os

# Make sure importing src works when running tests via discovery
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from scripts.create_tables import create_tables
from database import Database
from config import DB_CONFIG


class TestCreateTables(unittest.TestCase):
    """
    Tests for verifying table creation functionality.
    """

    def test_create_tables(self):
        """
        Ensure the create_tables() function successfully creates the 'reviews' table.
        """
        conn = Database(**DB_CONFIG).connect()

        # Call the function
        result = create_tables()
        self.assertTrue(result, "create_tables() did not return True.")

        # Check if table exists in PostgreSQL
        cur = conn.cursor()
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'reviews'
            );
        """)

        exists = cur.fetchone()[0]
        self.assertTrue(exists, "'reviews' table was not created.")
        conn.close()


if __name__ == "__main__":
    unittest.main()
