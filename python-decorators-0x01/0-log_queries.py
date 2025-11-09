import sqlite3
import functools
import os

#### decorator to log SQL queries

def log_queries(func):
    """
    A decorator that logs the SQL query argument of a function
    before executing it.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 1. Find the query string from the function's arguments
        query_to_log = None
        
        # Check if 'query' is in keyword arguments
        if 'query' in kwargs:
            query_to_log = kwargs['query']
        # If not, assume it's the first positional argument
        elif args:
            query_to_log = args[0]
            
        # 2. Log the query
        if query_to_log:
            print(f"[LOG] Executing Query: {query_to_log}")
        else:
            # Fallback if the query couldn't be found
            print(f"[LOG] Executing {func.__name__}...")
        
        # 3. Execute the original function and return its result
        return func(*args, **kwargs)
        
    return wrapper

#### --- Example Usage ---

# A simple function to set up our database for the example
def setup_database():
    db_name = 'users.db'
    if os.path.exists(db_name):
        os.remove(db_name)
        
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
    conn.commit()
    conn.close()

@log_queries
def fetch_all_users(query):
    """Fetches all users from the database based on a query."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# 1. Set up the database
setup_database()

# 2. Fetch users while logging the query
print("Fetching users...")
users = fetch_all_users(query="SELECT * FROM users")

print("\n--- Results ---")
for user in users:
    print(user)

# 3. Clean up the dummy database
if os.path.exists('users.db'):
    os.remove('users.db')