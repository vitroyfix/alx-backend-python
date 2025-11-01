#!/usr/bin/python3
import seed
import sys

def paginate_users(page_size, offset):
    connection = None
    try:
        connection = seed.connect_to_prodev()
        if connection is None:
            print("Failed to connect to database.", file=sys.stderr)
            return []
            
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"An error occurred during pagination: {e}", file=sys.stderr)
        return []
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()


def lazy_pagination(page_size):
    offset = 0
    
    while True:
        page = paginate_users(page_size, offset)
        
        if not page:
            break
            
        yield page
        
        offset += page_size