#!/usr/bin/python3
import mysql.connector
import csv
import sys
import os

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'root')
DB_NAME = 'ALX_prodev'


def connect_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}", file=sys.stderr)
        return None


def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        print(f"Database {DB_NAME} created or already exists.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}", file=sys.stderr)


def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database {DB_NAME}: {err}", file=sys.stderr)
        return None


def create_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        );
        """
        cursor.execute(create_table_query)
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}", file=sys.stderr)


def insert_data(connection, data_file):
    cursor = connection.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM user_data;")
    if cursor.fetchone()[0] > 0:
        print("Data already populated.")
        cursor.close()
        return

    try:
        with open(data_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)

            insert_query = """
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            """
            rows_inserted = 0
            for row in reader:
                try:
                    cursor.execute(insert_query, tuple(row))
                    rows_inserted += 1
                except mysql.connector.Error as insert_err:
                    print(f"Error inserting row {row}: {insert_err}", file=sys.stderr)
            
            connection.commit()
            print(f"Inserted {rows_inserted} rows of data.")

    except FileNotFoundError:
        print(f"Error: Data file '{data_file}' not found.", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred during data insertion: {e}", file=sys.stderr)
    finally:
        cursor.close()