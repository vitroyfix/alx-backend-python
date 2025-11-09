import sqlite3
import os

DB_NAME = 'users.db'

# --- A small setup function to create the database for the example ---
def setup_database():
    """Creates a fresh users.db with an age column."""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Create table with age
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    
    # Insert sample data
    users_data = [
        ('Alice', 20),
        ('Bob', 28),
        ('Charlie', 35),
        ('David', 22)
    ]
    cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users_data)
    
    conn.commit()
    conn.close()

# --- Class-Based Context Manager for Executing a Query ---

class ExecuteQuery:
    """
    A context manager that opens a DB connection, executes a
    specific query, and returns the results, ensuring the
    connection is closed afterward.
    """
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        print(f"[Context Manager] Initialized with query: '{self.query}'")

    def __enter__(self):
        """
        Called when entering the 'with' statement.
        Opens connection, executes query, fetches results, and returns them.
        """
        print("[__enter__] Opening connection...")
        try:
            self.conn = sqlite3.connect(self.db_name)
            cursor = self.conn.cursor()
            
            print(f"[__enter__] Executing query with params: {self.params}")
            cursor.execute(self.query, self.params)
            results = cursor.fetchall()
            
            # This context manager returns the *results*, not the connection
            return results
        
        except Exception as e:
            # If __enter__ fails, __exit__ will still be called
            # (with an exception). We should re-raise here.
            print(f"[__enter__] FAILED: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Called when exiting the 'with' statement.
        Closes the connection.
        """
        if self.conn:
            # We don't need to commit/rollback for a SELECT,
            # but we must close the connection.
            self.conn.close()
            print("[__exit__] Connection closed.")
            
        if exc_type:
            print(f"[__exit__] An error occurred inside the 'with' block: {exc_value}")
        
        # Return False to re-raise any exceptions
        return False

# --- Main execution ---

# 1. Create the dummy database
setup_database()

print("\n--- Using the ExecuteQuery context manager ---")

# 2. Define the query and parameters
sql_query = "SELECT * FROM users WHERE age > ?"
parameters = (25,)

try:
    # 3. Use the 'with' statement
    # 'users' will be the *results* returned by __enter__
    with ExecuteQuery(DB_NAME, sql_query, parameters) as users:
        print("[With Block] Query executed. Results received.")
        
        print("\n--- Query Results (Users older than 25) ---")
        if users:
            for user in users:
                print(user)
        else:
            print("No users found.")

# The __exit__ method is automatically called here

except Exception as e:
    print(f"\n[Main] An unexpected error occurred: {e}")

finally:
    # 4. Clean up the dummy database
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print("\n[Main] Cleaned up database file.")