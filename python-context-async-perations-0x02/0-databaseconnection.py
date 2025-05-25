import sqlite3

class DatabaseConnection:
    def __init__(self, database_path):
        self.database_path = database_path
        self.connection = None
    
    def __enter__(self):
        self.connection = sqlite3.connect(self.database_path)
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

# Example usage
if __name__ == "__main__":
    # Using the context manager
    with DatabaseConnection("example.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)