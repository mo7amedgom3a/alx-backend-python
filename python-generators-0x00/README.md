# Python Generators - Advanced Data Processing

## About the Project

This project introduces advanced usage of Python generators to efficiently handle large datasets, process data in batches, and simulate real-world scenarios involving live updates and memory-efficient computations. The tasks focus on leveraging Python's `yield` keyword to implement generators that provide iterative access to data, promoting optimal resource utilization, and improving performance in data-driven applications.

## Learning Objectives

By completing this project, you will:

- **Master Python Generators**: Learn to create and utilize generators for iterative data processing, enabling memory-efficient operations.
- **Handle Large Datasets**: Implement batch processing and lazy loading to work with extensive datasets without overloading memory.
- **Simulate Real-world Scenarios**: Develop solutions to simulate live data updates and apply them to streaming contexts.
- **Optimize Performance**: Use generators to calculate aggregate functions like averages on large datasets, minimizing memory consumption.
- **Apply SQL Knowledge**: Use SQL queries to fetch data dynamically, integrating Python with databases for robust data management.

## Requirements

- Proficiency in Python 3.x
- Understanding of `yield` and Python's generator functions
- Familiarity with SQL and database operations (MySQL and SQLite)
- Basic knowledge of database schema design and data seeding
- Ability to use Git and GitHub for version control and submission

## Key Concepts

### Python Generators
Generators are functions that use the `yield` keyword to produce a sequence of values over time, rather than computing and returning all values at once. This enables memory-efficient iteration over large datasets.

### Batch Processing
Processing data in smaller chunks (batches) to manage memory usage effectively when dealing with large datasets that cannot fit entirely in memory.

### Lazy Loading
A technique where data is loaded only when needed, reducing initial memory consumption and improving application startup time.

### Memory Optimization
Using generators to process data iteratively minimizes memory footprint by avoiding the need to store entire datasets in memory simultaneously.

### Database Integration
Combining Python generators with SQL queries to fetch and process data dynamically from databases, enabling efficient data pipeline implementations.

### Project Description

This project demonstrates the use of Python generators for efficient data processing. Below is a description of each file in the repository:

- **0-main.py**: This script connects to a MySQL database, creates a database named `ALX_prodev`, creates a table named `user_data`, inserts data from a CSV file into the table, and then retrieves and prints the first 5 rows from the `user_data` table. It uses the `seed.py` module to handle database connections and operations.
- **0-stream_users.py**: This script defines a generator function `stream_users` that fetches rows one by one from the `user_data` table using `yield`. It connects to the `ALX_prodev` database and retrieves all rows in a memory-efficient manner.
- **1-batch_processing.py**: This script defines two functions: `stream_users_in_batches` which fetches rows from the `user_data` table in batches using a generator, and `batch_processing` which processes each batch to filter users over the age of 25.
- **1-main.py**: This script uses the `stream_users` generator from `0-stream_users.py` to iterate over the first 20 users and print them. It also includes a mechanism to exhaust the generator to ensure proper cleanup.
- **2-lazy_paginate.py**: This script implements lazy pagination using generators. It defines `paginate_users` to fetch users in pages and `lazy_paginate` to yield users page by page, optimizing memory usage.
- **2-main.py**: This script imports the `batch_processing` function from `1-batch_processing.py` and prints users in batches of 50.
- **3-main.py**: This script imports the `lazy_paginate` function from `2-lazy_paginate.py` and prints all users retrieved through lazy pagination.
- **4-stream_ages.py**: This script defines a generator `stream_user_ages` that yields user ages one by one from the `user_data` table. It also includes a function `calculate_average_age` to calculate the average age of users using the generator without loading the entire dataset into memory.
- **seed.py**: This module contains functions to connect to a MySQL database, create the `ALX_prodev` database, create the `user_data` table, and insert data from a CSV file into the table. It provides the necessary database setup and utility functions for the other scripts.
- **setup_db.sql**: This file is intended to contain SQL commands for setting up the database.