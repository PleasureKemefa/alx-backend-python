#!/usr/bin/env python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    """Fetch a single page of users from user_data using LIMIT/OFFSET."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """Generator that yields pages lazily from user_data."""
    offset = 0
    while True:  # SINGLE loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
