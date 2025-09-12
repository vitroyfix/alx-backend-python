#!/usr/bin/env python3
"""
Task 2: Concurrent Asynchronous Database Queries.

This script demonstrates how to run multiple asynchronous
SQLite queries at the same time using aiosqlite and asyncio.

Queries:
    - Fetch all users
    - Fetch users older than 40
"""

import asyncio
import aiosqlite


async def async_fetch_users(db_name="users.db"):
    """
    Fetch all users from the database.
    
    Args:
        db_name (str): SQLite database file (default: 'users.db').

    Returns:
        list of tuples: All rows from the users table.
    """
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users(db_name="users.db"):
    """
    Fetch users older than 40 from the database.
    
    Args:
        db_name (str): SQLite database file (default: 'users.db').

    Returns:
        list of tuples: Users older than 40.
    """
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    """
    Run both queries concurrently and print results.
    """
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(),
    )

    print("All Users:", all_users)
    print("Users older than 40:", older_users)


if __name__ == "__main__":
    # Run the async queries concurrently
    asyncio.run(fetch_concurrently())
