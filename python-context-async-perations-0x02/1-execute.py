import sqlite3

class ExecuteQuery:
    def __init__(self, query, *params):
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None
        self.result = None
    
    def __enter__(self):
        self.connection = sqlite3.connect(':memory:')  # or your database file
        self.cursor = self.connection.cursor()
        self.result = self.cursor.execute(self.query, self.params).fetchall()
        return self.result
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

with ExecuteQuery("SELECT * FROM users WHERE age > ?", 25) as result:
    print(result)