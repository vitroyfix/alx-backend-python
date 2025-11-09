import time
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
            # Call the next function in the stack (the retry wrapper)
            result = func(conn, *args, **kwargs)
            return result
        except Exception as e:
            # This will catch the final, re-raised exception if all retries fail
            print(f"[DB] Error: {e}")
            raise
        finally:
            if conn:
                conn.close()
                print("[DB] Connection closed.")
    return wrapper

def retry_on_failure(retries=3, delay=1):
    """
    Decorator factory: Retries a function if it raises an exception.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(conn, *args, **kwargs):
            """
            The wrapper expects 'conn' as its first argument,
            which is provided by the @with_db_connection decorator.
            """
            attempts_left = retries
            while attempts_left > 0:
                try:
                    # Pass 'conn' and other args to the real function
                    return func(conn, *args, **kwargs)
                except Exception as e:
                    attempts_left -= 1
                    print(f"[Retry] {func.__name__} failed: {e}. Retries left: {attempts_left}")
                    
                    if attempts_left == 0:
                        print(f"[Retry] No retries left. Raising final exception.")
                        raise # Re-raise the last exception
                    
                    print(f"[Retry] Waiting {delay} second(s) before retrying...")
                    time.sleep(delay)
        return decorator
    return decorator

# --- Function using the decorators ---

# A global counter to simulate failures
_failure_counter = 0

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetches users, but simulates 2 failures before succeeding
    to test the retry decorator.
    """
    global _failure_counter
    
    # Simulate 2 failures before succeeding
    if _failure_counter < 2:
        _failure_counter += 1
        print("   -> Simulating a transient database error...")
        raise sqlite3.OperationalError("database is locked") # A plausible error
        
    print("   -> Success! Fetching data.")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# --- Main execution ---

setup_database()

print("--- Attempting to fetch users with retry... ---")
try:
    users = fetch_users_with_retry()
    print("\n--- Results ---")
    print(users)
except Exception as e:
    print(f"\n[Main] Fetch failed permanently: {e}")

# Clean up
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)