import time
import sqlite3 
import functools


query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('example.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from kwargs or args
        query = kwargs.get('query') or (args[1] if len(args) > 1 else None)
        
        if query and query in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[query]
        
        # Execute the function and cache the result
        result = func(*args, **kwargs)
        if query:
            query_cache[query] = result
            print(f"Cache miss. Cached result for query: {query}")
        
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")