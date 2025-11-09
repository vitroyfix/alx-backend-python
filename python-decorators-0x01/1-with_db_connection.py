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
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
    conn.commit()
    conn.close()

# --- Decorator Implementation ---

def with_db_connection(func):
    """
    Decorator that opens a database connection, passes it to
    the function as the first argument, and closes it afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[DB] Opening connection to {DB_NAME}...")
        
        # 'sqlite3.connect' as a context manager handles
        # automatic open, commit/rollback, and close.
        with sqlite3.connect(DB_NAME) as conn:
            print("[DB] Connection established.")
            
            # Call the original function (func), passing the
            # connection as the FIRST argument.
            result = func(conn, *args, **kwargs)
            
            print("[DB] Closing connection...")
            return result
        # Connection is automatically closed here
    return wrapper

# --- Function using the decorator ---

@with_db_connection 
def get_user_by_id(conn, user_id): 
    """Fetches a user by their ID from the database."""
    print(f"   -> Executing query for user_id: {user_id}")
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 

# --- Main execution ---

# 1. Create the dummy database
setup_database()

# 2. Fetch user by ID with automatic connection handling
print("--- Calling get_user_by_id(user_id=1) ---")
user = get_user_by_id(user_id=1)

print("\nResult:")
print(user)

# 3. Clean up the dummy database
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)