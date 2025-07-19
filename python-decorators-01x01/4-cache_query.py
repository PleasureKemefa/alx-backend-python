#!/usr/bin/env python3
import time
import sqlite3
import functools

# Global cache for query results
query_cache = {}

# Decorator to manage database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Decorator to cache query results based on query string
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Determine query string from args or kwargs
        query = None
        if args:
            query = args[0]
        elif 'query' in kwargs:
            query = kwargs['query']

        if query in query_cache:
            print("Returning cached result for query.")
            return query_cache[query]
        else:
            print("Executing and caching query.")
            result = func(conn, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will execute and cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will return the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
