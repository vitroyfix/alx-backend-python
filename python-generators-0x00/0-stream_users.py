#!/usr/bin/python3
import seed
import sys

def stream_users():
    connection = None
    try:
        connection = seed.connect_to_prodev()
        if connection is None:
            print("Failed to connect to database.", file=sys.stderr)
            return

        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM user_data;")

        for row in cursor:
            yield row

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()