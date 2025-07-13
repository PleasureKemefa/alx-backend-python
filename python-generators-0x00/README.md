# 0x00. Python - Generators

## 📍 Project: Python Generator with SQL Streaming

This project demonstrates how to use **Python generators** to efficiently fetch and process rows from a MySQL database **one at a time** using a streaming approach. It is part of the ALX Backend curriculum.

---

## 🧠 Learning Objectives

- Understand how Python generators work
- Connect and interact with a MySQL database using `mysql-connector-python`
- Create databases and tables dynamically
- Insert data from a CSV file
- Stream large datasets using generators to improve memory efficiency

---

## 🛠️ Technologies Used

- **Python 3.8+**
- **MySQL Server**
- **mysql-connector-python**
- **CSV (standard library)**

---

## 🧪 How It Works

### Main Components

- `seed.py`: Contains all the logic for:
  - Connecting to MySQL
  - Creating the database and table
  - Inserting data from `user_data.csv`
  - Streaming rows using a generator

- `0-main.py`: Script to test and demonstrate how the generator works.

---

## 📁 File Structure

```bash
python-generators-0x00/
├── 0-main.py
├── seed.py
├── user_data.csv
└── README.md