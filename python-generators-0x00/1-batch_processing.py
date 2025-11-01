#!/usr/bin/python3
import seed
import sys

def stream_users_in_batches(batch_size=50):
    connection = None
    try:
        connection = seed.connect_to_prodev()
        if connection is None:
            print("Failed to connect to database.", file=sys.stderr)
            return
            
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size=50):
    for batch in stream_users_in_batches(batch_size):
        
        for user in batch:
            if user['age'] > 25:
                print(user)