#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """Generator that yields rows in batches of given size."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password_here",  # Replace with your actual password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """Processes each batch and prints users over age 25."""
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch:  # loop 2
            if user['age'] > 25:
                print(user)  # Output the filtered user
