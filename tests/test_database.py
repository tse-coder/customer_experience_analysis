import unittest
import psycopg2
from src.database import get_connection


class TestDatabaseConnection(unittest.TestCase):
    """
    Tests for verifying database connection behavior.
    """

    def test_connection_success(self):
        """
        Ensure that a valid connection to PostgreSQL can be established.
        """
        conn = get_connection()
        self.assertIsNotNone(conn, "Connection returned None.")
        self.assertIsInstance(conn, psycopg2.extensions.connection, "Connection is not a psycopg2 connection.")
        conn.close()

    def test_connection_failure(self):
        """
        Force a connection failure by temporarily overriding psycopg2.connect.
        Expect get_connection() to raise an exception.
        """
        original_connect = psycopg2.connect

        def fail_connect(*args, **kwargs):
            raise psycopg2.OperationalError("Mock failure")

        # Patch psycopg2.connect
        psycopg2.connect = fail_connect

        with self.assertRaises(Exception):
            get_connection()

        # Restore original connection method
        psycopg2.connect = original_connect


if __name__ == "__main__":
    unittest.main()
