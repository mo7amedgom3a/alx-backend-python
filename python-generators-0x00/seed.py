import mysql.connector
import csv

DB_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'

def connect_db():
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2003"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database {DB_NAME} created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2003",  # Replace with your actual password
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to {DB_NAME}: {err}")
        return None

def create_table(connection):
    """Creates the table user_data if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                user_id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                age INT
            )
        """)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, data):
    """Inserts data into the user_data table from a CSV file."""
    cursor = connection.cursor()
    try:
        with open(data, 'r') as file:
            csv_data = csv.reader(file)
            next(csv_data)  # Skip the header row
            for row in csv_data:
                sql = f"INSERT INTO {TABLE_NAME} (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
                val = (row[0], row[1], row[2], int(row[3]))
                cursor.execute(sql, val)
            connection.commit()
            print("Data inserted successfully")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    except FileNotFoundError:
        print(f"Error: The file '{data}' was not found.")
    finally:
        cursor.close()