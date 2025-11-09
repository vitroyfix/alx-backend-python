import sqlite3 
import functools
import os

DB_NAME = 'users.db'

# --- A small setup function to create the database for the example ---
def setup_database():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE)")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
    conn.commit()
    conn.close()

# --- Decorator Implementations ---

def with_db_connection(func):
    """
    Decorator that opens and closes a database connection.
    It passes the connection to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            print(f"[DB] Connection opened to {DB_NAME}.")
            # Call the next function in the stack (the transactional wrapper)
            result = func(conn, *args, **kwargs)
            return result
        except Exception as e:
            print(f"[DB] Error: {e}")
            raise
        finally:
            if conn:
                conn.close()
                print("[DB] Connection closed.")
    return wrapper

def transactional(func):
    """
    Decorator that wraps a function in a database transaction.
    It commits on success and rolls back on failure.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        """
        The wrapper expects 'conn' as its first argument,
        which is provided by the @with_db_connection decorator.
        """
        try:
            print("   [TX] Starting transaction...")
            # Call the actual function (e.g., update_user_email)
            result = func(conn, *args, **kwargs)
            
            # If the function succeeds, commit the transaction
            print("   [TX] Committing transaction...")
            conn.commit()
            return result
        except Exception as e:
            # If the function fails, roll back the transaction
            print(f"   [TX] ERROR: {e}. Rolling back transaction...")
            conn.rollback()
            raise # Re-raise the exception so the caller knows it failed
    return wrapper

# --- Functions using the decorators ---

@with_db_connection
@transactional 
def update_user_email(conn, user_id, new_email): 
    """Updates a user's email. This will SUCCEED."""
    print(f"      -> Executing: Update email for user {user_id}")
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

@with_db_connection
@transactional
def add_user_with_error(conn):
    """Tries to add a user that will cause an error. This will FAIL."""
    print("      -> Executing: Attempting to add user 'Charlie' (valid)")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES ('Charlie', 'charlie@example.com')")
    # This next line will FAIL because the 'email' column is UNIQUE
    print("      -> Executing: Attempting to add 'David' with duplicate email (will fail)")
    cursor.execute("INSERT INTO users (name, email) VALUES ('David', 'alice@example.com')")

@with_db_connection
def get_user_by_email(conn, email):
    """Helper to check data. (No transaction needed for a SELECT)"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    return cursor.fetchone()

# --- Main execution ---

setup_database()

# --- 1. Test the SUCCESS (commit) case ---
print("\n--- 1. Testing SUCCESS (commit) ---")
print("Before:", get_user_by_email(email='alice@example.com'))
try:
    new_email = 'alice_new@example.com'
    update_user_email(user_id=1, new_email=new_email)
    print("After:", get_user_by_email(email=new_email))
except Exception as e:
    print(f"Update failed: {e}")

# --- 2. Test the FAILURE (rollback) case ---
print("\n--- 2. Testing FAILURE (rollback) ---")
print("User 'Charlie' exists?", get_user_by_email(email='charlie@example.com'))
try:
    add_user_with_error()
except Exception as e:
    print(f"   [Main] Caught expected error: {e}")

# Check if 'Charlie' was rolled back (he should not exist)
print("User 'Charlie' exists after rollback?", get_user_by_email(email='charlie@example.com'))

# Clean up
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)