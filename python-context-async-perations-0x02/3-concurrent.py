import asyncio
import aiosqlite  # The async version of sqlite3
import sqlite3    # Using the standard library for the initial setup
import os
import time

DB_NAME = 'users_async.db'

# --- 1. Synchronous Setup Function ---
def setup_database():
    """Creates a fresh users.db with an age column for the example."""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    
    # Using standard sqlite3 for setup is fine
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create table with age
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    
    # Insert sample data
    users_data = [
        ('Alice', 30),
        ('Bob', 45),
        ('Charlie', 50),
        ('David', 25)
    ]
    cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users_data)
    
    conn.commit()
    conn.close()
    print("[Setup] Database created.")

# --- 2. Asynchronous Query Functions ---

async def async_fetch_users():
    """Fetches all users from the database."""
    print("  [Task 1] Starting: Fetch all users...")
    
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            # 'await' is used for the I/O operation
            results = await cursor.fetchall()
            
    print("  [Task 1] Finished.")
    return results

async def async_fetch_older_users():
    """Fetches users older than 40."""
    print("  [Task 2] Starting: Fetch users > 40...")
    
    query = "SELECT * FROM users WHERE age > ?"
    params = (40,)
    
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(query, params) as cursor:
            # 'await' is used for the I/O operation
            results = await cursor.fetchall()
            
    print("  [Task 2] Finished.")
    return results

# --- 3. Main Concurrent Function ---



async def fetch_concurrently():
    """
    Runs both fetch operations concurrently using asyncio.gather.
    """
    print("\n--- Starting concurrent fetches ---")
    start_time = time.time()
    
    # asyncio.gather() takes multiple awaitables (our async functions)
    # and runs them concurrently. It waits for all to complete.
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    end_time = time.time()
    print(f"--- Concurrent fetches finished in {end_time - start_time:.4f} seconds ---")
    
    # Print the results
    print("\n[Results] All Users:")
    for user in all_users:
        print(f"  {user}")
        
    print("\n[Results] Older Users (> 40):")
    for user in older_users:
        print(f"  {user}")

# --- 4. Main Execution ---

if __name__ == "__main__":
    # 1. Set up the database
    setup_database()
    
    # 2. Run the main async function
    # asyncio.run() creates and manages the event loop
    asyncio.run(fetch_concurrently())
    
    # 3. Clean up
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print("\n[Cleanup] Database file removed.")