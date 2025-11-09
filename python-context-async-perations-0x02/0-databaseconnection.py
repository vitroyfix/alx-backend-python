import sqlite3
import os

DB_NAME = 'users.db'

# --- A small setup function to create the database for the example ---
def setup_database():
    """Creates a fresh users.db for the example."""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
    conn.commit()
    conn.close()

# --- Class-Based Context Manager ---

class DatabaseConnection:
    """
    A class-based context manager for handling SQLite database connections.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        print(f"[Context Manager] Initialized for database: {self.db_name}")

    def __enter__(self):
        """
        Called when entering the 'with' statement.
        Opens the connection and returns it.
        """
        print("[__enter__] Opening connection...")
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Called when exiting the 'with' statement.
        Handles commit/rollback and closes the connection.
        
        - exc_type: The type of exception (None if no error)
        - exc_value: The exception instance (None if no error)
        - traceback: The traceback object (None if no error)
        """
        if self.conn:
            if exc_type:
                # An error occurred
                print(f"[__exit__] Error: {exc_value}. Rolling back transaction.")
                self.conn.rollback()
            else:
                # No error occurred
                print("[__exit__] No errors. Committing transaction.")
                self.conn.commit()
            
            # Always close the connection
            self.conn.close()
            print("[__exit__] Connection closed.")
            
        # Returning False (or None) re-raises any exception that occurred.
        # Returning True would suppress the exception.
        return False

# --- Main execution ---

# 1. Create the dummy database
setup_database()

print("\n--- Using the DatabaseConnection context manager ---")

try:
    # 2. Use the 'with' statement
    # 'conn' will be the object returned by __enter__
    with DatabaseConnection(DB_NAME) as conn:
        print("[With Block] Connection successful. Executing query...")
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()

        print("\n--- Query Results ---")
        for row in results:
            print(row)

# The __exit__ method is automatically called here

except Exception as e:
    print(f"\n[Main] An unexpected error occurred: {e}")

finally:
    # 3. Clean up the dummy database
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print("\n[Main] Cleaned up database file.")