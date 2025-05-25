import sqlite3
from datetime import datetime
import functools

#### decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Executing query: {args[0]} at {datetime.now()}")
        with open('query_log.txt', 'a') as log_file:
            log_file.write(f"{datetime.now()}: {args[0]}\n")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")