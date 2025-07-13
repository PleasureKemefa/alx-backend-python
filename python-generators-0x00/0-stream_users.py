#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator that yields rows from user_data one by one as dictionaries."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password_here",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:  # SINGLE loop
            yield row

    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
