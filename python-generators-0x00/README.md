Python Generators - Project 0x00

This project explores the use of Python generators for efficient data processing, particularly in the context of streaming large datasets from a MySQL database. The goal is to understand and implement memory-efficient data handling techniques like lazy loading, batch processing, and streaming aggregations.

Concepts Covered

    Generators: Creating and using generator functions with the yield keyword.

    Database Streaming: Fetching data from a MySQL database row by row, in batches, or page by page.

    Memory Efficiency: Performing calculations (like averages) and processing data without loading the entire dataset into memory.

    Lazy Loading: Implementing paginated data fetching that only queries the database when the next page is needed.

    Batch Processing: Reading and processing large datasets in manageable chunks.

Requirements

    Python 3

    MySQL Server

    mysql-connector-python library (pip install mysql-connector-python)

    A user_data.csv file in the root of the directory (not included in this repo, must be provided).

Database Setup

The seed.py script is responsible for setting up the database. Before running, you may need to set environment variables for your MySQL credentials:
Bash

export DB_HOST="localhost"
export DB_USER="your_mysql_user"
export DB_PASS="your_mysql_password"

Then, run the main file to initialize the database:
Bash

./0-main.py

This will:

    Connect to your MySQL server.

    Create the ALX_prodev database if it doesn't exist.

    Create the user_data table.

    Populate the table with data from user_data.csv.

File Descriptions

seed.py

A utility module containing all database connection and setup functions:

    connect_db(): Connects to the MySQL server.

    create_database(connection): Creates the ALX_prodev database.

    connect_to_prodev(): Connects specifically to the ALX_prodev database.

    create_table(connection): Creates the user_data table.

    insert_data(connection, data_file): Populates the table from a CSV.

0-stream_users.py

    stream_users(): A generator function that connects to the user_data table and yields one user at a time as a dictionary. This demonstrates basic, memory-efficient streaming.

1-batch_processing.py

    stream_users_in_batches(batch_size): A generator that fetches users from the database in batches (lists) of a specified size.

    batch_processing(batch_size): Uses the stream_users_in_batches generator to fetch data and then processes each batch, filtering for users over the age of 25.

2-lazy_paginate.py

    paginate_users(page_size, offset): A helper function (provided) that fetches a specific page of data using LIMIT and OFFSET.

    lazy_pagination(page_size): A generator that lazily fetches pages of data. It yields one page at a time and only queries the database for the next page when the generator is advanced.

4-stream_ages.py

    stream_user_ages(): A generator that streams only the age column from the database, yielding one age at a time.

    calculate_average_age(): Consumes the stream_user_ages generator to calculate the average age of all users without loading all ages into memory simultaneously.

