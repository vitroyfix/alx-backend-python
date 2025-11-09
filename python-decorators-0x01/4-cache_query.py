import time
import sqlite3 
import functools
import os

DB_NAME = 'users.db'
# A simple, global dictionary for our cache
query_cache = {}

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

# --- Decorator 1 (from previous task) ---

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
            # Call the next function in the stack (the cache wrapper)
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

# --- Decorator 2 (Cache Implementation) ---

def cache_query(func):
    """
    Decorator that caches the result of a function based on
    its query argument.
    
    It expects the decorated function to receive 'conn' as
    the first argument, and the query string as either the
    second positional arg or a keyword arg 'query'.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # 1. Determine the query key from the arguments
        query_key = None
        if 'query' in kwargs:
            query_key = kwargs['query']
        elif args:
            # args[0] will be the first argument *after* conn
            query_key = args[0]

        # 2. Check the cache for this key
        if query_key in query_cache:
            print(f"[Cache] HIT: Returning cached result for '{query_key}'")
            return query_cache[query_key]
        
        # 3. Cache MISS: Execute the original function
        print(f"[Cache] MISS: Executing query '{query_key}'")
        result = func(conn, *args, **kwargs)
        
        # 4. Store the result in the cache
        print(f"[Cache] Storing result for '{query_key}'")
        query_cache[query_key] = result
        return result
    return wrapper

# --- Function using the decorators ---

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetches users, but we'll add a delay to simulate a slow query."""
    print("   -> (Database query is running... this will take 1s)")
    time.sleep(1) # Simulate a slow, expensive query
    
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# --- Main execution ---

setup_database()
print("--- 1. First call (will be SLOW and will populate the cache) ---")
start_time = time.time()
users = fetch_users_with_cache(query="SELECT * FROM users")
print(f"   -> Call 1 took: {time.time() - start_time:.2f}s")
print(users)

print("\n--- 2. Second call (will be FAST from cache) ---")
start_time = time.time()
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(f"   -> Call 2 took: {time.time() - start_time:.2f}s")
print(users_again)

# Clean up
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)