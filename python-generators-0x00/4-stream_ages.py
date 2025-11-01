#!/usr/bin/python3
import seed
import sys

def stream_user_ages():
    connection = None
    try:
        connection = seed.connect_to_prodev()
        if connection is None:
            print("Failed to connect to database.", file=sys.stderr)
            return

        cursor = connection.cursor()
        
        cursor.execute("SELECT age FROM user_data;")

        for row in cursor:
            yield row[0]

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if connection:
            connection.close()


def calculate_average_age():
    total_age = 0
    user_count = 0

    for age in stream_user_ages():
        total_age += int(age)
        user_count += 1

    if user_count > 0:
        average_age = total_age / user_count
        print(f"Average age of users: {average_age}")
    else:
        print("No users found to calculate average age.")


if __name__ == "__main__":
    calculate_average_age()