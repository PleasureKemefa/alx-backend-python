#!/usr/bin/env python3
import seed  # assumes seed.py has connect_to_prodev()

def stream_user_ages():
    """Generator that yields user ages one by one."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # 1st loop
        yield age

    cursor.close()
    connection.close()


def calculate_average_age():
    """Calculates and prints the average age of all users."""
    total = 0
    count = 0

    for age in stream_user_ages():  # 2nd loop
        total += age
        count += 1

    average = total / count if count else 0
    print(f"Average age of users: {average}")
